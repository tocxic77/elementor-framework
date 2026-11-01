#!/usr/bin/env python3
"""verificar_need.py — la puerta de 01_NEED, ejecutable.

Uso:  python verificar_need.py <cliente>/01_NEED.yaml
Sale 1 si falta una respuesta de nivel `bloquea` o si una respuesta no tiene fuente.
"""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("falta PyYAML: pip install pyyaml")
    sys.exit(2)

# id: (nivel, pregunta) — 20 preguntas del cuestionario, mismo número en el formulario
PREGUNTAS = {
    "a1": ("bloquea", "¿qué se vende en una frase?"),
    "a2": ("bloquea", "¿qué problema resuelve y en qué se nota?"),
    "a3": ("bloquea", "¿qué alternativa usa el comprador si esto no existiera?"),
    "a4": ("bloquea", "¿qué acción primaria y medible?"),
    "a5": ("bloquea", "¿qué se puede afirmar con evidencia propia?"),
    "a6": ("avisa", "¿qué está prohibido decir?"),
    "b1": ("bloquea", "¿quién firma el contrato?"),
    "b2": ("avisa", "¿quién influye y quién usa lo entregado?"),
    "b3": ("bloquea", "¿cuál es la objeción principal?"),
    "b4": ("avisa", "¿qué sabe ya el comprador?"),
    "b5": ("info", "¿en qué contexto lee?"),
    "c1": ("bloquea", "¿qué material propio existe y con qué medida?"),
    "c2": ("bloquea", "¿qué afirmaciones están autorizadas y con fuente?"),
    "c3": ("bloquea", "¿qué material está vetado?"),
    "c4": ("avisa", "¿qué falta y cuánto cuesta?"),
    "c5": ("avisa", "¿quién autoriza cada pieza?"),
    "d1": ("bloquea", "¿quién edita después de entregar?"),
    "d2": ("avisa", "¿qué puede cambiar sin romper el sistema?"),
    "d3": ("bloquea", "¿quién firma la dirección visual?"),
    "d4": ("info", "¿cuándo se revisa?"),
}
VACIOS = {"", "pendiente", "tbd", "por definir", "n/a", "null", "none"}


def vacio(v):
    if v is None:
        return True
    if isinstance(v, str) and v.strip().lower() in VACIOS:
        return True
    if isinstance(v, (list, dict)) and not v:
        return True
    return False


def main(path):
    p = Path(path)
    if not p.exists():
        print("no existe el archivo:", path)
        return 1
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    r = d.get("respuestas") or {}
    fallas, avisos, ok = [], [], 0
    for qid, (nivel, preg) in PREGUNTAS.items():
        item = r.get(qid)
        valor = item.get("respuesta", item.get("valor")) if isinstance(item, dict) else item
        fuente = item.get("fuente") if isinstance(item, dict) else None
        if vacio(valor):
            (fallas if nivel == "bloquea" else avisos).append("%-3s %s" % (qid.upper(), preg))
        elif isinstance(item, dict) and vacio(fuente):
            fallas.append("%-3s %s · respondida sin fuente" % (qid.upper(), preg))
        else:
            ok += 1
    print("necesidad ·", d.get("cliente", p.stem), "·", d.get("estado", "sin estado"))
    print("-" * 66)
    print(f"  respondidas con fuente  {ok}/{len(PREGUNTAS)}")
    extra = [k for k in r if k not in PREGUNTAS]
    if extra:
        print("  claves fuera de esquema  %s" % ", ".join(map(str, extra)))
    for f in fallas:
        print("  BLOQUEA  ", f)
    for a in avisos:
        print("  avisa    ", a)
    print("-" * 62)
    bloqueado = bool(fallas)
    print("NEED BLOQUEADO" if bloqueado else "NEED COMPLETO",
          f"· {len(fallas)} bloqueantes · {len(avisos)} avisos")
    return 1 if bloqueado else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
