#!/usr/bin/env python3
"""Audita un sitio WordPress + Elementor ya existente y emite números, no impresiones.

Cubre el flujo que el framework no tenía: leer lo que ya está publicado antes de tocarlo.
Combina dos fuentes —el MCP de Elementor (estructura real) y el HTML servido (lo que ve
el visitante)— porque cada una miente distinto: el MCP no ve el HTML que un mu-plugin
sirve por encima, y el HTML no ve qué plantillas ni componentes existen.

Regla de esta puerta desde Sprint C: **lo que no se pudo leer no se cuenta como fallo**.
Antes, una página que no respondía entraba como `""` y aparecía como «0 imágenes»; ahora se
declara NO MEDIDO y el comando sale 3, no 1. Y la condición «404» de una plantilla dejó de
ser un aprobado o un fallo: es un aviso, porque el código real lo mide `verificar_404.py`.

    ELEMENTOR_MCP_URL   https://<sitio>/wp-json/elementor/mcp/
    ELEMENTOR_MCP_KEY   credencial Basic

Uso:
    python auditar_sitio.py --sitio https://ejemplo.cl [--json]
Salida: 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO (sin credenciales o sin datos).
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "framework" / "tools"))
from _comun import FALLA, NOMBRE, NO_MEDIDO, OK, Puerta  # noqa: E402
from verificar_sistema import rpc  # noqa: E402


def html_de(url):
    """(html, motivo). `html is None` significa no medido, no vacío."""
    peticion = urllib.request.Request(url, headers={"User-Agent": "auditor-sitio/1.0"})
    try:
        with urllib.request.urlopen(peticion, timeout=45) as r:
            return r.read().decode("utf-8", "ignore"), None
    except urllib.error.HTTPError as e:
        return None, "HTTP %s" % e.code
    except Exception as e:  # noqa: BLE001
        return None, type(e).__name__


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
        print("NO MEDIDO · faltan ELEMENTOR_MCP_URL / ELEMENTOR_MCP_KEY: sin instrumento no hay auditoría")
        return NO_MEDIDO

    p = Puerta("sitio", args.sitio)
    cab = {"Authorization": "Basic " + clave, "User-Agent": "auditor-sitio/1.0"}
    _, sesion, _ = rpc(url_mcp, cab, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                                      "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                                 "clientInfo": {"name": "auditor", "version": "1"}}})
    _, _, cuerpo = rpc(url_mcp, cab, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}, sesion)
    try:
        nombres = [t["name"] for t in json.loads(cuerpo)["result"]["tools"]]
    except Exception:  # noqa: BLE001
        print("NO MEDIDO · el MCP no devolvió la lista de herramientas")
        return NO_MEDIDO

    def buscar(*claves):
        for n in nombres:
            if all(c in n.lower() for c in claves):
                return n
        return ""

    t_posts = buscar("list", "post")
    t_estructura = buscar("structure")
    t_componentes = buscar("component")
    t_plantillas = buscar("list", "site", "part")

    paginas = llamar(sesion, cab, url_mcp, t_posts, {"post_type": "page", "per_page": 25}, 3)
    if isinstance(paginas, dict):
        paginas = paginas.get("posts", []) or []
    paginas = paginas if isinstance(paginas, list) else None

    componentes = llamar(sesion, cab, url_mcp, t_componentes, {}, 4)
    if isinstance(componentes, dict):
        componentes = componentes.get("components", []) or []
    componentes = componentes if isinstance(componentes, list) else None

    plantillas = llamar(sesion, cab, url_mcp, t_plantillas, {}, 5)
    if isinstance(plantillas, dict):
        plantillas = (plantillas.get("result") or plantillas.get("templates")
                      or plantillas.get("site_parts") or [])
    plantillas = [t for t in plantillas if isinstance(t, dict)] if isinstance(plantillas, list) else None

    if paginas is None:
        p.sin_medir("el MCP no devolvió páginas publicadas")
    if componentes is None:
        p.sin_medir("el MCP no devolvió componentes")
    if plantillas is None:
        p.sin_medir("el MCP no devolvió plantillas")

    filas = []
    for pagina in paginas or []:
        if pagina.get("status") != "publish":
            continue
        ruta = (pagina.get("url") or "").replace(args.sitio, "") or "/"
        estructura = llamar(sesion, cab, url_mcp, t_estructura, {"post_id": pagina["id"]},
                            10 + len(filas))
        if estructura is None:
            p.sin_medir("%s: el MCP no devolvió estructura" % ruta)
            elementos = None
        elif isinstance(estructura, dict):
            contador = estructura.get("element_count")
            elementos = contador if isinstance(contador, int) else len(estructura.get("elements") or [])
        elif isinstance(estructura, list):
            elementos = len(estructura)
        else:
            p.sin_medir("%s: estructura con forma desconocida" % ruta)
            elementos = None

        html, motivo = html_de(pagina.get("url", ""))
        if html is None:
            p.sin_medir("%s: no se pudo leer el HTML servido (%s)" % (ruta, motivo))
            continue
        filas.append({"id": pagina["id"], "ruta": ruta, "elementor": elementos, **medir_html(html)})

    tipos = {}
    for t in plantillas or []:
        tipo = t.get("type") or t.get("template_type") or "?"
        estado = "activa" if t.get("is_active") else t.get("post_status", "?")
        tipos.setdefault(tipo, []).append(estado)
    duplicadas = {k: v for k, v in tipos.items() if v.count("activa") > 1}
    inactivas = {k: v for k, v in tipos.items() if len(v) > 1 and v.count("activa") <= 1}
    con_condicion_404 = [t.get("title", "") for t in plantillas or []
                         if t.get("type") == "error-404" and "404" in " ".join(t.get("conditions", []))]

    p.mide("páginas medidas", len(filas))
    p.mide("componentes", "—" if componentes is None else len(componentes))
    p.mide("plantillas", ", ".join("%s=%d" % (k, len(v)) for k, v in tipos.items()) or "ninguna")

    if inactivas:
        p.aviso("plantillas inactivas duplicadas (higiene de biblioteca): %s" % ", ".join(inactivas))
    if con_condicion_404:
        # La condición en metadatos no prueba comportamiento: eso lo mide verificar_404.py.
        p.aviso("plantilla 404 con condición declarada (%s): el código real lo mide verificar_404.py"
                % ", ".join(con_condicion_404))

    medibles = [f for f in filas if f.get("elementor") is not None]
    no_elementor = [f["ruta"] for f in medibles if f["elementor"] == 0]
    if no_elementor:
        p.falla("%d de %d páginas no están construidas con Elementor: %s"
                % (len(no_elementor), len(medibles), ", ".join(no_elementor)))
    if componentes is not None and not componentes:
        p.falla("el kit no tiene componentes reutilizables")
    if duplicadas:
        p.falla("plantillas duplicadas por tipo: %s"
                % ", ".join("%s=%d" % (k, len(v)) for k, v in duplicadas.items()))

    if filas:
        sin_h1 = [f["ruta"] for f in filas if f["h1"] != 1]
        sin_imagenes = [f["ruta"] for f in filas if f["imagenes"] == 0]
        sin_favicon = [f["ruta"] for f in filas if not f["favicon"]]
        sin_og = [f["ruta"] for f in filas if not f["og_image"]]
        en_linea = sum(f["estilos_en_linea"] for f in filas)
        if sin_h1:
            p.falla("páginas sin exactamente un H1: %s" % ", ".join(sin_h1))
        if sin_imagenes:
            p.falla("%d de %d páginas sin una sola imagen: %s"
                    % (len(sin_imagenes), len(filas), ", ".join(sin_imagenes)))
        if sin_favicon:
            p.falla("%d de %d páginas sin favicon: %s"
                    % (len(sin_favicon), len(filas), ", ".join(sin_favicon)))
        if sin_og:
            p.falla("%d de %d páginas sin og:image (sin tarjeta al compartir): %s"
                    % (len(sin_og), len(filas), ", ".join(sin_og)))
        if en_linea > 20:
            p.falla("%d estilos en línea en el HTML servido" % en_linea)

    if args.json:
        print(json.dumps({"resultado": NOMBRE[p.codigo], "paginas": filas,
                          "componentes": None if componentes is None else len(componentes),
                          "plantillas": tipos, "fallas": p.fallas,
                          "sin_medir": p.sin_medir_motivos, "avisos": p.avisos},
                         ensure_ascii=False, indent=1))
        return p.codigo

    if filas:
        print("%-22s %9s %6s %9s %3s %6s" % ("ruta", "elementor", "img", "secciones", "h1", "bytes"))
        for f in filas:
            print("%-22s %10s %6d %10d %3d %6d"
                  % (f["ruta"][:22], "—" if f["elementor"] is None else f["elementor"],
                     f["imagenes"], f["secciones"], f["h1"], f["bytes"]))
        print()
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main())
