#!/usr/bin/env python3
"""Convierte el material que falta en un plan de entrevista.

Lee lo que el cliente tiene (medir_material), lo que la biblioteca necesita (MECANISMOS)
y el protocolo de MATERIALES.yaml, y devuelve sólo lo que hay que conseguir: a quién
preguntarle, con qué pregunta, qué documento lo prueba y en qué campo se archiva.

No es una guía genérica: es la lista de huecos de este cliente.

Uso:  python plan_material.py --cliente <dir>
Sale 0 si pudo medir; 1 si la biblioteca usa un material sin protocolo.
"""
import argparse
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml  # noqa: E402
import medir_material  # noqa: E402

MECANISMOS = os.path.join(AQUI, "..", "04_DIRECTION", "MECANISMOS.yaml")
PROTOCOLO = os.path.join(AQUI, "..", "04_DIRECTION", "MATERIALES.yaml")
ORDEN = ["dueño", "cliente_final", "material_fotografico", "archivo"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--mecanismos", default=MECANISMOS)
    ap.add_argument("--protocolo", default=PROTOCOLO)
    args = ap.parse_args()

    bib, err = cargar_yaml(args.mecanismos)
    if err:
        print("ERROR · %s" % err)
        return 1
    prot, err = cargar_yaml(args.protocolo)
    if err:
        print("ERROR · %s" % err)
        return 1

    protocolo = prot.get("materiales") or {}
    usados = {m for v in (bib.get("mecanismos") or {}).values()
              for m in (v.get("requiere") or []) + (v.get("requiere_uno_de") or [])
              + list((v.get("minimo") or {}).keys())}
    sin_protocolo = sorted(usados - set(protocolo))
    if sin_protocolo:
        print("ERROR · la biblioteca usa materiales sin protocolo de obtención:")
        for m in sin_protocolo:
            print("  - " + m)
        return 1

    medidas, err = medir_material.medir(args.cliente)
    if err:
        print("ERROR · %s" % err)
        return 1

    faltan = {}
    for nombre, valor in medidas.items():
        if valor[0] is not None and valor[0] > 0:
            continue
        umbral = (protocolo[nombre].get("umbral")
                  if nombre in protocolo else 1) or 1
        faltan[nombre] = (valor[0], umbral)

    if not faltan:
        print("MATERIAL COMPLETO · no hay nada que pedir")
        return 0

    print("LO QUE FALTA · %d de %d materiales\n" % (len(faltan), len(medidas)))
    for quien in ORDEN:
        grupo = [(n, v) for n, v in faltan.items()
                 if (protocolo.get(n) or {}).get("quien") == quien]
        if not grupo:
            continue
        print("A %s" % quien.upper().replace("_", " "))
        for nombre, (valor, umbral) in grupo:
            p = protocolo[nombre]
            estado = "no medido" if valor is None else "%d de %d" % (valor, umbral)
            print("\n  · %s  (%s)" % (nombre, estado))
            for pregunta in (p.get("pregunta") or []):
                print("      ?  %s" % pregunta)
            print("      →  documento: %s" % p.get("documento", "—"))
            print("      →  queda en:  %s" % p.get("destino", "—"))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
