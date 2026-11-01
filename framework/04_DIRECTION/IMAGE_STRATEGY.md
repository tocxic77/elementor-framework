# IMAGE_STRATEGY — qué imagen puede ocupar qué banda

Decide una sola cosa: **con qué se llena cada hueco de imagen, y qué se admite cuando no
hay material**. No decide estilo (eso es `04_DIRECTION.md`) ni recorte (eso es `03_CURATION`).

## Tres niveles, cada uno con su forma de verificarse

| Nivel | Qué es | Cómo se comprueba | Confianza |
|---|---|---|---|
| **A · Real** | foto o video propio de una operación que ocurrió | EXIF de cámara (`Make`/`Model`/`DateTime`) presente **o** declaración firmada de quién la tomó, cuándo y con qué | alta |
| **B · Derivada** | diagrama, esquema, infografía, captura de planilla o documento real | existe el documento fuente; el diagrama lo representa sin inventar cifras | media |
| **C · Generada** | imagen sintética (Gemini, GPT Image, Midjourney, Flux, Ideogram) | declaración de `prompt_id` + `motivo_falta` de material real | baja |

Un nivel que no se puede comprobar no es un nivel: es una etiqueta. Por eso el nivel A no se
acepta por buena fe del archivo, sino por metadatos o por declaración firmada.

## Estado del material: no se escribe aquí

El framework no guarda el inventario de ningún cliente. Cada proyecto mide su material con
`tools/inventario_activos.py` y lo deja en `clients/<cliente>/03_ASSETS.yaml`; la asignación a
bandas vive en `clients/<cliente>/03_SELECCION.md`.

Regla de lectura del inventario: el nivel A se acepta por EXIF de cámara **o** por procedencia
declarada y firmada. Las dos columnas no se mezclan, y `verificar_activos.py` falla si una
procedencia queda sin declarar.

## La regla que sí se puede hacer cumplir

> **Una imagen generada nunca reemplaza un activo real disponible.**

Forma ejecutable: toda imagen `generada` en el inventario debe traer `motivo_falta` (qué
material real no existía, con nombre de banda y tema) y `prompt_id`. Si en el inventario hay
un activo `real` del mismo `tema` sin usar, la puerta falla:

```
FALLA  hero · generada reemplaza real disponible: marraqueta.jpg (4032×1908, sin usar)
```

Una regla que no puede fallar no es una regla.

## Prioridad por banda

| Banda | Primero | Después | IA |
|---|---|---|---|
| P1 hero | video real de operación (6 clips) | foto real a sangre | sólo si no hay ninguna del tema |
| P3 casos | foto real del proceso descrito | captura de documento autorizado | nunca: un caso con imagen sintética es un caso inventado |
| P2 método | diagrama (nivel B) | numerales + filetes | abstracción de flujo, sin texto |
| P4 cifras | nada: números sobre ink | — | prohibida: una cifra con imagen generada sugiere dato falso |
| P8 contacto | foto real del retrato (**falta**) | ninguna | prohibida: un retrato sintético de la persona que firma el sitio |
| P9 artículo | foto real del tema | diagrama | sólo atmósfera, jamás un resultado |

## Qué se puede generar y qué no

**Permitido:** atmósfera (vapor, harina en contraluz, textura de masa), abstracción
(flujo de información, red de procesos, movimiento de datos), fondo neutro para texto.

**Prohibido:** personas, laboratorios, plantas, productos, resultados, certificados,
logos, manos sosteniendo algo. Todo eso es evidencia: si no existe, no se dibuja.

## Sobre los prompts que propuso el revisor

El revisor propone una base de prompts por categoría. La idea es correcta; el texto de los
prompts, no: «Premium corporate photography», «Professional environment», «Sophisticated
corporate atmosphere» son exactamente las palabras con las que un generador devuelve la foto
de banco que se quiere evitar. Un prompt no se escribe con adjetivos de calidad, se escribe
con materia: qué equipo, qué luz, qué distancia, qué se ve y qué no.

La base corregida está en `prompts.yaml`, con `prohibido` y `verifica` por categoría.
