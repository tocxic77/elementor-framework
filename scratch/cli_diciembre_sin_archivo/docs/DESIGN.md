# DESIGN.md — PENNACCHIOTTI

**Estado:** borrador para aprobación. Fuente canónica de diseño.
**Versión:** 1.1 (2026-10-26) — añade §Dirección de imagen y registra la capa tipográfica aplicada.
**Última actualización:** 26 de octubre de 2026
**Verificado contra:** kit activo de Elementor V4 (14 variables, 22 clases globales) y `pp.css` servido en producción.

---

## Dirección editorial

Papel, tinta, precisión editorial. El sitio se comporta como un documento técnico bien impreso: tipografía con carácter, jerarquía por tamaño y peso, espacio como material de trabajo, cero efectos decorativos.

**No es:** una landing de startup tecnológica, un catálogo de tarjetas, una página con degradados y halos.

**Anti-referencias:** azul tecnológico, morado/cian, terracota, glassmorphism, sombras difusas, radios grandes, iconos en tile sobre títulos, marquesinas.

## Modo de superficie

Cuatro modos. Toda página declara el suyo antes de diseñarse; el modo fija qué reglas aplican.

| Modo | Páginas | Regla |
|---|---|---|
| `Persuade` | Home, Soluciones, Contacto *(modo a revisar)* | problema → solución → evidencia → CTA. Un solo CTA primario |
| `Read` | Perspectivas y artículos | densidad de lectura, sin CTA intermedio que corte el texto. Modo `Read` no persuade |
| `Legal` | Privacidad, términos, cookies | sin CTA comercial, sin persuasión, sin imágenes. Fecha de vigencia y responsable del tratamiento visibles |
| `Utility` | 404, gracias, estado de error del formulario | una sola acción, sin narrativa. La página de error no se disculpa: ofrece la salida |

No se mezclan: la página de contacto no vende la oferta, la inicia. `/contacto/` queda en `Persuade` por ahora; su comportamiento descrito es el de `Utility` y el cambio de modo es una decisión pendiente, no un supuesto. `Legal` no es hipotético: privacidad y términos están pendientes y el formulario ya recoge datos personales (`docs/FASE0-estado-y-propuesta-v1.md:44`).

Las skills **remiten a esta tabla** y no la redefinen.

## Tokens — color

| Token (variable) | Valor | Rol | Contraste medido |
|---|---|---|---|
| `ivory` | `#FBFAF9` | fondo principal | — |
| `ink` | `#223035` | banda oscura | — |
| `gray` | `#EFEFEF` | fondo alterno | — |
| `sage` | `#D5DEDE` | acento estructural | 9,94:1 sobre tinta |
| `heading` | `#20282D` | titulares | 12,9:1 sobre marfil |
| `text` | `#263037` | cuerpo | 12,9:1 sobre marfil |
| `muted` | `#85979B` | **no usar como texto sobre claro** | 2,92:1 ✗ |
| `#586A70` (clase) | | secundario sobre claro | 5,43:1 ✓ AA |

**Deuda registrada:** la variable `muted` no cumple AA sobre marfil. Hasta que se cambie a `#586A70`, el texto secundario usa la clase `pp-muted`.

## Tokens — tipografía

| Rol | Familia | Tamaño/línea | Peso |
|---|---|---|---|
| display | Newsreader | 56/60 | 400 |
| h2 | Newsreader | 42/50 | 400 |
| h3 | DM Sans | 26/34 | 500 |
| lead | DM Sans | 18/29 | 400 |
| body | DM Sans | 15/25 | 400 |
| etiqueta | DM Sans | 13/20, mayúsculas, tracking 0,08em | 500 |

Medida de lectura: 45–75 caracteres. `text-wrap: balance` en titulares, `pretty` en cuerpo.

**Prohibido el eyebrow sobre un titular.** `pp-eyebrow` solo cuando la etiqueta informa (categoría, metadato), nunca como adorno encima de un h1/h2.

## Tokens — espaciado

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 80 · 112 · 160`

Banda: 112 escritorio / 80 tablet / 64 móvil. Gap de rejilla: 32 escritorio / 24 móvil.

## Layout — contrato de contenedores

Elementor V4 pone `e-flexbox` en `flex-direction: row` por defecto. Por eso **todo contenedor declara su función**, incluso cuando coincide con el valor por defecto:

| Clase | Uso | Definición |
|---|---|---|
| `pp-band` | sección | superficie + padding vertical por breakpoint |
| `pp-wrap` | contenedor | ancho máximo + gutter |
| `pp-stack` | flujo vertical | `flex-direction: column`, `min-width: 0`, `width: 100%` |
| `pp-stack--sm/md/lg` | variantes de stack | **solo cambian el gap** |
| `pp-cluster` | acciones y metadatos | `row`, `wrap`, `align-items: center`, gap corto |
| `pp-grid2` / `pp-grid3` | columnas estructurales | grid con breakpoint a una columna |

**Estado real:** `pp-band`, `pp-wrap`, `pp-grid2`, `pp-grid3`, `pp-cta-row` existen. **`pp-stack`, sus variantes y `pp-cluster` no existen todavía** y deben crearse con `manage-classes` antes de usarse.

Regla semántica: contenido editorial vertical → `pp-stack`; acciones o piezas de ancho intrínseco → `pp-cluster`; columnas de contenido → grid. Nunca un flex row libre para simular grid.

Criterio de apilado: se apila cuando el texto no conserva 420 px o el formulario 480 px, no solo por ancho de viewport.

## Componentes

Header, footer, botón (`pp-cta`, `pp-cta--ghost`), tarjeta de artículo (`pp-card`), bloque de evidencia, CTA final, formulario (`pp-form*`), tarjeta de modalidad, paso del método, imagen de hero (`pp-hero-img`), figura (`pp-figure`).

## Motion

Dos o tres momentos como máximo: entrada del hero, revelado de secciones, respuesta del CTA. Opacidad + desplazamiento 20–28 px, 600–750 ms, ease-out exponencial. Sin rebote, sin bucles, sin marquesinas. `prefers-reduced-motion` respetado.

## Dirección de imagen

Regla base: **la marca es una persona que controla procesos, no una empresa que los anuncia.** La imagen muestra operación real o no se usa. Hoy la portada no tiene ninguna imagen: eso es el defecto, no una decisión estética.

### Qué se fotografía

| Sujeto | Encuadre | Para qué |
|---|---|---|
| Sala de molienda en operación (bancos de cilindros, cinta, tolvas) | horizontal 16:10, gran angular sin deformar | hero |
| Silos, romana, ensacado, carga | horizontal 4:3 | banda de contexto |
| Planilla de control y tablero llenados a mano, con anotaciones reales | detalle 1:1 o 4:3, cenital | evidencia de método |
| Muestra de harina o grano en la mano, y análisis de granulometría | detalle 1:1, fondo del propio mesón | oferta técnica |
| Persona trabajando de espaldas o de perfil, en su puesto | 4:3, figura pequeña en el cuadro | transferencia de conocimiento |

La persona aparece **dentro del trabajo**, nunca mirando a cámara. Manos, espalda, perfil y contexto valen más que un retrato corporativo.

### Tratamiento

- Luz: la del lugar. Si es artificial, lateral y dura; se admite sombra marcada.
- Color neutro y cálido, sin dominante azul. Nada de HDR, viñeta, desenfoque artificial ni filtro de «moderno».
- Contraste alto pero con detalle en las sombras; el negro aplastado se corrige.
- Grano fino aceptable: la foto debe parecer tomada, no renderizada.
- El texto nunca se apoya en un velo que tape la foto. Velo máximo de tinta al 60 % y el sujeto sigue reconocible; si hace falta más, no va foto y va dato.

### Ilustración

Solo diagramas de proceso, y solo cuando el texto no alcanza: flujo de estandarización, matriz de decisión, línea de tiempo del método. Trazo de 1 px en `ink`, relleno en `sage`, fondo transparente o marfil, tipografía DM Sans, sin sombras, sin degradados, sin iconos decorativos. Nunca ilustración de relleno.

### Prohibido

Stock genérico (apretón de manos, sonrisa con portátil, equipo frente a un cristal, globo terráqueo, gráficos flotantes) · imágenes generadas por IA con anatomía o texto defectuoso · collage o mockup de software · marcas de agua · texto incrustado en la imagen · fotos de instalaciones de clientes sin autorización escrita · retratos de terceros · placeholders y «imagen próximamente».

### Reglas de entrega

| Pieza | Formato | Peso máximo | Ancho |
|---|---|---|---|
| Hero | JPEG progresivo, 16:10 | 120 KB | 1600 px |
| Figura | JPEG, 4:3 | 80 KB | 1200 px |
| Detalle / evidencia | JPEG, 1:1 | 60 KB | 800 px |

- Alt descriptivo de la operación, ≤ 120 caracteres: «Banco de cilindros en la sala de molienda durante el turno de noche», no «imagen de molino».
- Alt vacío solo en imágenes decorativas; aquí no hay decorativas.
- Una imagen cada dos bandas como mínimo en modo `Persuade`. Ninguna en `Legal`.
- Si no existe foto verificable, la banda se resuelve con dato medido, cita o tabla de evidencia. **Nunca con relleno.**
- Prioridad de producción: hero del home → figura del método → evidencia de `/soluciones/` → retrato de `/sobre-mi/` a ≥ 800 px de origen (hoy el original es 200 px, ver §Identidad personal).

### Fuente de las imágenes

Fotografía propia en operación, o encargo con lista de tomas cerrada (esta tabla). El Laboratorio de Granos y Harinas de la U. Mayor está cerrado: no hay archivo propio reutilizable, así que la primera tanda se produce, no se busca. Immich queda descartado como fuente (§CAMBIOS 2026-10-26).

## Accesibilidad

- AA en todo texto; verificable con la tabla de contraste.
- Foco visible en interactivos; navegación por teclado completa.
- Etiqueta asociada a cada campo; error junto al campo y con recuperación explícita.
- Browser surfaces tematizadas: `::selection`, caret, scrollbar, `:focus-visible`, offset de subrayado, numerales tabulares.
- Estados diseñados: hover, focus, disabled, loading, error, vacío.
- Targets ≥ 44×44 px. `lang="es-CL"`.

## Responsive

| Ancho | Contacto | Home | Regla |
|---|---|---|---|
| 1440 | 2 columnas 5/7 | hero + bandas | completo |
| 1200 | 2 columnas 5/7 | idem | gutter 48 |
| 1024 | **1 columna** | 2 columnas solo si el texto conserva 420 px | validar |
| 768 | 1 columna | 1 columna | tipo −10 % |
| 390 | 1 columna | 1 columna | H1 ≤ 40 px |
| 320 | 1 columna | 1 columna | sin decorativos |

## Antipatrones

Contenedores sin dirección declarada · eyebrow sobre titular · texto con degradado · halos cromáticos · tarjetas anidadas · icono en tile sobre título · marquesina · sombras duras · CSS por `data-id` · `position:absolute` o márgenes negativos para resolver solapamiento · `overflow:hidden` como arreglo · `display:none` para ocultar lo no resuelto · cifras sin validar · placeholders publicados.

## Deuda viva

**Resuelto 2026-10-26 (medido en producción):** el H1 salía en `#FFFFFF` sobre marfil (1,04:1) porque el kit 2116 traía la tipografía de la plantilla demo; titulares y escala ya siguen esta tabla (§CAMBIOS 2026-10-26). También se definieron los tokens `--font-display` y `--heading` que `pp.css` usaba sin declarar.

1. Variable `muted` fuera de AA — sigue: el texto secundario usa la clase `pp-muted`.
2. `pp-stack`, variantes y `pp-cluster` sin crear.
3. Columnas de `/contacto/` sin clase de stack y contenedores sin dirección.
4. CSS con selectores por `data-id` en `pp.css`.
5. Eyebrows sobre titulares en la portada.
6. Footer «© 2023 eramic» oculto por CSS, no reemplazado.
7. **Párrafo:** hereda `#6C6F73` del kit (`--e-global-color-text`), 5,05:1. Debe ser `#263037`.
8. **`h4`–`h6`:** siguen en Mukta Vaani 600; este documento no define token para ellas, así que no se tocaron.
9. **Imagen:** la portada no tiene ninguna. `uploads/2026/10/hero-1600.jpg` existe (HTTP 200) pero no entra porque la regla `.pp-band--ink:has(.pp-hero-img)` fue escrita para la capa de clases `pp-*` y el árbol V4 no las usa.
10. **Kit 2116:** conserva la paleta de la plantilla demo (`#FB3434`, `#3D19CC`, `#1F242E`, `#6C6F73`, `#FFFFFF`). Neutralizada solo en titulares; las variables globales siguen ahí.
11. **`/soluciones/`:** dos `h1` en el árbol; uno se oculta por CSS en lugar de eliminarse.

## Identidad personal (2026-10-26)

La marca es una persona: Mario Pennacchiotti, consultor. No hay logotipo corporativo ni debe haberlo. La identidad se sostiene en tres piezas.

### 1. Retrato

| | |
|---|---|
| Archivo | `wp-content/uploads/pp/mario-pennacchiotti.png` (attachment 2200) |
| Original | 200 × 200 px, cuadrado, fondo vegetación |
| Uso | círculo de 96 px como máximo, borde `sage` de 1 px y halo marfil de 7 px |
| Dónde | cabecera de `/sobre-mi/` y de `/contacto/`, antes del título |

**Límite medido:** el original es 200 px. A 96 px de visualización queda a 2,08× en pantallas retina, justo en el borde. Por encima de 100 px se ve blando. Un retrato para hero o media columna necesita ≥ 800 px de origen; mientras no exista, el retrato no se agranda.

### 2. Monograma MP

| | |
|---|---|
| Archivos | `mp-mark-ink-512.png` (2201, tinta `#223035`) y `mp-mark-ivory-512.png` (2202) |
| Construcción | iniciales en Newsreader, 44 % del cuadro, centrado óptico |
| Uso | icono del sitio (favicon) en la versión tinta; la marfil queda para fondos oscuros |
| Dónde no | no reemplaza al nombre en la cabecera: `PENNACCHIOTTI` se lee completo |

### 3. Reglas de aplicación

- El retrato nunca se recorta en cuadrado duro (sin `border-radius`) ni se usa como fondo de sección.
- Una sola pieza visual por pantalla: retrato **o** monograma, nunca ambos.
- El nombre se escribe siempre `Mario Pennacchiotti`, sin cargo ni título académico delante.
- Firma: `© 2026 Mario Pennacchiotti · Santiago, Chile`.

### Aplicación actual

| Ruta | Pieza | Cómo |
|---|---|---|
| `/sobre-mi/` (12) | retrato 96 px | `pp.css` → `body.page-id-12 .site-main::before` |
| `/contacto/` (14) | retrato 96 px | `pp.css` → `body.page-id-14 .site-main::before` |
| Todo el sitio | favicon | opción `site_icon` → attachment 2201 |
