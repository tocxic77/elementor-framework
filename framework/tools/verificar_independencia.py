#!/usr/bin/env python3
"""verificar_independencia.py — el framework no puede nombrar a ningún cliente.

Lee los nombres de carpeta en `clients/` y los busca dentro de `framework/` **y** de
`adapters/` (el adaptador también se distribuye: si nombra a un cliente, deja de ser
reutilizable). Sale 1 si aparece alguno.

Un repositorio sin `clients/` no puede demostrar independencia: sale NO MEDIDO (3), no OK.
Para correrlo en CI hace falta un cliente de prueba: `--clients tests/fixtures/clients`.

Uso:
    python verificar_independencia.py [--clients DIR] [--framework DIR] [--adapters DIR]
Sale 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta  # noqa: E402

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
EXCLUIR = {".png", ".jpg", ".jpeg", ".mp4", ".zip", ".pyc"}


def main(argv):
    ap = argparse.ArgumentParser(description="independencia del framework")
    ap.add_argument("--clients", default=str(RAIZ / "clients"))
    ap.add_argument("--framework", default=str(RAIZ / "framework"))
    ap.add_argument("--adapters", default=str(RAIZ / "adapters"))
    args = ap.parse_args(argv)

    p = Puerta("independencia")
    clients = Path(args.clients)
    if not clients.is_dir():
        p.aviso("no existe %s: no hay nombres de cliente contra los que medir" % clients)
        return p.imprimir()
    nombres = sorted(d.name.lower() for d in clients.iterdir()
                     if d.is_dir() and not d.name.startswith(("_", ".")))
    if not nombres:
        p.aviso("%s no tiene ninguna carpeta de cliente" % clients)
        return p.imprimir()

    revisados, hallazgos = 0, []
    cortos = [n for n in nombres if len(n) < 4]
    for n in cortos:
        p.aviso("nombre de cliente demasiado corto para buscarlo sin falsos positivos: «%s»" % n)
    buscables = [n for n in nombres if len(n) >= 4]
    # Coincidencia por token: `prueba` no debe aparecer dentro de «comprueba» ni de
    # «tabla-como-prueba». Guiones y dígitos cuentan como parte del token.
    patrones = [(n, re.compile(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(n))) for n in buscables]
    for raiz in (Path(args.framework), Path(args.adapters)):
        if not raiz.is_dir():
            continue
        for archivo in sorted(raiz.rglob("*")):
            if not archivo.is_file() or archivo.suffix.lower() in EXCLUIR:
                continue
            if any(parta in (".git", "__pycache__") for parta in archivo.parts):
                continue
            revisados += 1
            try:
                lineas = archivo.read_text(encoding="utf-8", errors="ignore").lower().splitlines()
            except OSError:
                continue
            for n, patron in patrones:
                for i, linea in enumerate(lineas, 1):
                    if patron.search(linea):
                        hallazgos.append((archivo.relative_to(RAIZ), i, n, linea.strip()[:70]))

    p.mide("clientes", "%d (%s)" % (len(nombres), ", ".join(nombres) or "ninguno"))
    p.mide("archivos revisados", revisados)
    for ruta, i, n, linea in hallazgos:
        p.falla("ACOPLA %s:%d [%s] %s" % (ruta, i, n, linea))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
