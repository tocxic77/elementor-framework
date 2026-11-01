#!/usr/bin/env python3
"""verificar_activos.py — la regla «una imagen generada nunca reemplaza un real disponible».

Uso: python verificar_activos.py <cliente>/03_ASSETS.yaml

Comprueba:
  1. todo activo declara nivel (real | derivada | generada);
  2. nivel real con procedencia verificada debe traer exif: true;
  3. nivel derivada debe citar su fuente documental;
  4. nivel generada debe traer prompt_id y motivo_falta;
  5. si hay un activo real del mismo tema sin usar, la generada no puede ocupar el hueco;
  6. las imágenes deben medir ≥2400 px de ancho para uso de banda completa.
"""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("falta PyYAML: pip install pyyaml")
    sys.exit(2)

MIN_ANCHO = 2400


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    p = Path(argv[0])
    if not p.exists():
        print("no existe:", p)
        return 1
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    activos = d.get("activos") or []
    fallas, avisos = [], []
    for a in activos:
        n = a.get("archivo", "?")
        nivel = (a.get("nivel") or "").lower()
        if nivel not in ("real", "derivada", "generada"):
            fallas.append(f"{n}: nivel no declarado o desconocido «{nivel}»")
            continue
        if nivel == "real":
            if (a.get("procedencia") or "") == "verificada" and not a.get("exif"):
                fallas.append(f"{n}: procedencia verificada sin EXIF")
            if (a.get("procedencia") or "") not in ("verificada", "declarada"):
                fallas.append(f"{n}: procedencia sin declarar")
        if nivel == "derivada" and not a.get("fuente"):
            fallas.append(f"{n}: derivada sin documento fuente")
        if nivel == "generada":
            if not a.get("prompt_id"):
                fallas.append(f"{n}: generada sin prompt_id")
            if not a.get("motivo_falta"):
                fallas.append(f"{n}: generada sin motivo_falta")
            tema = a.get("tema")
            reales_libres = [b.get("archivo") for b in activos
                             if (b.get("nivel") or "").lower() == "real"
                             and tema and b.get("tema") == tema
                             and not b.get("usado")]
            if reales_libres:
                fallas.append("%s: generada reemplaza real disponible del tema «%s»: %s"
                              % (n, tema, ", ".join(reales_libres)))
        if (a.get("tipo") or "imagen") == "imagen":
            w = a.get("ancho") or 0
            if w and w < MIN_ANCHO:
                avisos.append(f"{n}: {w} px de ancho, bajo {MIN_ANCHO} → no sirve a sangre")
        if a.get("usado") and (a.get("autorizacion") or "").lower() == "pendiente":
            fallas.append(f"{n}: en uso y sin autorización de publicación")
    print("activos ·", d.get("cliente", p.stem))
    print("-" * 62)
    print("  total %d · reales %d · derivadas %d · generadas %d" % (
        len(activos),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "real"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "derivada"),
        sum(1 for a in activos if (a.get("nivel") or "").lower() == "generada")))
    for f in fallas:
        print("  FALLA  ", f)
    for a in avisos[:6]:
        print("  avisa  ", a)
    print("-" * 62)
    print("ACTIVOS OK" if not fallas else f"ACTIVOS CON FALLAS · {len(fallas)}")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
