#!/usr/bin/env python3
"""verificar_evidencia.py — registro de afirmaciones y su uso en la página.

Uso:
  python verificar_evidencia.py <cliente>/02_EVIDENCE.yaml
  python verificar_evidencia.py <cliente>/02_EVIDENCE.yaml --html 05_SYSTEM/index.html

Comprueba:
  1. toda afirmación `validada` tiene fuente y, si cita archivo, el archivo existe;
  2. toda afirmación `rechazada` tiene motivo;
  3. (--html) todo número publicado está en una afirmación validada;
  4. (--html) ningún número de una afirmación rechazada aparece en la página.
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("falta PyYAML: pip install pyyaml")
    sys.exit(2)

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
    if not argv:
        print(__doc__)
        return 2
    base = Path(argv[0])
    if not base.exists():
        print("no existe:", base)
        return 1
    d = yaml.safe_load(base.read_text(encoding="utf-8")) or {}
    afirmaciones = d.get("afirmaciones") or []
    fallas = []
    validas, rechazadas = [], []
    for a in afirmaciones:
        ev = a.get("id", "?")
        estado = (a.get("estado") or "").lower()
        if estado == "validada":
            if not a.get("fuente"):
                fallas.append(f"{ev} validada sin fuente")
            else:
                ruta = Path(str(a["fuente"]).split(":")[0])
                if ruta.suffix and not ruta.exists():
                    fallas.append(f"{ev} fuente inexistente: {ruta}")
            validas.append(a)
        elif estado == "rechazada":
            if not a.get("motivo"):
                fallas.append(f"{ev} rechazada sin motivo")
            rechazadas.append(a)
        else:
            fallas.append(f"{ev} estado no reconocido: {estado or 'vacío'}")

    print("evidencia ·", d.get("cliente", base.stem))
    print("-" * 62)
    print(f"  afirmaciones {len(afirmaciones)} · validadas {len(validas)} · rechazadas {len(rechazadas)}")

    if "--html" in argv:
        html = Path(argv[argv.index("--html") + 1])
        if not html.exists():
            fallas.append(f"no existe la página: {html}")
        else:
            visible = texto_visible(html.read_text(encoding="utf-8", errors="ignore"))
            presentes = numeros(visible)
            permitidos, vetados = set(), set()
            for a in validas:
                permitidos |= numeros(str(a.get("valor", "")))
            for a in rechazadas:
                vetados |= {n for n in numeros(str(a.get("valor", ""))) if n >= 10}
            if not presentes:
                fallas.append(f"NO MEDIDO: 0 cifras detectadas en {html.name}")
            for n in sorted(presentes & vetados):
                fallas.append(f"{n} es cifra rechazada y está publicada en {html.name}")
            huerfanas = sorted(presentes - permitidos)
            for n in huerfanas:
                fallas.append(f"{n} publicada sin afirmación validada")
            print(f"  cifras en página {len(presentes)} · respaldadas {len(presentes & permitidos)}")

    for f in fallas:
        print("  FALLA  ", f)
    print("-" * 62)
    print("EVIDENCIA OK" if not fallas else f"EVIDENCIA INCOMPLETA · {len(fallas)} fallas")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
