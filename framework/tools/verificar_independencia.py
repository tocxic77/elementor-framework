#!/usr/bin/env python3
"""verificar_independencia.py — el framework no puede nombrar a ningún cliente.

Lee los nombres de carpeta en clients/ y busca cada uno dentro de framework/.
Sale 1 si aparece alguno: un artefacto del framework que menciona a un cliente
dejó de ser reutilizable.

Uso (desde 04_WEB/): python framework/tools/verificar_independencia.py
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRAMEWORK = os.path.join(RAIZ, "framework")
CLIENTS = os.path.join(RAIZ, "clients")
EXCLUIR = {".png", ".jpg", ".jpeg", ".mp4", ".zip"}


def main():
    if not os.path.isdir(CLIENTS):
        print("sin clients/ · nada que verificar")
        return 0
    nombres = [d.lower() for d in os.listdir(CLIENTS) if os.path.isdir(os.path.join(CLIENTS, d))]
    if not nombres:
        print("clients/ vacío · 0 clientes, 0 acoplamientos")
        return 0
    hallazgos = []
    for base, _, archivos in os.walk(FRAMEWORK):
        for a in archivos:
            if os.path.splitext(a)[1].lower() in EXCLUIR:
                continue
            p = os.path.join(base, a)
            try:
                texto = open(p, encoding="utf-8", errors="ignore").read().lower()
            except OSError:
                continue
            for n in nombres:
                for i, linea in enumerate(texto.splitlines(), 1):
                    if n in linea:
                        hallazgos.append((os.path.relpath(p, RAIZ), i, n, linea.strip()[:70]))
    print("clientes: %d · archivos del framework revisados" % len(nombres))
    print("-" * 62)
    for ruta, i, n, linea in hallazgos:
        print("  ACOPLA  %s:%d  [%s]  %s" % (ruta, i, n, linea))
    print("-" * 62)
    if hallazgos:
        print("INDEPENDENCIA ROTA · %d referencias" % len(hallazgos))
        return 1
    print("FRAMEWORK INDEPENDIENTE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
