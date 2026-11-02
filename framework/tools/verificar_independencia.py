#!/usr/bin/env python3
"""verificar_independencia.py — el framework no puede nombrar a ningún cliente.

Dos medidas, porque una sola es ciega:

1. **Nombres de cliente.** Lee las carpetas de `clients/` y busca cada nombre dentro de
   `framework/` y `adapters/`. Sin `clients/` esta medida no aplica: el repositorio
   publicado nunca tiene clientes, así que sola daría NO MEDIDO para siempre.
2. **Dominios citados.** Toda URL en `framework/` y `adapters/` tiene que apuntar a un
   dominio declarado de herramienta o documentación. Es la medida que sí corre en el
   repositorio publicado, y la que detecta que alguien escribió la URL del sitio de un
   cliente en un ejemplo.

Uso:
    python verificar_independencia.py [--clients DIR] [--framework DIR] [--adapters DIR]
                                      [--permitir dominio ...]
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

# Dominios que el framework puede citar: documentación y herramientas que usa.
DOMINIOS = {
    "github.com", "raw.githubusercontent.com", "api.github.com", "objects.githubusercontent.com",
    "img.shields.io", "shields.io",
    "elementor.com", "elementorcdn.com", "wordpress.org", "developer.wordpress.org", "w.org",
    "w3.org", "schema.org",
    "fonts.googleapis.com", "fonts.gstatic.com",
    "python.org", "pypi.org", "npmjs.com",
    "localhost", "127.0.0.1", "ejemplo.cl", "example.com",
}
RE_URL = re.compile(r"https?://([a-z0-9][a-z0-9.-]*\.[a-z]{2,})")


def permitido(dominio, extra):
    if dominio in DOMINIOS or dominio in extra:
        return True
    return any(dominio.endswith("." + d) for d in (DOMINIOS | extra))


def main(argv):
    ap = argparse.ArgumentParser(description="independencia del framework")
    ap.add_argument("--clients", default=str(RAIZ / "clients"))
    ap.add_argument("--framework", default=str(RAIZ / "framework"))
    ap.add_argument("--adapters", default=str(RAIZ / "adapters"))
    ap.add_argument("--permitir", nargs="*", default=[], help="dominios extra aceptados")
    args = ap.parse_args(argv)

    p = Puerta("independencia")
    extra = {d.strip().lower() for d in args.permitir if d.strip()}
    raices = [Path(r) for r in (args.framework, args.adapters) if Path(r).is_dir()]
    if not raices:
        p.sin_medir("no existe framework/ ni adapters/ que revisar")
        return p.imprimir()

    # 1 · nombres de cliente
    clients = Path(args.clients)
    nombres = []
    if not clients.is_dir():
        p.aviso("no existe %s: el repositorio publicado no declara clientes, no hay nombres que buscar" % clients)
    else:
        nombres = sorted(d.name.lower() for d in clients.iterdir()
                         if d.is_dir() and not d.name.startswith(("_", ".")))
        if not nombres:
            p.aviso("%s no tiene ninguna carpeta de cliente" % clients)
    cortos = [n for n in nombres if len(n) < 4]
    for n in cortos:
        p.aviso("nombre de cliente demasiado corto para buscarlo sin falsos positivos: «%s»" % n)
    buscables = [n for n in nombres if len(n) >= 4]
    patrones = [(n, re.compile(r"(?<![a-z0-9-])%s(?![a-z0-9-])" % re.escape(n))) for n in buscables]

    revisados, acoplamientos, dominios = 0, [], {}
    for raiz in raices:
        for archivo in sorted(raiz.rglob("*")):
            if not archivo.is_file() or archivo.suffix.lower() in EXCLUIR:
                continue
            if any(parte in (".git", "__pycache__") for parte in archivo.parts):
                continue
            revisados += 1
            try:
                lineas = archivo.read_text(encoding="utf-8", errors="ignore").lower().splitlines()
            except OSError:
                continue
            for i, linea in enumerate(lineas, 1):
                for n, patron in patrones:
                    if patron.search(linea):
                        acoplamientos.append((archivo.relative_to(RAIZ), i, "ACOPLA a «%s»" % n, linea.strip()[:70]))
                for dominio in RE_URL.findall(linea):
                    dominios.setdefault(dominio, []).append("%s:%d" % (archivo.relative_to(RAIZ), i))

    p.mide("archivos revisados", revisados)
    p.mide("nombres de cliente buscados", "%d" % len(buscables) if buscables else "0 (repositorio sin clients/)")
    p.mide("dominios distintos citados", "%d (%s)" % (len(dominios), ", ".join(sorted(dominios)) or "ninguno"))

    for ruta, i, motivo, linea in acoplamientos:
        p.falla("%s %s:%d %s" % (motivo, ruta, i, linea))
    externos = {d: v for d, v in dominios.items() if not permitido(d, extra)}
    for dominio, sitios in sorted(externos.items()):
        p.falla("DOMINIO no declarado %s en %s (si es herramienta, añádelo a DOMINIOS)" % (dominio, ", ".join(sitios[:3])))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
