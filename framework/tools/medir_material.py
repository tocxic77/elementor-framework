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

FUENTES = {
    "trayectoria_publica": "01_NEED.yaml trayectoria[].verificable",
    "atributos_verificables": "01_NEED.yaml atributos[].documento",
    "propiedades_propias": "01_NEED.yaml propiedades[] tipo: dominio",
}

# Etiqueta de la fuente para los materiales que distinguen declarado de verificado.
FUENTES = {
    "trayectoria_publica": "01_NEED.yaml trayectoria[].verificable",
    "atributos_verificables": "01_NEED.yaml atributos[].documento",
    "propiedades_propias": "01_NEED.yaml propiedades[] tipo: dominio",
}

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


def hay(valor):
    """0 no habilita el mecanismo, pero tampoco es «no medido»: None sí lo es."""
    return valor is not None and valor > 0


def texto(valor):
    """Las respuestas de 01_NEED.yaml son dicts con `respuesta`; algunas son texto plano."""
    if isinstance(valor, dict):
        return str(valor.get("respuesta") or "").strip()
    return str(valor or "").strip()


# material → (cómo se mide, fuente que lo prueba). None = no hay campo donde vivir.
def medir(cliente):
    need, err_need = cargar_yaml(os.path.join(cliente, "01_NEED.yaml"))
    act, err_act = cargar_yaml(os.path.join(cliente, "03_ASSETS.yaml"))
    evid, _ = cargar_yaml(os.path.join(cliente, "02_EVIDENCE.yaml"))
    evid = evid or {}
    if err_need:
        return None, err_need
    respuestas = need.get("respuestas") or {}
    intencion = need.get("intencion") or {}

    visuales = [a for a in (act.get("activos") or [])
                if isinstance(a, dict) and a.get("seleccionado")
                and str(a.get("autorizacion") or "").strip().lower() == "propia"]

    # Una oferta gratis es una oferta. `precio: 0` es precio publicado; `precio: null` es
    # precio no publicado; la ausencia de `ofertas` no es cero, es NO MEDIDO.
    # Las afirmaciones llevan `tipo`: sin él no se puede saber si son prueba, caso o trayectoria.
    afirmaciones = [a for a in (evid.get("afirmaciones") or []) if isinstance(a, dict)]

    def con_tipo(cual):
        return len([a for a in afirmaciones
                    if str(a.get("tipo") or "").strip().lower() == cual
                    and str(a.get("estado") or "").strip().lower() in ("validada", "validado", "aprobada")])

    # Declarado y vacío no es lo mismo que no declarado.
    def verificados(clave, campo_prueba):
        """Cuenta declaraciones con prueba. Declarar un hecho no lo hace publicable."""
        if clave not in need:
            return None, 0
        entradas = [x for x in (need.get(clave) or []) if isinstance(x, dict)]
        con_prueba = [x for x in entradas if str(x.get(campo_prueba) or "").strip()]
        return len(con_prueba), len(entradas)

    def cuenta(clave, elemento, campos):
        if clave not in need:
            return None
        return len([x for x in (need.get(clave) or [])
                    if isinstance(x, dict) and any(x.get(c) for c in campos)])

    trayectoria = verificados("trayectoria", "verificable")
    atributos = verificados("atributos", "documento")
    # Una propiedad es un dominio propio. Un canal de YouTube se controla, no se posee.
    if "propiedades" in need:
        props = [x for x in (need.get("propiedades") or []) if isinstance(x, dict)]
        dominios = [x for x in props if str(x.get("tipo") or "dominio").strip().lower() == "dominio"]
        propiedades = (len(dominios), len(props))
    else:
        propiedades = (None, 0)

    ofertas = [o for o in (need.get("ofertas") or []) if isinstance(o, dict)]
    con_precio = [o for o in ofertas if o.get("precio") is not None]

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
        "testimonios_reales": (con_tipo("testimonio"),
                               "02_EVIDENCE.yaml afirmaciones tipo: testimonio"),
        "caso_documentado": (con_tipo("caso"), "02_EVIDENCE.yaml afirmaciones tipo: caso"),
        "trayectoria_publica": (trayectoria[0], trayectoria[1]),
        "ofertas_distintas": (len(ofertas) if ofertas else (None if "ofertas" not in need else 0),
                              "01_NEED.yaml ofertas (gratis cuenta)"),
        "precio_publico": (len(con_precio) if ofertas else (None if "ofertas" not in need else 0),
                           "01_NEED.yaml ofertas[].precio (0 = gratis, null = no publicado)"),
        "atributos_verificables": (atributos[0], atributos[1]),
        "propiedades_propias": (propiedades[0], propiedades[1]),
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
        if isinstance(fuente, int):   # (con prueba, declarados)
            fuente = "%s  ·  %d de %d declarados con prueba" % (
                FUENTES.get(nombre, ""), valor or 0, fuente)
        print("  %-30s %-8s %s" % (nombre, marca, fuente))

    disponibles, faltan = [], []
    for nombre, datos in mecanismos.items():
        # `requiere`: todos. `requiere_uno_de`: al menos uno.
        faltantes = [m for m in (datos.get("requiere") or []) if not hay(medidas.get(m, (None,))[0])]
        for material, umbral in (datos.get("minimo") or {}).items():
            valor = medidas.get(material, (None,))[0]
            if valor is None:
                aviso = material
            elif valor < umbral:
                aviso = "%s: %d de %d" % (material, valor, umbral)
            else:
                continue
            if material not in faltantes and aviso not in faltantes:
                faltantes = [f for f in faltantes if f != material] + [aviso]
        alternativas = datos.get("requiere_uno_de") or []
        if alternativas and not any(hay(medidas.get(m, (None,))[0]) for m in alternativas):
            faltantes.append("uno de: " + " / ".join(alternativas))
        (faltan if faltantes else disponibles).append((nombre, faltantes))

    print("\nDISPONIBLES %d de %d" % (len(disponibles), len(mecanismos)))
    for nombre, _ in disponibles:
        print("  ✓ " + nombre)

    if faltan:
        print("\nNO DISPONIBLES %d" % len(faltan))
        for nombre, motivos in faltan:
            print("  × %-34s %s" % (nombre, ", ".join(motivos)))
    print("\nPOR PRINCIPIO")
    no_disponibles = dict(faltan)
    for grupo in sorted({(v.get("grupo") or "sin_grupo") for v in mecanismos.values()}):
        nombres = [n for n, v in mecanismos.items() if (v.get("grupo") or "sin_grupo") == grupo]
        listos = [n for n in nombres if n not in no_disponibles]
        print("  %-12s %d de %d disponibles" % (grupo, len(listos), len(nombres)))

    print("\nUn mecanismo no disponible no se diseña: se declara el hueco.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
