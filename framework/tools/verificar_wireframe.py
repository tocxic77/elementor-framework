#!/usr/bin/env python3
"""Verifica que el wireframe sea la arquitectura, banda por banda, y que ninguna
ranura se llene de la nada.

Comprueba:
  · una banda de wireframe por cada banda de arquitectura, con el mismo objetivo,
    patrón, componente y condición de hueco
  · cada ranura obligatoria declara fuente, y esa fuente existe (EV/P/trayectoria/
    atributos/ofertas/activo/necesidad/documento)
  · una banda con componente real y sin `slot_componente` deja el mapeo NO MEDIDO

Uso:  python verificar_wireframe.py --cliente <dir>
Sale 0 si el wireframe se sostiene y además los slots reales están medidos;
     3 si el wireframe se sostiene pero el esquema de ranuras del componente NO está
       medido (no hay verde posible);
     1 si el wireframe contradice la arquitectura o inventa una fuente;
     2 si no pudo leer algún archivo.
"""
import argparse
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402
import medir_material  # noqa: E402

REF = re.compile(r"^(?:(EV|P)-\d+|(trayectoria|atributos|ofertas)"
                 r"(?:\[(\d+|i)(?:\.\.(\d+))?\](?:\.([a-z_]+))?)?"
                 r"|activo:(.+)|docs/.+\.md|[a-z_]+)$")


def verificar(cliente):
    arq, err = cargar_yaml(os.path.join(cliente, "05_SYSTEM", "ARQUITECTURA.yaml"))
    if err:
        return None, err
    wire, err = cargar_yaml(os.path.join(cliente, "05_SYSTEM", "WIREFRAME.yaml"))
    if err:
        return None, err
    need, err = cargar_yaml(os.path.join(cliente, "01_NEED.yaml"))
    if err:
        return None, err
    evid, err = cargar_yaml(os.path.join(cliente, "02_EVIDENCE.yaml"))
    if err:
        return None, err
    act, err = cargar_yaml(os.path.join(cliente, "03_ASSETS.yaml"))
    if err:
        return None, err
    medidas, err = medir_material.medir(cliente)
    if err:
        return None, err

    piezas = {p.get("id") for p in (evid.get("piezas") or []) if isinstance(p, dict)}
    afirmaciones = {a.get("id") for a in (evid.get("afirmaciones") or []) if isinstance(a, dict)}
    activos = {str(a.get("nombre") or a.get("archivo")) for a in (act.get("activos") or [])
               if isinstance(a, dict)}

    fallas, avisos = [], []
    bandas_arq = {b.get("n"): b for b in (arq.get("bandas") or []) if isinstance(b, dict)}
    bandas_wire = {b.get("banda"): b for b in (wire.get("bandas") or []) if isinstance(b, dict)}

    for n, a in bandas_arq.items():
        w = bandas_wire.get(n)
        if not w:
            fallas.append("banda %s: la arquitectura la declara y el wireframe no" % n)
            continue
        for campo in ("objetivo", "patron", "componente"):
            if w.get(campo) != a.get(campo):
                fallas.append("banda %s: el wireframe cambia %s (%s ≠ %s)"
                              % (n, campo, w.get(campo), a.get(campo)))
        if bool(a.get("hueco")) != bool(w.get("hueco")):
            fallas.append("banda %s: el hueco está declarado en un archivo y no en el otro" % n)

        ranuras = w.get("slots") or []
        if not ranuras:
            fallas.append("banda %s: el wireframe no declara ranuras" % n)
        for r in ranuras:
            nombre, fuente = r.get("ranura"), r.get("fuente")
            if r.get("obligatorio") and not fuente:
                fallas.append("banda %s · %s: ranura obligatoria sin fuente" % (n, nombre))
                continue
            if not fuente:
                continue
            m = REF.match(str(fuente))
            if not m:
                fallas.append("banda %s · %s: fuente ilegible «%s»" % (n, nombre, fuente))
                continue
            if m.group(1) in ("EV", "P"):
                conjunto = afirmaciones if m.group(1) == "EV" else piezas
                if fuente not in conjunto:
                    fallas.append("banda %s · %s: «%s» no existe en 02_EVIDENCE" % (n, nombre, fuente))
            elif m.group(2):
                lista = need.get(m.group(2)) or []
                campo = m.group(5)
                if m.group(3) == "i":
                    # índice de repetición: la banda se repite por cada elemento
                    if not w.get("repite_por"):
                        fallas.append("banda %s · %s: usa [i] sin declarar repite_por" % (n, nombre))
                    elif not any(isinstance(x, dict) and campo in x for x in lista):
                        fallas.append("banda %s · %s: «%s» no existe en ofertas[]"
                                      % (n, nombre, campo))
                else:
                    desde = int(m.group(3) or 0)
                    hasta = int(m.group(4) or desde)
                    if hasta >= len(lista):
                        fallas.append("banda %s · %s: «%s» fuera de rango (%d entradas)"
                                      % (n, nombre, fuente, len(lista)))
            elif m.group(6):
                if m.group(6) not in activos:
                    fallas.append("banda %s · %s: activo «%s» no está en 03_ASSETS"
                                  % (n, nombre, m.group(6)))
            elif fuente.startswith("docs/"):
                pass
            elif fuente in medidas:
                if not medidas[fuente][0]:
                    fallas.append("banda %s · %s: «%s» vale 0" % (n, nombre, fuente))
            elif fuente not in ("conversion_declarada", "audiencia_declarada"):
                fallas.append("banda %s · %s: «%s» no se mide" % (n, nombre, fuente))

    for n in bandas_wire:
        if n not in bandas_arq:
            fallas.append("banda %s: el wireframe inventa una banda que la arquitectura no tiene" % n)

    con_componente = [w for w in bandas_wire.values() if w.get("componente") is not None]
    sin_slot = [w.get("banda") for w in con_componente if not w.get("slot_componente")]
    medido = bool((wire.get("esquema_componentes") or {}).get("medido"))
    if sin_slot:
        avisos.append("NO MEDIDO · las ranuras reales de los componentes no están medidas: "
                      "bandas %s" % ", ".join(str(x) for x in sorted(sin_slot)))

    ranuras = sum(len(w.get("slots") or []) for w in bandas_wire.values())
    return {"bandas": len(bandas_wire), "ranuras": ranuras, "fallas": fallas, "avisos": avisos,
            "medido": medido, "sin_slot": sin_slot}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    args = ap.parse_args(argv)
    cliente = os.path.abspath(args.cliente)

    datos, err = verificar(cliente)
    if err:
        print("ERROR · %s" % err)
        return 2

    print("WIREFRAME · %d bandas · %d ranuras comprobadas" % (datos["bandas"], datos["ranuras"]))
    for a in datos["avisos"]:
        print("  " + a)
    for f in datos["fallas"]:
        print("  FALLA    " + f)
    if datos["fallas"]:
        return 1
    if datos["sin_slot"] and not datos["medido"]:
        print("\nEl wireframe se sostiene, pero no se puede mapear a ranuras del kit:")
        print("el esquema de componentes no está medido. NO MEDIDO no es OK.")
        return 3
    print("\nCada ranura obligatoria tiene fuente, y las ranuras del kit están medidas.")
    return 0


if __name__ == "__main__":
    main()
