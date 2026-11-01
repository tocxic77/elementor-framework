"""Sube los activos de identidad y el mu-plugin que los declara, y verifica en vivo.

No imprime credenciales. Verifica con HTTP real: si aparece el 500 se borra el mu-plugin.
"""
import os
import sys
import urllib.request
from ftplib import FTP

ENV = r"C:\Users\mario\AppData\Local\hermes\.env"
CFG = {}
for linea in open(ENV, encoding="utf-8", errors="ignore"):
    if "=" in linea and not linea.strip().startswith("#"):
        k, v = linea.split("=", 1)
        CFG[k.strip()] = v.strip().strip('"').strip("'")

BASE = r"C:\drive\OneDrive - agroTerramica\03_Desarrollo\04_WEB\clients\pennacchiotti\deploy"
ASSETS = os.path.join(BASE, "assets", "identity")
DOCROOT = "/pennacchiotti.cl/wp-content"

ENVIOS = [
    (os.path.join(ASSETS, "pp-favicon-512.png"), DOCROOT + "/themes/hello-elementor-child/assets/pp-favicon-512.png"),
    (os.path.join(ASSETS, "pp-favicon-180.png"), DOCROOT + "/themes/hello-elementor-child/assets/pp-favicon-180.png"),
    (os.path.join(ASSETS, "pp-favicon-32.png"), DOCROOT + "/themes/hello-elementor-child/assets/pp-favicon-32.png"),
    (os.path.join(ASSETS, "pp-og-1200x630.jpg"), DOCROOT + "/themes/hello-elementor-child/assets/pp-og-1200x630.jpg"),
    (os.path.join(BASE, "mu-plugins", "pp-identidad.php"), DOCROOT + "/mu-plugins/pp-identidad.php"),
]


def conectar():
    ftp = FTP()
    ftp.connect(CFG["HOSTGATOR_FTP_HOST"], int(CFG.get("HOSTGATOR_FTP_PORT") or 21), timeout=60)
    ftp.login(CFG["HOSTGATOR_FTP_USER"], CFG["HOSTGATOR_FTP_PASS"])
    return ftp


def verificar(url, marcas):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "verif/1"}), timeout=40) as r:
            html = r.read().decode("utf-8", "ignore")
            estado = r.status
    except Exception as e:  # noqa: BLE001
        return "ERROR %s" % e, False
    faltan = [m for m in marcas if m not in html]
    return "%s · faltan %s" % (estado, faltan or "nada"), not faltan


ftp = conectar()
for local, remoto in ENVIOS:
    with open(local, "rb") as f:
        ftp.storbinary("STOR " + remoto, f)
    print("subido:", remoto.split("/")[-1], os.path.getsize(local) // 1024, "KB")
ftp.quit()

ok = True
for ruta in ("/", "/contacto/", "/sobre-mi/"):
    detalle, bien = verificar("https://pennacchiotti.cl" + ruta, ['rel="icon"', "og:image", "twitter:card"])
    print("  %-14s %s" % (ruta, detalle))
    ok = ok and bien

if not ok:
    print("\nNo verifica: borrando mu-plugin para no dejar el sitio a medias")
    ftp = conectar()
    ftp.delete(DOCROOT + "/mu-plugins/pp-identidad.php")
    ftp.quit()
    sys.exit(1)
print("\nIDENTIDAD EN VIVO")
