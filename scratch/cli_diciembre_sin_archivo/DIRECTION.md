# DIRECTION — pennacchiotti.cl

Versión: v1.3 · Fecha: 2026-10-31 · Emitido a: Mario Pennacchiotti (aprobación) · Hermes (construcción)
Estado: **borrador para aprobación** — no vigente hasta firma. Ningún cambio de render se hace por este documento sin firma.
Historial: v1.0 (13:06) emisión inicial · v1.1 (16:20) E-1 marco de portada, E-2 taxonomía, E-3 restos del demo · v1.2 (16:35) E-4 composición, remedición de §5/§7 sobre la 11269 y tres criterios nuevos de §9 · v1.3 (16:45) E-6 accesibilidad medida y `h1` duplicado, E-7 migración de tema como decisión separada. Ninguna versión se reescribe en silencio: todas quedan en §10.

> **Regla de fuente única.** Este documento no reescribe tokens. Los valores viven en
> `docs/DESIGN.md` (§Tokens, §Dirección de imagen, §Identidad personal) y en
> `docs/PRODUCT.md` (§Oferta, §Evidencia). Aquí se decide y se apunta. Si un valor
> aquí contradice el render medido, gana el render hasta que uno de los dos se corrija,
> y la discrepancia se registra en §10.

---

## 0. Declaración de cumplimiento (la llena quien construye)

Pieza: ______ · DIRECTION.md consultado: sí/no · Excepciones declaradas: ______

---

## 1. Brief

- **Qué se produce:** dirección visual ejecutable para el sitio público de PENNACCHIOTTI (WordPress + Elementor V4 sobre tema Leroux, sitio en producción).
- **Para quién:** propietarios y gerencias de operaciones, calidad y procesos de organizaciones agroalimentarias y de operaciones intensivas en conocimiento técnico (`PRODUCT.md:21-29`).
- **Qué cambia si funciona (negocio):** un gerente entiende en menos de 30 segundos qué se vende y para quién, y agenda una conversación (`PRODUCT.md:80-92`). Si el sitio sigue pareciendo una demo de plantilla, la credencial técnica no se transfiere y el CTA no se usa.
- **Restricción dura:** el sitio está **en vivo**; no hay presupuesto de licencias nuevo; el material fotográfico propio es escaso (3 archivos válidos optimizados, `CAMBIOS 2026-10-28 21:20`); el tema Leroux 1.3.1 está parcheado a mano y no se actualiza solo (`CAMBIOS 2026-10-26 21:35`).
- **Supuestos elegidos (y por qué):**
  1. La dirección se decide **sin una ronda nueva de preguntas**: `fase2-tres-direcciones.md` ya fijó el vector de parámetros y tres direcciones con coste, y `DESIGN.md` ya fijó paleta, tipografía, antipatrones e imagen. Volver a preguntar lo mismo produce un cuarto documento sin render.
  2. El dominio visual dominante es **operación y proceso** (§5), porque es lo único para lo que existe fotografía propia verificable y es lo que `PRODUCT.md:10-12` vende.
  3. El nivel de formalidad es **8/10** (firma técnica, no despacho regulado), medido contra el vector de `fase2` (sobriety 8 · editorial_character 9 · technological_feel 3).

---

## 2. Investigación

| Fuente (URL) | Qué se toma | Qué NO se copia | Licencia / derechos |
|---|---|---|---|
| `leroux.qodeinteractive.com/business-home/` (referencia declarada por Mario, `CAMBIOS 2026-10-26 20:15`) | Marco: cabecera de 96 px, CTA en píldora al final del menú, alternancia de bandas, fotografía a sangre, densidad de 394 palabras | El slider, los contadores animados por JS, los widgets de lista vacíos, el texto en inglés, cualquier enlace al sitio del vendedor | GPL 3 (tema ya instalado y parcheado) |
| `pentagram.com` | Autoridad por tipografía y espacio; la página como documento; cero ornamento | La estética de portafolio de estudio (galería de proyectos, color como firma de autor) | Referencia de patrón; no se reutiliza ningún asset |
| `fraunhofer.de` | Jerarquía informativa de instituto técnico aplicado: método, dato y capacidad visibles; fotografía de laboratorio real | Densidad burocrática, mega-menú, azul institucional, iconografía corporativa | Referencia de patrón; no se reutiliza ningún asset |
| `normcph.com` | Aire, escala y fotografía tratada como material noble | La calma de lifestyle, el beige decorativo, la ausencia de contenido verificable | Referencia de patrón; no se reutiliza ningún asset |
| `design-system.service.gov.uk` | Disciplina de accesibilidad y de componentes; el servicio antes que la marca | La esterilidad institucional y la ausencia total de carácter editorial | Código MIT / contenido OGL; no se copia código |

**Descartado y por qué:**

| Referencia propuesta por terceros | Por qué se rechaza |
|---|---|
| Linear, Stripe, Bolt, Kin + Carta | `DESIGN.md:14-16` prohíbe la estética de landing de startup tecnológica (azul tecnológico, degradados, halos, radios grandes). Adoptarlas obliga a enmendar la ley, no a aplicarla. |
| McKinsey, IDEO, Big Four | Es exactamente la percepción que hay que evitar: consultoría corporativa genérica (§3, «qué no quiero parecer»). |
| Moodboards de Pinterest / bancos de imágenes | No se decide una dirección con material sin licencia ni con imágenes que `DESIGN.md:126` prohíbe (stock genérico, sonrisa con portátil, equipo frente a un cristal). |

**Contradicción registrada:** la lista de referentes que circuló en la revisión externa (Linear, Stripe, Instrument, Field.io) choca con la lista de rechazo vigente del proyecto. Se resuelve a favor de `DESIGN.md` (veto de proyecto) y se ofrece enmienda en §10 si Mario quiere abrir esa puerta.

---

## 3. Parámetros

- **Horas de diseño:** 0 (esta dirección cierra trabajo ya pagado en `fase2` y `DESIGN.md`). Horas de construcción: **10 h** portada · **6 h** por página restante (5 páginas) · **4 h** sistema (clases globales + componentes).
- **Coste de assets:** fuentes **0 USD** (Newsreader y DM Sans, Google Fonts, OFL) · imágenes **0 USD** (autoría propia: `Imagenes/`, `video/`) · ilustración **0 USD** (diagramas en CSS/SVG, no se encargan) · plugins **0 USD** (Elementor, Leroux, Leroux Core ya instalados).
- **Coste real no monetario:** una jornada de toma fotográfica propia (molienda en operación, planilla de control, detalle de material). Es el único insumo que falta y no lo produce una herramienta.
- **Hitos:** emisión v1.0 → corrección de marco de la portada (§11 E-1) → retirada de restos del demo (§11 E-3) → clases globales → páginas internas. *(v1.1: el hito «firma → portada V4 como front page» ya está cumplido; la 11269 sirve `/` desde el 2026-10-28.)*
- **Fecha de congelamiento:** **2026-11-02**. Después de esa fecha, cambiar la dirección exige enmienda v1.1, no una sesión nueva.
- **Aprueba:** Mario Pennacchiotti. **Nadie más puede aprobar una excepción.**
- **Fuera de alcance:** logotipo corporativo (no existe ni debe existir, `DESIGN.md:188`), plantillas de impresión, redes sociales, campañas pagadas, correo, y la producción de fotografía cuando no haya sesión agendada.

---

## 4. Requisitos por departamento

| Departamento | Requisito |
|---|---|
| Negocio | Una sola acción primaria por página: «Agendar una conversación» → `/contacto/` (`PRODUCT.md:87-92`). Tres cifras publicables (350+, 40+, 5). Ninguna otra cifra. |
| Copy / contenido | Español de Chile, registro editorial sobrio y técnico; se nombra el problema antes de la solución; prohibido vocablo de consultoría (`PRODUCT.md:51-57`). La estandarización es medio, no oferta (`PRODUCT.md:14-19`). **Nomenclatura fija de servicios** (E-2): Desarrollo de capacidades · Procesos y estandarización · Información y decisiones · Innovación aplicada. Se usan carácter a carácter en menú, portada, `/soluciones/` y pie. |
| SEO | `docs/SEO-CONTRACT.md` manda: canonical y `robots` explícitos, un `h1` por página, `FAQPage` solo si la FAQ es visible, sin duplicados indexables. |
| Legal / confidencialidad | Sin material de clientes ni procesos identificables de terceros sin autorización escrita (`PRODUCT.md:94-98`). Nada de antiguos empleadores con nombre o cifra. |
| Accesibilidad | WCAG AA medido sobre el fondo real; foco visible; teclado completo; etiqueta por campo; objetivos ≥ 44×44 px; `lang="es-CL"`. Es veto, no polish. |
| Stack / herramienta | WordPress 6.x + Elementor 4.x. La portada **en vivo es 11269**, V4 atómico, servida con plantilla `elementor_canvas` (**corregido en v1.1**: v1.0 afirmaba que la 11269 no estaba publicada y que en vivo corría la 335 en V3; medido el 2026-10-31 16:00, `/` responde `page-id-11269` + `elementor-template-canvas`, 192 `e-flexbox`). Edición por MCP de Elementor; tema `leroux-child` con `pp.css` cache-busteado por `filemtime`. |
| Medios | Imagen: JPEG progresivo — hero 16:10 1600 px ≤ 120 KB · figura 4:3 1200 px ≤ 80 KB · detalle 1:1 800 px ≤ 60 KB. Video: H.264 `+faststart`, sin audio, ≤ 1,8 MB con póster ≤ 70 KB. Breakpoints a medir: 1440 · 1200 · 1024 · 768 · 390 · 320. |

---

## 5. Direcciones consideradas

Las tres provienen de `docs/fase2-tres-direcciones.md`, no se reinventan. Se añade el estado real de ejecución medido el 2026-10-31.

| | A. Editorial contemporánea | **B. Consultora boutique (recomendada)** | C. Técnica-operacional |
|---|---|---|---|
| Composición | una columna, medida 65 caracteres, bandas de 160 px | asimetría 5/7 y 4/8, bandas alternadas, imagen a sangre | rejilla 12 columnas, asimetría 3/9 |
| Tipografía | H1 80-88 px, Newsreader dominante | escala completa 56/42/26, Newsreader + DM Sans | H1 64 px, medida corta |
| Color | marfil con tinta en el texto | alternancia marfil / tinta / salvia | bandas oscuras frecuentes |
| Imagen | 2 fotos, blanco y negro | 6-8 fotos propias, color neutro | 1 foto documental de material |
| Densidad | media | media | alta |
| Coste | 20 h · 2 fotos | 24 h · 6-8 fotos | 26 h · método documentado |
| Riesgo | se lee como blog si el copy falla | **se cae con imágenes sintéticas** | fría para un dueño de empresa |

**Por qué B (con dos préstamos de A):** A no depende del banco fotográfico para sostenerse, pero ya no estamos en ese escenario: existe fotografía propia verificada (línea de marraqueta, texturómetro, masa) y existe video de hero producido con duotono al token `ink`. B es la única que traduce visualmente «operación real» sin inventar imágenes, y su riesgo declarado —caerse con imágenes sintéticas— se neutraliza con la regla de §6: **si no hay foto propia, va dato, no relleno.**

**Ejes estructurales que las separan:** densidad (media/alta) y papel de la imagen (soporte vs. adorno). **No** se separan por color: las tres comparten paleta.

**Estado de ejecución (medido 2026-10-31):**

| | Portada 11269 «Portada 2026» | Portada 335 «en vivo» |
|---|---|---|
| Motor | V4 atómico, 192 `e-flexbox` | **94 nodos V3, 0 V4** |
| H1 | 1 | **5** (4 del RevSlider + el del tema) |
| Palabras | 720 | 669 |
| Imágenes | 1 | 22 (mayor: 574 KB) |
| Texto de apertura | tesis de `PRODUCT.md` | «From strategy to delivery…» (demo, inglés) |
| Enlaces del hero | internos | **5 a `leroux.qodeinteractive.com`** y 3 a una entrada inexistente |

**Corrección v1.1 (medición 2026-10-31 16:00):** la dirección decidida **está construida y publicada**. `/` sirve la 11269. El problema no es de despliegue sino de **marco**: la portada se publicó con plantilla `elementor_canvas`, y por eso no imprime cabecera, pie ni navegación — 0 `<nav>`, 0 `<header>`, 0 `<footer>`; 11 enlaces internos, todos infraestructura de WordPress (`feed`, `wp-json`, `oembed`, `xmlrpc`), ninguno navegable. Un visitante que entra por `/` no puede ir a ninguna otra página. Corrección: E-1 (§11).

**Remedición sobre la 11269 (2026-10-31 16:30, v1.2):** la columna «335» de la tabla anterior es **histórica** —describe la portada que servía antes del 28-10— y no es el estado actual. Sobre la 11269 servida hoy: **1 `h1`** (no 5), **0 enlaces a `leroux.qodeinteractive.com`** (no 5), **1 `<img>`** (no 22), **722 palabras** visibles, `scrollWidth` = `innerWidth` a 390 px (sin desborde). Las mediciones de v1.0 en §7 sobre la 335 se conservan etiquetadas como históricas.

---

## 6. Decisión: ley visual

### Paleta

Fuente: `DESIGN.md:33-46` + medición en producción (`CAMBIOS 2026-10-26 00:30`). Contraste sobre el fondo real, no sobre el hex teórico.

| Token | Hex | Rol | Contraste medido |
|---|---|---|---|
| `ivory` | `#FBFAF9` | fondo claro, texto de banda oscura | 13,06:1 sobre `#223035` |
| `ink` | `#223035` | banda oscura, fondo del sitio | — |
| `gray` | `#EFEFEF` | fondo alterno, texto de pie | 11,05:1 sobre `#223035` |
| `sage` | `#D5DEDE` | acento estructural | 9,94:1 sobre `ink` |
| `heading` | `#20282D` | titulares sobre claro | 14,36:1 sobre `ivory` |
| `text` | `#263037` | cuerpo sobre claro | 12,9:1 sobre `ivory` |
| `muted` | `#586A70` | secundario sobre claro | 5,43:1 ✓ |
| `#A9B3B4` | | secundario sobre oscuro | 5,3:1 ✓ |
| `#85979B` | | **prohibido como texto** | 2,92:1 ✗ |

**Prohibidos:** `#FB3434` y `#3D19CC` (residuo de la plantilla demo en el kit 2116), degradados de cualquier tipo, halos, glassmorphism, sombras difusas, terracota, y cualquier color fuera de esta tabla como texto.

### Tipografía

- **Titulares:** Newsreader 400, tracking normal, `text-wrap: balance`.
- **Cuerpo y UI:** DM Sans 400/500, `text-wrap: pretty`.
- **Escala (escritorio / tablet / móvil):** display 56/1.07 · h2 42/1.19 · h3 26/1.31 · lead 18/29 · body 18/29 en lectura y 15/25 en UI y metadatos · caption 13/20 mayúsculas tracking 0,08 em.
- **Medida de línea:** 60-75 caracteres en cuerpo (720 px a 18 px), máximo 22 en titular.
- **Jerarquía:** un solo `h1` visible y en el DOM; no se salta nivel; no se reduce cuerpo para que quepa.
- **Discrepancia registrada:** `DESIGN.md:56` declara body 15/25; el render de páginas mide 18-19 px. Se resuelve así: 15/25 es el token `size-body` para UI, 18/29 es el cuerpo editorial. `DESIGN.md` debe corregirse a v1.2 (§10).

### Retícula y contenedores

- **Columnas:** 12 · **gutter:** 32 escritorio / 24 móvil · **contenedor:** 1300 px (medido en el marco Leroux), lectura 720-780 px.
- **Breakpoints y qué cambia:** 1440 completo · 1200 gutter 48 · 1024 una columna si el texto baja de 420 px · 768 tipo −10 % · 390 H1 ≤ 40 px · 320 sin elementos decorativos.
- **Todo contenedor declara su función** (`pp-band`, `pp-wrap`, `pp-stack`, `pp-cluster`, `pp-grid2/3`). Un `e-flexbox` sin dirección declarada es defecto.
- **`pp-grid3` con tope (v1.2, E-4):** existe en el kit pero **máximo una vez por página** y nunca dos bandas consecutivas con la misma rejilla. Una rejilla de tres iguales es la excepción, no el componente por defecto: si la sección no necesita tres columnas, no se usa.
- **Estado real:** 0 clases globales registradas en el kit. `pp-stack`, sus variantes y `pp-cluster` **no existen todavía** y deben crearse antes de componer una página nueva. Mientras no existan, ninguna página nueva se construye: se compondría con CSS por `data-id`, que está prohibido.

### Espaciado

Escala `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 80 · 112 · 160`. Banda: 112 / 80 / 64 px. Ningún valor fuera de la escala sin enmienda.

### Imagen

- **Tratamiento:** luz del lugar; color neutro y cálido sin dominante azul; contraste alto con detalle en sombras; grano fino aceptable; sin viñeta, sin HDR, sin desenfoque artificial. El texto nunca se apoya en un velo que tape al sujeto: velo de tinta máximo 60 %.
- **Proporciones:** hero 16:10 · figura 4:3 · detalle 1:1. Bandas a sangre solo en 16:10 y 3,78:1 (la 3,78:1 se oculta bajo 767 px: mide 103 px en móvil).
- **Video:** admitido en hero, autoplay silenciado, en bucle, `poster` obligatorio, ≤ 1,8 MB en 1080p y versión 9:16 para móvil. Usar `video/pp-hero-linea-1080p.mp4` (1,7 MB) o `video/pp-mascara-tinta-1080p.mp4` (218 KB). El metraje con marca de agua horneada está prohibido (`video/FUENTES.md`).
- **Política de placeholders:** si no hay foto propia verificable, **no va imagen**: va dato medido, cita o tabla de evidencia. Nunca «imagen próximamente», nunca stock genérico.
- **No se aceptan:** stock de banco (apretón de manos, sonrisa con portátil, equipo frente a un cristal), imágenes generadas por IA con anatomía o texto defectuoso, collage o mockup de software, marcas de agua, texto incrustado, instalaciones de clientes sin autorización escrita, retratos de terceros.
- **Corrección de contexto:** la operación agroalimentaria **sí** puede aparecer (la fotografía de línea de marraqueta y texturómetro es de autoría propia y está autorizada, `CAMBIOS 2026-10-26 19:59`). Lo que no puede aparecer es una planta, marca o cliente identificable de un tercero. La identidad no depende del trigo; depende del **control de proceso**, que sobrevive si mañana la operación es minería o manufactura.

### Materiales / textura / profundidad

Papel mate. Sin texturas, sin ruido, sin imágenes de fondo en las bandas de texto. La profundidad se produce por alternancia de superficie (marfil / tinta / salvia / gris), nunca por sombra.

### Movimiento

- Entrada de hero 750 ms, opacidad 0→1 + 24 px, ease-out exponencial; revelado de sección 600 ms; respuesta de CTA 150 ms.
- **Máximo dos momentos por página.** No se anima texto por letra, no hay parallax, no hay contadores animados por JS (el contador de Leroux dejaba el número vacío: se imprime por CSS, `CAMBIOS 2026-10-27 05:40`), no hay marquesinas.
- `prefers-reduced-motion: reduce` desactiva todo salvo el cambio de color de foco.

### Densidad y jerarquía

La jerarquía se logra por **escala, peso y espacio**, en ese orden. Referencia medida: la home de Leroux tiene 394 palabras de contenido; la portada 11269 tiene **720**. El objetivo editorial es ≤ 500 en `persuade`. Prohibido sustituir jerarquía con iconos, líneas de color o etiquetas mayúsculas decorativas.

### Modo de superficie

| Modo | Páginas | Consecuencia de layout |
|---|---|---|
| `persuade` | `/`, `/soluciones/`, `/capacitacion/`, `/contacto/` | problema → método → evidencia → CTA. Un CTA primario. Imagen cada dos bandas como mínimo. |
| `read` | `/perspectivas/` | una columna 720 px, 18/29, sin CTA intermedio, sin imágenes salvo figura propia. |
| `legal` | `/privacidad/` | sin CTA comercial, sin imágenes, 17/29 centrado, fecha de vigencia visible. |
| `utility` | 404, gracias, error de formulario | una acción, sin narrativa. |

---

## 7. Lista de rechazo

1. **No** sliders con texto de plantilla ni con enlaces fuera del dominio propio (*v1.0, histórico sobre la 335:* 5 enlaces a `leroux.qodeinteractive.com` y 3 a una entrada inexistente. *Remedido en la 11269, 2026-10-31:* **0**).
2. **No** más de un `h1` por página, ni oculto por CSS (*v1.0, histórico:* 5 en la portada 335. *Remedido 2026-10-31:* 1 en la 11269 y 1 en `/soluciones/`. El defecto vigente de la portada no es el `h1`: es que no tiene navegación).
3. **No** imágenes del tema demo (`main-home-img-*`, `blog-list-img-*`), ni banners de stock, ni video con marca de agua.
4. **No** CSS por `data-id` ni `!important` fuera de un caso documentado con su reversión.
5. **No** `display:none` para ocultar lo que no se resolvió (pie del tema, bloques demo, segundo `h1`).
6. **No** eyebrow sobre titular; no etiqueta mayúscula como adorno.
7. **No** degradados, halos, glassmorphism, radios mayores de 4 px, sombras difusas, iconos en tile sobre títulos, marquesinas.
8. **No** contadores animados por JS ni cifras que no estén en `PRODUCT.md:69-78` (hoy: 350+, 40+, 5).
9. **No** clases inventadas en la página: si el componente no existe en el kit, se crea con `manage-classes` antes de usarlo.
10. **No** páginas construidas en V3: no aceptan tokens y obligan a CSS compensatorio.
11. **No** duplicar tokens: si un valor no está en `DESIGN.md`, se enmienda `DESIGN.md`.
12. **No** publicar con la caché de Elementor sucia: `_elementor_element_cache` + PURGE, verificado con `curl`.
13. **No** publicar una página pública sin cabecera, pie y navegación del tema. Plantilla `elementor_canvas` prohibida en páginas públicas (§11 E-1).
14. **No** cargar plugins ni familias tipográficas sin uso en la página: ni RevSlider 7.1.8 donde no hay slider (`sr7.js` carga en `/` y `/soluciones/`, que no lo tienen), ni Mukta Vaani, Roboto, Roboto Slab o Heebo del demo (§11 E-3).
15. **No** llamar «cuatro» a tres ejes distintos: servicios, método y modalidades tienen nombre propio y una sola presentación cada uno (§11 E-2).
16. **No** heredar copy del demo en el pie: «Consultoría en molinería y panificación» no figura en `PRODUCT.md` y contradice el posicionamiento; se corrige con copy aprobado, no con retoque de estilo.
17. **No** dejar el aviso de cookies con todas las categorías en «Ninguno» ni en tres botones sin jerarquía: es un control de cumplimiento, no un banner decorativo.
18. **No** dos bandas consecutivas con la misma rejilla, ni más de una rejilla de tres iguales por página (*v1.2, E-4*). La monotonía compositiva pasa todos los criterios mecánicos de §9; por eso necesita su propio rechazo.
19. **No** resolver la cabecera o el pie con `display:none` ni con CSS compensatorio: si el mecanismo elegido obliga a ocultar algo, el mecanismo está mal elegido (coherente con el rechazo 5).

---

## 8. Artefactos de construcción

| Artefacto | Formato | Ruta | Quién |
|---|---|---|---|
| Spec de retícula y contenedores | tabla en `DESIGN.md` §Layout | `docs/DESIGN.md` | ya existe |
| Spec tipográfica | tabla en `DESIGN.md` §Tokens | `docs/DESIGN.md` | ya existe |
| Spec de imagen | tabla en `DESIGN.md` §Dirección de imagen | `docs/DESIGN.md` | ya existe |
| Directiva de arte (este documento) | `DIRECTION.md` v1.1 | raíz del proyecto | emitido 2026-10-31 (v1.0 13:06 · v1.1 16:20) |
| Tokens en el kit | 14 variables globales | Elementor kit 2116 | ya cargadas |
| Clases globales | `pp-stack`, `pp-stack--sm/md/lg`, `pp-cluster`, `pp-band`, `pp-wrap`, `pp-grid2/3`, `pp-cta` | kit 2116 vía `manage-classes` | **pendiente** (0 registradas) |
| Contrato de portada | `node_tree` + cardinalidad + prohibidos | `docs/contratos/portada-v1.contract.yaml.md` | **pendiente** |
| Assets de imagen y video | JPEG / MP4 H.264 | `Imagenes/`, `video/` → `uploads/` | parcial (3 fotos, 4 videos) |

---

## 9. Criterios de aceptación

Cada criterio con su método. Un criterio no medido se reporta `N/A`, nunca se estima.

| Criterio | Método |
|---|---|
| Un solo `h1` visible **y** en el DOM | `document.querySelectorAll('h1').length` sobre el HTML servido |
| 0 enlaces fuera del dominio propio en contenido | `grep -o 'href="[^"]*"'` sobre el HTML servido |
| Contraste AA | contraste calculado contra el fondo computado (`getComputedStyle` del ancestro con color de fondo), no contra el hex teórico |
| 0 px de desborde horizontal | `documentElement.scrollWidth - innerWidth` en 1440 / 1200 / 1024 / 768 / 390 / 320 |
| 0 solapamientos entre hermanos | intersección de `getBoundingClientRect()` por par de hermanos |
| Medida de lectura | ancho del contenedor de párrafo ÷ ancho medio de carácter, dentro de 45-75 |
| Peso de imagen | `content-length` ≤ 120 / 80 / 60 KB según pieza |
| Peso de video | ≤ 1,8 MB + póster ≤ 70 KB, `poster` presente |
| Densidad | conteo de palabras del texto visible ≤ 500 en `persuade` |
| Tokens aplicados | 0 valores hex literales en los nodos V4 construidos; todo por variable |
| Render tras publicar | `PURGE` → 204 y HTML nuevo verificado con `curl` (la caché de Elementor no se invalida con PURGE solo) |
| Accesibilidad de teclado | recorrido completo con foco visible en cabecera, CTA y formulario |
| Navegación presente | `document.querySelectorAll('nav').length` ≥ 1 y ≥ 1 enlace de contenido a `/soluciones/` y a `/contacto/` en **toda** página publicada |
| Aviso de cookies no tapa contenido | área de intersección de `getBoundingClientRect()` entre elementos `position:fixed` y el `h1` / CTA primario = **0 px²**, medido a 390 px. *Hoy: 14.116 px² — el aviso cubre el CTA completo* |
| Rejilla no repetida | 0 pares de bandas consecutivas con la misma rejilla y la misma cardinalidad; ≤ 1 `pp-grid3` por página (rechazo 18) |
| Composición declarada | cada banda declara su rejilla y su función; ninguna banda se compone por defecto con tres columnas |
| Juicio visual | captura a 1440 y 390 revisada contra la rúbrica de antipatrones de `claude-design` (§11 E-5). Un criterio mecánico no sustituye este paso: un sitio plano los pasa todos |

---

## 10. Registro de emisión

| Versión | Fecha | Cambio | Emitido a |
|---|---|---|---|
| v1.0 | 2026-10-31 | emisión inicial. Cierra la ausencia de gate detectada: el proyecto tenía tokens (`DESIGN.md`), vector y tres direcciones (`fase2`), y ninguna ley que las hiciera ejecutables. | Mario Pennacchiotti |
| v1.1 | 2026-10-31 | enmienda de ejecución tras medición en vivo y revisión externa: E-1 marco de la portada (sin nav/pie) · E-2 una taxonomía y tres ejes · E-3 retirada de restos del demo. Corrige además la premisa falsa de §5 («portada no publicada»): `/` sirve la 11269. No toca tokens, paleta ni tipografía. | Mario Pennacchiotti |
| v1.2 | 2026-10-31 | E-4 regla de composición (la ley sólo medía cumplimiento; el molde de tres tarjetas lo pasaba entero) · E-5 juicio visual en el circuito · remedición de §5 y §7 sobre la 11269 (1 `h1`, 0 enlaces externos, 1 imagen, 722 palabras) · taxonomía fijada en §4 · tres criterios nuevos en §9 (navegación, solape de cookies con el CTA, rejilla repetida) · `pp-grid3` con tope. | Mario Pennacchiotti |
| v1.3 | 2026-10-31 | E-6 contraste **computado** en banda (el criterio existía y no cazó texto a 1,4:1), retiro de eyebrows sobre titular, numerales del método restituidos, y `h1` duplicado medido en 3 de 5 páginas · E-7 migración de tema (Hello child) declarada como decisión separada, no ejecutada. | Mario Pennacchiotti |

**Pendiente de firma de Mario (tres decisiones, no veinte):**

1. **Dirección:** B con préstamos de A (recomendada) frente a A pura. Cambia una cosa: si la fotografía es soporte o es adorno.
2. **Dominio dominante:** operación y proceso (recomendado) frente a laboratorio y medición. Cambia el peso del video frente a la fotografía de detalle.
3. **Vigencia del congelamiento:** 2026-11-02.

**Discrepancias abiertas con `DESIGN.md` (a corregir en v1.2):** body 15/25 vs 18/29 medido · `muted` `#85979B` fuera de AA · deuda #2 (`pp-stack`, `pp-cluster` sin crear) · deuda #4 (CSS por `data-id`).
**Discrepancias nuevas registradas en v1.1:** 4 familias tipográficas cargadas en producción (Newsreader, DM Sans, **Mukta Vaani**, **Roboto**) contra las 2 declaradas en §6 · RevSlider 7.1.8 en páginas sin slider · pie de `/soluciones/` con copy ausente de `PRODUCT.md`.

---

## 11. Enmienda — correcciones de ejecución (v1.1 → v1.2)

Se abre porque la medición del 2026-10-31 16:00 contradijo el estado declarado en v1.0, no porque la dirección sea otra. **No se toca ningún token, paleta, tipografía ni retícula de §6.** Toca marco, taxonomía y restos del demo. Cada corrección declara qué falló, qué cambia, qué se acepta perder y cómo se verifica.

### E-1 · La portada vuelve al marco del tema

**Qué falló (medido en `/`, HTML servido):** plantilla `elementor-template-canvas`; 0 `<nav>`, 0 `<header>`, 0 `<footer>`; 11 enlaces internos y ninguno navegable (todos `feed`, `wp-json`, `oembed`, `xmlrpc`). En `/soluciones/`, 3 `<nav>`, 2 `<header>`, 1 `<footer>`. La portada es la página que más tráfico recibe y es la única sin salida.

**Qué cambia:** la portada usa la misma plantilla que `/soluciones/` (`page-template-default`), con cabecera del tema (header template 2129) y pie. El árbol V4 de la 11269 se conserva; se ajusta al contenedor de 1300 px del marco, no el marco al contenido. Aplica a toda página pública: `/`, `/soluciones/`, `/capacidades/`, `/perspectivas/`, `/contacto/`.

**Qué se acepta perder:** el control absoluto del arranque a sangre y del ancho en la primera banda; la cabecera ocupa 96 px y el `qodef-content-grid-1300` limita. Se acepta porque la banda de hero ya vive dentro de 1300.

**Se verifica:** `grep -c '<nav'` ≥ 1 en cada página publicada · la portada contiene ≥ 1 enlace de contenido a `/soluciones/` y ≥ 1 a `/contacto/` · `grep -c 'elementor-template-canvas'` = 0 en páginas públicas · un solo viewport (`width=device-width, initial-scale=1`) en todas.

### E-2 · Una taxonomía, tres ejes con nombre propio

**Qué falló (medido):** tres listas de cuatro cosas distintas compitiendo sin nombrarse: 4 líneas de trabajo en portada (Desarrollo de capacidades · Procesos y estandarización · Información y decisiones · Innovación aplicada), 4 pasos de método (Diagnóstico · Estructuración · Implementación · Transferencia) y 4 modalidades en `/soluciones/` (Diagnóstico · Diseño y estandarización · Implementación y adopción · Formación). Las tres se presentan igual —tarjetas del mismo peso— y por eso se leen como la misma oferta repetida tres veces.

**Qué cambia:**

| Eje | Qué es | Nombres fijos | Dónde aparece | Forma |
|---|---|---|---|---|
| **Servicios** | lo que se vende | los 4 de la portada, carácter a carácter | menú, portada, `/soluciones/`, pie | 4 bloques con nombre, peso desigual; nunca numerados |
| **Método** | cómo se trabaja | Diagnóstico · Estructuración · Implementación · Transferencia | una sola vez, en portada | secuencia horizontal con numeral grande; no tarjetas |
| **Modalidades** | cómo se contrata | Diagnóstico · Diseño y estandarización · Implementación y adopción · Formación | solo `/soluciones/` | tabla de 4 filas con qué incluye / qué recibes / qué aportas |

Ninguna sección usa la palabra «cuatro» como argumento, ni repite el molde de tres tarjetas. Los tres ejes llevan encabezado que los nombra («Servicios», «Cómo trabajo», «Cómo contratar»).

**Qué se acepta perder:** la simetría entre secciones; dos páginas dejan de verse «completas» con cuatro bloques iguales.

**Se verifica:** el menú y el pie listan exactamente los 4 nombres de servicios, idénticos al H3 correspondiente de `/soluciones/` · el método aparece una sola vez y con numeral, no como tarjeta · las modalidades solo existen en `/soluciones/` y como tabla · 0 secciones consecutivas con la misma cardinalidad y el mismo componente.

### E-3 · Retirada de restos del demo

**Qué falló (medido):** RevSlider 7.1.8 enqueued en `/` y `/soluciones/` (`sr7.css`, `libs/tptools.js`, `sr7.js`) sin un solo slider en la página · **6 familias tipográficas** pedidas contra 2 declaradas: DM Sans (dos peticiones distintas), Newsreader y del demo **Mukta Vaani, Roboto, Roboto Slab, Heebo** · `twitter:title` «Portada 2026 - Mario Pennacchiotti» vs `og:title` «Control y estandarización de procesos · PENNACCHIOTTI» · aviso de cookies con todas las categorías en «Ninguno» y tres botones sin jerarquía · pie de `/soluciones/`: «Consultoría en molinería y panificación» (copy del demo, ausente de `PRODUCT.md`).

**Qué cambia:** RevSlider se desactiva salvo en una página que realmente lo use (hoy: ninguna); solo Newsreader y DM Sans se encolan; un viewport único; metas idénticas al `<title>` de la página (manda `SEO-CONTRACT.md`); aviso de cookies reducido a aceptar / rechazar / configurar con categorías en estado real; el pie toma copy de `PRODUCT.md`, no del demo.

**Qué se acepta perder:** el slider como recurso narrativo (no se usaba) y las familias tipográficas del demo en cualquier pieza.

**Se verifica:** `grep -c revslider` = 0 en `/` y `/soluciones/` · `family=` en el HTML = 2 (DM Sans y Newsreader; hoy 6) · viewport único en todas las páginas · `twitter:title` = `og:title` = `<title>` · 0 cadenas «molinería» en el HTML servido («eramic» ya no aparece desde el 24-10).

### E-4 · Regla de composición (lo que la ley no decía)

**Qué falló (diagnóstico externo, aceptado):** §9 medía sólo lo que un sitio plano puede cumplir —contraste, desborde, medida de lectura, cardinalidad de `h1`—. Cinco bandas de tres tarjetas idénticas pasan **todos** esos criterios. El molde no era un error de ejecución: era un hueco de la ley, agravado porque §6 listaba `pp-grid3` entre las clases del sistema y con eso lo volvía el componente por defecto.

**Qué cambia:**

| Sección | Forma obligatoria | Prohibido |
|---|---|---|
| Servicios (4 líneas) | bloques con peso desigual, nombre como titular | rejilla de 4 iguales |
| Método (4 pasos) | secuencia horizontal, numeral grande, línea de continuidad | tarjetas, contadores, iconos en tile |
| Casos (3) | lista editorial: situación → método → resultado, texto corrido con numeral | tarjetas del mismo peso |
| Cifras (3) | una sola línea de texto, cifra en el flujo de la frase | tres bloques monumentales |

Máximo **una** rejilla de tres por página; **0** pares de bandas consecutivas con la misma rejilla y cardinalidad (rechazos 18 y 19, §6).

**Qué se acepta perder:** la simetría entre secciones y la velocidad de componer: una sola rejilla sirve para todo, y por eso se usaba.

**Se verifica:** conteo de rejillas por página (≤ 1 `pp-grid3`); 0 pares consecutivos con la misma rejilla; lectura de la estructura del documento servido, no de la impresión.

### E-5 · Juicio visual en el circuito

**Qué falló:** el circuito verifica cumplimiento, no composición. `art-director` lo dice en su pitfall 7 —no audita—, `claude-design` pide capturas «si el entorno las permite», y este modelo es de texto: nadie juzgaba si la página **se ve diseñada**. De ahí los moldes: llegaban aprobados por métricas.

**Qué cambia:** cada sección pasa tres puertas antes de darse por hecha.

1. **Mecánica:** los criterios de §9, medidos sobre el HTML servido y a 390 px.
2. **Visual:** captura a 1440 y 390 revisada contra la rúbrica de antipatrones de `claude-design` (molde de tres, cifras monumentales, eyebrown sobre titular, iconos en tile, simetría plana) por un modelo de visión —Gemini vía `vision_bridge`, o el revisor externo de Mario—. Devuelve hallazgos con banda y coordenada, no impresiones.
3. **Aprobación:** Mario aprueba sección por sección. Sin (1) y (2) no se le pide.

**Qué se acepta perder:** velocidad. Una página de 10 bandas ya no se cierra en una sesión.

**Se verifica:** cada sección tiene su par de capturas fechado y su nota de revisión visual; ninguna sección se declara lista sin las dos.

### E-6 · Accesibilidad medida, no declarada

**Qué falló:** el criterio de contraste de §9 existía y no cazó el defecto real. Revisión visual externa sobre captura: «El método» sale blanco sobre salvia (≈1,4:1) y los rótulos «CASO 01/02/03» salen gris claro sobre marfil. Los numerales 01–04 del método están en el DOM y no se ven. La causa es que se comparaba contra el hex teórico del token, no contra el fondo computado del ancestro. Además, §1 y el rechazo 6 prohíben el eyebrow sobre titular y la portada lo usa en casi todas las bandas.

**Qué cambia:**

1. El contraste se mide **computado**: `getComputedStyle` del texto contra el primer ancestro con `backgroundColor` no transparente, en el nodo tal como lo sirve el servidor. Un valor de token no cuenta como medición.
2. Se retiran los eyebrows decorativos sobre titular en toda la portada; `pp-eyebrow` queda sólo para etiquetas que informan (categoría de artículo, metadato de ficha).
3. Los numerales del método vuelven al texto visible con contraste ≥ 4,5:1 (no 3:1: son texto, no ornamento).
4. **`h1` duplicado (medido 2026-10-31):** `/contacto/` imprime «Contacto» + el `h1` de contenido; `/perspectivas/` y `/sobre-mi/` imprimen el título **dos veces** con el mismo texto. pp.css oculta `.entry-title` para `page-id-14`, pero el nodo duplicado no es `.entry-title` en las tres. Se corrige en el árbol o en la plantilla, nunca con otra regla `display:none` (rechazo 5).

**Qué se acepta perder:** algunas bandas quedan sin rótulo superior; el método pierde el aire de «maqueta» y gana legibilidad.

**Se verifica:** 0 textos por debajo de 4,5:1 (3:1 en ≥24 px) medidos computados en las cinco bandas y a 390/1440 · 0 eyebrows sobre `h1`/`h2` · `document.querySelectorAll('h1').length === 1` en las **cinco** páginas publicadas.

### E-7 · Migración de tema (decisión separada, no ejecutada)

**Qué es:** el sitio corre sobre `leroux` + `leroux-child`. Para poder vender sitios y para dejar de depender de un tema cuya CSS y diseño no son licenciables (`licensing/README_License.txt`: GPL sólo en PHP/HTML; CSS, imágenes y diseño quedan bajo la licencia comprada), la base a reutilizar debe ser propia.

**Decisión propuesta, no aplicada:** child theme sobre **Hello Elementor** (GPL), con `tokens.css`, `components.css` y `utilities.css`. El cliente edita con Elementor; el diseño vive en el CSS propio. Los patrones se escriben en **HTML y CSS** como fuente; el JSON de Elementor es adaptador por proyecto, nunca el origen.

**Por qué no se ejecuta ahora:** cambiar de tema invalida el mecanismo de E-1 (la cabecera actual es la plantilla 2129 de Leroux) y obliga a rehacer portada y páginas internas en un mismo movimiento. Se ejecuta cuando E-1, E-3 y E-6 estén medidos y aprobados, en un entorno de pruebas con copia previa — nunca sobre el sitio en vivo sin respaldo verificado.

**Se verifica (cuando se decida):** paridad de las cinco páginas contra la línea base de capturas · mismas clases `pp-*` · 0 CSS por `page-id` · peso total ≤ línea base.

### Aprobación de esta enmienda

La **v1.3** no se aplica hasta que Mario firme. Al firmarla quedan cerradas, con los valores recomendados de §10 salvo objeción expresa: dirección B con préstamos de A · dominio operación y proceso · congelamiento 2026-11-02.

**Alcance de la firma (salvedad explícita):** la firma congela las **reglas del sistema** — tokens, vetos, criterios de §9 y las enmiendas E-1…E-7 —, no la estética final de pennacchiotti.cl. El estado visual del sitio sigue sujeto a E-4 y a la aprobación por sección de Mario; ninguna captura se declara definitiva por el solo hecho de que el documento esté firmado. Ninguna regla se cambia por gusto: se cambia por enmienda.

**Condición del congelamiento:** el 02-11 sólo vale si la firma llega antes. Congelar un documento con una premisa vencida es peor que mover la fecha: si no hay firma al 01-11 23:59, la fecha se re-emite en v1.4 y se registra el motivo.

Orden de ejecución tras la firma, **en entorno de pruebas con copia previa**: **E-3** (restos del demo, 15 min, sin riesgo de render) → **E-6** (contraste computado, eyebrows, `h1` duplicado: es lo que hoy impide leer la página) → **E-1** (plantilla, cabecera y pie; sin `display:none`) → captura 1440/390/768 y puerta visual de la portada → **E-2** (taxonomía, toca copy y estructura) → **E-4** (recomposición banda por banda, con captura por sección) → captura final. **E-7** no entra en esta tanda: es otra decisión. Ningún paso se declara hecho sin la medición de su criterio.

---

## E-8 — Duotono selectivo · aprobada 2026-10-31

**Motivo.** Las once piezas usables son fotografía de operación. Medido: el color del pan, el
brillo del acero, la diferencia entre masa cruda y horneada y los indicadores de pantalla son
información; el duotono la elimina. Una ley visual que borra evidencia contradice el principio
del sistema.

**Regla.**

- Fotografía documental → **color real**, balance neutro, sin `filter`.
- Abstracciones, esquemas y diagramas → **duotono ink** (`#223035` / `#FBFAF9`).
- Velo `rgba(34,48,53,…)` sobre foto **sólo** para sostener texto encima; contraste resultante
  ≥ 4,5:1 medido sobre el píxel más claro del área de texto.

**Qué se acepta perder.** La uniformidad cromática entre foto y gráfico: la página mezcla
registro documental en color con gráfico en duotono.

**Qué no cambia.** Numerales serif, filetes de 1 px, paleta, escala y tiempos.

**Verificación.** En el CSS final: 0 reglas con `filter: grayscale|sepia|duotone` aplicadas a
un `img` de contenido; toda abstracción con dos colores como máximo.

Aprobada por Mario el 2026-10-31. No modifica el resto de la firma; el documento sigue
pendiente de firma de v1.3.
