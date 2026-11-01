# 03_SELECCION — foto → banda → tratamiento

Decide una sola cosa: **qué archivo ocupa cada banda, con qué recorte, y en qué estado está**.
No decide la ley visual (`04_DIRECTION`) ni el peso (`06_DEPLOYMENT`).

Se armó con `03_ASSETS.yaml` (medidas reales) y con lectura de contenido de las piezas
principales. Cada asignación dice **cómo se comprobó**, porque un nombre de archivo no prueba
lo que la foto muestra.

## Asignación

| Banda | Archivo | Medida | Ratio | Nivel | Estado |
|---|---|---|---|---|---|
| P1 hero — video | `pp-hero-flujo.mp4` (6 clips de 10 s) + `pp-hero-flujo-poster.jpg` | 1080p | 16:9 | A | **listo** |
| P1 hero — foto de respaldo | `masa desgarrada.jpg` | 4032×2268 | 16:9 | A | **listo** (sin marcas visibles) |
| P1 hero — alternativa | `linea marraqueta.jpg` | 4032×2268 | 16:9 | A | **requiere autorización** |
| P2 paso 1 · diagnóstico | `masa desgarrada.jpg` (recorte 1:1) | 4032×2268 | 1:1 | A | listo |
| P2 paso 2 · medición | `texturometro 2.jpeg` | 3840×2160 | 16:9 | A | listo |
| P2 pasos 3 y 4 · ejecución y control | sin foto | — | — | — | **intencional**: numeral serif + filete |
| P3 casos | sin foto | — | — | — | **faltante**: no hay caso documentado |
| P4 cifras | sin imagen | — | — | — | por ley del sistema (P4 es tipografía) |
| P6 servicios | `ciabatta cruda.jpg` o `pan zanahoria.jpg` | 4032×1908 | 2,11:1 | A | listo (una sola, no mosaico) |
| P8 contacto | **falta el retrato** | — | — | — | **bloqueante** |
| P9 artículo | `granola.jpg` | 4000×2252 | 16:9 | A | listo |
| P9 detalle de dato | `indicadores nir.jpeg` | 1024×768 | 4:3 | A (foto de pantalla) | **requiere anonimizar** |

## Lo que la lectura de contenido encontró

Cuatro piezas se miraron antes de asignarlas. Dos de ellas traen un problema que el nombre del
archivo no delataba:

**`linea marraqueta.jpg`** — línea industrial de marraqueta: los panes avanzan por una cinta
metálica a la salida de un horno, y en el encuadre hay un letrero que dice *«EQUIPAMIENTO
BRIGADA DE EMERGENCIA»*. Es la mejor foto de operación del set y a la vez la más riesgosa:
un letrero de planta puede identificar la instalación. `PRODUCT.md:96-98` prohíbe publicar
procesos identificables de plantas de terceros. Publicable sólo con recorte que elimine el
letrero **y** autorización escrita.

**`indicadores nir.jpeg`** — dos monitores con el control de calidad de «Harina Multiuso»:
humedad 14,8 %, gluten húmedo 25,4 %, cenizas 0,632 %, proteína 9,9 %, almidón dañado 5,0 %,
picas 37, W 232,5, absorción 48,3. Son datos de un lote real y legibles. Sirve como prueba de
método, no como resultado propio: hay que desenfocar los valores antes de publicarla, o no
publicarla.

**`texturometro 2.jpeg`** — analizador de textura Perten TVT 6700 con calibre digital sobre
rebanadas de pan de molde. Marca de equipo visible, no de cliente: se acepta. Es la prueba
visual más concreta de «criterios técnicos explícitos con evidencia asociada».

**`masa desgarrada.jpg`** — masa dentro de maquinaria, estructura metálica, luz superior. Sin
marcas, sin personas, sin letreros: la pieza más segura para la banda de entrada.

## Estado del inventario, medido

```
20 archivos · 11 con EXIF de cámara · 9 sin EXIF (exportaciones 720–1599 px)
11 usables a sangre (≥2400 px) · 9 sólo en detalle o descartadas · 1 ilegible
clips: 6 × 10 s = 60 s
```

Los 11 originales están entre 3840 y 4032 px de ancho: sirven para banda completa a 1440.
Los 9 sin EXIF no son «no reales»: son exportaciones comprimidas de originales, y ninguno
llega a 2400 px salvo `amasadora 2.jpg`, que no abre.

## Lo que falta, con nombre y consecuencia

| Falta | Qué bloquea | Consecuencia si no llega |
|---|---|---|
| **Retrato de Mario** | P8 contacto | la banda de contacto no tiene rostro: el sitio queda sin autor |
| Foto de capacitación o trabajo con personas | P2/P3 | el método se explica sin nadie ejecutándolo; se compensa con numerales |
| Un caso documentado | P3 | «Casos» no puede existir como banda: se retira del menú, no se rellena |
| Datos de lote autorizados | P9 | el detalle de pantalla se anonimiza o se retira |

## Una tensión con la firma, que no resuelvo solo

La firma aprobada incluye **duotono ink**. Aplicado a estas fotos documentales, el duotono
borra justo lo que las hace evidencia: el color del pan, el brillo del acero, la diferencia
entre masa cruda y horneada. Medido: las 11 piezas son fotografía de operación, no abstracción.

Propuesta para enmienda **E-8**: duotono ink se aplica a **abstracciones y diagramas**; la
fotografía documental va en color con balance neutro y un velo ink sólo cuando hay texto
encima. Si se aprueba, `IMAGE_STRATEGY.md` ya la contempla en la banda P1 (velo de
legibilidad) y el resto del sistema no cambia.

## Orden de ejecución con esto hecho

```
1. firma de DIRECTION.md v1.3                (Mario)
2. E-8 duotono selectivo                     (decisión de Mario)
3. autorización de linea marraqueta.jpg      (Mario / cliente)
4. retrato                                    (Mario, con quien lo fotografíe)
5. E-3 en entorno de pruebas                  (bloqueado por 1 y por copia previa)
```

Mientras 3 y 4 no existan, el hero usa `masa desgarrada.jpg` o el video, y `P8` no se
construye. No se rellena con una imagen generada: lo prohíbe la regla de activos.
