#!/usr/bin/env python3
"""Audita un sitio WordPress + Elementor ya existente y emite números, no impresiones.

Cubre el flujo que el framework no tenía: leer lo que ya está publicado antes de tocarlo.
Combina dos fuentes —el MCP de Elementor (estructura real) y el HTML servido (lo que ve
el visitante)— porque cada una miente distinto: el MCP no ve el HTML que un mu-plugin
sirve por encima, y el HTML no ve qué plantillas ni componentes existen.

    ELEMENTOR_MCP_URL   https://<sitio>/wp-json/elementor/mcp/
    ELEMENTOR_MCP_KEY   credencial Basic

Uso:
    python auditar_sitio.py --sitio https://ejemplo.cl
Sale 0 si el sitio pasa las comprobaciones; 1 si alguna falla.
"""
import argparse
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verificar_sistema import rpc  # noqa: E402


def html_de(url):
    pet = urllib.request.Request(url, headers={"User-Agent": "auditor-sitio/1.0"})
    try:
        with urllib.request.urlopen(pet, timeout=45) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        return "" if "404" in str(e) else None


def medir_html(html):
    def cuenta(patron):
        return len(re.findall(patron, html, re.I))
    # El banner de cookies inyecta su propio <img>: no es contenido editorial.
    etiquetas_img = re.findall(r"<img\b[^>]*>", html, re.I)
    imagenes = [t for t in etiquetas_img if not re.search(r"cookie|cc-|consent", t, re.I)]
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    return {
        "bytes": len(html),
        "imagenes": len(imagenes),
        "videos": cuenta(r"<video\b"),
        "secciones": cuenta(r"<section\b"),
        "h1": len(h1),
        "h1_texto": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h1[0])).strip()[:60] if h1 else "",
        "estilos_en_linea": cuenta(r'\sstyle="'),
        "heredoc": "pp-pages" in html,
        "favicon": bool(re.search(r'rel=["\'][^"\']*icon', html, re.I)),
        "og_image": bool(re.search(r'property=["\']og:image', html, re.I)),
    }


def llamar(sesion, cab, url, nombre, args, ident):
    if not nombre:
        return None
    estado, _, cuerpo = rpc(url, cab, {"jsonrpc": "2.0", "id": ident, "method": "tools/call",
                                       "params": {"name": nombre, "arguments": args}}, sesion)
    if estado != 200 or '"result"' not in cuerpo:
        return None
    try:
        texto = json.loads(cuerpo)["result"]["content"][0]["text"]
        return json.loads(texto) if texto.strip().startswith(("{", "[")) else texto
    except Exception:  # noqa: BLE001
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sitio", required=True, help="URL base, sin barra final")
    ap.add_argument("--json", action="store_true", help="salida JSON en lugar de tabla")
    args = ap.parse_args()

    url_mcp = os.environ.get("ELEMENTOR_MCP_URL", "").strip()
    clave = os.environ.get("ELEMENTOR_MCP_KEY", "").strip()
    if not (url_mcp and clave):
        print("FALTAN ELEMENTOR_MCP_URL / ELEMENTOR_MCP_KEY")
        return 1

    cab = {"Authorization": "Basic " + clave, "User-Agent": "auditor-sitio/1.0"}
    _, sesion, _ = rpc(url_mcp, cab, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                                 "clientInfo": {"name": "auditor", "version": "1"}}})
    _, _, cuerpo = rpc(url_mcp, cab, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, sesion)
    nombres = [t["name"] for t in json.loads(cuerpo)["result"]["tools"]]

    def buscar(*claves):
        for n in nombres:
            if all(c in n.lower() for c in claves):
                return n
        return ""

    t_posts = buscar("list", "post")
    t_estructura = buscar("structure")
    t_componentes = buscar("component")
    t_plantillas = buscar("list", "site", "part")
    t_estilos = buscar("default", "style")

    paginas = llamar(sesion, cab, url_mcp, t_posts, {"post_type": "page", "per_page": 25}, 3) or {}
    paginas = paginas.get("posts", paginas if isinstance(paginas, list) else [])
    componentes = llamar(sesion, cab, url_mcp, t_componentes, {}, 4) or {}
    componentes = componentes.get("components", []) if isinstance(componentes, dict) else []
    plantillas = llamar(sesion, cab, url_mcp, t_plantillas, {}, 5) or {}
    if isinstance(plantillas, dict):
        plantillas = plantillas.get("result") or plantillas.get("templates") or plantillas.get("site_parts") or []
    plantillas = [t for t in plantillas if isinstance(t, dict)]

    filas, fallos = [], []
    for p in paginas:
        if p.get("status") != "publish":
            continue
        estructura = llamar(sesion, cab, url_mcp, t_estructura, {"post_id": p["id"]}, 10 + len(filas))
        elementos = 0
        if isinstance(estructura, dict):
            elementos = estructura.get("element_count") or len(estructura.get("elements", []) or [])
        elif isinstance(estructura, list):
            elementos = len(estructura)
        m = medir_html(html_de(p.get("url", "")) or "")
        fila = {"id": p["id"], "ruta": (p.get("url") or "").replace(args.sitio, "") or "/",
                "elementor": elementos, **m}
        filas.append(fila)

    tipos = {}
    for t in plantillas:
        tipo = t.get("type") or t.get("template_type") or "?"
        estado = "activa" if t.get("is_active") else t.get("post_status", "?")
        tipos.setdefault(tipo, []).append(estado)
    duplicadas = {k: v for k, v in tipos.items() if len(v) > 1}
    mal_condicionadas = [t.get("title", "") for t in plantillas
                         if t.get("type") == "error-404" and "404" not in " ".join(t.get("conditions", []))]
    inactivas_con_duplicado = [t.get("title", "") for t in plantillas
                               if not t.get("is_active") and len(tipos.get(t.get("type"), [])) > 1]

    no_elementor = [f["ruta"] for f in filas if f["elementor"] == 0]
    sin_imagenes = [f["ruta"] for f in filas if f["imagenes"] == 0]
    sin_favicon = [f["ruta"] for f in filas if not f["favicon"]]
    sin_og = [f["ruta"] for f in filas if not f["og_image"]]
    h1_multiple = [f["ruta"] for f in filas if f["h1"] != 1]
    inline = sum(f["estilos_en_linea"] for f in filas)

    if no_elementor:
        fallos.append("%d de %d páginas no están construidas con Elementor" % (len(no_elementor), len(filas)))
    if not componentes:
        fallos.append("el kit no tiene componentes reutilizables")
    if duplicadas:
        fallos.append("plantillas duplicadas por tipo: %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in duplicadas.items()))
    if mal_condicionadas:
        fallos.append("plantilla 404 sin condición de 404: %s" % ", ".join(mal_condicionadas))
    if h1_multiple:
        fallos.append("páginas sin exactamente un H1: %s" % ", ".join(h1_multiple))
    if sin_imagenes:
        fallos.append("%d de %d páginas sin una sola imagen" % (len(sin_imagenes), len(filas)))
    if sin_favicon:
        fallos.append("%d de %d páginas sin favicon" % (len(sin_favicon), len(filas)))
    if sin_og:
        fallos.append("%d de %d páginas sin og:image (sin tarjeta al compartir)" % (len(sin_og), len(filas)))
    if inline > 20:
        fallos.append("%d estilos en línea en el HTML servido" % inline)

    if args.json:
        print(json.dumps({"paginas": filas, "componentes": len(componentes),
                          "plantillas": tipos, "fallos": fallos}, ensure_ascii=False, indent=1))
    else:
        print("%-22s %8s %6s %8s %3s %6s" % ("ruta", "elementor", "img", "secciones", "h1", "bytes"))
        for f in filas:
            print("%-22s %9d %6d %10d %3d %6d" % (f["ruta"][:22], f["elementor"], f["imagenes"],
                                                  f["secciones"], f["h1"], f["bytes"]))
        print()
        print("componentes: %d · plantillas: %s" % (len(componentes), ", ".join("%s=%d" % (k, len(v)) for k, v in tipos.items())))
        print()
        if fallos:
            print("AUDITORÍA · %d fallos" % len(fallos))
            for f in fallos:
                print("  - " + f)
        else:
            print("AUDITORÍA · 0 fallos")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
