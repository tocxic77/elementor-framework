#!/usr/bin/env python3
"""verificar_estatico.py — capa estática de la puerta de calidad.

Uso:  python verificar_estatico.py <carpeta-o-archivo>
Salida: informe legible + exit 1 si falla un bloqueante.

No necesita navegador: mira los archivos. La capa renderizada (contraste computado,
desborde, rejillas) vive en verificar.js y se ejecuta sobre la página servida.
"""
import os
import re
import sys

BLOQUEA = "BLOQUEA"
AVISA = "avisa"
INFO = "info"

HEX = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")


def archivos(base, ext):
    if os.path.isfile(base):
        return [base]
    out = []
    for root, _, files in os.walk(base):
        for f in files:
            if f.lower().endswith(ext):
                out.append(os.path.join(root, f))
    return sorted(out)


def leer(p):
    with open(p, encoding="utf-8", errors="ignore") as fh:
        return fh.read()


rows = []


def check(nivel, ok, nombre, detalle):
    rows.append((nivel, ok, nombre, detalle))


def main(base):
    htmls = archivos(base, ".html")
    csss = archivos(base, ".css")
    if not htmls:
        print("no hay HTML en", base)
        return 2

    # 1 · un solo h1 por página
    for h in htmls:
        n = len(re.findall(r"<h1[\s>]", leer(h), flags=re.I))
        check(BLOQUEA, n == 1, os.path.basename(h) + " · h1", str(n))

    # 2 · viewport presente
    for h in htmls:
        ok = bool(re.search(r'name=["\']viewport["\']', leer(h), flags=re.I))
        check(BLOQUEA, ok, os.path.basename(h) + " · viewport", "ok" if ok else "falta meta viewport")

    # 3 · cero page-id en CSS
    total_pid = sum(len(re.findall(r"page-id", leer(c))) for c in csss)
    check(BLOQUEA, total_pid == 0, "CSS sin page-id", str(total_pid) + " ocurrencias")

    # 4 · estilos en línea
    inline = sum(len(re.findall(r"\sstyle=[\"']", leer(h))) for h in htmls)
    check(AVISA, inline == 0, "sin estilos en línea", str(inline) + " atributos style=")

    # 5 · deriva de paleta: hex fuera de tokens.css
    drifts = []
    for c in csss:
        if os.path.basename(c) == "tokens.css":
            continue
        for m in sorted(set(HEX.findall(leer(c)))):
            drifts.append(os.path.basename(c) + ":" + m)
    check(AVISA, len(drifts) == 0, "colores fuera de tokens.css", ", ".join(drifts[:6]) or "ninguno")

    # 6 · recursos referenciados existen
    faltan = []
    for h in htmls:
        base_dir = os.path.dirname(h)
        for ref in re.findall(r'(?:src|href)=["\']([^"\'#?:]+)["\']', leer(h)):
            if ref.startswith(("http", "//", "mailto:", "tel:")):
                continue
            if not os.path.exists(os.path.join(base_dir, ref)):
                faltan.append(os.path.basename(h) + " → " + ref)
    check(BLOQUEA, len(faltan) == 0, "recursos locales existen", ", ".join(faltan[:5]) or "todos")

    # 7 · peso de lo referenciado por la página principal (informativo)
    principal = next((h for h in htmls if os.path.basename(h).lower() == "index.html"), htmls[0])
    peso = 0
    base_dir = os.path.dirname(principal)
    for ref in re.findall(r'(?:src|href)="([^"#?:]+)"', leer(principal)):
        if ref.startswith(("http", "//", "mailto:", "tel:")):
            continue
        p = os.path.join(base_dir, ref)
        if os.path.isfile(p):
            peso += os.path.getsize(p)
    check(INFO, True, "peso de " + os.path.basename(principal), "%.1f MB" % (peso / 1048576.0))

    # 8 · tokens presentes: en la carpeta o enlazados desde otro directorio del repo
    tokens_ok = any(os.path.basename(c) == "tokens.css" for c in csss)
    if not tokens_ok:
        for h in htmls:
            for ref in re.findall(r'href=["\']([^"\'#?:]+\.css)["\']', leer(h)):
                p = os.path.normpath(os.path.join(os.path.dirname(h), ref))
                if os.path.basename(p) == "tokens.css" and os.path.isfile(p):
                    tokens_ok = True
    check(BLOQUEA, tokens_ok, "tokens.css presente", "ok" if tokens_ok else "no encontrado, ni local ni enlazado")

    bloqueantes = [r for r in rows if r[0] == BLOQUEA and not r[1]]
    ancho = max(len(r[2]) for r in rows) + 2
    print("\nverificación estática ·", base)
    print("-" * (ancho + 46))
    for nivel, ok, nombre, detalle in rows:
        marca = "OK   " if ok else ("FALLA" if nivel == BLOQUEA else "avisa")
        print("%s  %-*s %s" % (marca, ancho, nombre, detalle))
    print("-" * (ancho + 46))
    print("%d comprobaciones · %d bloqueantes fallando" % (len(rows), len(bloqueantes)))
    return 1 if bloqueantes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
