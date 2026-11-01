#!/usr/bin/env python3
"""verificar_release.py — una sola secuencia: no se puede publicar salteando puertas.

El framework asumía que el operador corre todas las puertas. La realidad operativa es que
corre las mínimas. Este comando corre la secuencia completa en orden, se detiene en la
primera FALLA y no declara OK si alguna puerta quedó NO MEDIDA (sin instrumento).

Pasos (en este orden, todos contra un cliente):

    1  independencia   el framework no nombra al cliente
    2  need            01_NEED.yaml — 20 preguntas con fuente
    3  evidencia       02_EVIDENCE.yaml (+ cada página de 05_SYSTEM)
    4  activos         03_ASSETS.yaml — procedencia y medida de la imagen
    5  tokens          tokens.css ↔ sistema.yaml — una sola fuente de verdad
    6  estatico        05_SYSTEM/*.html — capa estática de la puerta de calidad
    7  sistema         el kit vivo de Elementor (requiere ELEMENTOR_MCP_URL)
    8  estructura      ADAPTER.md reglas 1-7 sobre el export de _elementor_data del cliente

Uso:
    python verificar_release.py [<cliente>] [--html archivo ...] [--json]
    python verificar_release.py                      # sólo las puertas del repositorio

Códigos: 0 todo medido y en verde · 1 alguna FALLA · 3 algo quedó NO MEDIDO.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import FALLA, NOMBRE, NO_MEDIDO, OK  # noqa: E402

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent


def correr(nombre, script, args):
    """Ejecuta una puerta y devuelve (código, primera línea de resultado, salida)."""
    ruta = Path(script) if Path(script).is_absolute() else (AQUI / script)
    if not ruta.exists():
        return 2, "falta la puerta %s" % script, ""
    r = subprocess.run([sys.executable, str(ruta)] + [str(a) for a in args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    salida = (r.stdout or "") + (r.stderr or "")
    resumen = next((l.strip() for l in reversed(salida.strip().splitlines()) if l.strip()), "")
    return r.returncode, resumen, salida


def main(argv):
    ap = argparse.ArgumentParser(description="secuencia de release")
    ap.add_argument("cliente", nargs="?", default="")
    ap.add_argument("--html", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    cliente = Path(args.cliente).resolve() if args.cliente else None
    pasos = []

    if cliente:
        if not cliente.is_dir():
            print("ERROR DE USO · no existe el cliente: %s" % cliente)
            return 2
        htmls = list(args.html)
        sistema_dir = cliente / "05_SYSTEM"
        if not htmls and sistema_dir.is_dir():
            htmls = sorted(str(h) for h in sistema_dir.glob("*.html"))
        pasos += [
            ("independencia", "verificar_independencia.py", ["--clients", str(cliente.parent)]),
            ("need", "verificar_need.py", [cliente / "01_NEED.yaml"]),
            ("evidencia", "verificar_evidencia.py",
             [cliente / "02_EVIDENCE.yaml"] + sum([["--html", h] for h in htmls], [])),
            ("activos", "verificar_activos.py", [cliente / "03_ASSETS.yaml"]),
        ]
    pasos.append(("tokens", "verificar_tokens.py", []))
    if cliente and (cliente / "05_SYSTEM").is_dir():
        pasos.append(("estatico", "verificar_estatico.py", [cliente / "05_SYSTEM"]))
    if os.environ.get("ELEMENTOR_MCP_URL"):
        pasos.append(("sistema", str(RAIZ / "adapters" / "elementor" / "verificar_sistema.py"), []))
    else:
        pasos.append(("sistema", "", []))

    # Estructura: se audita el export si el cliente tiene uno; si no, NO MEDIDO.
    export = None
    if cliente:
        for patron in ("05_SYSTEM/_elementor_data*.json", "06_DEPLOYMENT/estructura*.json",
                       "**/_elementor_data*.json"):
            encontrados = sorted(cliente.glob(patron))
            if encontrados:
                export = encontrados[0]
                break
    if export:
        pasos.append(("estructura", str(RAIZ / "adapters" / "elementor" / "auditar_estructura.py"),
                      [export]))
    else:
        pasos.append(("estructura", "", []))

    resultados = []
    cortado = False
    for nombre, script, argumentos in pasos:
        if cortado:
            resultados.append({"paso": nombre, "codigo": None, "resultado": "no ejecutado (secuencia cortada)"})
            continue
        if not script:
            motivo = {
                "sistema": "sin ELEMENTOR_MCP_URL: el kit vivo no se midió",
                "estructura": "sin export de _elementor_data: el artefacto publicado no se auditó",
            }.get(nombre, "sin instrumento")
            resultados.append({"paso": nombre, "codigo": NO_MEDIDO, "resultado": motivo})
            continue
        codigo, resumen, salida = correr(nombre, script, argumentos)
        resultados.append({"paso": nombre, "codigo": codigo, "resultado": resumen, "salida": salida})
        if codigo == FALLA:
            cortado = True

    codigos = [r["codigo"] for r in resultados if r["codigo"] is not None]
    if FALLA in codigos:
        codigo_final = FALLA
    elif NO_MEDIDO in codigos:
        codigo_final = NO_MEDIDO
    else:
        codigo_final = OK

    if args.json:
        print(json.dumps({"resultado": NOMBRE[codigo_final],
                          "cliente": str(cliente) if cliente else None,
                          "pasos": [{k: v for k, v in r.items() if k != "salida"} for r in resultados]},
                         ensure_ascii=False, indent=2))
        return codigo_final

    print("release · %s" % (cliente.name if cliente else "repositorio"))
    print("-" * 78)
    print("%-14s %-8s %s" % ("puerta", "salida", "resultado"))
    for r in resultados:
        marca = {OK: "OK", FALLA: "FALLA", NO_MEDIDO: "NO MED", 2: "ERROR", None: "—"}[r["codigo"]]
        print("%-14s %-8s %s" % (r["paso"], marca, r["resultado"][:80]))
    print("-" * 78)
    fallidas = [r["paso"] for r in resultados if r["codigo"] == FALLA]
    no_medidas = [r["paso"] for r in resultados if r["codigo"] == NO_MEDIDO]
    if fallidas:
        print("NO PUBLICABLE · fallan: %s" % ", ".join(fallidas))
        for r in resultados:
            if r["codigo"] == FALLA:
                print()
                print(r.get("salida", "").strip())
    elif no_medidas:
        print("NO PUBLICABLE · sin medir: %s" % ", ".join(no_medidas))
    else:
        print("PUBLICABLE · todas las puertas medidas y en verde")
    return codigo_final


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
