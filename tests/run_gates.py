#!/usr/bin/env python3
"""run_gates.py — casos de prueba de las puertas. Sin pytest, sin red, sin credenciales.

Cada caso levanta un cliente de prueba en un directorio temporal, corre la puerta de verdad
como subproceso y compara el código de salida. Lo que se prueba no es que la puerta diga OK
sobre un buen documento: es que **falle** sobre el defecto que dice detectar.

Uso:    python tests/run_gates.py [-v]
Sale   0 si todos los casos pasan · 1 si alguno falla.
"""
import copy
import http.server
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
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
    seleccionado: false
    autorizacion: propia
  - archivo: generada.jpg
    tipo: imagen
    nivel: generada
    procedencia: declarada
    ancho: 2600
    alto: 1700
    tema: detalle
    prompt_id: hero-operacion
    motivo_falta: "no existe material del tema"
    seleccionado: true
    autorizacion: propia
    publicado_en: [index]
"""

PAGINA_OK = """<!doctype html><html><head><meta name="viewport" content="width=device-width">
<link rel="stylesheet" href="tokens.css">
<title>prueba</title></head><body><h1>Prueba</h1>
<img src="generada.jpg" alt="operación">
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
        # El gate estático exige que los recursos citados existan; servido exige que la
        # imagen declarada en uso aparezca publicada. Un byte basta para ambas cosas.
        self.escribir("05_SYSTEM/generada.jpg", "stub")

    def escribir(self, rel, texto):
        (self.cliente / rel).write_text(texto, encoding="utf-8")

    def yaml(self, rel):
        return self.cliente / rel


resultados = []


def stdout_de(script, args, donde=None):
    """Stdout del instrumento, para los casos que no se deciden por código de salida."""
    import subprocess
    cmd = [sys.executable, str((donde or RAIZ / "framework" / "tools") / script)] + list(args)
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8").stdout


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

        # patrones · el mapa tipo → componente se comprueba sin MCP
        patrones_ok = c.tmp / "sistema_patrones.yaml"
        patrones_ok.write_text(original, encoding="utf-8")
        esperar("sistema · patrones coherentes, sin MCP es NO MEDIDO",
                correr("verificar_sistema.py", ["--sistema", patrones_ok], donde=RAIZ / "adapters" / "elementor")[0], 3)
        patrones_ok.write_text(original.replace("componente: 11383", "componente: 99999"),
                               encoding="utf-8")
        esperar("sistema · patrón que apunta a un componente inexistente falla",
                correr("verificar_sistema.py", ["--sistema", patrones_ok], donde=RAIZ / "adapters" / "elementor")[0], 1)
        patrones_ok.write_text(original.replace("credencial:\n    componente: null",
                                                "credencial:\n    componente: 12345"),
                               encoding="utf-8")
        esperar("sistema · un hueco declarado no es error, uno inventado sí",
                correr("verificar_sistema.py", ["--sistema", patrones_ok], donde=RAIZ / "adapters" / "elementor")[0], 1)

        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace("seleccionado: false", "usado: false"))
        esperar("activos · el campo «usado» ya no vale",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 1)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK.replace(
            "    autorizacion: propia\n    publicado_en: [index]", "    publicado_en: [index]"))
        esperar("activos · seleccionado sin autorización es NO MEDIDO",
                correr("verificar_activos.py", [c.yaml("03_ASSETS.yaml")])[0], 3)
        c.escribir("03_ASSETS.yaml", ACTIVOS_OK)
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

        def anidar(d, niveles):
            """La hoja está en el nivel 3: `niveles` más la dejan en 3+niveles."""
            cola, nodo = hoja(d), None
            for i in range(niveles, 0, -1):
                nuevo = {"id": "n%d" % i, "elType": "e-flexbox",
                         "settings": {"configuration-id": "n%d" % i}, "elements": []}
                if nodo:
                    nuevo["elements"] = [nodo]
                nodo = nuevo
            cola["elements"] = [nodo]

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
        def con_spacer(d):
            d[0]["elements"][0]["elements"].append(
                {"id": "sp", "elType": "widget", "widgetType": "spacer",
                 "settings": {"classes": ["pp-band"], "configuration-id": "sp"}, "elements": []})
            return d
        # mecanismos · el material se mide; lo que no se puede medir no queda en verde
        bib = c.tmp / "MECANISMOS.yaml"
        original_bib = (RAIZ / "framework" / "04_DIRECTION" / "MECANISMOS.yaml").read_text(encoding="utf-8")
        bib.write_text(original_bib, encoding="utf-8")
        esperar("mecanismos · biblioteca medible contra un cliente completo",
                correr("medir_material.py", ["--cliente", c.cliente, "--mecanismos", bib])[0], 0)
        bib.write_text(original_bib.replace("requiere: [problema_declarado]",
                                            "requiere: [problema_que_no_existe]"), encoding="utf-8")
        previo = (c.cliente / "02_EVIDENCE.yaml").read_text(encoding="utf-8")
        c.escribir("02_EVIDENCE.yaml", """
afirmaciones:
  - {id: T1, valor: uno, tipo: testimonio, estado: validada}
  - {id: T2, valor: dos, tipo: testimonio, estado: validada}
  - {id: T3, valor: tres, tipo: testimonio, estado: validada}
""")
        import re as _re
        esperar("materiales · tres testimonios declarados dejan de ser NO MEDIDO",
                int(bool(_re.search(r"testimonios_reales\s+3\b", stdout_de(
                    "medir_material.py", ["--cliente", str(c.cliente)])))), 1)
        c.escribir("02_EVIDENCE.yaml", previo)

        otro = Path(c.tmp) / "clients" / "solo-declarado"
        otro.mkdir(parents=True, exist_ok=True)
        for f in ("01_NEED.yaml", "02_EVIDENCE.yaml", "03_ASSETS.yaml"):
            (otro / f).write_text((c.cliente / f).read_text(encoding="utf-8"), encoding="utf-8")
        (otro / "01_NEED.yaml").write_text(
            (otro / "01_NEED.yaml").read_text(encoding="utf-8")
            + "\ntrayectoria:\n  - hecho: algo vivido\n    verificable: null\n", encoding="utf-8")
        esperar("materiales · declarado sin verificador no cuenta como trayectoria publica",
                int(bool(_re.search(r"trayectoria_publica\s+0\b", stdout_de(
                    "medir_material.py", ["--cliente", str(otro)])))), 1)

        cinco = c.cliente / "05_SYSTEM"
        cinco.mkdir(parents=True, exist_ok=True)
        spec = cinco / "COMPONENTE-prueba.yaml"
        spec.write_text("componente: pp-prueba\nestado: especificado\n"
                        "satisface: [prueba_material]\n"
                        "ranuras:\n  - {nombre: imagen, tipo: imagen, material: evidencia_visual_propia}\n",
                        encoding="utf-8")
        esperar("componente - una ranura con el material exigido sostiene el mecanismo",
                correr("verificar_componente.py", ["--cliente", c.cliente, "--spec", spec])[0], 0)
        spec.write_text("componente: pp-prueba\nestado: especificado\n"
                        "satisface: [prueba_material]\n"
                        "ranuras:\n  - {nombre: pie, tipo: texto_parrafo, material: evidencia_verbal}\n",
                        encoding="utf-8")
        esperar("componente - declarar un mecanismo que ninguna ranura sostiene falla",
                correr("verificar_componente.py", ["--cliente", c.cliente, "--spec", spec])[0], 1)
        spec.write_text("componente: pp-prueba\nestado: especificado\n"
                        "satisface: [escalera_de_compromiso]\n"
                        "ranuras:\n  - {nombre: titulo, tipo: texto_titulo, material: ofertas_distintas}\n",
                        encoding="utf-8")
        esperar("componente - un minimo no alcanzado falla",
                correr("verificar_componente.py", ["--cliente", c.cliente, "--spec", spec])[0], 1)
        cinco = c.cliente / "05_SYSTEM"
        cinco.mkdir(parents=True, exist_ok=True)
        ARQ = ("bandas:\n"
               "  - {n: 1, objetivo: metodo, mecanismos: [metodo_en_secuencia], patron: proceso,"
               " componente: 11383, evidencia: ['problema_declarado']}\n")
        WIRE = ("esquema_componentes: {medido: false}\n"
                "bandas:\n"
                "  - {banda: 1, objetivo: metodo, patron: proceso, componente: 11383, slots: ["
                "{ranura: titulo, slot_componente: titulo, fuente: 'docs/PRODUCT.md', obligatorio: true}]}\n")
        (cinco / "ARQUITECTURA.yaml").write_text(ARQ, encoding="utf-8")
        (cinco / "WIREFRAME.yaml").write_text(WIRE, encoding="utf-8")
        esperar("wireframe · coherente pero con slots del kit sin medir devuelve 3",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 3)
        (cinco / "WIREFRAME.yaml").write_text(WIRE.replace("fuente: 'docs/PRODUCT.md', ", ""),
                                                encoding="utf-8")
        esperar("wireframe · ranura obligatoria sin fuente falla",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 1)
        (cinco / "WIREFRAME.yaml").write_text(WIRE.replace("componente: 11383", "componente: 11377"),
                                                encoding="utf-8")
        esperar("wireframe · componente distinto al de la arquitectura falla",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 1)
        (cinco / "WIREFRAME.yaml").write_text(WIRE.replace("banda: 1", "banda: 2"), encoding="utf-8")
        (cinco / "WIREFRAME.yaml").write_text(WIRE.replace("slot_componente: titulo", "slot_componente: epigrafe"),
                                                encoding="utf-8")
        esperar("wireframe - ranura que el componente no expone falla",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 1)
        (cinco / "WIREFRAME.yaml").write_text(
            WIRE.replace("esquema_componentes: {medido: false}", "esquema_componentes: {medido: true}"),
            encoding="utf-8")
        esperar("wireframe - todas las ranuras mapeadas y esquema medido da 0",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 0)
        (cinco / "WIREFRAME.yaml").write_text(WIRE.replace("banda: 1", "banda: 2"), encoding="utf-8")
        esperar("wireframe · banda que la arquitectura no tiene falla",
                correr("verificar_wireframe.py", ["--cliente", c.cliente])[0], 1)
        (cinco / "WIREFRAME.yaml").write_text(WIRE, encoding="utf-8")

        arq = c.tmp / "arq.yaml"
        arq.write_text(
            "bandas:\n"
            "  - {n: 1, objetivo: metodo, mecanismos: [metodo_en_secuencia], patron: proceso,"
            " componente: 11383, evidencia: ['problema_declarado'], activo: null, cta: null}\n",
            encoding="utf-8")
        esperar("composicion · una banda sostenible pasa",
                correr("verificar_composicion.py", ["--cliente", c.cliente, "--arquitectura", str(arq)])[0], 0)
        arq.write_text(
            "bandas:\n"
            "  - {n: 1, objetivo: metodo, mecanismos: [metodo_en_secuencia, prueba_distribuida],"
            " patron: proceso, componente: 11383, evidencia: ['problema_declarado']}\n"
            "prohibidos:\n  - {mecanismo: prueba_distribuida, motivo: sin testimonios}\n",
            encoding="utf-8")
        esperar("composicion · un mecanismo prohibido por material falla",
                correr("verificar_composicion.py", ["--cliente", c.cliente, "--arquitectura", str(arq)])[0], 1)
        arq.write_text(
            "bandas:\n"
            "  - {n: 1, objetivo: relleno, mecanismos: [], patron: proceso, componente: 11383}\n",
            encoding="utf-8")
        esperar("composicion · una banda sin mecanismo es decorativa y falla",
                correr("verificar_composicion.py", ["--cliente", c.cliente, "--arquitectura", str(arq)])[0], 1)
        arq.write_text(
            "bandas:\n"
            "  - {n: 1, objetivo: hero, mecanismos: [metodo_en_secuencia], patron: apertura,"
            " componente: 11383}\n",
            encoding="utf-8")
        esperar("composicion · componente que no es el del patron falla",
                correr("verificar_composicion.py", ["--cliente", c.cliente, "--arquitectura", str(arq)])[0], 1)

        respaldo = (c.cliente / "02_EVIDENCE.yaml").read_text(encoding="utf-8")
        (c.cliente / "02_EVIDENCE.yaml").write_text(respaldo +
            "\npiezas:\n  - {id: P-A, tipo: medio, titulo: ajeno, publicable: true, "
            "url: 'https://otro-dominio.cl/nota'}\n", encoding="utf-8")
        esperar("migracion · una pieza ajena se mide y no es autoridad propia",
                correr("medir_migracion.py", ["--cliente", c.cliente])[0], 0)
        (c.cliente / "02_EVIDENCE.yaml").write_text(respaldo +
            "\npiezas:\n  - {id: P-X, tipo: medio, titulo: sin prueba, publicable: true}\n",
            encoding="utf-8")
        esperar("migracion · pieza publicable sin url ni archivo falla",
                correr("medir_migracion.py", ["--cliente", c.cliente])[0], 1)
        c.escribir("02_EVIDENCE.yaml", respaldo)

        esperar("materiales · el plan de entrevista se genera desde los huecos",
                correr("plan_material.py", ["--cliente", c.cliente])[0], 0)
        c.escribir("MEC_inventado.yaml", """
mecanismos:
  inventado:
    grupo: prueba
    requiere: [material_que_no_existe]
""")
        esperar("materiales · un material sin protocolo de obtención falla",
                correr("plan_material.py", ["--cliente", c.cliente,
                                            "--mecanismos", str(c.yaml("MEC_inventado.yaml"))])[0], 1)

        ref = c.escribir("REFERENTES.yaml", """
cliente: acme-industrial
referentes:
  - sitio: ejemplo.com
    tipo: referente
    observados: [promesa_de_resultado, contraste_binario]
""")
        esperar("referentes · los mecanismos observados existen en la biblioteca",
                correr("medir_referentes.py", ["--cliente", c.cliente])[0], 0)
        c.escribir("REFERENTES.yaml", """
cliente: acme-industrial
referentes:
  - sitio: ejemplo.com
    tipo: referente
    observados: [promesa_de_resultado, mecanismo_inventado]
""")
        esperar("referentes · un mecanismo inventado en un referente falla",
                correr("medir_referentes.py", ["--cliente", c.cliente])[0], 1)

        esperar("mecanismos · material inexistente en la biblioteca falla",
                correr("medir_material.py", ["--cliente", c.cliente, "--mecanismos", bib])[0], 1)

        esperar("estructura · spacer es FALLA, no aviso", estructura(con_spacer), 1)
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
        esperar("estructura · R5 profundidad 5 falla", estructura(lambda d: anidar(d, 2)), 1)
        esperar("estructura · R5 profundidad 6 falla", estructura(lambda d: anidar(d, 3)), 1)
        esperar("estructura · R6 configuration-id duplicado falla",
                estructura(lambda d: hoja(d)["settings"].update({"configuration-id": "banda-hero"})), 1)
        esperar("estructura · R7 breakpoint 1024 falla",
                estructura(lambda d: hoja(d)["settings"].update(gap_tablet={"unit": "px", "size": 1024})), 1)
        esperar("estructura · export sin configuration-id es NO MEDIDO", estructura(sin_cid), 3)
        esperar("estructura · JSON que no es _elementor_data es NO MEDIDO", estructura(sin_tipo), 3)
        esperar("estructura · lista vacía es NO MEDIDO", estructura(lambda d: d.clear()), 3)

        # SITIO PUBLICADO · lo que recibe el visitante
        sitio = c.tmp / "sitio"
        (sitio / "img").mkdir(parents=True)
        (sitio / "index.html").write_text(
            '<html><head><link rel="stylesheet" href="x.css"></head><body><h1>Portada</h1>'
            '<img src="img/real.jpg">'
            '<img src="img/fondo.jpg" srcset="img/fondo.jpg 800w, img/fondo2.jpg 1600w">'
            '</body></html>', encoding="utf-8")
        (sitio / "x.css").write_text(".hero{background:url('img/fondo.jpg')}", encoding="utf-8")
        (sitio / "otra.html").write_text('<html><body><h1>Otra</h1></body></html>', encoding="utf-8")
        roto = sitio / "roto.html"
        roto.write_text('<html><body><h1>x</h1><img src="img/intrusa.jpg"></body></html>',
                        encoding="utf-8")

        def registro(*filas):
            destino = c.tmp / "assets_servido.yaml"
            cuerpo = ""
            for nombre, sel, aut, destino_paginas in filas:
                cuerpo += "  - archivo: %s\n    seleccionado: %s\n" % (nombre, str(sel).lower())
                if aut:
                    cuerpo += "    autorizacion: %s\n" % aut
                if destino_paginas:
                    cuerpo += "    publicado_en: [%s]\n" % ", ".join(destino_paginas)
            destino.write_text("activos:\n" + cuerpo, encoding="utf-8")
            return destino

        completo = registro(("real.jpg", True, "propia", ["index"]),
                            ("fondo.jpg", True, "propia", ["index"]),
                            ("fondo2.jpg", True, "propia", ["index"]))
        esperar("servido · inventario y HTML coinciden",
                correr("verificar_servido.py", [completo, "--html", sitio / "index.html"])[0], 0)
        esperar("servido · imagen servida fuera del inventario falla",
                correr("verificar_servido.py", [completo, "--html", roto])[0], 1)
        esperar("servido · publicado sin seleccionar falla",
                correr("verificar_servido.py",
                       [registro(("real.jpg", False, "propia", ["index"])),
                        "--html", sitio / "index.html"])[0], 1)
        esperar("servido · se sirve con autorización pendiente y falla",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "pendiente", ["index"]),
                                 ("fondo.jpg", True, "propia", ["index"]),
                                 ("fondo2.jpg", True, "propia", ["index"])),
                        "--html", sitio / "index.html"])[0], 1)
        esperar("servido · declara una página y esa página no lo sirve falla",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "propia", ["index"]),
                                 ("fondo.jpg", True, "propia", ["index"]),
                                 ("fondo2.jpg", True, "propia", ["index", "otra"])),
                        "--html", sitio / "index.html", "--html", sitio / "otra.html"])[0], 1)
        esperar("servido · se sirve en una página que no declara falla",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "propia", ["contacto"]),
                                 ("fondo.jpg", True, "propia", ["index"]),
                                 ("fondo2.jpg", True, "propia", ["index"])),
                        "--html", sitio / "index.html"])[0], 1)
        esperar("servido · destino que no se leyó es NO MEDIDO",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "propia", ["index"]),
                                 ("fondo.jpg", True, "propia", ["index"]),
                                 ("fondo2.jpg", True, "propia", ["index"]),
                                 ("nunca.jpg", True, "propia", ["contacto"])),
                        "--html", sitio / "index.html"])[0], 3)
        esperar("servido · sin autorización declarada es NO MEDIDO",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "", ["index"]),
                                 ("fondo.jpg", True, "", ["index"]),
                                 ("fondo2.jpg", True, "", ["index"])),
                        "--html", sitio / "index.html"])[0], 3)
        esperar("servido · sin HTML es NO MEDIDO",
                correr("verificar_servido.py", [completo])[0], 3)

        # 404 real contra HTTP
        def servir(modo):
            class Manejador(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    if modo == "301":
                        self.send_response(301)
                        self.send_header("Location", "/")
                        self.end_headers()
                        return
                    if self.path == "/" or modo == "200":
                        cuerpo = b"<html><body><h1>Portada</h1><img src='/img/real.jpg'></body></html>"
                        self.send_response(200)
                    else:
                        cuerpo = b"<html><body><h1>No encontrado</h1></body></html>"
                        self.send_response(404)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(cuerpo)

                def log_message(self, *a):
                    pass

            srv = http.server.HTTPServer(("127.0.0.1", 0), Manejador)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            servidores.append(srv)
            return "http://127.0.0.1:%d" % srv.server_address[1]

        servidores = []
        esperar("404 · un 404 real pasa",
                correr("verificar_404.py", ["--sitio", servir("404")])[0], 0)
        esperar("404 · 200 en ruta inexistente falla",
                correr("verificar_404.py", ["--sitio", servir("200")])[0], 1)
        esperar("404 · 301 hacia la portada falla",
                correr("verificar_404.py", ["--sitio", servir("301")])[0], 1)
        esperar("404 · servido lee la página remota y la cruza",
                correr("verificar_servido.py",
                       [registro(("real.jpg", True, "propia", ["index"])),
                        "--sitio", servir("200"), "--pagina", "/"])[0], 0)
        hueco = socket.socket()
        hueco.bind(("127.0.0.1", 0))
        puerto = hueco.getsockname()[1]
        hueco.close()
        esperar("404 · sin respuesta es NO MEDIDO",
                correr("verificar_404.py", ["--sitio", "http://127.0.0.1:%d" % puerto])[0], 3)
        for srv in servidores:
            srv.shutdown()

        # auditar_sitio: sin credenciales no hay auditoría, y eso no es un fallo
        entorno = {k: v for k, v in os.environ.items() if not k.startswith("ELEMENTOR_")}
        r = subprocess.run([sys.executable, str(adaptador / "auditar_sitio.py"),
                            "--sitio", "https://ejemplo.cl"],
                           capture_output=True, text=True, env=entorno, cwd=str(RAIZ))
        esperar("sitio · sin credenciales sale NO MEDIDO", r.returncode, 3)

        # ARQUITECTURA DE SITIO · lo que sólo existe entre páginas
        def paginas(n=3, cabecera="PENNACCHIOTTI", cta=False, distinto=False):
            d = c.tmp / ("exports%d" % (n * 100 + (1 if distinto else 0) + (2 if cta else 0)))
            d.mkdir(exist_ok=True)
            for i in range(n):
                bloque_cabecera = {
                    "id": "h", "elType": "e-flexbox",
                    "settings": {"classes": ["pp-band"], "gap": {"unit": "px", "size": 24},
                                 "configuration-id": "h"},
                    "elements": [{"id": "l", "elType": "widget", "widgetType": "e-heading",
                                  "settings": {"classes": ["pp-display"],
                                               "title": ("%s %d" % (cabecera, i)) if distinto else cabecera,
                                               "configuration-id": "l"}, "elements": []}]}
                cuerpo = {"id": "c", "elType": "e-flexbox",
                          "settings": {"classes": ["pp-band"], "configuration-id": "c"},
                          "elements": [{"id": "t", "elType": "widget", "widgetType": "e-heading",
                                        "settings": {"classes": ["pp-display"],
                                                     "title": "Pagina %d" % i,
                                                     "configuration-id": "t"}, "elements": []}]}
                elementos_pagina = [bloque_cabecera, cuerpo]
                if cta:
                    elementos_pagina.append({
                        "id": "cta", "elType": "e-flexbox",
                        "settings": {"classes": ["pp-band"], "configuration-id": "cta"},
                        "elements": [
                            {"id": "x", "elType": "widget", "widgetType": "e-heading",
                             "settings": {"classes": ["pp-display"], "title": "Hablemos",
                                          "configuration-id": "x"}, "elements": []},
                            {"id": "y", "elType": "widget", "widgetType": "e-paragraph",
                             "settings": {"classes": ["pp-body"], "text": "Escribenos",
                                          "configuration-id": "y"}, "elements": []}]})
                elementos_pagina.append({
                    "id": "f", "elType": "e-flexbox",
                    "settings": {"classes": ["pp-band"], "configuration-id": "f"},
                    "elements": [{"id": "p", "elType": "widget", "widgetType": "e-paragraph",
                                  "settings": {"classes": ["pp-body"],
                                               "text": ("Pie %d" % i) if distinto else "Pie",
                                               "configuration-id": "p"}, "elements": []}]})
                (d / ("pagina-%d.json" % i)).write_text(json.dumps(elementos_pagina),
                                                        encoding="utf-8")
            return d

        esperar("arquitectura · cabecera y pie copiados en 3 páginas fallan",
                correr("verificar_arquitectura.py", [paginas(3)])[0], 1)
        esperar("arquitectura · páginas con cabecera propia no fallan",
                1 if correr("verificar_arquitectura.py", [paginas(3, distinto=True)])[0] == 1 else 0, 0)
        esperar("arquitectura · un bloque repetido es REVISAR, no falla",
                1 if correr("verificar_arquitectura.py",
                            [paginas(3, cta=True, distinto=True)])[0] == 1 else 0, 0)
        esperar("arquitectura · con dos páginas no se puede juzgar",
                correr("verificar_arquitectura.py", [paginas(2)])[0], 3)
        vacia = c.tmp / "exports_vacia"
        vacia.mkdir(exist_ok=True)
        esperar("arquitectura · carpeta sin exports es NO MEDIDO",
                correr("verificar_arquitectura.py", [vacia])[0], 3)

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
