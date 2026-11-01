#!/usr/bin/env python3
"""Comprueba que el sistema de diseño sigue existiendo en Elementor.

No conoce ningún cliente: lee endpoint y credenciales del entorno.

    ELEMENTOR_MCP_URL   https://<sitio>/wp-json/elementor/mcp/
    ELEMENTOR_MCP_USER  usuario de WordPress
    ELEMENTOR_MCP_KEY   application password

Uso:  python verificar_sistema.py [--sistema sistema.yaml] [--tokens tokens.css]
Sale 0 si todo pasa; 1 si algo falta; 3 si no se pudo medir (sin MCP o sin .env).
El mapa `patrones` se comprueba siempre, antes de cualquier llamada: es local.
No imprime credenciales.
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "framework", "tools"))
from _comun import cargar_yaml  # noqa: E402


def leer_yaml_minimo(ruta):
    """Lector suficiente para sistema.yaml: listas de mapas en una línea."""
    texto = open(ruta, encoding="utf-8").read()
    datos = {"variables": [], "clases": [], "componentes": []}
    bloque = None
    for linea in texto.splitlines():
        limpia = linea.strip()
        if not limpia or limpia.startswith("#"):
            continue
        if re.match(r"^(variables|clases|componentes|pendientes):", limpia):
            bloque = limpia.split(":")[0]
            continue
        if limpia.startswith("- {") and bloque in datos:
            pares = re.findall(r"(\w+):\s*(\"[^\"]*\"|[^,}]+)", limpia)
            datos[bloque].append({k: v.strip().strip('"') for k, v in pares})
    return datos


def rpc(url, cabeceras, cuerpo, sesion=None):
    h = dict(cabeceras)
    h["Content-Type"] = "application/json"
    h["Accept"] = "application/json, text/event-stream"
    h["MCP-Protocol-Version"] = "2025-06-18"
    if sesion:
        h["MCP-Session-Id"] = sesion
    pet = urllib.request.Request(url, data=json.dumps(cuerpo).encode(), headers=h, method="POST")
    try:
        with urllib.request.urlopen(pet, timeout=60) as r:
            return r.status, r.headers.get("Mcp-Session-Id"), r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, None, e.read().decode("utf-8", "ignore")


def revisar_patrones(ruta):
    """El mapa tipo → componente tiene que apuntar a componentes que existen.

    Se comprueba sin MCP y antes de cualquier llamada: es un dato local, y un mapa que apunta
    a un componente borrado manda a construir con un id inexistente.
    """
    datos, error = cargar_yaml(ruta)
    if error:
        return ["no se pudo leer %s: %s" % (ruta, error)]
    componentes = {c.get("id") for c in (datos.get("componentes") or []) if isinstance(c, dict)}
    patrones = datos.get("patrones") or {}
    if not patrones:
        return ["sistema.yaml no declara patrones: no hay mapa tipo → componente"]
    fallos = []
    for tipo, valor in patrones.items():
        destino = (valor or {}).get("componente") if isinstance(valor, dict) else valor
        if destino is None:
            continue                      # hueco declarado, no error
        try:
            destino = int(destino)
        except (TypeError, ValueError):
            fallos.append("patrón «%s»: componente «%s» no es un id" % (tipo, destino))
            continue
        if destino not in componentes:
            fallos.append("patrón «%s»: componente %d no está entre los componentes declarados"
                          % (tipo, destino))
    return fallos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sistema", default=os.path.join(AQUI, "sistema.yaml"))
    ap.add_argument("--tokens", default=os.path.join(AQUI, "..", "..", "framework", "05_SYSTEM", "tokens.css"))
    args = ap.parse_args()

    fallos_patrones = revisar_patrones(args.sistema)
    if fallos_patrones:
        print("SISTEMA INCOMPLETO · patrones: %d fallos" % len(fallos_patrones))
        for f in fallos_patrones:
            print("  - " + f)
        return 1
    print("0 · patrones: mapa tipo → componente coherente")

    url = os.environ.get("ELEMENTOR_MCP_URL", "").strip()
    usuario = os.environ.get("ELEMENTOR_MCP_USER", "").strip()
    clave = os.environ.get("ELEMENTOR_MCP_KEY", "").strip()
    if not (url and usuario and clave):
        print("NO MEDIDO · faltan variables ELEMENTOR_MCP_URL / ELEMENTOR_MCP_USER / ELEMENTOR_MCP_KEY: "
              "el kit vivo no se comprobó")
        return 3

    # La credencial puede venir ya codificada (base64 de usuario:contraseña) o en crudo.
    if ":" in clave and not re.fullmatch(r"[A-Za-z0-9+/=]{20,}", clave):
        credencial = base64.b64encode((usuario + ":" + clave).encode()).decode()
    elif ":" in clave:
        credencial = base64.b64encode(clave.encode()).decode()
    else:
        credencial = clave
    cab = {"Authorization": "Basic " + credencial, "User-Agent": "verificador-sistema/1.0"}
    sistema = leer_yaml_minimo(args.sistema)

    fallos, pasos = [], 0

    estado, sesion, cuerpo = rpc(url, cab, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                            "params": {"protocolVersion": "2025-06-18",
                                                       "capabilities": {},
                                                       "clientInfo": {"name": "verificador", "version": "1"}}})
    pasos += 1
    if estado != 200:
        print("MCP no responde a initialize: %s" % estado)
        return 1

    estado, _, cuerpo = rpc(url, cab, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, sesion)
    pasos += 1
    herramientas = [t["name"] for t in json.loads(cuerpo)["result"]["tools"]] if estado == 200 else []
    herramienta_componentes = next((h for h in herramientas
                                    if "component" in h.lower() and "list" in h.lower()), "")
    if not herramienta_componentes:
        fallos.append("no aparece la herramienta que lista componentes")
    if not any("class" in h.lower() for h in herramientas):
        fallos.append("no aparece la herramienta de clases globales")
    print("1 · herramientas MCP: %d" % len(herramientas))

    estado, _, cuerpo = rpc(url, cab, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                                       "params": {"name": herramienta_componentes, "arguments": {}}}, sesion)
    pasos += 1
    if estado != 200 or "result" not in cuerpo:
        fallos.append("list-components falló: %s %s" % (estado, cuerpo[:120]))
        titulos = []
    else:
        texto = json.loads(cuerpo)["result"]["content"][0]["text"]
        datos = json.loads(texto) if texto.strip().startswith(("{", "[")) else {}
        lista = datos.get("components", datos if isinstance(datos, list) else [])
        titulos = [c.get("title") or c.get("name", "") for c in lista]
    esperados = [c["titulo"] for c in sistema["componentes"]]
    ausentes = [t for t in esperados if t not in titulos]
    for t in ausentes:
        fallos.append("componente ausente: %s" % t)
    print("2 · componentes: %d en el kit, %d esperados" % (len(titulos), len(esperados)))

    if os.path.isfile(args.tokens):
        css = open(args.tokens, encoding="utf-8").read()
        declaradas = set(re.findall(r"--([a-z0-9-]+)\s*:", css, re.I))
        etiquetas = [v["label"] for v in sistema["variables"]]
        huerfanas = [e for e in etiquetas if e not in declaradas]
        for h in huerfanas:
            fallos.append("variable sin token de origen: %s" % h)
        print("3 · variables: %d declaradas, %d con token en origen" % (len(etiquetas), len(etiquetas) - len(huerfanas)))
    else:
        fallos.append("no se encontró tokens.css en %s" % args.tokens)

    print()
    if fallos:
        print("SISTEMA INCOMPLETO · %d comprobaciones, %d fallos" % (pasos, len(fallos)))
        for f in fallos:
            print("  - " + f)
        return 1
    print("SISTEMA OK · %d comprobaciones, 0 fallos" % pasos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
