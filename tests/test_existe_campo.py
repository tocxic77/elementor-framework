"""Regresión del agujero que permitió construir bandas con fuentes inexistentes.

Antes: `fuente: problema_declarado` pasaba el gate porque el campo también existe como
material medido, aunque en 01_NEED.yaml esté en null. El wireframe citaba un campo
vacío y nadie protestaba.

Se prueba la función, no el gate entero: es la unidad que decide "esta fuente existe".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "framework" / "tools"))
from _comun import existe_campo  # noqa: E402

NEED = {
    "respuestas": {"a1": {"respuesta": "texto real"}, "a2": {"respuesta": None}},
    "atributos": [{"atributo": "Ingeniero agrónomo"}, {"atributo": "Jefe de laboratorio"}],
    "intencion": {"audiencia": ["propietarios"]},
    "problema_declarado": None,
}

CASOS = [
    ("campo vacío con nombre válido", "problema_declarado", False, "vacio"),
    ("campo inexistente", "problema_que_nadie_escribio", False, "no existe"),
    ("índice fuera de rango", "atributos[9]", False, "indice"),
    ("lista sin índice", "atributos", True, None),
    ("campo anidado con valor", "respuestas.a1.respuesta", True, None),
    ("campo anidado en null", "respuestas.a2.respuesta", False, "vacio"),
    ("campo anidado con índice", "atributos[0].atributo", True, None),
    ("clave ausente en el anidado", "atributos[0].inexistente", False, "clave"),
    ("no es un campo", "docs/PRODUCT.md", False, "no es un campo"),
]


def main():
    fallas = 0
    for nombre, ref, esperado, pista in CASOS:
        obtenido, motivo = existe_campo(NEED, ref)
        if obtenido != esperado or (pista and pista not in (motivo or "")):
            fallas += 1
            print("FALLA  %-32s ref=%-28s obtenido %s (%s) · esperado %s"
                  % (nombre, ref, obtenido, motivo, esperado))
        else:
            print("ok     %-32s %s" % (nombre, motivo or "existe"))
    print("%d casos · %d ok · %d fallas" % (len(CASOS), len(CASOS) - fallas, fallas))
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
