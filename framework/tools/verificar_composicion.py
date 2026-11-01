#!/usr/bin/env python3
"""Verifica que una arquitectura propuesta sólo use lo que el cliente puede sostener.

Comprueba, banda por banda:
  · el mecanismo existe en la biblioteca y está DISPONIBLE según `medir_material`
  · el mecanismo no figura en `prohibidos` (contradicción)
  · el patrón existe en `sistema.yaml` y el componente declarado es el suyo
  · el activo existe, está seleccionado y tiene autorización
  · cada evidencia citada existe en 01_NEED / 02_EVIDENCE
  · la oferta del CTA existe

Una banda sin mecanismo es una banda decorativa: FALLA.
Uso:  python verificar_composicion.py --cliente <dir> [--arquitectura <yaml>]
Sale 0 si la composición se sostiene; 1 si alguna banda promete lo que el material
no permite; 2 si no pudo medir (y entonces no hay verde posible).
"""
import argparse
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402
import medir_material  # noqa: E402

MECANISMOS = os.path.normpath(os.path.join(AQUI, "..", "04_DIRECTION", "MECANISMOS.yaml"))
SISTEMA = os.path.normpath(os.path.join(AQUI, "..", "..", "adapters", "elementor", "sistema.yaml"))
REF = re.compile(r"^(?:(EV|P)-\d+|(trayectoria|atributos|ofertas)\[(\d+)\]|([a-z_]+))$")


def revisar(cliente, ruta):
    bib, err = cargar_yaml(MECANISMOS)
    if err:
        return None, "no se pudo leer la biblioteca: %s" % err
    mecanismos = bib.get("mecanismos") or {}
    sis, err = cargar_yaml(SISTEMA)
    if err:
        return None, "no se pudo leer sistema.yaml: %s" % err
    patrones = sis.get("patrones") or {}
    arq, err = cargar_yaml(ruta)
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
    disponibles, _ = medir_material.disponibilidad(medidas, mecanismos)
    disponibles = {n for n, _ in disponibles}

    piezas = {p.get("id") for p in (evid.get("piezas") or []) if isinstance(p, dict)}
    afirmaciones = {a.get("id") for a in (evid.get("afirmaciones") or []) if isinstance(a, dict)}
    activos = {str(a.get("nombre") or a.get("archivo")): a for a in (act.get("activos") or [])
               if isinstance(a, dict)}
    prohibidos = {p.get("mecanismo") for p in (arq.get("prohibidos") or []) if isinstance(p, dict)}

    fallas, avisos = [], []
    for b in (arq.get("bandas") or []):
        n = b.get("n")
        usados = b.get("mecanismos") or []
        if not usados:
            fallas.append("banda %s: sin mecanismo, es una banda decorativa" % n)

        for m in usados:
            if m not in mecanismos:
                fallas.append("banda %s: mecanismo inexistente «%s»" % (n, m))
            elif m in prohibidos:
                fallas.append("banda %s: «%s» está en la lista de prohibidos" % (n, m))
            elif m not in disponibles:
                fallas.append("banda %s: «%s» no está disponible para este cliente" % (n, m))

        patron = b.get("patron")
        if patron not in patrones:
            fallas.append("banda %s: patrón «%s» no existe en sistema.yaml" % (n, patron))
        else:
            esperado = patrones[patron].get("componente")
            declarado = b.get("componente")
            if esperado != declarado:
                fallas.append("banda %s: componente %s no es el del patrón «%s» (%s)"
                              % (n, declarado, patron, esperado))
            if esperado is None and not b.get("hueco"):
                avisos.append("banda %s: el patrón «%s» no tiene componente y la banda no declara el hueco"
                              % (n, patron))

        activo = b.get("activo")
        if activo:
            if activo not in activos:
                fallas.append("banda %s: activo «%s» no está en 03_ASSETS.yaml" % (n, activo))
            else:
                a = activos[activo]
                aut = str(a.get("autorizacion") or "").strip()
                if not a.get("seleccionado"):
                    fallas.append("banda %s: activo «%s» no está seleccionado" % (n, activo))
                if aut in ("", "None", "pendiente", "no_autorizado"):
                    fallas.append("banda %s: activo «%s» sin autorización (%s)"
                                  % (n, activo, aut or "sin declarar"))

        for ref in (b.get("evidencia") or []):
            m = REF.match(str(ref))
            if not m:
                fallas.append("banda %s: referencia de evidencia ilegible «%s»" % (n, ref))
                continue
            if m.group(1) in ("EV", "P"):
                conjunto = afirmaciones if m.group(1) == "EV" else piezas
                if ref not in conjunto:
                    fallas.append("banda %s: evidencia «%s» no existe" % (n, ref))
            elif m.group(2):
                lista = need.get(m.group(2)) or []
                if int(m.group(3)) >= len(lista):
                    fallas.append("banda %s: evidencia «%s» fuera de rango (%d entradas)"
                                  % (n, ref, len(lista)))
            else:
                clave = m.group(1) if m.group(1) else ref
                if clave in medidas:
                    if not medidas[clave][0]:
                        fallas.append("banda %s: evidencia «%s» vale 0" % (n, ref))
                elif clave not in ("conversion_declarada", "audiencia_declarada"):
                    fallas.append("banda %s: evidencia «%s» no se mide" % (n, ref))

        cta = b.get("cta")
        if cta:
            ref = str(cta.get("oferta") or "")
            m = REF.match(ref)
            if not m or not m.group(2) == "ofertas":
                fallas.append("banda %s: la oferta del CTA no es una referencia a ofertas[]" % n)
            else:
                ofertas = need.get("ofertas") or []
                if int(m.group(3)) >= len(ofertas):
                    fallas.append("banda %s: oferta «%s» fuera de rango" % (n, ref))
            if not str(cta.get("destino") or "").startswith("/"):
                fallas.append("banda %s: destino del CTA no es una ruta del sitio" % n)

    return {"bandas": len(arq.get("bandas") or []), "fallas": fallas,
            "avisos": avisos, "disponibles": len(disponibles), "total": len(mecanismos)}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    ap.add_argument("--arquitectura", default=None)
    args = ap.parse_args(argv)
    cliente = os.path.abspath(args.cliente)
    ruta = args.arquitectura or os.path.join(cliente, "05_SYSTEM", "ARQUITECTURA.yaml")

    datos, err = revisar(cliente, ruta)
    if err:
        print("ERROR · %s" % err)
        return 2

    print("COMPOSICIÓN · %s · %d bandas" % (os.path.basename(ruta), datos["bandas"]))
    print("  mecanismos disponibles en el cliente: %d de %d\n" % (datos["disponibles"], datos["total"]))
    for a in datos["avisos"]:
        print("  REVISAR  " + a)
    for f in datos["fallas"]:
        print("  FALLA    " + f)
    if datos["fallas"]:
        print("\nLa composición no se sostiene: %d fallas." % len(datos["fallas"]))
        return 1
    print("Cada banda usa un mecanismo disponible, un patrón real y evidencia que existe.")
    return 0


if __name__ == "__main__":
    main()
