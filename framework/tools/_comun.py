#!/usr/bin/env python3
"""_comun.py — piezas compartidas por las puertas del framework.

Tres reglas que estas piezas hacen cumplir, y que las puertas anteriores no cumplían:

  1. una ruta citada dentro de un documento se resuelve contra el documento,
     nunca contra el directorio desde el que se invoca la puerta (el mismo gate
     no puede dar OK o FALLA según dónde estés parado);
  2. un documento vacío no es un documento que pasa: cero afirmaciones, cero
     activos o cero clientes es un FALLA, no un OK silencioso;
  3. una comprobación que no pudo medir sale NO MEDIDO, nunca OK.

Códigos de salida (los mismos en todas las puertas):

    0  OK          todo lo que la puerta mide se midió y pasó
    1  FALLA       algo medido incumple la regla
    2  ERROR_USO   argumentos o documento ilegible: no se midió nada
    3  NO_MEDIDO   la puerta corrió pero no había nada que medir, o falta el
                   instrumento (credenciales, herramienta del MCP, archivo)

Sin dependencias fuera de la stdlib, salvo PyYAML cuando el documento es YAML.
"""
import re
import sys
from pathlib import Path

OK, FALLA, ERROR_USO, NO_MEDIDO = 0, 1, 2, 3
NOMBRE = {OK: "OK", FALLA: "FALLA", ERROR_USO: "ERROR DE USO", NO_MEDIDO: "NO MEDIDO"}

_FUENTE = re.compile(r"^(?P<ruta>.+?)(?::(?P<linea>\d+)(?:-\d+)?)?$")


def cargar_yaml(ruta):
    """(datos, error). Un YAML vacío, nulo o que no es un mapa es un error de uso."""
    try:
        import yaml
    except ImportError:
        return None, "falta PyYAML: pip install pyyaml"
    p = Path(ruta)
    if not p.exists():
        return None, "no existe el archivo: %s" % ruta
    try:
        datos = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:  # YAML roto: no se adivina
        return None, "YAML ilegible en %s: %s" % (ruta, e)
    if datos is None:
        return None, "documento vacío: %s" % ruta
    if not isinstance(datos, dict):
        return None, "el documento no es un mapa: %s" % ruta
    return datos, None


def resolver_fuente(fuente, base):
    """`archivo:línea` citado en un documento → ruta real, resuelta contra el documento.

    `base` es el directorio del documento que cita, no el cwd. Acepta rutas absolutas
    y devuelve None si la fuente no nombra un archivo (p. ej. «Mario, 2026-10-31»).
    """
    m = _FUENTE.match(str(fuente).strip())
    if not m:
        return None
    ruta = m.group("ruta").strip()
    if not ruta or not Path(ruta).suffix:
        return None
    p = Path(ruta)
    return p if p.is_absolute() else (Path(base) / p)


def archivo_de(ruta):
    """Directorio del documento, que es la base de sus rutas relativas."""
    return Path(ruta).resolve().parent


class Puerta:
    """Acumula medidas, fallas y avisos, y decide el código de salida."""

    def __init__(self, titulo, archivo=None):
        self.titulo = titulo
        self.archivo = archivo
        self.fallas = []
        self.avisos = []
        self.sin_medir_motivos = []
        self.medidas = {}

    def falla(self, mensaje):
        self.fallas.append(mensaje)

    def aviso(self, mensaje):
        self.avisos.append(mensaje)

    def sin_medir(self, mensaje):
        """La regla aplicaba y no se pudo medir: NO MEDIDO, nunca OK."""
        self.sin_medir_motivos.append(mensaje)

    def mide(self, clave, valor):
        self.medidas[clave] = valor

    @property
    def codigo(self):
        if self.fallas:
            return FALLA
        if self.sin_medir_motivos or not self.medidas:
            return NO_MEDIDO
        return OK

    def imprimir(self):
        print("%s%s" % (self.titulo, "" if self.archivo is None else " · " + str(self.archivo)))
        print("-" * 66)
        for clave, valor in self.medidas.items():
            print("  mide     %s: %s" % (clave, valor))
        for m in self.fallas:
            print("  FALLA    %s" % m)
        for m in self.sin_medir_motivos:
            print("  NO MED   %s" % m)
        for m in self.avisos:
            print("  avisa    %s" % m)
        print("-" * 66)
        print("%s · %d fallas · %d sin medir · %d avisos"
              % (NOMBRE[self.codigo], len(self.fallas), len(self.sin_medir_motivos), len(self.avisos)))
        return self.codigo


def salir(funcion):
    """Envuelve un main(argv) -> int y garantiza el código de salida."""
    sys.exit(funcion(sys.argv[1:]))
