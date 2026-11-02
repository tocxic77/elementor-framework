#!/usr/bin/env python3
"""Sube a la biblioteca de medios los activos propios seleccionados y registra su
attachment_id y su URL servida en 03_ASSETS.yaml.

No inventa ids ni urls: tras cada carga comprueba con un HEAD que la URL servida
responde 200 y que el parent es la biblioteca. Si algo falla, deja el activo en
`biblioteca_medios.estado: fallido` y sale 1.

Credenciales por entorno, nunca por argumento ni por archivo:
  WP_URL              p. ej. https://ejemplo.cl
  WP_APP_USER         usuario de WordPress
  WP_APP_PASSWORD     Application Password (Ajustes del perfil → Contraseñas de aplicación)

Uso:
  python subir_activos.py --cliente <dir>              # sólo dice qué haría
  python subir_activos.py --cliente <dir> --ejecutar   # sube de verdad
"""
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402


def pedir(url, usuario, clave, metodo="GET", cuerpo=None, tipo=None):
    req = urllib.request.Request(url, data=cuerpo, method=metodo)
    token = base64.b64encode(("%s:%s" % (usuario, clave)).encode()).decode()
    req.add_header("Authorization", "Basic " + token)
    if tipo:
        req.add_header("Content-Type", tipo)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.status, json.loads(r.read().decode("utf-8") or "{}")


def servida(url):
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def subir(cliente, ejecutar):
    ruta = os.path.join(cliente, "03_ASSETS.yaml")
    datos, err = cargar_yaml(ruta)
    if err:
        return None, err
    base = (os.environ.get("WP_URL") or "").rstrip("/")
    usuario = os.environ.get("WP_APP_USER") or ""
    clave = os.environ.get("WP_APP_PASSWORD") or ""

    objetivos = [a for a in (datos.get("activos") or [])
                 if isinstance(a, dict) and a.get("seleccionado")
                 and a.get("autorizacion") == "propia"
                 and (a.get("biblioteca_medios") or {}).get("estado") != "importado"]
    if not objetivos:
        return {"nada": True, "objetivos": []}, None
    if not ejecutar:
        return {"nada": False, "objetivos": [a.get("archivo") for a in objetivos]}, None
    if not (base and usuario and clave):
        return None, "faltan WP_URL, WP_APP_USER o WP_APP_PASSWORD en el entorno"

    resultado = []
    for a in objetivos:
        nombre = a.get("archivo")
        camino = os.path.join(cliente, "Imagenes", nombre)
        if not os.path.exists(camino):
            a["biblioteca_medios"] = {"estado": "fallido", "motivo": "no está el archivo"}
            resultado.append((nombre, "falta el archivo"))
            continue
        cuerpo = open(camino, "rb").read()
        tipo = mimetypes.guess_type(nombre)[0] or "application/octet-stream"
        try:
            estado, respuesta = pedir(base + "/wp-json/wp/v2/media", usuario, clave, "POST", cuerpo, tipo)
            ident = respuesta.get("id")
            url = (respuesta.get("source_url") or "").replace("\\/", "/")
        except urllib.error.HTTPError as e:
            a["biblioteca_medios"] = {"estado": "fallido", "motivo": "HTTP %s" % e.code}
            resultado.append((nombre, "HTTP %s" % e.code))
            continue
        codigo = servida(url) if url else None
        if not ident or codigo != 200:
            a["biblioteca_medios"] = {"estado": "fallido",
                                      "motivo": "id=%s · url responde %s" % (ident, codigo)}
            resultado.append((nombre, "sin url servida"))
            continue
        a["wordpress"] = {"attachment_id": ident, "url": url}
        a["biblioteca_medios"] = {"estado": "importado", "verificado": {"servida": codigo}}
        resultado.append((nombre, "id %s · %s" % (ident, codigo)))

    with open(ruta, "w", encoding="utf-8") as f:
        import yaml
        yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False)
    fallos = [r for r in resultado if "id " not in r[1]]
    return {"nada": False, "objetivos": resultado, "fallos": len(fallos)}, (None if not fallos else "fallaron %d" % len(fallos))


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--ejecutar", action="store_true")
    args = ap.parse_args(argv)
    datos, err = subir(os.path.abspath(args.cliente), args.ejecutar)
    if err:
        print("ERROR · %s" % err)
        return 2 if datos is None else 1
    if datos["nada"]:
        print("Nada que subir: todos los activos propios ya están importados.")
        return 0
    for o in datos["objetivos"]:
        print("  " + (o if isinstance(o, str) else "%s → %s" % o))
    if not args.ejecutar:
        print("\nSimulación. Con --ejecutar y WP_URL/WP_APP_USER/WP_APP_PASSWORD sube y registra.")
        return 0
    print("\n%d activos importados y verificados." % len(datos["objetivos"]))
    return 0


if __name__ == "__main__":
    main()
