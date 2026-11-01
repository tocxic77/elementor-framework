#!/usr/bin/env python3
"""verificar_servido.py — qué activos llegaron al HTML, no qué activos se declararon.

El registro `03_ASSETS.yaml` dice qué material existe, cuál está autorizado y cuál se pensaba
usar. Hasta hoy nadie comprobaba el paso siguiente: que ese material sea el que la página
publica. Ese hueco permite tres falsos verdes:

  1. una imagen publicada que **no está** en el inventario (entró sin pasar por la puerta de
     material ni por la de autorización);
  2. un activo marcado `usado: true` que **no aparece** en ninguna página: uno de los dos
     documentos miente;
  3. un activo con `autorizacion: pendiente` que sí se está sirviendo.

Compara por nombre de archivo (basename, sin query ni hash). Los orígenes externos —otro
dominio, `data:`, fuentes del tema— se cuentan aparte y no se juzgan: no hay inventario
contra el que compararlos, y darlos por buenos sería el falso verde que este gate evita.

Uso:
    python verificar_servido.py <cliente>/03_ASSETS.yaml --html <cliente>/05_SYSTEM/index.html
    python verificar_servido.py <cliente>/03_ASSETS.yaml --sitio https://ejemplo.cl --pagina / --pagina /soluciones
Salida: 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta, cargar_yaml  # noqa: E402

IMG = re.compile(r"<img\b[^>]*>", re.I)
FUENTE = re.compile(r"<source\b[^>]*>|<video\b[^>]*>", re.I)
ATRIBUTO = re.compile(r"""([a-z:\-]*(?:src|srcset|href|poster|bg|content))\s*=\s*["']([^"']+)["']""", re.I)
CSS_URL = re.compile(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", re.I)
HOJA = re.compile(r"""<link\b[^>]*rel=["'][^"']*stylesheet[^>]*>""", re.I)
BANNER = re.compile(r"cookie|cc-|consent|gdpr", re.I)
DESCRIPTOR = re.compile(r"\s+\d+(\.\d+)?[wx]$", re.I)
IMAGEN = re.compile(r"\.(jpe?g|png|webp|avif|gif|svg|jfif|mp4|webm)$")


def basename(fuente):
    limpio = urllib.parse.urlparse(fuente.strip()).path
    limpio = urllib.parse.unquote(limpio).replace("\\", "/")
    return limpio.rsplit("/", 1)[-1].lower()


def referencias(html, host=None, css=""):
    """(locales, externas) — nombres de archivo citados en el HTML servido y su CSS."""
    locales, externas = set(), set()
    for etiqueta in IMG.findall(html) + FUENTE.findall(html):
        if BANNER.search(etiqueta):
            continue
        for _atributo, valor in ATRIBUTO.findall(etiqueta):
            for parte in re.split(r",\s*", valor):
                # En srcset el descriptor («800w», «2x») va tras un espacio; el nombre no.
                fuente = DESCRIPTOR.sub("", parte.strip())
                if fuente:
                    _clasificar(fuente, host, locales, externas)
    for valor in CSS_URL.findall(html) + CSS_URL.findall(css):
        _clasificar(valor, host, locales, externas)
    for etiqueta in re.findall(r"<meta\b[^>]*og:image[^>]*>", html, re.I):
        for _atributo, valor in ATRIBUTO.findall(etiqueta):
            _clasificar(valor, host, locales, externas)
    for etiqueta in re.findall(r"""<link\b[^>]*rel=["'][^"']*icon[^>]*>""", html, re.I):
        for _atributo, valor in ATRIBUTO.findall(etiqueta):
            _clasificar(valor, host, locales, externas)
    return locales, externas


def hojas_de(html, carpeta):
    """CSS que la página carga y que está al lado: las imágenes de fondo viven ahí."""
    texto = []
    for etiqueta in HOJA.findall(html):
        for _atributo, valor in ATRIBUTO.findall(etiqueta):
            if valor.startswith(("http:", "https:", "//")):
                continue
            archivo = (carpeta / urllib.parse.urlparse(valor).path).resolve()
            try:
                archivo.relative_to(carpeta.resolve())
            except ValueError:
                continue
            if archivo.is_file():
                texto.append(archivo.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(texto)


def _clasificar(fuente, host, locales, externas):
    fuente = fuente.strip()
    if not fuente or fuente.startswith(("data:", "#", "mailto:")):
        return
    partes = urllib.parse.urlparse(fuente)
    if partes.scheme in ("http", "https") and partes.netloc:
        if host and partes.netloc.lower() == host.lower():
            locales.add(basename(fuente))
        else:
            externas.add(partes.netloc.lower() + "/" + basename(fuente))
        return
    if re.search(IMAGEN, basename(fuente)):
        locales.add(basename(fuente))


def html_remoto(url, timeout=45):
    peticion = urllib.request.Request(url, headers={"User-Agent": "verificar-servido/1.0"})
    try:
        with urllib.request.urlopen(peticion, timeout=timeout) as r:
            return r.read().decode("utf-8", "ignore"), None
    except urllib.error.HTTPError as e:
        return None, "HTTP %s" % e.code
    except Exception as e:  # noqa: BLE001 — red, DNS, TLS
        return None, "%s: %s" % (type(e).__name__, e)


def main(argv):
    ap = argparse.ArgumentParser(description="inventario ↔ HTML publicado")
    ap.add_argument("activos")
    ap.add_argument("--html", action="append", default=[], help="página local (repetible)")
    ap.add_argument("--sitio", default="", help="URL base para leer el sitio publicado")
    ap.add_argument("--pagina", action="append", default=[], help="ruta a leer del sitio (repetible)")
    args = ap.parse_args(argv)

    datos, error = cargar_yaml(args.activos)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2

    p = Puerta("servido", Path(args.activos).name)
    activos = datos.get("activos") or []
    if not activos:
        p.falla("el registro no declara activos: no hay inventario contra el que comparar")

    inventario = {}
    for a in activos:
        if a.get("archivo"):
            clave = basename(str(a["archivo"]))
            inventario[clave] = a

    locales, externas, leidas, ilegibles = set(), set(), [], []
    host = urllib.parse.urlparse(args.sitio).netloc if args.sitio else None

    for ruta in args.html:
        archivo = Path(ruta)
        if not archivo.exists():
            p.falla("no existe la página: %s" % ruta)
            continue
        html = archivo.read_text(encoding="utf-8", errors="ignore")
        l, e = referencias(html, host, hojas_de(html, archivo.parent))
        locales |= l
        externas |= e
        leidas.append("%s (%d)" % (archivo.name, len(l)))

    if args.sitio:
        rutas = args.pagina or ["/"]
        for ruta in rutas:
            url = args.sitio.rstrip("/") + (ruta if ruta.startswith("/") else "/" + ruta)
            html, motivo = html_remoto(url)
            if html is None:
                ilegibles.append("%s (%s)" % (ruta, motivo))
                continue
            l, e = referencias(html, host)
            locales |= l
            externas |= e
            leidas.append("%s (%d)" % (ruta, len(l)))

    for ruta in ilegibles:
        p.aviso("no se pudo leer %s" % ruta)
    if not leidas:
        p.sin_medir("no se leyó ninguna página: no hay HTML servido que comparar")
        p.mide("inventario", len(inventario))
        return p.imprimir()

    p.mide("páginas leídas", ", ".join(leidas))
    p.mide("referencias locales", len(locales))
    p.mide("externas ignoradas", len(externas))
    if externas:
        p.aviso("orígenes externos no comparables: " + ", ".join(sorted(externas)[:5]))

    for nombre in sorted(locales):
        if nombre not in inventario:
            p.falla("%s se sirve y no está en el inventario" % nombre)
        elif (inventario[nombre].get("autorizacion") or "").lower() == "pendiente":
            p.falla("%s se sirve con autorización pendiente" % nombre)

    for nombre, a in sorted(inventario.items()):
        if a.get("usado") and nombre not in locales:
            p.falla("%s está marcado en uso y no aparece en ninguna página servida" % nombre)

    usados = [n for n, a in inventario.items() if a.get("usado")]
    p.mide("declarados en uso", "%d · servidos %d" % (len(usados), len(set(usados) & locales)))
    p.mide("servidos fuera del inventario", len([n for n in locales if n not in inventario]))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
