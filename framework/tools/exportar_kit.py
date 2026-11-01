#!/usr/bin/env python3
"""Exporta el esquema del kit medido al cliente, con huella del origen.

Existe para que `05_SYSTEM/KIT-SCHEMA.yaml` no sea una segunda verdad escrita a
mano: se genera desde adapters/elementor/COMPONENTES.yaml y lleva el sha256 de su
fuente. Si el kit se vuelve a medir y cambia, la huella deja de coincidir y
`verificar_wireframe.py` lo declara.

Uso:  python exportar_kit.py --cliente <dir>
"""
import argparse
import hashlib
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402

KIT = os.path.normpath(os.path.join(AQUI, "..", "..", "adapters", "elementor", "COMPONENTES.yaml"))


def exportar(cliente):
    datos, err = cargar_yaml(KIT)
    if err:
        return None, err
    sha = hashlib.sha256(open(KIT, "rb").read()).hexdigest()
    lineas = [
        "# GENERADO por framework/tools/exportar_kit.py — no editar a mano.",
        "# Esquema del kit para el cliente: mismas ranuras que COMPONENTES.yaml, con huella.",
        "generado: %s" % datos.get("medido"),
        "fuente: adapters/elementor/COMPONENTES.yaml",
        "sha256_fuente: %s" % sha,
        "instrumento: %s" % datos.get("fuente"),
        "no_medido: %s" % (datos.get("no_medido") or []),
        "",
        "componentes:",
    ]
    for c in datos.get("componentes") or []:
        lineas.append("  %d:" % c["id"])
        lineas.append("    nombre: %s" % c["nombre"])
        lineas.append("    uid: %s" % c["uid"])
        lineas.append("    ranuras: [%s]" % ", ".join(r["nombre"] for r in c["ranuras"]))
        lineas.append("    tipos: {%s}" % ", ".join("%s: %s" % (r["nombre"], r["tipo"])
                                                    for r in c["ranuras"]))
        for x in (c.get("restricciones") or []):
            lineas.append("    # %s" % x)
    destino = os.path.join(cliente, "05_SYSTEM", "KIT-SCHEMA.yaml")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    return {"destino": destino, "componentes": len(datos.get("componentes") or []), "sha": sha[:12]}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    args = ap.parse_args(argv)
    datos, err = exportar(os.path.abspath(args.cliente))
    if err:
        print("ERROR · %s" % err)
        return 2
    print("KIT-SCHEMA · %d componentes · sha256 %s · %s"
          % (datos["componentes"], datos["sha"], datos["destino"]))
    return 0


if __name__ == "__main__":
    main()
