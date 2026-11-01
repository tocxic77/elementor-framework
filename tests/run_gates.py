#!/usr/bin/env python3
"""run_gates.py — casos de prueba de las puertas. Sin pytest, sin red, sin credenciales.

Cada caso levanta un cliente de prueba en un directorio temporal, corre la puerta de verdad
como subproceso y compara el código de salida. Lo que se prueba no es que la puerta diga OK
sobre un buen documento: es que **falle** sobre el defecto que dice detectar.

Uso:    python tests/run_gates.py [-v]
Sale   0 si todos los casos pasan · 1 si alguno falla.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TOOLS = RAIZ / "framework" / "tools"
VERBOSE = "-v" in sys.argv

PREGUNTAS = ["a1", "a2", "a3", "a4", "a5", "a6", "b1", "b2", "b3", "b4",
             "b5", "c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4"]

NEED_OK = "cliente: acme-industrial\nestado: completo\nrespuestas:\n" + "".join(
    '  %s: {respuesta: "x", fuente: "Mario, 2026-11-01"}\n' % q for q in PREGUNTAS)

EVIDENCIA_OK = """cliente: acme-industrial
afirmaciones:
  - id: EV-001
    valor: "350+ profesionales"
    estado: validada
    fuente: "docs/PRODUCT.md:3"
  - id: EV-002
    valor: "margen >55 %"
    estado: rechazada
    motivo: "fuera de la autorización"
"""

ACTIVOS_OK = """cliente: acme-industrial
activos:
  - archivo: real.jpg
    tipo: imagen
    nivel: real
    procedencia: declarada
    ancho: 3000
    alto: 2000
    tema: operacion
    usado: false
  - archivo: generada.jpg
    tipo: imagen
    nivel: generada
    procedencia: declarada
    ancho: 2600
    alto: 1700
    tema: detalle
    prompt_id: hero-operacion
    motivo_falta: "no existe material del tema"
    usado: true
"""

PAGINA_OK = """<!doctype html><html><head><meta name="viewport" content="width=device-width">
<link rel="stylesheet" href="tokens.css">
<title>prueba</title></head><body><h1>Prueba</h1>
<p>Más de 350+ profesionales formados.</p></body></html>
"""

TOKENS_CSS = ":root{ --ink:#223035; --body:16px; }\n"


def correr(script, args, cwd=None, donde=None):
    r = subprocess.run([sys.executable, str((donde or TOOLS) / script)] + [str(a) for a in args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


class Caso:
    def __init__(self, tmp):
        self.tmp = Path(tmp)
        self.cliente = self.tmp / "clients" / "acme-industrial"
        (self.cliente / "docs").mkdir(parents=True, exist_ok=True)
        (self.cliente / "05_SYSTEM").mkdir(parents=True, exist_ok=True)
        (self.cliente / "docs" / "PRODUCT.md").write_text("# producto\n\n350 profesionales\n", encoding="utf-8")
        self.escribir("01_NEED.yaml", NEED_OK)
        self.escribir("02_EVIDENCE.yaml", EVIDENCIA_OK)
        self.escribir("03_ASSETS.yaml", ACTIVOS_OK)
        self.escribir("05_SYSTEM/index.html", PAGINA_OK)
        self.escribir("05_SYSTEM/tokens.css", TOKENS_CSS)

    def escribir(self, rel, texto):
        (self.cliente / rel).write_text(texto, encoding="utf-8")

    def yaml(self, rel):
        return self.cliente / rel


resultados = []


def esperar(nombre, obtenido, esperado):
    ok = obtenido == esperado
    resultados.append((nombre, ok, obtenido, esperado))
    if VERBOSE or not ok:
        print("%s  %-52s obtenido %s · esperado %s"
              % ("ok   " if ok else "FALLA", nombre, obtenido, esperado))


def main():
    tmp = tempfile.mkdtemp(prefix="puertas-")
    try:
        c = Caso(tmp)

        # 01_NEED
        esperar("need · documento completo", correr("verificar_need.py", [c.yaml("01_NEED.yaml")])[0], 0)
        c.escribir("01_NEED.yaml", NEED_OK.replace('a1: {respuesta: "x", fuente: "Mario, 2026-11-01"}',
                                                  "a1: {respuesta: null, fuente: null}"))
        esperar("need · null bloquea", correr("verificar_need.py", [c.yaml("01_NEED.yaml")])[0], 1)
        c.escribir("01_NEED.yaml", "")
        esperar("need · documento vacío es error de uso",
                correr("verificar_need.py", [c.yaml("01_NEED.yaml")])[0], 2)
        c.escribir("01_NEED.yaml", NEED_OK)

        # 02_MATERIAL · evidencia — el caso que fallaba: misma fuente, otro cwd
        esperar("evidencia · fuente existe (cwd = tmp)",
                correr("verificar_evidencia.py", [c.yaml("02_EVIDENCE.yaml")], cwd=tmp)[0], 0)
        esperar("evidencia · fuente existe (cwd = tools)",
                correr("verificar_evidencia.py", [c.yaml("02_EVIDENCE.yaml")], cwd=TOOLS)[0], 0)
        esperar("evidencia · cifra de página respaldada",
                correr("verificar_evidencia.py",
                       [c.yaml("02_EVIDENCE.yaml"), "--html", c.yaml("05_SYSTEM/index.html")], cwd=tmp)[0], 0)
        c.escribir("02_EVIDENCE.yaml", EVIDENCIA_OK.replace("docs/PRODUCT.md:3", "docs/NO-EXISTE.md:3"))
        esperar("evidencia · fuente inexistente falla",
                correr("verificar_evidencia.py", [c.yaml("02_EVIDENCE.yaml")], cwd=tmp)[0], 1)
        c.escribir("02_EVIDENCE.yaml", "cliente: acme-industrial\nafirmaciones: []\n")
        esperar("evidencia · registro vacío falla",
                correr("verificar_evidencia.py", [c.yaml("02_EVIDENCE.yaml")], cwd=tmp)[0], 1)
        c.escribir("02_EVIDENCE.yaml", EVIDENCIA_OK)
        c.escribir("05_SYSTEM/index.html", PAGINA_OK.replace("350+", "900+"))
        esperar("evidencia · cifra sin afirmación falla",
                correr("verificar_evidencia.py",
                       [c.yaml("02_EVIDENCE.yaml"), "--html", c.yaml("05_SYSTEM/index.html")], cwd=tmp)[0], 1)
        c.escribir("05_SYSTEM/index.html", PAGINA_OK)

        # 03_ASSETS
        esperar("activos · registro válido", correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 0)
        c.escribir("03_ASSETS.yaml", "cliente: acme-industrial\nactivos: []\n")
        esperar("activos · registro vacío falla",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace("nivel: generada", "nivel:"))
        esperar("activos · activo sin nivel falla",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace("tema: detalle", "tema: operacion"))
        esperar("activos · generada reemplaza real libre falla",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace("ancho: 2600", "ancho: 0"))
        esperar("activos · en uso sin ancho medido falla",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace("ancho: 2600", "ancho: 1200"))
        esperar("activos · en uso bajo 2400 px falla",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK)

        # independencia
        framework = c.tmp / "framework"
        framework.mkdir(exist_ok=True)
        (framework / "nota.md").write_text("patrón reutilizable, sin nombres propios\n", encoding="utf-8")
        esperar("independencia · framework limpio",
                correr("verificar_independencia.py",
                       ["--clients", c.cliente.parent, "--framework", framework,
                        "--adapters", c.tmp / "sin-adapters"])[0], 0)
        (framework / "nota.md").write_text("ver acme-industrial para el ejemplo\n", encoding="utf-8")
        esperar("independencia · cliente nombrado falla",
                correr("verificar_independencia.py",
                       ["--clients", c.cliente.parent, "--framework", framework,
                        "--adapters", c.tmp / "sin-adapters"])[0], 1)
        esperar("independencia · sin clients es NO MEDIDO",
                correr("verificar_independencia.py",
                       ["--clients", c.tmp / "no-existe", "--framework", framework])[0], 3)

        # tokens
        esperar("tokens · adaptador y tokens.css coinciden", correr("verificar_tokens.py", [])[0], 0)
        sistema = c.tmp / "sistema.yaml"
        original = (RAIZ / "adapters" / "elementor" / "sistema.yaml").read_text(encoding="utf-8")
        sistema.write_text(original.replace('"#223035"', '"#FF0000"'), encoding="utf-8")
        esperar("tokens · color divergente falla",
                correr("verificar_tokens.py", ["--sistema", sistema,
                                               "--css", c.tmp / "sin-css"])[0], 1)
        sistema.write_text(original.replace('"Newsreader"', '"Playfair Display"'), encoding="utf-8")
        esperar("tokens · tipografía divergente falla",
                correr("verificar_tokens.py", ["--sistema", sistema,
                                               "--css", c.tmp / "sin-css"])[0], 1)

        # ADAPTER.md · las siete reglas, sobre _elementor_data
        adaptador = RAIZ / "adapters" / "elementor"
        plantilla = json.loads((RAIZ / "tests" / "fixtures" / "estructura" / "valida.json")
                               .read_text(encoding="utf-8"))

        def hoja(d):
            return d[0]["elements"][0]["elements"][0]

        def estructura(mutar=None):
            datos = copy.deepcopy(plantilla)
            if mutar:
                mutar(datos)
            destino = c.tmp / "export.json"
            destino.write_text(json.dumps(datos), encoding="utf-8")
            return correr("auditar_estructura.py", [destino], donde=adaptador)[0]

        def profundidad5(d):
            cola = hoja(d)
            cola["elements"] = [{"id": "n1", "elType": "e-flexbox", "settings": {"configuration-id": "n1"},
                                 "elements": [{"id": "n2", "elType": "e-flexbox",
                                               "settings": {"configuration-id": "n2"},
                                               "elements": [{"id": "n3", "elType": "e-flexbox",
                                                             "settings": {"configuration-id": "n3"},
                                                             "elements": []}]}]}]

        def sin_tipo(d):
            pila = list(d)
            while pila:
                el = pila.pop()
                el.pop("elType", None)
                pila.extend(el.get("elements") or [])

        def sin_cid(d):
            pila = list(d)
            while pila:
                el = pila.pop()
                (el.get("settings") or {}).pop("configuration-id", None)
                pila.extend(el.get("elements") or [])

        esperar("estructura · página conforme pasa", estructura(), 0)
        esperar("estructura · R1 container prohibido",
                estructura(lambda d: d[0].update(elType="container")), 1)
        esperar("estructura · R2 text-editor prohibido",
                estructura(lambda d: hoja(d).update(widgetType="text-editor")), 1)
        esperar("estructura · R2 html prohibido",
                estructura(lambda d: hoja(d).update(widgetType="html")), 1)
        esperar("estructura · R3 estilo local falla",
                estructura(lambda d: hoja(d)["settings"].update(padding="2rem")), 1)
        esperar("estructura · R3 clase no registrada falla",
                estructura(lambda d: hoja(d)["settings"].update(classes=["pp-display", "pp-inventada"])), 1)
        esperar("estructura · R4 hex local falla",
                estructura(lambda d: hoja(d)["settings"].update(color="#FF0000")), 1)
        esperar("estructura · R5 profundidad 6 falla", estructura(profundidad5), 1)
        esperar("estructura · R6 configuration-id duplicado falla",
                estructura(lambda d: hoja(d)["settings"].update({"configuration-id": "banda-hero"})), 1)
        esperar("estructura · R7 breakpoint 1024 falla",
                estructura(lambda d: hoja(d)["settings"].update(gap_tablet={"unit": "px", "size": 1024})), 1)
        esperar("estructura · export sin configuration-id es NO MEDIDO", estructura(sin_cid), 3)
        esperar("estructura · JSON que no es _elementor_data es NO MEDIDO", estructura(sin_tipo), 3)
        esperar("estructura · lista vacía es NO MEDIDO", estructura(lambda d: d.clear()), 3)

        # release
        codigo, salida = correr("verificar_release.py", [c.cliente])
        esperar("release · cliente válido no falla", 1 if codigo == 1 else 0, 0)
        esperar("release · declara lo que no pudo medir",
                1 if "estructura" in salida and "sin export" in salida else 0, 1)
        export = c.cliente / "05_SYSTEM" / "_elementor_data.json"
        export.write_text(json.dumps(plantilla), encoding="utf-8")
        esperar("release · con export conforme no falla",
                1 if correr("verificar_release.py", [c.cliente])[0] == 1 else 0, 0)
        roto = copy.deepcopy(plantilla)
        hoja(roto).update(widgetType="text-editor")
        export.write_text(json.dumps(roto), encoding="utf-8")
        esperar("release · export con text-editor corta la secuencia",
                correr("verificar_release.py", [c.cliente])[0], 1)
        export.unlink()
        c.escribir("03_ASSETS.yaml", "cliente: acme-industrial\nactivos: []\n")
        esperar("release · cliente roto corta la secuencia",
                correr("verificar_release.py", [c.cliente])[0], 1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    fallas = [r for r in resultados if not r[1]]
    print("-" * 78)
    print("%d casos · %d ok · %d fallas" % (len(resultados), len(resultados) - len(fallas), len(fallas)))
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())
