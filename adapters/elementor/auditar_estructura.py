#!/usr/bin/env python3
"""auditar_estructura.py — las siete reglas de ADAPTER.md, sobre el artefacto publicado.

El adaptador documenta siete reglas (ADAPTER.md:20-32) y hasta hoy ninguna se ejecutaba:
`verificar_sistema.py` mira el kit, no la página. Este gate lee `_elementor_data` — la
estructura real que Elementor guarda — y comprueba **exactamente esas siete reglas**:

  R1  estructura externa: e-flexbox · e-div-block · e-component; nunca container/section/column
  R2  texto con e-heading · e-paragraph; nunca text-editor/html/text/editor
  R3  estilo en clase global: ninguna propiedad de estilo declarada en el elemento
  R4  cero hex literales en los ajustes: los colores van por var(--token)
  R5  anidación máxima 4 niveles
  R6  `configuration-id` único por composición
  R7  breakpoints del kit: nunca 1024/767 (son 1025/768)

Autoridad: **sólo** `adapters/elementor/sistema.yaml`, y sólo su lista `clases:` para saber
qué label se puede aplicar. Este gate no mira tokens.css, ni theme.css, ni el kit: si
empezara a comparar las cuatro representaciones a la vez, reproduciría la deriva que el
propio framework prohíbe. La relación tokens.css ↔ sistema.yaml la mide `verificar_tokens.py`.

Filosofía: no es un segundo Elementor. Si ve algo prohibido, falla; si ve algo que no
conoce, avisa. No intenta decidir si el widget es correcto, sólo si está permitido.

Entrada: un JSON con `_elementor_data` tal cual lo guarda el post — la lista de elementos,
o un objeto con la clave `_elementor_data` / `data` / `elements`. Si el JSON no parece
`_elementor_data` (elementos sin `elType`), sale NO MEDIDO: no se inventa una estructura.

Uso:
    python auditar_estructura.py <export.json> [--sistema sistema.yaml] [--json]
Salida: 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "framework" / "tools"))
from _comun import Puerta  # noqa: E402

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
MAX_PROFUNDIDAD = 4

CONSTRUCTORES = {"e-flexbox", "e-div-block", "e-component"}
CONSTRUCTORES_PROHIBIDOS = {"container", "section", "column", "inner-section"}
TEXTO = {"e-heading", "e-paragraph"}
WIDGETS_PROHIBIDOS = {"text-editor", "html", "text", "editor", "wysiwyg"}

# Propiedades que el framework exige declarar en una clase global (regla 3).
# `gap` no está: la regla 5 lo exige en el padre como espaciado estructural.
ESTILO = re.compile(
    r"^(color|background|background-color|border|font|font-family|font-size|font-weight|"
    r"line-height|letter-spacing|margin|padding|text-align|text-transform|"
    r"typography_\w+|_?(margin|padding)_(top|right|bottom|left)|box-shadow|opacity)", re.I)
# Claves que no son estilo aunque empiecen igual.
NO_ESTILO = re.compile(r"(_css_classes|css_classes|classes|class|__globals__|_id|id|"
                       r"configuration-id|configuration_id|_element_id|content|title|text|"
                       r"editor|tag|link|url|alt|caption|image|src)$", re.I)
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
CLASES = re.compile(r"(_css_classes|css_classes|classes|class)$", re.I)


def cargar_estructura(ruta):
    """Devuelve (lista_de_elementos, error)."""
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "no existe el archivo: %s" % ruta
    except json.JSONDecodeError as e:
        return None, "JSON inválido en %s: %s" % (ruta, e)
    if isinstance(datos, str):
        try:
            datos = json.loads(datos)
        except json.JSONDecodeError:
            return None, "el campo del export es una cadena que no es JSON"
    if isinstance(datos, list):
        return datos, None
    if isinstance(datos, dict):
        for clave in ("_elementor_data", "data", "elements", "content"):
            if clave in datos:
                return cargar_valor(datos[clave])
        return None, "el JSON no tiene _elementor_data, data ni elements"
    return None, "el JSON no es ni una lista de elementos ni un objeto"


def cargar_valor(valor):
    if isinstance(valor, str):
        try:
            valor = json.loads(valor)
        except json.JSONDecodeError:
            return None, "el campo es una cadena que no contiene JSON"
    if not isinstance(valor, list):
        return None, "el contenido no es una lista de elementos"
    return valor, None


def cid(el):
    """`configuration-id` puede venir como clave del elemento o dentro de settings."""
    for fuente in (el, el.get("settings") if isinstance(el.get("settings"), dict) else {}):
        for clave in ("configuration-id", "configurationId", "configuration_id"):
            if isinstance(fuente, dict) and fuente.get(clave):
                return str(fuente[clave])
    return None


def recorrer(elementos, profundidad=1, ruta="", acumulado=None):
    """Genera (elemento, profundidad, ruta_legible) en orden de documento."""
    acumulado = [] if acumulado is None else acumulado
    for i, el in enumerate(elementos or []):
        if not isinstance(el, dict):
            continue
        propia = "%s[%d]" % (ruta or "raíz", i)
        acumulado.append((el, profundidad, propia))
        recorrer(el.get("elements") or [], profundidad + 1, propia, acumulado)
    return acumulado


def claves_de_estilo(settings, prefijo=""):
    """Claves de settings que declaran estilo fuera de una clase global."""
    for clave, valor in (settings or {}).items():
        if not isinstance(clave, str):
            continue
        if NO_ESTILO.search(clave):
            continue
        if ESTILO.search(clave):
            yield "%s%s" % (prefijo, clave), valor
        elif isinstance(valor, dict):
            for sub, v in claves_de_estilo(valor, "%s%s." % (prefijo, clave)):
                yield sub, v


def main(argv):
    ap = argparse.ArgumentParser(description="ADAPTER.md reglas 1-7 sobre _elementor_data")
    ap.add_argument("export")
    ap.add_argument("--sistema", default=str(AQUI / "sistema.yaml"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    p = Puerta("estructura", Path(args.export).name)
    elementos, error = cargar_estructura(args.export)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2

    from _comun import cargar_yaml
    sistema, error = cargar_yaml(args.sistema)
    if error:
        print("ERROR DE USO · %s" % error)
        return 2
    registradas = {str(c.get("label")) for c in (sistema.get("clases") or []) if c.get("label")}
    if not registradas:
        print("ERROR DE USO · %s no declara clases: no hay autoridad contra la que validar" % args.sistema)
        return 2

    planos = recorrer(elementos)
    if not planos:
        print("NO MEDIDO · el export no contiene elementos: no hay estructura que auditar")
        return 3
    if not any(isinstance(el.get("elType"), str) for el, _, _ in planos):
        p.aviso("ningún elemento declara `elType`: no parece un export de Elementor")
        p.sin_medir("el JSON no tiene forma de _elementor_data")
        return p.imprimir()

    # R1 · R2 · R4 · R7 por elemento; R3 · R6 en el recorrido completo
    ids, con_cid, sin_cid = {}, 0, 0
    profundidad_max = 0
    for el, prof, ruta in planos:
        tipo = (el.get("elType") or "").strip()
        widget = (el.get("widgetType") or "").strip() or None
        settings = el.get("settings") if isinstance(el.get("settings"), dict) else {}
        profundidad_max = max(profundidad_max, prof)

        # R1 · estructura externa
        if tipo in CONSTRUCTORES_PROHIBIDOS:
            p.falla("R1 %s: estructura %s prohibida (usa e-flexbox o e-div-block)" % (ruta, tipo))
        elif tipo == "container" or widget in CONSTRUCTORES_PROHIBIDOS:
            p.falla("R1 %s: contenedor heredado «%s»" % (ruta, widget or tipo))
        elif tipo not in ("widget", "e-component") and tipo not in CONSTRUCTORES and tipo:
            p.aviso("R1 %s: estructura «%s» no está en la lista conocida" % (ruta, tipo))

        # R2 · texto
        if widget in WIDGETS_PROHIBIDOS:
            p.falla("R2 %s: widget %s prohibido (usa e-heading o e-paragraph)" % (ruta, widget))
        elif widget and not widget.startswith("e-") and tipo == "widget":
            p.aviso("R2 %s: widget «%s» fuera de la capa atómica" % (ruta, widget))

        # R3 · estilo local
        for clave, valor in claves_de_estilo(settings):
            if isinstance(valor, (str, int, float)) and str(valor).strip():
                p.falla("R3 %s: «%s» declara estilo en el elemento; va en una clase global"
                        % (ruta, clave))

        # R4 · hex literal
        for clave, valor in claves_de_estilo(settings):
            texto = str(valor)
            for h in HEX.findall(texto):
                p.falla("R4 %s: hex %s en «%s» (usa var(--token))" % (ruta, h, clave))

        # R5 · anidación (se informa abajo con el máximo medido)
        # R6 · configuration-id
        identificador = cid(el)
        if identificador:
            con_cid += 1
            if identificador in ids:
                p.falla("R6 %s: configuration-id «%s» repetido (ya en %s)"
                        % (ruta, identificador, ids[identificador]))
            else:
                ids[identificador] = ruta
        else:
            sin_cid += 1

        # R7 · breakpoints
        for clave, valor in settings.items():
            if isinstance(clave, str) and re.search(r"_(tablet|mobile|tablet_extra|mobile_extra)$", clave):
                if re.search(r"\b(1024|767)\b", str(valor)):
                    p.falla("R7 %s: breakpoint heredado %s en «%s» (el kit usa 1025/768)"
                            % (ruta, valor, clave))

        # Clases aplicadas: autoridad única = sistema.yaml
        for clave, valor in settings.items():
            if isinstance(clave, str) and CLASES.search(clave):
                tokens = valor if isinstance(valor, list) else str(valor).split()
                for t in tokens:
                    if not isinstance(t, str) or not t.strip():
                        continue
                    if t not in registradas:
                        p.falla("R3 %s: clase «%s» no registrada en sistema.yaml" % (ruta, t))

    if profundidad_max > MAX_PROFUNDIDAD:
        p.falla("R5 anidación de %d niveles (máximo %d)" % (profundidad_max, MAX_PROFUNDIDAD))

    if con_cid == 0:
        p.sin_medir("ningún elemento declara configuration-id: el export no permite juzgar R6")
    elif sin_cid:
        p.falla("R6 %d de %d elementos sin configuration-id" % (sin_cid, len(planos)))

    p.mide("elementos", len(planos))
    p.mide("profundidad máxima", "%d de %d" % (profundidad_max, MAX_PROFUNDIDAD))
    p.mide("configuration-id", "%d únicos, %d sin declarar" % (len(ids), sin_cid))
    p.mide("clases registradas", "%d en sistema.yaml" % len(registradas))
    p.mide("widgets usados", ", ".join(sorted({(el.get("widgetType") or el.get("elType") or "?")
                                               for el, _, _ in planos})))

    if args.json:
        print(json.dumps({"resultado": p.codigo, "fallas": p.fallas,
                          "sin_medir": p.sin_medir_motivos, "avisos": p.avisos,
                          "medidas": p.medidas}, ensure_ascii=False, indent=2))
        return p.codigo
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
