"""Genera los activos de identidad que el gate de auditoría exige.

- og:image 1200x630 desde masa-desgarrada-2400.jpg (recorte central, sin texto añadido).
- favicon: monograma "P" en la serif del sistema (Newsreader) sobre ink #223035,
  en 512, 180 y 32 px. No inventa un logotipo: usa la marca tipográfica que el sitio ya
  tiene en el header.
"""
import os
import subprocess
import sys
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "identity")
FUENTE_URL = ("https://github.com/google/fonts/raw/main/ofl/newsreader/"
              "Newsreader%5Bopsz,wght%5D.ttf")
FUENTE = os.path.join(SALIDA, "Newsreader.ttf")
INK = (34, 48, 53, 255)
IVORY = (251, 250, 249, 255)

os.makedirs(SALIDA, exist_ok=True)

# 1 · og:image
origen = os.path.join(BASE, "masa-desgarrada-2400.jpg")
im = Image.open(origen).convert("RGB")
objetivo = 1200 / 630
ancho, alto = im.size
if ancho / alto > objetivo:
    nuevo = (int(alto * objetivo), alto)
else:
    nuevo = (ancho, int(ancho / objetivo))
izq = (ancho - nuevo[0]) // 2
sup = (alto - nuevo[1]) // 2
im = im.crop((izq, sup, izq + nuevo[0], sup + nuevo[1])).resize((1200, 630), Image.LANCZOS)
im.save(os.path.join(SALIDA, "pp-og-1200x630.jpg"), quality=88, optimize=True)
print("og:image 1200x630 ·", os.path.getsize(os.path.join(SALIDA, "pp-og-1200x630.jpg")) // 1024, "KB")

# 2 · favicon con la serif del sistema
if not os.path.exists(FUENTE):
    subprocess.run(["curl", "-sL", "-o", FUENTE, FUENTE_URL], check=True)
fuente = ImageFont.truetype(FUENTE, 400)
try:
    fuente.set_variation_by_axes([72, 400])  # opsz, wght: display, regular
except Exception:
    pass

grande = Image.new("RGBA", (512, 512), INK)
d = ImageDraw.Draw(grande)
caja = d.textbbox((0, 0), "P", font=fuente)
ancho_p = caja[2] - caja[0]
alto_p = caja[3] - caja[1]
d.text(((512 - ancho_p) / 2 - caja[0], (512 - alto_p) / 2 - caja[1] - 10), "P", font=fuente, fill=IVORY)
grande.save(os.path.join(SALIDA, "pp-favicon-512.png"))
for lado in (180, 32):
    grande.resize((lado, lado), Image.LANCZOS).save(os.path.join(SALIDA, "pp-favicon-%d.png" % lado))

for f in sorted(os.listdir(SALIDA)):
    ruta = os.path.join(SALIDA, f)
    print("  %-24s %6d KB" % (f, os.path.getsize(ruta) // 1024))
