#!/usr/bin/env python3
"""verificar_404.py — que la página que no existe devuelva 404 de verdad.

`auditar_sitio.py` comprobaba que la plantilla `error-404` tuviera la condición «404» en sus
metadatos. Eso no prueba nada: hay WordPress que devuelven **200** con una página que parece
un error, y entonces el buscador indexa infinitas URL basura y el visitante nunca ve el 404.

Este gate pide una URL que no existe y mira el código de estado real:

  · 404                      → bien
  · 200                      → FALLA: la página de error es una página más
  · 301/302/307 a otra ruta  → FALLA: redirección silenciosa, soft-404
  · 403/500                  → FALLA: la ruta no existe pero el error no es 404
  · sin respuesta (DNS, TLS) → NO MEDIDO: no hay instrumento, no es un fallo del sitio

Además compara el `h1` de la portada con el del 404: si son idénticos, el código puede ser
404 y el contenido seguir siendo la portada.

Uso:
    python verificar_404.py --sitio https://ejemplo.cl
    python verificar_404.py --sitio https://ejemplo.cl --slug no-existe-a1b2c3 --json
Salida: 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import json
import random
import re
import string
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta  # noqa: E402

UA = {"User-Agent": "verificar-404/1.0"}


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    """No sigue redirecciones: un 301 hacia la portada es exactamente lo que hay que ver."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


ABRIDOR = urllib.request.build_opener(SinRedireccion)


def pedir(url, timeout=30):
    """(código, cuerpo, error_de_red)."""
    try:
        with ABRIDOR.open(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore"), None
    except urllib.error.HTTPError as e:
        cuerpo = ""
        try:
            cuerpo = e.read().decode("utf-8", "ignore")
        except Exception:  # noqa: BLE001
            pass
        return e.code, cuerpo, None
    except Exception as e:  # noqa: BLE001 — DNS, TLS, timeout
        return None, "", "%s: %s" % (type(e).__name__, e)


def primer_h1(html):
    encontrado = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    if not encontrado:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", encontrado[0])).strip()[:80]


def main(argv):
    ap = argparse.ArgumentParser(description="404 real contra HTTP")
    ap.add_argument("--sitio", required=True, help="URL base, sin barra final")
    ap.add_argument("--slug", default="", help="ruta inexistente a pedir (por defecto, aleatoria)")
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    base = args.sitio.rstrip("/")
    if not re.match(r"^https?://", base):
        print("ERROR DE USO · --sitio debe empezar por http:// o https://")
        return 2

    p = Puerta("404", base)
    sufijo = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    rutas = [args.slug or "/no-existe-%s" % sufijo, "/%s/%s" % (sufijo, sufijo)]

    codigos = {}
    for ruta in rutas:
        url = base + ruta
        codigo, cuerpo, error = pedir(url, args.timeout)
        if error:
            p.sin_medir("%s sin respuesta: %s" % (ruta, error))
            continue
        codigos[ruta] = codigo
        if codigo == 404:
            continue
        if codigo == 200:
            p.falla("%s devuelve 200: la página de error es una página real e indexable" % ruta)
        elif codigo in (301, 302, 303, 307, 308):
            p.falla("%s redirige con %s en vez de devolver 404" % (ruta, codigo))
        else:
            p.falla("%s devuelve %s y no 404" % (ruta, codigo))

        # 200 con la portada dentro es el soft-404 clásico
        if codigo == 200:
            portada, _, _ = pedir(base + "/", args.timeout)
            h1_error, h1_portada = primer_h1(cuerpo), primer_h1(portada or "")
            if h1_error and h1_error == h1_portada:
                p.falla("%s sirve el h1 de la portada («%s»): soft-404" % (ruta, h1_error))

    if codigos:
        p.mide("códigos", ", ".join("%s → %s" % (r, c) for r, c in codigos.items()))
        p.mide("rutas probadas", "%d de 2" % len(codigos))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
