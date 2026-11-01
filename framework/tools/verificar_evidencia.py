#!/usr/bin/env python3
"""verificar_evidencia.py — registro de afirmaciones y su uso en la página.

Comprueba:
  1. toda afirmación `validada` tiene fuente y, si cita archivo, el archivo existe
     (la ruta se resuelve contra el YAML, no contra el directorio de invocación);
  2. toda afirmación `rechazada` tiene motivo;
  3. un registro sin afirmaciones es una FALLA: no hay nada que sostenga la página;
  4. (--html) todo número publicado está en una afirmación validada;
  5. (--html) ningún número de una afirmación rechazada aparece en la página;
  6. (--html) una página sin cifras detectables se reporta NO MEDIDO, no OK.

Uso:
    python verificar_evidencia.py <cliente>/02_EVIDENCE.yaml
    python verificar_evidencia.py <cliente>/02_EVIDENCE.yaml --html <cliente>/05_SYSTEM/index.html
    python verificar_evidencia.py <cliente>/02_EVIDENCE.yaml --html a.html --html b.html

Sale  0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta, archivo_de, cargar_yaml, resolver_fuente  # noqa: E402

CLAIM = re.compile(r"(\d[\d.,]*)\s*(\+|%|países|profesionales|organizaciones|años|plantas|empresas)")


def numeros(texto):
    """Números de afirmación (con +, % o unidad), normalizados a entero."""
    out = set()
    for n, _u in CLAIM.findall(texto):
        limpio = n.replace(".", "").replace(",", "").strip()
        if limpio.isdigit():
            out.add(int(limpio))
    return out


def texto_visible(html):
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", html)


def main(argv):
    ap = argparse.ArgumentParser(description="puerta de 02_MATERIAL")
    ap.add_argument("evidencia")
    ap.add_argument("--html", action="append", default=[],
                    help="página a cruzar contra el registro (repetible)")
    args = ap.parse_args(argv)

    base = archivo_de(args.evidencia)
    datos, error = cargar_yaml(args.evidencia)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2

    p = Puerta("evidencia", Path(args.evidencia).name)
    afirmaciones = datos.get("afirmaciones") or []
    if not afirmaciones:
        p.falla("el registro no tiene afirmaciones: la fase exige al menos una con fuente")

    validas, rechazadas = [], []
    for a in afirmaciones:
        ev = a.get("id", "?")
        estado = (a.get("estado") or "").lower()
        if estado == "validada":
            fuente = a.get("fuente")
            if not fuente:
                p.falla("%s validada sin fuente" % ev)
            else:
                ruta = resolver_fuente(fuente, base)
                if ruta is not None and not ruta.exists():
                    p.falla("%s fuente inexistente: %s (ruta resuelta contra el directorio del YAML)"
                            % (ev, ruta.name if ruta.parent == base else ruta))
            validas.append(a)
        elif estado == "rechazada":
            if not a.get("motivo"):
                p.falla("%s rechazada sin motivo" % ev)
            rechazadas.append(a)
        else:
            p.falla("%s estado no reconocido: %s" % (ev, estado or "vacío"))

    p.mide("afirmaciones", len(afirmaciones))
    p.mide("validadas / rechazadas", "%d / %d" % (len(validas), len(rechazadas)))

    permitidos, vetados = set(), set()
    sin_cifras = []
    for a in validas:
        permitidos |= numeros(str(a.get("valor", "")))
    for a in rechazadas:
        vetados |= {n for n in numeros(str(a.get("valor", ""))) if n >= 10}

    for pagina in args.html:
        html = Path(pagina)
        if not html.is_absolute() and not html.exists():
            html = base / html
        if not html.exists():
            p.falla("no existe la página: %s" % pagina)
            continue
        visible = texto_visible(html.read_text(encoding="utf-8", errors="ignore"))
        presentes = numeros(visible)
        if not presentes:
            sin_cifras.append(html.name)
            p.aviso("%s: 0 cifras detectables, las reglas 4 y 5 no aplican en esa página" % html.name)
            continue
        p.mide("cifras en %s" % html.name,
               "%d · respaldadas %d" % (len(presentes), len(presentes & permitidos)))
        for n in sorted(presentes & vetados):
            p.falla("%d es cifra de una afirmación rechazada y está publicada en %s" % (n, html.name))
        for n in sorted(presentes - permitidos):
            p.falla("%d publicada sin afirmación validada en %s" % (n, html.name))

    if args.html:
        cruzadas = len(args.html) - len(sin_cifras)
        p.mide("páginas cruzadas", "%d de %d con cifras" % (cruzadas, len(args.html)))
        if cruzadas == 0:
            p.sin_medir("ninguna de las %d páginas tenía cifras detectables: la regla 4 no se midió"
                        % len(args.html))
    else:
        p.aviso("sin --html: se verificó el registro, no la página publicada")

    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
