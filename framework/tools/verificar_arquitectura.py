#!/usr/bin/env python3
"""verificar_arquitectura.py — la página puede estar bien y el sitio mal construido.

`auditar_estructura.py` mide una página: sus widgets, su profundidad, sus ids. Ninguna de
esas reglas ve lo que sólo existe entre páginas. Con una cabecera copiada en seis páginas,
las seis pasan todas las reglas y el sitio queda con seis copias que hay que editar a mano.

Este gate mide tres cosas, y sólo tres:

  A1. CABECERA / PIE REPETIDOS → FALLA. Toma el primer bloque de raíz de cada página (la
      cabecera) y el último (el pie), calcula su huella estructural e ignora ids y
      `configuration-id` —una cabecera copiada los tiene distintos y sigue siendo la misma
      cabecera—. Si la misma huella abre 3 o más páginas, no es una cabecera: son copias.
      Se arregla con un Site Part de Theme Builder, no editando las páginas.

  A2. PLANTILLAS GLOBALES → NO MEDIDO si no hay MCP. Que existan Header/Footer/Single/
      Archive/404 como plantillas sólo se puede comprobar contra el kit; sin instrumento se
      declara, no se supone.

  A3. BLOQUES REPETIDOS → AVISO (REVISAR), nunca FALLA. Un mismo subárbol en 3 o más
      páginas puede ser un componente que falta… o un CTA legal que debe ser idéntico. No se
      puede saber la intención desde el export, así que no se acusa.

Convención: `clients/<cliente>/05_SYSTEM/_elementor_data/<pagina>.json`, un export por página.

Uso:
    python verificar_arquitectura.py <dir_de_exports>
Salida: 0 OK · 1 FALLA · 2 ERROR DE USO · 3 NO MEDIDO.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comun import Puerta  # noqa: E402

# Con dos páginas no se puede distinguir una cabecera compartida de una coincidencia.
MIN_PAGINAS = 3
# Un bloque tiene que tener cuerpo para contar como candidato a componente.
MIN_ELEMENTOS_BLOQUE = 3


def elementos(ruta):
    """Lista de elementos de raíz, o (None, motivo)."""
    try:
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "no existe"
    except json.JSONDecodeError as e:
        return None, "JSON inválido: %s" % e
    if isinstance(datos, str):
        try:
            datos = json.loads(datos)
        except json.JSONDecodeError:
            return None, "el export es una cadena que no es JSON"
    if isinstance(datos, dict):
        for clave in ("_elementor_data", "data", "elements", "content"):
            if clave in datos:
                datos = datos[clave]
                break
        else:
            return None, "no parece _elementor_data"
    if isinstance(datos, str):
        try:
            datos = json.loads(datos)
        except json.JSONDecodeError:
            return None, "el campo interno es una cadena que no es JSON"
    if not isinstance(datos, list):
        return None, "la estructura no es una lista"
    return datos, None


def texto_de(ajustes):
    for clave in ("title", "text", "editor"):
        valor = ajustes.get(clave)
        if isinstance(valor, str) and valor.strip():
            return re.sub(r"\s+", " ", valor).strip()[:60]
    return ""


def huella(bloque):
    """Identidad estructural: tipo, clases y texto. Sin ids ni configuration-id.

    Un bloque copiado entre páginas tiene ids nuevos y `configuration-id` nuevos; si la
    huella los incluyera, la copia sería indistinguible de un componente distinto.
    """
    partes, pila = [], [bloque]
    while pila:
        el = pila.pop()
        ajustes = el.get("settings") or {}
        clases = ajustes.get("classes") or ajustes.get("_css_classes") or ajustes.get("css_classes") or []
        if isinstance(clases, str):
            clases = [clases]
        partes.append("%s|%s|%s|%s" % (el.get("elType") or "?", el.get("widgetType") or "",
                                        ",".join(map(str, clases)), texto_de(ajustes)))
        pila.extend(reversed(el.get("elements") or []))
    return hashlib.sha1("\n".join(partes).encode("utf-8")).hexdigest()[:12]


def contar(bloque):
    total, pila = 0, [bloque]
    while pila:
        el = pila.pop()
        total += 1
        pila.extend(el.get("elements") or [])
    return total


def subarboles(bloque):
    """Todos los descendientes (sin la raíz de la página) con su huella."""
    salida, pila = [], list(bloque.get("elements") or [])
    while pila:
        el = pila.pop()
        if contar(el) >= MIN_ELEMENTOS_BLOQUE:
            salida.append(el)
        pila.extend(el.get("elements") or [])
    return salida


def main(argv):
    ap = argparse.ArgumentParser(description="arquitectura de sitio sobre _elementor_data")
    ap.add_argument("exports", help="carpeta con un export por página")
    args = ap.parse_args(argv)

    carpeta = Path(args.exports)
    if not carpeta.is_dir():
        print("ERROR DE USO · no es una carpeta: %s" % carpeta)
        return 2

    archivos = sorted(carpeta.glob("*.json"))
    p = Puerta("arquitectura", carpeta.name)
    if not archivos:
        p.sin_medir("no hay exports en %s: sin páginas no hay sitio que medir" % carpeta)
        return p.imprimir()

    paginas = {}
    for archivo in archivos:
        datos, motivo = elementos(archivo)
        if datos is None:
            p.aviso("%s no se pudo leer (%s)" % (archivo.name, motivo))
            continue
        if not datos:
            p.aviso("%s está vacío" % archivo.name)
            continue
        paginas[archivo.stem.lower()] = datos

    p.mide("páginas", "%d de %d archivos" % (len(paginas), len(archivos)))
    if len(paginas) < MIN_PAGINAS:
        p.sin_medir("%d páginas: con menos de %d no se puede distinguir una cabecera "
                    "compartida de una coincidencia" % (len(paginas), MIN_PAGINAS))
        return p.imprimir()

    # A1 · cabecera (primer bloque de raíz) y pie (último)
    for posicion, nombre_humano in ((0, "cabecera"), (-1, "pie")):
        por_huella = {}
        for pagina, datos in paginas.items():
            bloque = datos[posicion]
            por_huella.setdefault(huella(bloque), []).append(pagina)
        for firma, donde in sorted(por_huella.items(), key=lambda x: -len(x[1])):
            if len(donde) >= MIN_PAGINAS:
                p.falla("%s idéntica en %d páginas (%s): debe ser un Site Part de Theme Builder, "
                        "no una copia por página"
                        % (nombre_humano, len(donde), ", ".join(sorted(donde))))
        p.mide("%s distintas" % nombre_humano, len(por_huella))

    # A2 · plantillas globales: sin MCP no se puede saber
    p.sin_medir("plantillas Header/Footer/Single/Archive/404: requiere el kit (ELEMENTOR_MCP_URL)")

    # A3 · bloques repetidos: candidatos a componente, nunca acusación
    repeticiones = {}
    for pagina, datos in paginas.items():
        vistas = set()
        for bloque in datos:
            for sub in subarboles(bloque):
                firma = huella(sub)
                if firma in vistas:
                    continue
                vistas.add(firma)
                repeticiones.setdefault(firma, {}).setdefault(pagina, contar(sub))
    candidatos = {f: v for f, v in repeticiones.items() if len(v) >= MIN_PAGINAS}
    for firma, donde in sorted(candidatos.items(), key=lambda x: -len(x[1]))[:5]:
        p.aviso("bloque de %d elementos repetido en %d páginas (%s): revisar si es un componente"
                % (max(donde.values()), len(donde), ", ".join(sorted(donde))))
    p.mide("bloques repetidos en %d+ páginas" % MIN_PAGINAS, len(candidatos))
    return p.imprimir()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
