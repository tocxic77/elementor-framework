#!/usr/bin/env python3
"""Verifica que una especificación de componente sirva de verdad a los mecanismos
que dice satisfacer.

No mira el aspecto: mira que cada material que el mecanismo exige tenga una ranura
capaz de llevarlo, y que el cliente tenga ese material en cantidad suficiente.

Uso:  python verificar_componente.py --cliente <dir> --spec <yaml>
Sale 0 si la especificación sostiene sus mecanismos; 1 si declara satisfacer algo
que sus ranuras no pueden llevar; 2 si no pudo leer; 3 si el material no está medido.
"""
import argparse
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402
import medir_material  # noqa: E402

MECANISMOS = os.path.normpath(os.path.join(AQUI, "..", "04_DIRECTION", "MECANISMOS.yaml"))


def revisar(cliente, ruta_spec):
    bib, err = cargar_yaml(MECANISMOS)
    if err:
        return None, err
    mecanismos = bib.get("mecanismos") or {}
    spec, err = cargar_yaml(ruta_spec)
    if err:
        return None, err
    medidas, err = medir_material.medir(cliente)
    if err:
        return None, err

    portado = {r.get("material") for r in (spec.get("ranuras") or [])
               if isinstance(r, dict) and r.get("material")}
    fallas, avisos, cubiertos = [], [], []
    for nombre in (spec.get("satisface") or []):
        datos = mecanismos.get(nombre)
        if not datos:
            fallas.append("«%s» no existe en la biblioteca de mecanismos" % nombre)
            continue
        faltan = [m for m in (datos.get("requiere") or []) if m not in portado]
        if faltan:
            fallas.append("«%s» exige %s y ninguna ranura lo lleva" % (nombre, ", ".join(faltan)))
            continue
        for material in (datos.get("requiere") or []):
            valor = medidas.get(material, (None,))[0]
            if valor is None:
                avisos.append("«%s» depende de %s, que no está medido" % (nombre, material))
            elif valor == 0:
                fallas.append("«%s» depende de %s y el cliente tiene 0" % (nombre, material))
            else:
                cubiertos.append("%s ← %s (%d)" % (nombre, material, valor))
        for material, umbral in (datos.get("minimo") or {}).items():
            valor = medidas.get(material, (None,))[0]
            if valor is None or valor < umbral:
                fallas.append("«%s» exige %s ≥ %d y hay %s" % (nombre, material, umbral, valor))

    return {"componente": spec.get("componente"), "estado": spec.get("estado"),
            "cubiertos": cubiertos, "fallas": fallas, "avisos": avisos}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--spec", required=True)
    args = ap.parse_args(argv)

    datos, err = revisar(os.path.abspath(args.cliente), os.path.abspath(args.spec))
    if err:
        print("ERROR · %s" % err)
        return 2

    print("COMPONENTE · %s · estado %s" % (datos["componente"], datos["estado"]))
    for c in datos["cubiertos"]:
        print("  OK       " + c)
    for a in datos["avisos"]:
        print("  NO MEDIDO " + a)
    for f in datos["fallas"]:
        print("  FALLA    " + f)
    if datos["fallas"]:
        print("\nLa especificación promete mecanismos que sus ranuras no sostienen.")
        return 1
    if datos["avisos"]:
        return 3
    print("\nCada mecanismo declarado tiene ranura y material suficiente en el cliente.")
    return 0


if __name__ == "__main__":
    main()
