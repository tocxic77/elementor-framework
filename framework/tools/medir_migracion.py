#!/usr/bin/env python3
"""Mide cuánta autoridad pública vive todavía en dominios ajenos.

La migración de autoridad no es copiar contenido: es publicar en el dominio propio
una pieza por cada hecho que hoy sólo existe en casa de otro. Este instrumento
cuenta las piezas, dice cuántas son propias y cuáles se caen cuando el dominio
ajeno cierre.

Uso:  python medir_migracion.py --cliente <dir del cliente>
Sale 0 si pudo medir; 1 si una pieza publicable no tiene ni URL ni archivo;
2 si falta el cliente o el archivo archivado que la pieza dice tener.
"""
import argparse
import os
import sys
from urllib.parse import urlparse

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402


def bases(cliente):
    """Dónde buscar un archivo archivado: junto al cliente y subiendo hasta 03_Desarrollo."""
    candidatas = [cliente]
    try:
        candidatas.append(os.path.dirname(os.path.dirname(os.path.dirname(cliente))))
    except Exception:
        pass
    return [b for b in candidatas if b]


def dominio_de(url):
    if not url:
        return None
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def medir(cliente):
    need, err_need = cargar_yaml(os.path.join(cliente, "01_NEED.yaml"))
    if err_need:
        return None, err_need
    evid, err_evid = cargar_yaml(os.path.join(cliente, "02_EVIDENCE.yaml"))
    if err_evid:
        return None, err_evid

    propios = {dominio_de("https://" + str(p.get("dominio")))
               for p in (need.get("propiedades") or [])
               if isinstance(p, dict) and str(p.get("tipo") or "dominio") == "dominio"}
    propios.discard(None)

    piezas = [p for p in (evid.get("piezas") or []) if isinstance(p, dict)]
    if not piezas:
        return None, "02_EVIDENCE.yaml no declara piezas públicas: no hay nada que medir"

    filas, faltan_prueba = [], []
    for p in piezas:
        url, archivo = p.get("url"), p.get("archivo")
        host = dominio_de(url)
        if p.get("publicable") and not (url or archivo):
            faltan_prueba.append(p.get("id") or p.get("titulo"))
        sitio = "propia" if host and host in propios else ("ajena" if host else "sin url")
        existe = None
        if archivo:
            existe = any(os.path.exists(os.path.join(b, archivo)) for b in bases(cliente))
        filas.append({"id": p.get("id"), "tipo": p.get("tipo"), "sitio": sitio,
                      "host": host, "archivo": existe, "vigencia": p.get("vigencia"),
                      "publicable": bool(p.get("publicable"))})
    return {"filas": filas, "propios": sorted(propios), "sin_prueba": faltan_prueba}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    args = ap.parse_args(argv)
    cliente = os.path.abspath(args.cliente)

    datos, err = medir(cliente)
    if err:
        print("ERROR · %s" % err)
        return 2

    filas = datos["filas"]
    publicables = [f for f in filas if f["publicable"]]
    propias = [f for f in publicables if f["sitio"] == "propia"]
    ajenas = [f for f in publicables if f["sitio"] == "ajena"]

    print("MIGRACIÓN DE AUTORIDAD · %s" % os.path.basename(cliente.rstrip("/\\")))
    print("  dominios propios: %s\n" % (", ".join(datos["propios"]) or "ninguno"))
    print("  %-6s %-20s %-7s %-9s %s" % ("ID", "TIPO", "SITIO", "ARCHIVO", "VIGENCIA"))
    for f in filas:
        archivo = "sí" if f["archivo"] else ("NO" if f["archivo"] is False else "—")
        print("  %-6s %-20s %-7s %-9s %s" % (f["id"], (f["tipo"] or "")[:20], f["sitio"], archivo,
                                             f["vigencia"] or "—"))
        if f["archivo"] is False:
            print("         ↑ el archivo declarado no está en disco: la prueba no se puede mostrar")

    total = len(publicables)
    print("\nAUTORIDAD MIGRADA  %d de %d  (%d %%)" % (
        len(propias), total, round(100.0 * len(propias) / total) if total else 0))
    if ajenas:
        print("SIGUE FUERA DE CASA")
        for f in ajenas:
            print("  × %-6s %-20s %s" % (f["id"], f["tipo"], f["host"] or "sin dominio"))
    if datos["sin_prueba"]:
        print("\nERROR · piezas publicables sin URL ni archivo: %s" % ", ".join(datos["sin_prueba"]))
        return 1
    return 0


if __name__ == "__main__":
    main()
