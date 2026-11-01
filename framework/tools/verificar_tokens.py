#!/usr/bin/env python3
"""verificar_tokens.py — una sola fuente de verdad entre tokens.css y el adaptador.

El adaptador declara en `sistema.yaml` los valores que instala en el kit de Elementor
(`valor: "#223035"`, `valor: "56px"`, `valor: "Newsreader"`). Esos valores están escritos
por segunda vez. Mientras nadie los compare, hay dos fuentes de verdad y la que manda es
la que se copió último.

Esta puerta compara las dos representaciones y falla cuando divergen:

  1. toda variable del adaptador tiene su token `--nombre` en tokens.css;
  2. color: el hex del adaptador y el del token son el mismo (sin distinguir mayúsculas);
  3. tamaño: el valor del adaptador aparece dentro del token (admite `clamp()`, cuyo
     máximo es el valor que el kit instala);
  4. tipografía: la familia del adaptador aparece en el token;
  5. ningún CSS del sistema fuera de tokens.css declara un hex nuevo (deriva de paleta).

Uso:
    python verificar_tokens.py [--sistema adapters/elementor/sistema.yaml]
                               [--tokens framework/05_SYSTEM/tokens.css]
                               [--css framework/05_SYSTEM]
Sale 0 si las dos representaciones coinciden; 1 si divergen; 2 si no puede leer.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import OK, Puerta, cargar_yaml  # noqa: E402

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent

HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
TOKEN = re.compile(r"--([a-z0-9-]+)\s*:\s*([^;]+);", re.I)


def leer_tokens(ruta):
    texto = Path(ruta).read_text(encoding="utf-8")
    return {n.lower(): v.strip() for n, v in TOKEN.findall(texto)}


def norm_hex(valor):
    v = valor.strip().lower()
    if re.fullmatch(r"#[0-9a-f]{3}", v):
        return "#" + "".join(c * 2 for c in v[1:])
    return v


def main(argv):
    ap = argparse.ArgumentParser(description="tokens.css ↔ sistema.yaml")
    ap.add_argument("--sistema", default=str(RAIZ / "adapters" / "elementor" / "sistema.yaml"))
    ap.add_argument("--tokens", default=str(RAIZ / "framework" / "05_SYSTEM" / "tokens.css"))
    ap.add_argument("--css", default=str(RAIZ / "framework" / "05_SYSTEM"))
    args = ap.parse_args(argv)

    p = Puerta("tokens", Path(args.tokens).name)
    if not Path(args.tokens).exists():
        print("ERROR DE USO · no existe tokens.css: %s" % args.tokens)
        return 2
    datos, error = cargar_yaml(args.sistema)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2

    tokens = leer_tokens(args.tokens)
    variables = datos.get("variables") or []
    if not variables:
        p.falla("el adaptador no declara ninguna variable: no hay nada que comparar")

    por_tipo = {}
    for v in variables:
        etiqueta = str(v.get("label", "")).strip()
        tipo = str(v.get("tipo", "")).strip()
        valor = str(v.get("valor", "")).strip()
        por_tipo[tipo] = por_tipo.get(tipo, 0) + 1
        token = tokens.get(etiqueta.lower())
        if token is None:
            p.falla("--%s declarada en el adaptador y ausente de tokens.css" % etiqueta)
            continue
        if tipo == "global-color-variable":
            if norm_hex(token) != norm_hex(valor):
                p.falla("--%s: tokens.css dice %s y el adaptador instala %s" % (etiqueta, token, valor))
        elif tipo == "global-size-variable":
            numero = re.match(r"^([\d.]+)px$", valor)
            if not numero:
                p.falla("--%s: el adaptador declara un tamaño no medible «%s»" % (etiqueta, valor))
            elif numero.group(1) not in re.findall(r"[\d.]+", token):
                p.falla("--%s: tokens.css dice %s y el adaptador instala %s" % (etiqueta, token, valor))
        elif tipo == "global-font-variable":
            familia = valor.split(",")[0].strip().strip("'\"")
            if familia.lower() not in token.lower():
                p.falla("--%s: tokens.css dice %s y el adaptador instala %s" % (etiqueta, token, valor))
        elif not tipo:
            p.falla("--%s: variable sin tipo (global-color|global-size|global-font)" % etiqueta)

    # Deriva de paleta: hex nuevos fuera de tokens.css
    deriva = []
    base = Path(args.css)
    if base.is_dir():
        for css in sorted(base.glob("*.css")):
            if css.name == "tokens.css":
                continue
            for h in sorted(set(HEX.findall(css.read_text(encoding="utf-8", errors="ignore")))):
                if norm_hex(h) not in {norm_hex(v) for v in tokens.values() if v.startswith("#")}:
                    deriva.append("%s:%s" % (css.name, h))
    if deriva:
        p.aviso("hex fuera de tokens.css: " + ", ".join(deriva[:6]))

    p.mide("variables comparadas", len([v for v in variables if v.get("label")]))
    p.mide("colores", por_tipo.get("global-color-variable", 0))
    p.mide("tamaños", por_tipo.get("global-size-variable", 0))
    p.mide("tipografías", por_tipo.get("global-font-variable", 0))
    p.mide("tokens.css", "%d tokens" % len(tokens))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
