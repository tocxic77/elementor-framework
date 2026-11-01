#!/usr/bin/env python3
"""Cruza los mecanismos observados en los referentes con el material del cliente.

Dos preguntas, una salida:
  1. ¿Los mecanismos que el referente usa existen en la biblioteca? (un nombre inventado es error)
  2. ¿Cuáles de esos mecanismos puede sostener este cliente con el material que tiene?

Es un instrumento, no una puerta: no impide publicar, impide copiar lo insostenible.

Uso:  python medir_referentes.py --cliente <dir> [--mecanismos MECANISMOS.yaml]
Sale 0 si pudo medir; 1 si el archivo cita un mecanismo que no está en la biblioteca.
"""
import argparse
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml  # noqa: E402
import medir_material  # noqa: E402

MECANISMOS_POR_DEFECTO = os.path.join(AQUI, "..", "04_DIRECTION", "MECANISMOS.yaml")


def disponibilidad(mecanismos, medidas):
    """Devuelve (disponibles, motivos por mecanismo no disponible)."""
    libres, motivos = set(), {}
    for nombre, datos in mecanismos.items():
        faltan = [m for m in (datos.get("requiere") or []) if not medidas.get(m, (None,))[0]]
        alternativas = datos.get("requiere_uno_de") or []
        if alternativas and not any(medidas.get(m, (None,))[0] for m in alternativas):
            faltan.append("uno de: " + " / ".join(alternativas))
        if faltan:
            motivos[nombre] = ", ".join(faltan)
        else:
            libres.add(nombre)
    return libres, motivos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--mecanismos", default=MECANISMOS_POR_DEFECTO)
    args = ap.parse_args()

    bib, err = cargar_yaml(args.mecanismos)
    if err:
        print("ERROR · %s" % err)
        return 1
    mecanismos = bib.get("mecanismos") or {}

    ref, err = cargar_yaml(os.path.join(args.cliente, "REFERENTES.yaml"))
    if err:
        print("ERROR · %s" % err)
        return 1
    sitios = ref.get("referentes") or []
    if not sitios:
        print("NO MEDIDO · %s/REFERENTES.yaml no declara referentes" % args.cliente)
        return 1

    medidas, err = medir_material.medir(args.cliente)
    if err:
        print("ERROR · %s" % err)
        return 1
    libres, motivos = disponibilidad(mecanismos, medidas)

    inventados, total_obs, sostenibles_total, distintos = [], 0, set(), set()
    for sitio in sitios:
        nombre = sitio.get("sitio") or "(sin nombre)"
        obs = sitio.get("observados") or []
        total_obs += len(obs)
        distintos.update(obs)
        inventados += ["%s → %s" % (nombre, m) for m in obs if m not in mecanismos]
        puede = [m for m in obs if m in libres]
        no_puede = [m for m in obs if m in mecanismos and m not in libres]
        sostenibles_total.update(puede)
        print("\n%s · %s · %s" % (nombre, sitio.get("tipo", "?"),
                                  "%d mecanismos observados" % len(obs)))
        print("  puede sostener: %d" % len(puede))
        if no_puede:
            print("  no puede sostener: %d" % len(no_puede))
            for m in no_puede:
                print("    × %-34s falta %s" % (m, motivos.get(m, "material")))

    print("\n%d observaciones · %d mecanismos distintos en %d referentes · %d sostenibles aquí"
          % (total_obs, len(distintos), len(sitios), len(sostenibles_total)))

    if inventados:
        print("\nERROR · mecanismos que no están en la biblioteca:")
        for x in inventados:
            print("  - " + x)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
