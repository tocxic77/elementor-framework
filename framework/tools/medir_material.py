#!/usr/bin/env python3
"""Mide qué mecanismos de impacto están habilitados por el material de un cliente.

No es una puerta: es el instrumento que responde «¿este mecanismo siquiera está
disponible?» antes de que alguien lo diseñe. Un mecanismo cuyo material no se puede
medir queda NO DISPONIBLE, no en verde.

Uso:  python medir_material.py --cliente <dir del cliente> [--mecanismos MECANISMOS.yaml]
Sale 0 si pudo medir; 1 si la biblioteca cita un material que no existe.
"""
import argparse
import ast
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from _comun import cargar_yaml  # noqa: E402

MECANISMOS_POR_DEFECTO = os.path.join(AQUI, "..", "04_DIRECTION", "MECANISMOS.yaml")


def lista(valor):
    """`audiencia` se guardó como texto «['a', 'b']» en algunos clientes: se acepta igual."""
    if isinstance(valor, list):
        return valor
    if isinstance(valor, str) and valor.strip().startswith("["):
        try:
            devuelto = ast.literal_eval(valor)
            if isinstance(devuelto, list):
                return devuelto
        except (ValueError, SyntaxError):
            pass
    return [valor] if valor else []


def texto(valor):
    """Las respuestas de 01_NEED.yaml son dicts con `respuesta`; algunas son texto plano."""
    if isinstance(valor, dict):
        return str(valor.get("respuesta") or "").strip()
    return str(valor or "").strip()


# material → (cómo se mide, fuente que lo prueba). None = no hay campo donde vivir.
def medir(cliente):
    need, err_need = cargar_yaml(os.path.join(cliente, "01_NEED.yaml"))
    act, err_act = cargar_yaml(os.path.join(cliente, "03_ASSETS.yaml"))
    if err_need:
        return None, err_need
    respuestas = need.get("respuestas") or {}
    intencion = need.get("intencion") or {}

    visuales = [a for a in (act.get("activos") or [])
                if isinstance(a, dict) and a.get("seleccionado")
                and str(a.get("autorizacion") or "").strip().lower() == "propia"]

    return {
        "problema_declarado": (1 if texto(respuestas.get("a2")) else 0, "01_NEED.yaml a2"),
        "objecion_declarada": (1 if (texto(intencion.get("objecion")) or texto(respuestas.get("b3")))
                               else 0, "01_NEED.yaml intencion.objecion"),
        "conversion_declarada": (1 if texto(intencion.get("accion")) else 0,
                                 "01_NEED.yaml intencion.accion"),
        "audiencia_declarada": (len([x for x in lista(intencion.get("audiencia")) if x]),
                                "01_NEED.yaml intencion.audiencia"),
        "evidencia_visual_propia": (len(visuales),
                                    "03_ASSETS.yaml activos seleccionados con autorizacion: propia"),
        "testimonios_reales": (None, "02_EVIDENCE.yaml: las afirmaciones no declaran tipo"),
        "caso_documentado": (None, "02_EVIDENCE.yaml: las afirmaciones no declaran tipo"),
        "trayectoria_publica": (None, "02_EVIDENCE.yaml: las afirmaciones no declaran tipo"),
        "ofertas_distintas": (None, "01_NEED.yaml: no hay lista de ofertas"),
        "atributos_verificables": (None, "01_NEED.yaml: no hay lista de atributos"),
        "precio_publico": (None, "01_NEED.yaml: no hay campo de precio"),
        "propiedades_propias": (None, "no hay inventario de propiedades propias"),
    }, None


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
    if not mecanismos:
        print("ERROR · %s no declara mecanismos" % args.mecanismos)
        return 1

    medidas, err = medir(args.cliente)
    if err:
        print("ERROR · %s" % err)
        return 1

    # Vocabulario cerrado: un mecanismo que pide un material desconocido es un error de dato.
    desconocidos = sorted({m for v in mecanismos.values()
                           for m in (v.get("requiere") or []) + (v.get("requiere_uno_de") or [])
                           if m not in medidas})
    if desconocidos:
        print("ERROR · la biblioteca cita materiales que no se miden: %s" % ", ".join(desconocidos))
        return 1

    print("MATERIAL                          VALOR    FUENTE")
    for nombre, (valor, fuente) in medidas.items():
        marca = "NO MED" if valor is None else str(valor)
        print("  %-30s %-8s %s" % (nombre, marca, fuente))

    disponibles, faltan = [], []
    for nombre, datos in mecanismos.items():
        # `requiere`: todos. `requiere_uno_de`: al menos uno.
        faltantes = [m for m in (datos.get("requiere") or []) if not medidas.get(m, (None,))[0]]
        alternativas = datos.get("requiere_uno_de") or []
        if alternativas and not any(medidas.get(m, (None,))[0] for m in alternativas):
            faltantes.append("uno de: " + " / ".join(alternativas))
        (faltan if faltantes else disponibles).append((nombre, faltantes))

    print("\nDISPONIBLES %d de %d" % (len(disponibles), len(mecanismos)))
    for nombre, _ in disponibles:
        print("  ✓ " + nombre)

    if faltan:
        print("\nNO DISPONIBLES %d" % len(faltan))
        for nombre, motivos in faltan:
            print("  × %-34s %s" % (nombre, ", ".join(motivos)))
    print("\nUn mecanismo no disponible no se diseña: se declara el hueco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
