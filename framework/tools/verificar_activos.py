#!/usr/bin/env python3
"""verificar_activos.py — la regla «una imagen generada nunca reemplaza un real disponible».

Comprueba:
  1. el registro declara activos (un registro vacío es FALLA, no OK);
  2. ningún activo usa ya `usado`, el campo que mezclaba selección y publicación;
  3. todo activo declara nivel (real | derivada | generada);
  4. nivel real: procedencia declarada, y si es `verificada` debe traer `exif: true`;
  5. nivel derivada: cita su documento fuente;
  6. nivel generada: trae `prompt_id`, `motivo_falta` y `tema`, y no ocupa el hueco de un
     real del mismo tema que sigue sin seleccionar;
  7. medida: un activo **seleccionado** sin ancho medido (0, null o ausente) es FALLA; por
     debajo de 2400 px también; si no está seleccionado, es aviso;
  8. derechos: un activo seleccionado sin `autorizacion` declarada es NO MEDIDO — no se
     puede afirmar que publicarlo sea legítimo, y «no lo comprobé» no es «está bien».

`seleccionado` y `publicado_en` responden a dos preguntas distintas y no se sustituyen:
`seleccionado` es la decisión (elegido, y con derechos declarados), `publicado_en` es la
afirmación de dónde aparece. La publicación real la mide verificar_servido.py contra el
HTML. Antes había un solo campo, `usado`, que obligaba a los gates a asumir `usado ==
publicado`, y esa equivalencia resultó falsa contra el cliente real.

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
    if any("usado" in a for a in activos):
        p.falla("el registro todavía usa «usado», que mezcla dos preguntas: "
                "separa «seleccionado» (decisión) y «publicado_en» (afirmación)")

    reales = [a for a in activos if (a.get("nivel") or "").lower() == "real"]
    if activos and not reales:
        p.aviso("0 activos reales: todo el material es derivado o generado; declara por qué")

    for a in activos:
        n = a.get("archivo", "?")
        nivel = (a.get("nivel") or "").lower()
        seleccionado = bool(a.get("seleccionado"))
        destinos = a.get("publicado_en") or []
        autorizacion = (a.get("autorizacion") or "").strip().lower()

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
                      if tema and b.get("tema") == tema and not b.get("seleccionado")]
            if libres:
                p.falla("%s: generada reemplaza real disponible del tema «%s»: %s"
                        % (n, tema, ", ".join(libres)))

        if (a.get("tipo") or "imagen") == "imagen":
            ancho = a.get("ancho")
            medido = isinstance(ancho, int) and ancho > 0
            if not medido:
                (p.falla if seleccionado else p.aviso)(
                    "%s: ancho no medido (ancho=%r)%s"
                    % (n, ancho, " y el activo está seleccionado" if seleccionado else ""))
            elif ancho < MIN_ANCHO:
                (p.falla if seleccionado else p.aviso)(
                    "%s: %d px de ancho, bajo %d → no sirve a sangre%s"
                    % (n, ancho, MIN_ANCHO, " y está seleccionado" if seleccionado else ""))

        if destinos and not seleccionado:
            p.falla("%s: declara publicarse en %s sin estar seleccionado"
                    % (n, ", ".join(map(str, destinos))))
        if seleccionado and not autorizacion:
            p.sin_medir("%s: seleccionado sin autorización declarada (propia/licencia/pendiente)" % n)
        elif seleccionado and autorizacion == "pendiente":
            p.falla("%s: seleccionado y sin autorización de publicación" % n)
        if seleccionado and not destinos:
            p.aviso("%s: seleccionado y todavía sin destino publicado declarado" % n)

    p.mide("activos", "%d · reales %d · derivadas %d · generadas %d" % (
        len(activos),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "real"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "derivada"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "generada")))
    p.mide("seleccionados / sin seleccionar",
           "%d / %d" % (sum(1 for a in activos if a.get("seleccionado")),
                        sum(1 for a in activos if not a.get("seleccionado"))))
    p.mide("con destino publicado", sum(1 for a in activos if a.get("publicado_en")))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
