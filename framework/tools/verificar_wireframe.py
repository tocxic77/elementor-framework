#!/usr/bin/env python3
"""Verifica que el wireframe sea la arquitectura, banda por banda, que ninguna
ranura se llene de la nada y que cada ranura exista de verdad en el kit.

Comprueba:
  · una banda de wireframe por cada banda de arquitectura, con el mismo objetivo,
    patron, componente y condicion de hueco
  · cada ranura obligatoria declara fuente, y esa fuente existe
  · `slot_componente` nombra una ranura que el componente SI expone, segun
    adapters/elementor/COMPONENTES.yaml (medido por MCP)
  · una ranura obligatoria sin asiento en el kit se declara `hueco_kit: true`
  · una banda sin componente y con `spec` tiene su especificacion y esta cubre
    todas sus ranuras

Uso:  python verificar_wireframe.py --cliente <dir>
Sale 0 si todo encaja y el kit no tiene huecos; 3 si el wireframe se sostiene pero
queda algun hueco de kit o una medicion pendiente; 1 si contradice la arquitectura,
inventa una fuente o nombra una ranura que el componente no tiene; 2 si no pudo leer.
"""
import argparse
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml, salir  # noqa: E402
import medir_material  # noqa: E402

KIT = os.path.normpath(os.path.join(AQUI, "..", "..", "adapters", "elementor", "COMPONENTES.yaml"))
SISTEMA = os.path.normpath(os.path.join(AQUI, "..", "..", "adapters", "elementor", "sistema.yaml"))
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
    kit, err = cargar_yaml(KIT)
    if err:
        return None, "no se pudo leer el kit medido: %s" % err
    medidas, err = medir_material.medir(cliente)
    if err:
        return None, err

    sis, err = cargar_yaml(SISTEMA)
    if err:
        return None, "no se pudo leer sistema.yaml: %s" % err
    patrones = sis.get("patrones") or {}
    no_admite = kit.get("restricciones_permanentes") or {}
    kit_por_id = {c.get("id"): {r.get("nombre") for r in (c.get("ranuras") or [])}
                  for c in (kit.get("componentes") or []) if isinstance(c, dict)}
    piezas = {p.get("id") for p in (evid.get("piezas") or []) if isinstance(p, dict)}
    afirmaciones = {a.get("id") for a in (evid.get("afirmaciones") or []) if isinstance(a, dict)}
    activos = {str(a.get("nombre") or a.get("archivo")) for a in (act.get("activos") or [])
               if isinstance(a, dict)}

    fallas, huecos = [], []
    import hashlib
    ruta_esquema = os.path.join(cliente, "05_SYSTEM", "KIT-SCHEMA.yaml")
    if os.path.exists(ruta_esquema):
        esquema, err_e = cargar_yaml(ruta_esquema)
        if err_e:
            fallas.append("KIT-SCHEMA.yaml no se pudo leer: %s" % err_e)
        else:
            huella = hashlib.sha256(open(KIT, "rb").read()).hexdigest()
            if esquema.get("sha256_fuente") != huella:
                fallas.append("KIT-SCHEMA.yaml quedó viejo: su huella no coincide con el kit medido")
    bandas_arq = {b.get("n"): b for b in (arq.get("bandas") or []) if isinstance(b, dict)}
    bandas_wire = {b.get("banda"): b for b in (wire.get("bandas") or []) if isinstance(b, dict)}

    for n, a in sorted(bandas_arq.items()):
        w = bandas_wire.get(n)
        if not w:
            fallas.append("banda %s: la arquitectura la declara y el wireframe no" % n)
            continue
        for campo in ("objetivo", "patron", "componente"):
            if w.get(campo) != a.get(campo):
                fallas.append("banda %s: el wireframe cambia %s (%s != %s)"
                              % (n, campo, w.get(campo), a.get(campo)))
        if bool(a.get("hueco")) != bool(w.get("hueco")):
            fallas.append("banda %s: el hueco esta declarado en un archivo y no en el otro" % n)

        componente = w.get("componente")
        props = set()
        if componente is not None:
            if componente not in kit_por_id:
                fallas.append("banda %s: el componente %s no esta medido en COMPONENTES.yaml"
                              % (n, componente))
            else:
                props = kit_por_id[componente]

        spec_ranuras = set()
        if w.get("spec"):
            ruta_spec = os.path.join(cliente, "05_SYSTEM", w["spec"])
            spec, err = cargar_yaml(ruta_spec)
            if err:
                fallas.append("banda %s: falta la especificacion %s" % (n, w["spec"]))
            else:
                spec_ranuras = {r.get("nombre") for r in (spec.get("ranuras") or [])
                                if isinstance(r, dict)}

        ranuras = w.get("slots") or []
        if not ranuras:
            fallas.append("banda %s: el wireframe no declara ranuras" % n)
        for r in ranuras:
            nombre, fuente = r.get("ranura"), r.get("fuente")
            slot = r.get("slot_componente")

            if slot is not None:
                if componente is not None and props and slot not in props:
                    permanente = slot in (no_admite.get(componente) or [])
                    fallas.append("banda %s - %s: el componente %s no expone la ranura '%s'%s"
                                  % (n, nombre, componente, slot,
                                     " (restriccion permanente medida)" if permanente else ""))
                elif componente is None and w.get("spec") and slot not in spec_ranuras:
                    fallas.append("banda %s - %s: la especificacion %s no declara la ranura '%s'"
                                  % (n, nombre, w.get("spec"), slot))
                elif componente is None and not w.get("spec"):
                    fallas.append("banda %s - %s: nombra la ranura '%s' pero la banda no tiene componente"
                                  % (n, nombre, slot))
            elif r.get("obligatorio") and not r.get("hueco_kit") and not r.get("fuera_de_componente"):
                fallas.append("banda %s - %s: ranura obligatoria sin asiento en el kit y sin declarar el hueco"
                              % (n, nombre))
            if r.get("hueco_kit"):
                # un hueco bloquea sólo si la ranura es obligatoria y el patrón ya
                # tiene componente: si el patrón no lo tiene, es backlog declarado.
                tiene_componente = (patrones.get(w.get("patron")) or {}).get("componente") is not None
                bloquea = bool(r.get("obligatorio")) and tiene_componente
                huecos.append({"texto": "banda %s - %s: el kit no tiene esta ranura" % (n, nombre),
                               "bloquea": bloquea})

            if r.get("obligatorio") and not fuente:
                fallas.append("banda %s - %s: ranura obligatoria sin fuente" % (n, nombre))
                continue
            if not fuente:
                continue
            m = REF.match(str(fuente))
            if not m:
                fallas.append("banda %s - %s: fuente ilegible '%s'" % (n, nombre, fuente))
                continue
            if m.group(1) in ("EV", "P"):
                conjunto = afirmaciones if m.group(1) == "EV" else piezas
                if fuente not in conjunto:
                    fallas.append("banda %s - %s: '%s' no existe en 02_EVIDENCE" % (n, nombre, fuente))
            elif m.group(2):
                lista = need.get(m.group(2)) or []
                campo = m.group(5)
                if m.group(3) == "i":
                    if not w.get("repite_por"):
                        fallas.append("banda %s - %s: usa [i] sin declarar repite_por" % (n, nombre))
                    elif not any(isinstance(x, dict) and campo in x for x in lista):
                        fallas.append("banda %s - %s: '%s' no existe en ofertas[]" % (n, nombre, campo))
                else:
                    desde = int(m.group(3) or 0)
                    hasta = int(m.group(4) or desde)
                    if hasta >= len(lista):
                        fallas.append("banda %s - %s: '%s' fuera de rango (%d entradas)"
                                      % (n, nombre, fuente, len(lista)))
            elif m.group(6):
                if m.group(6) not in activos:
                    fallas.append("banda %s - %s: activo '%s' no esta en 03_ASSETS"
                                  % (n, nombre, m.group(6)))
            elif fuente.startswith("docs/"):
                pass
            elif fuente in medidas:
                if not medidas[fuente][0]:
                    fallas.append("banda %s - %s: '%s' vale 0" % (n, nombre, fuente))
            elif fuente not in ("conversion_declarada", "audiencia_declarada"):
                fallas.append("banda %s - %s: '%s' no se mide" % (n, nombre, fuente))

    for n in bandas_wire:
        if n not in bandas_arq:
            fallas.append("banda %s: el wireframe inventa una banda que la arquitectura no tiene" % n)

    ranuras = sum(len(w.get("slots") or []) for w in bandas_wire.values())
    return {"bandas": len(bandas_wire), "ranuras": ranuras, "fallas": fallas, "huecos": huecos,
            "medido": bool((wire.get("esquema_componentes") or {}).get("medido"))}, None


@salir
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--cliente", required=True)
    args = ap.parse_args(argv)
    cliente = os.path.abspath(args.cliente)

    datos, err = verificar(cliente)
    if err:
        print("ERROR - %s" % err)
        return 2

    bloquean = [h for h in datos["huecos"] if h["bloquea"]]
    print("WIREFRAME - %d bandas - %d ranuras - %d huecos de kit (%d bloquean)"
          % (datos["bandas"], datos["ranuras"], len(datos["huecos"]), len(bloquean)))
    for h in datos["huecos"]:
        print(("  HUECO    " if h["bloquea"] else "  BACKLOG  ") + h["texto"])
    for f in datos["fallas"]:
        print("  FALLA    " + f)
    if datos["fallas"]:
        print("\nEl wireframe promete lo que la composicion o el kit no sostienen.")
        return 1
    if bloquean or not datos["medido"]:
        print("\nCada ranura que existe esta mapeada a una ranura real del kit.")
        print("Bloquean la construccion %d ranuras obligatorias sin asiento." % len(bloquean))
        return 3
    if datos["huecos"]:
        print("\nTodas las ranuras obligatorias tienen asiento. Quedan %d huecos no bloqueantes."
              % len(datos["huecos"]))
        return 0
    print("\nTodas las ranuras tienen fuente y asiento real en el kit.")
    return 0


if __name__ == "__main__":
    main()
