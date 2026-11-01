#!/usr/bin/env python3
"""inventario_activos.py — escanea una carpeta de material y emite el inventario medido.

Uso: python inventario_activos.py <carpeta> [salida.yaml]

Mide ancho × alto (cabecera JPEG), peso y si conserva EXIF de cámara. Clasifica el nivel de
evidencia según IMAGE_STRATEGY.md:
  procedencia verificada  → tiene EXIF de cámara
  procedencia declarada   → no lo tiene; la autoría se firma aparte
No inventa `tema` ni `seleccionado`: eso lo llena quien cura.
"""
import glob
import os
import struct
import sys


def dims(path):
    with open(path, "rb") as f:
        if f.read(2) != b"\xff\xd8":
            return (0, 0)
        while True:
            b = f.read(2)
            if len(b) < 2 or b[0] != 0xFF:
                return (0, 0)
            m = b[1]
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                continue
            seg = struct.unpack(">H", f.read(2))[0]
            if m in (0xC0, 0xC1, 0xC2, 0xC3):
                f.read(1)
                h, w = struct.unpack(">HH", f.read(4))
                return (w, h)
            if m == 0xDA:
                return (0, 0)
            f.seek(seg - 2, 1)
    return (0, 0)


def tiene_exif(path):
    with open(path, "rb") as f:
        return b"Exif" in f.read(65536)


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    base = argv[0]
    salida = argv[1] if len(argv) > 1 else None
    vistos, filas = set(), []
    for p in sorted(glob.glob(os.path.join(base, "*"))):
        if p.lower().endswith((".mp4", ".mov")):
            tipo, w, h, ex = "video", 0, 0, False
        elif p.lower().endswith((".jpg", ".jpeg")):
            tipo, (w, h), ex = "imagen", dims(p), tiene_exif(p)
        else:
            continue
        clave = os.path.basename(p).lower()
        if clave in vistos:
            continue
        vistos.add(clave)
        filas.append(dict(archivo=os.path.basename(p), tipo=tipo, w=w, h=h,
                          kb=round(os.path.getsize(p) / 1024), exif=ex))
    lineas = ["# inventario medido · generado por inventario_activos.py", "activos:"]
    for r in filas:
        lineas += [
            "  - archivo: %s" % r["archivo"],
            "    tipo: %s" % r["tipo"],
            "    nivel: real",
            "    procedencia: %s" % ("verificada" if r["exif"] else "declarada"),
            "    exif: %s" % ("true" if r["exif"] else "false"),
            "    ancho: %d" % r["w"],
            "    alto: %d" % r["h"],
            "    kb: %d" % r["kb"],
            "    tema: null",
            "    seleccionado: false",
        ]
    texto = "\n".join(lineas) + "\n"
    if salida:
        open(salida, "w", encoding="utf-8").write(texto)
    verif = sum(1 for r in filas if r["exif"])
    sin_dim = sum(1 for r in filas if r["w"] == 0 and r["tipo"] == "imagen")
    print("activos %d · exif verificable %d · sin dimensiones %d" % (len(filas), verif, sin_dim))
    print("salida:", salida or "(stdout)")
    if not salida:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
