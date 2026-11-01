#!/usr/bin/env python3
"""verificar_activos.py — la regla «una imagen generada nunca reemplaza un real disponible».

Comprueba:
  1. el registro declara activos (un registro vacío es FALLA, no OK);
  2. todo activo declara nivel (real | derivada | generada);
  3. nivel real: procedencia declarada, y si es `verificada` debe traer `exif: true`;
  4. nivel derivada: cita su documento fuente;
  5. nivel generada: trae `prompt_id`, `motivo_falta` y `tema`, y no ocupa el hueco de un
     real del mismo tema que sigue sin usar;
  6. medida: un activo **en uso** cuyo ancho no se midió (0, null o ausente) es FALLA —
     no se puede afirmar que sirva a sangre sin haberlo medido;
  7. medida: un activo en uso por debajo de 2400 px es FALLA (el docstring de la fase 4
     prometía esta regla y el código sólo avisaba); si no está en uso, es aviso.

Uso:    python verificar_activos.py <cliente>/03_ASSETS.yaml
Sale    0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta, cargar_yaml  # noqa: E402

MIN_ANCHO = 2400
NIVELES = ("real", "derivada", "generada")


def main(argv):
    ap = argparse.ArgumentParser(description="puerta de 03_ASSETS")
    ap.add_argument("activos")
    args = ap.parse_args(argv)

    datos, error = cargar_yaml(args.activos)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2

    p = Puerta("activos", Path(args.activos).name)
    activos = datos.get("activos") or []
    if not activos:
        p.falla("el registro no declara activos: no hay nada que verificar y la fase exige material medido")

    reales = [a for a in activos if (a.get("nivel") or "").lower() == "real"]
    if activos and not reales:
        p.aviso("0 activos reales: todo el material es derivado o generado; declara por qué")

    for a in activos:
        n = a.get("archivo", "?")
        nivel = (a.get("nivel") or "").lower()
        usado = bool(a.get("usado"))

        if nivel not in NIVELES:
            p.falla("%s: nivel no declarado o desconocido «%s»" % (n, nivel))
            continue

        if nivel == "real":
            procedencia = (a.get("procedencia") or "").lower()
            if procedencia not in ("verificada", "declarada"):
                p.falla("%s: procedencia sin declarar" % n)
            if procedencia == "verificada" and not a.get("exif"):
                p.falla("%s: procedencia verificada sin EXIF" % n)

        if nivel == "derivada" and not a.get("fuente"):
            p.falla("%s: derivada sin documento fuente" % n)

        if nivel == "generada":
            if not a.get("prompt_id"):
                p.falla("%s: generada sin prompt_id" % n)
            if not a.get("motivo_falta"):
                p.falla("%s: generada sin motivo_falta" % n)
            tema = a.get("tema")
            if not tema:
                p.falla("%s: generada sin tema: no se puede comprobar que no reemplace a un real" % n)
            libres = [b.get("archivo") for b in reales
                      if tema and b.get("tema") == tema and not b.get("usado")]
            if libres:
                p.falla("%s: generada reemplaza real disponible del tema «%s»: %s"
                        % (n, tema, ", ".join(libres)))

        if (a.get("tipo") or "imagen") == "imagen":
            ancho = a.get("ancho")
            medido = isinstance(ancho, int) and ancho > 0
            if not medido:
                (p.falla if usado else p.aviso)(
                    "%s: ancho no medido (ancho=%r)%s"
                    % (n, ancho, " y el activo está en uso" if usado else ""))
            elif ancho < MIN_ANCHO:
                (p.falla if usado else p.aviso)(
                    "%s: %d px de ancho, bajo %d → no sirve a sangre%s"
                    % (n, ancho, MIN_ANCHO, " y está en uso" if usado else ""))

        if usado and (a.get("autorizacion") or "").lower() == "pendiente":
            p.falla("%s: en uso y sin autorización de publicación" % n)

    p.mide("activos", "%d · reales %d · derivadas %d · generadas %d" % (
        len(activos),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "real"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "derivada"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "generada")))
    p.mide("en uso / sin usar", "%d / %d" % (sum(1 for a in activos if a.get("usado")),
                                             sum(1 for a in activos if not a.get("usado"))))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
