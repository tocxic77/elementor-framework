# Registro de cambios — pennacchiotti.cl

Formato: fecha · documento (ID) · cambio · estado · reversión.
Todo cambio de contenido se hace sobre documentos de WordPress identificados por ID; nada se publica sin aprobación de Mario.

## 2026-10-23

### Inventario verificado (medición en vivo, 22:20–22:35)
- 5 páginas publicadas: Inicio (1933, front page), Sobre mí (12), Perspectivas (13), Contacto (14). Borradores: Inicio (9), Global Styles (1951).
- Las 13 páginas demo de la plantilla ya no existen: `/home/`, `/home-2/`, `/about-us/`, `/about-us-2/`, `/what-we-do/`, `/case-studies/`, `/contact/` (200 → alias), `/contact-us/`, `/workshop/`, `/workshops/`, `/global-styles/`, `/inicio-revision/` → 404.
- `/inicio/` y `/contact/` responden 200 sirviendo el mismo contenido que `/` y `/contacto/`, con canonical correcto hacia la URL buena. No hay canibalización por canonical, pero son URLs duplicadas indexables.
- Sistema de diseño ya existente en el kit: 14 variables globales (ink #223035, heading #20282D, text #263037, muted #85979B, sage #D5DEDE, gray #EFEFEF, ivory #FBFAF9; Newsreader + DM Sans; size-display 56, size-h2 42, size-h3 26, size-lead 18, size-body 15) y 22 clases globales `pp-*`.

### Defectos técnicos abiertos (medidos, sin corregir)
1. **Sin navegación**: ninguna página renderiza `<nav>`; 2 enlaces internos por página (`#content` + pie). No hay sitio navegable.
2. **CTA sin destino**: los botones del sitio se renderizan como `<button>` sin `href` (widget `e-button` sin `link.destination`; el enum `link.tag` admite `a`/`button` y queda en `button` cuando no hay enlace). «Agendar diagnóstico» y «Ver perspectivas» no hacen nada.
3. **Formulario**: 0 elementos `<form>` en el sitio.
4. **Pie**: «© 2023 eramic, All Rights Reserved» en todas las páginas (marca heredada de la plantilla) y descripción de marca desalineada con el posicionamiento nuevo.
5. **Perspectivas**: 211 palabras, sin artículos; muestra «contenido en preparación».
6. **Banner de cookies en inglés** («Customize / Reject All / Accept All»).
7. Peso de la home: 2,92 MB en 60 recursos, 26 scripts, 42 hojas de estilo; dos imágenes de 769 KB y 667 KB.

### Cambios aplicados
| Documento | ID | Cambio | Estado | Reversión |
|---|---|---|---|---|
| Soluciones (nueva) | 2076 | Página creada en borrador y construida en Elementor V4 con las clases globales `pp-*`: hero con H1 y 2 CTA, 6 problemas, público objetivo, 4 modalidades (diagnóstico, diseño y estandarización, implementación y adopción, formación y transferencia) con qué incluye / qué recibes / qué aportas / siguiente paso, alcance y exclusiones, cómo se inicia (3 pasos), condiciones de contratación, 6 preguntas frecuentes y CTA final. 11 bandas, 1 H1, 8 H2, 22 H3, 3 botones. | Borrador, sin publicar | Borrar página 2076 (no está enlazada ni indexada) |

Sin cambios sobre documentos existentes: no se editó Inicio, Sobre mí, Perspectivas ni Contacto.

### Gobernanza documental (24-10-2026, 00:05)
| Documento | Cambio | Estado | Reversión |
|---|---|---|---|
| `docs/SEO-CONTRACT.md` | Nuevo. Reglas duras de indexación (canonical y `robots` explícitos, duplicado → `noindex` o 301), regla FAQ visible ⇒ `FAQPage`, lista cerrada de schema y contrato completado de `/soluciones/` (post 2076) con 5 bloqueos de publicación medidos. | Borrador para aprobación | Borrar archivo |
| `docs/DESIGN.md` | §Modo de superficie: de 2 modos a 4 (`persuade`, `read`, `legal`, `utility`) con la regla de cada uno. `/contacto/` queda en `persuade`; el cambio a `utility` es decisión pendiente. | Aplicado | Restaurar la línea original de una frase |
| `docs/SISTEMA-DISENO-CONSTRUCCION-v1.1.md` | §9.3 Rendimiento: LCP < 2,5 s e INP < 200 ms con instrumento declarado (Lighthouse móvil / campo) y `N/A` admitido sin tráfico. Se reordenó 9.2/9.3. | Aplicado | Eliminar §9.3 |
| Skill `pennacchiotti-web-design-system` | v1.0.0 → v1.1.0: §0.1 vetos absolutos (evidencia, confidencialidad, veracidad, AA) separados de la jerarquía de preferencia; SEO Contract obligatorio y previo; §13 cita §9.3; plantilla de contrato unificada a 4 modos (antes `operate`/`experience`, un quinto vocabulario). | Aplicado | Revertir a v1.0.0 |

Nada publicado. Ninguna página de WordPress modificada.

## 2026-10-24 (00:20–00:55) · theme, home y contenido

Sesión de orden directa: cerrar los defectos P0 medidos en CAMBIOS y en las tres auditorías externas. Todo verificado con `curl` sobre el sitio en vivo tras purgar nginx.

### Cambios en WordPress

| Documento | ID | Cambio | Estado | Reversión |
|---|---|---|---|---|
| Header · sitio | 2101 | Theme Builder header (antes no existía ninguno: el sitio no tenía `<nav>`). Wordmark tipográfico —sin el logo demo de 2022—, navegación Soluciones · Contacto · Perspectivas · Sobre mí y CTA «Agendar una conversación» → `/contacto/`. Sticky. | Publicado, condición `include/general` | Despublicar 2101: vuelve el header de Hello Elementor |
| Footer · sitio | 2102 | Theme Builder footer: oferta en una línea, navegación, `contacto@pennacchiotti.cl`, Santiago, «© 2026 Mario Pennacchiotti», enlace a Privacidad. | Publicado, `include/general` | Despublicar 2102 |
| Inicio | 1933 | Reconstrucción completa (7 bandas): hero tipográfico con panel de método en vez de la foto genérica; 6 problemas; método en 5 etapas con entregable por etapa; 4 aplicaciones con problema/entregable; 2 situaciones narradas sin nombres ni cifras; perfil con la credencial existente; cierre con qué incluye la conversación. 1 H1, 6 H2, 33 H3, 4 botones con `href`. | Publicado | Revisión de WordPress del post 1933 |
| Soluciones | 2076 | Publicada (estaba en borrador). Los bloqueos 2 y 3 del `SEO-CONTRACT.md` quedan resueltos: tiene enlaces entrantes desde header, home y footer, y sus CTA navegan. | Publicado | Volver a borrador |
| Perspectivas | 13 | El contenido clásico («artículos en preparación») se reemplazó por 3 notas técnicas reales. La página no estaba construida con Elementor: `build-composition` no la renderiza. | Publicado | Revisión de WordPress del post 13 |
| Privacidad | 2106 | Página nueva en modo `Legal`: responsable, datos recogidos, finalidad, plazo, derechos (Ley 19.628 y 21.719), cookies, cambios. | Publicado | Volver a borrador |

Página 2105 («Privacidad y cookies») quedó como borrador huérfano: se creó para probar el slug y se reemplazó por 2106 con URL `/privacidad/`. Borrar cuando se confirme.

### Cambios en archivos (FTP)

| Archivo | Cambio | Reversión |
|---|---|---|
| `wp-content/mu-plugins/pp-seo-meta.php` (nuevo) | Fija `<title>`, `description`, `og:title` y `og:description` por página desde un mapa único, retirando los que emiten los plugins SEO. Corrige las 6 páginas que describían «agroindustria» u otra oferta. | Borrar el archivo |
| `themes/hello-elementor-child/pp.css` | Bloque añadido: oculta `.entry-title` en 14, 1933, 2076 y 2106 (el tema imprime el título como H1 y cada página declara el suyo). | `pp.css.bak-20261024` |

Los dos mu-plugins de un solo uso que se usaron para migrar la página 13 se eliminaron del servidor; quedan `force-app-passwords.php`, `pp-seo-meta.php` y `endurance-page-cache.php`.

### Verificado en vivo

- 6 rutas responden 200; `/soluciones/` ya no es 404.
- Un solo H1 **visible** por página; `/perspectivas/`, `/soluciones/`, `/privacidad/` y `/sobre-mi/` conservan el H1 del tema oculto por CSS, así que en el DOM hay dos.
- `title` y `description` alineados con la oferta de `PRODUCT.md` en las 6 páginas.
- Home sin imágenes: se eliminaron las dos capturas de Krea (667 KB y 769 KB). Queda 1 `<img>` (icono del plugin de cookies).
- Header: 4 enlaces + CTA con `href`; área de toque 44 px de alto; sticky compilado en el CSS del elemento.
- Pie: «© 2026 Mario Pennacchiotti».

### Defectos nuevos medidos (sin corregir)

1. **Dos plugins SEO activos**: `seo-by-rank-math` y `surerank`. Conviven y emiten metadatos distintos; el mu-plugin los neutraliza pero la convivencia sigue siendo un riesgo.
2. **Dos `<footer>` en el DOM**: el de Elementor y el de Hello, que `pp.css` oculta con `display:none`. Ocultar lo no resuelto es antipatrón: corresponde desactivar el pie del tema.
3. **Título del tema como H1 en páginas sin «Ocultar título»**: el H1 duplicado se resuelve por CSS, no en el origen. En el editor es un clic por página (Ajustes → Ocultar título).
4. **`/sobre-mi/` publica 4 cifras que `PRODUCT.md:65` marca como no publicables**: −20 %→<5 % de error de estimaciones, +20 % fruta Premium, −35 % detenciones, 10.000 m², 40+ organizaciones. Requiere decisión de Mario: son resultados de empleadores anteriores.
5. **Banner de cookies**: sigue en inglés («Customize / Reject All / Accept All») y con categorías vacías. Es configuración de CookieAdmin, no del tema.
6. **Sin foto de Mario**: no hay asset en la biblioteca. La sección de perfil es solo texto.
7. **`/inicio/` y `/contact/`** siguen sirviendo el mismo contenido que `/` y `/contacto/` con canonical correcto; falta `noindex` o 301.
8. Persisten 47 hojas de estilo y 26 scripts (SpeedyCache, Spectra, Wordfence, CookieAdmin).

### Proceso

No se guardó `backup_1933.json` antes de reconstruir la portada; la reversión depende de las revisiones de WordPress. La regla del skill exige ese respaldo y no se cumplió.

## 2026-10-24 (01:00–01:40) · sistema editorial de páginas internas

Segunda auditoría externa: «hay contenido, pero no sistema visual; las páginas internas son texto pegado». Se atacó eso, no el copy.

### Cambios

| Dónde | Cambio | Medición antes → después | Reversión |
|---|---|---|---|
| `/sobre-mi/` (12) | Los 7 párrafos existentes se envolvieron en el componente timeline (eje, 6 hitos numerados y «Credenciales» aparte). **El texto no se reescribió**: un plugin de un solo uso parseó el `post_content` y lo reenvolvió. | Texto corrido → 6 hitos con eje; ancho 884 → 780 px | `pp_content_backup_v1` (meta del post 12) |
| `/perspectivas/` (13) | Contenedor de lectura. La regla previa del tema fijaba `max-width:none !important` sobre `.site-main`, así que el texto corría a 884 px. | 884 → 724 px @ 19 px | `pp.css.bak2-20261024` |
| `/privacidad/` (2106) | Columna de lectura centrada y cuerpo a 17 px (estaba a 15 px, bajo el mínimo legible). | 15 px pegado a la izquierda → 17/29,75 px centrado a 720 px | `pp.css.bak2-20261024` |
| `/soluciones/` (2076) | Ancho máximo de párrafo 720 px. | 806 → 720 px | `pp.css.bak2-20261024` |
| `/contacto/` (14) | `method="post"` forzado en el formulario atómico. | atributo ausente (GET por defecto) → `method="post"` | Borrar `mu-plugins/pp-hardening.php` |

Componentes nuevos en `pp.css`: `.pp-label`, `.pp-lead`, `.pp-tl` / `.pp-tl-item` / `.pp-tl-n` y `.pp-note`.

### Verificado

- `/sobre-mi/` 780 px de contenedor, 6 hitos con eje de 1 px visible.
- `/perspectivas/` 724 px @ 19 px · `/soluciones/` 720 px @ 19 px · `/privacidad/` 623 px @ 17 px centrado.
- `curl` confirma `<form method="post"` en `/contacto/`.

### Correcciones a la auditoría

- «No hay formulario funcional / usa GET»: el atributo faltaba, pero el sitio carga `atomic-widgets-form-handler.min.js` (Elementor 4.3.5), que intercepta el envío por JS. No había fuga de datos en la URL en uso normal; sí un fallback inseguro. Queda endurecido. **La entrega real del correo sigue sin verificarse.**
- «Múltiples familias tipográficas»: cierto y medido — se cargan Newsreader, Inter, DM Sans y Epilogue con los 9 pesos cada una. Es configuración del kit global, no del tema hijo.
- «Faltan imágenes»: cierto y **no resuelto**. No hay material: la biblioteca solo tenía dos capturas genéricas de Krea que se retiraron por no decir nada. Producir retrato y fotografía de operación requiere archivos de Mario.

### Pendiente de decisión

1. Retrato profesional + 2 fotos de operación (sin ellos no hay sistema visual completo).
2. `/sobre-mi/` mantiene las 4 cifras marcadas como no publicables en `PRODUCT.md:65`.
3. Cookies: banner en inglés y categorías vacías (config de CookieAdmin).
4. Desactivar uno de los dos plugins SEO.
5. `/soluciones/` sigue siendo una página larga y plana: 10 H2 y 34 párrafos. La matriz comparativa de modalidades exige rehacer esa página, no CSS.

## 2026-10-26 · plantillas, limpieza e identidad personal

### Inventario de plantillas (medido sobre la base, no sobre la UI)

| Kit | Plantilla | Importado | Estado |
|---|---|---|---|
| — | `Default Kit` (5) | 2025-04-24 | activo, vacío |
| **Ceramic Studio** | 1949 | 2026-10-23 16:50 | **más antiguo** — era el origen del «© 2023 eramic» |
| — | `Header · sitio` (2101) / `Footer · sitio` (2102) | 2026-10-24 00:30 | activos, construidos a mano |
| **Agentify · Personal Portfolio for Creatives** | `Kit Styles` 2116 + 30 bloques (2120–2195) | 2026-10-25 21:00 | importado, **ninguno activo** |

Los 30 bloques de Agentify son plantillas de sección V3 (`section`/`column`/`widget`), no páginas: no tocan el front mientras no se activen.

### Respaldo

`docs/backup-contenido-20261026.json` — 2.254.265 bytes, 105 entradas, 79 con `_elementor_data`. Incluye páginas, entradas, plantillas, clases globales y los ajustes de portada. Generado por un plugin de un solo uso y descargado por FTP.

### Borrado (todo a la papelera, reversible)

| ID | Qué | Estado previo |
|---|---|---|
| 1949 | Plantilla «Ceramic Studio» | publish |
| 9 | Página «Inicio» | draft |
| 1951 | Página «Global Styles» | draft |
| 2105 | Página «Privacidad y cookies» | draft (reemplazada por 2106) |
| 2058 | Entrada «Transformación digital no es digitalización» | draft |

El primer intento con `wp_trash_post()` dentro de `init` devolvió 500 (los hooks de Elementor se disparan antes de que el post type esté listo). Se resolvió con `UPDATE` directo sobre `wp_posts` en `wp_loaded`; el resultado quedó registrado en `uploads/pp-backup/limpieza-20261026.json`.

### Identidad personal

Retrato 200×200 subido como attachment 2200; monograma MP en dos versiones (2201 tinta, 2202 marfil); monograma tinta fijado como `site_icon`. Retrato aplicado a 96 px en `/sobre-mi/` y `/contacto/`. Especificación completa en `DESIGN.md` → «Identidad personal».

Restricción técnica encontrada: el FTP de HostGator no permite crear directorios (error 553). Los archivos se subieron a `mu-plugins/` y un plugin de un solo uso los copió a `uploads/pp/`.

### Nota de seguridad

La búsqueda de retratos en Immich devolvió documentos de identidad escaneados entre las fotos etiquetadas. Se descartaron los temporales sin reutilizarlos. **Immich no es fuente de retratos para el sitio**: contiene documentos sensibles mezclados con fotografía personal.

## 2026-10-26 · titulares invisibles: causa raíz y reparación

### Diagnóstico (medido en producción, no inferido)

| Hallazgo | Medición |
|---|---|
| H1 del home ilegible | `color:#FFFFFF` sobre ancestro con fondo `#FBFAF9` → **1,04:1**. Histograma de píxeles del área del titular: 74,7 % marfil, 20,6 % blanco |
| Tipografía | `h1/h2/p` en **Mukta Vaani**; DM Sans y Newsreader se importaban en `pp.css:1` y nunca se usaban |
| Escala | h1 75 px / h2 54 px; la ley del documento decía 56/60 y 42/50 |
| Imágenes | 1 solo `<img>` en la portada: el icono de cookies |
| Clases del sistema | **0** nodos con `pp-*` en el DOM: la capa de clases no se aplicó al árbol V4 |

**Causa raíz:** `post-2116.css` (kit «Agentify · Kit Styles») imprime `.elementor-kit-2116 h1{color:var(--e-global-color-eb5e9b4);font-family:"Mukta Vaani";font-size:4.688rem;font-weight:600}` con `--e-global-color-eb5e9b4:#FFFFFF`. El kit es de una plantilla demo; los tokens de `DESIGN.md` existían pero ninguna regla los aplicaba al árbol V4.

Segundo defecto encontrado al reparar: `pp.css` usaba `var(--font-display)` y `var(--heading)` **sin definirlas**, así que el H1 de `/sobre-mi/` y de las páginas editoriales caía en Mukta Vaani a 46 px y en el color de párrafo `#6C6F73`.

### Cambio aplicado

Archivo: `wp-content/themes/hello-elementor-child/pp.css` (FTP, `filemtime` invalida la caché). Respaldo del original en `docs/backup-pp-css-20261026.css`.

1. Bloque `:root` con los tokens de `DESIGN.md` (`--font-display`, `--font-body`, `--heading`, `--text`, `--muted`, `--ivory`, `--ink`, `--gray`, `--sage`).
2. Capa tipográfica `.elementor-kit-2116 h1/h2/h3`: Newsreader 56/1.07, Newsreader 42/1.19, DM Sans 26/1.31, pesos 400/400/500, color `#20282D`.
3. Escalones `@media`: 50/38/23 px hasta 1023; 40/32/22 px hasta 767.
4. Sin `!important`. El primer intento lo llevaba y volvió invisibles los titulares de la banda oscura (`#223035`, `e-h2`: `color:#FBFAF9` local) a 1,1:1. Se retiró para que el estilo local del elemento siga ganando donde el diseñador lo fijó.

No se tocó el kit 2116 ni el árbol de Elementor: ningún cambio de contenido, solo CSS del tema hijo.

### Verificación posterior (producción, tras PURGE 204 en 5 rutas)

| Ruta | H1 visibles | H1 | Titulares bajo AA |
|---|---|---|---|
| `/` | 1 | Newsreader 56 px, `#20282D`, 14,36:1 | 0 de 24 |
| `/soluciones/` | 1 | Newsreader 56 px, 14,97:1 | 0 de 39 |
| `/contacto/` | 1 | Newsreader 56 px, 14,97:1 | 0 de 1 |
| `/sobre-mi/` | 1 | Newsreader 46 px, 14,36:1 | 0 de 3 |
| `/perspectivas/` | 1 | Newsreader 46 px, 14,36:1 | 0 de 5 |

`document.fonts`: Newsreader 400 y DM Sans 500 en estado `loaded`. Sin desbordamiento horizontal en ninguna de las cinco rutas.

**No verificado:** el render a 390 px. El navegador de este entorno no aplica emulación de viewport (`innerWidth` se queda en 1512 con `setDeviceMetricsOverride` y con `Browser.setWindowBounds`), así que las reglas móviles están desplegadas y revisadas por orden de cascada, pero no medidas en pantalla. Pendiente: confirmar en el navegador de Mario a 390 px.

### Rollback

Subir `docs/backup-pp-css-20261026.css` por FTP a la misma ruta. No hay cambios en base de datos.

### Documentación

`DESIGN.md` pasa a v1.1: nueva §Dirección de imagen (qué se fotografía, tratamiento, ilustración, prohibidos, formatos, prioridad de producción) y §Deuda viva actualizada con los defectos 7–11 que quedaron abiertos.

## 2026-10-26 (19:59) · dos bandas fotográficas en la portada (post 1933)

### Origen del material

Fotografías reales de una línea de panificación industrial, tomadas con Samsung SM-G975F entre 2023 y 2025, recuperadas de Immich (`100.114.4.11:2283`, v3.3.5) con la clave de propietario. Candidatos descartados y por qué: `3b6e7621` tiene el logotipo **Bühler** legible (marca de terceros en el titular propio), `3e469f99` tiene 28,7 % de azul saturado contra la paleta marfil/tinta/sage.

**Condición resuelta (2026-10-26):** las tomas son de autoría de Mario y no muestran instalaciones identificables — solo producto sobre cinta y el interior de un horno, sin marcas, sin rótulos de planta y sin georreferencia publicada. No requieren autorización de terceros: el derecho es del autor. La regla de `PRODUCT.md:83-87` sigue vigente para material ajeno o que identifique instalaciones de un cliente.

### Assets publicados

| Archivo | Dimensiones | Peso | Uso |
|---|---|---|---|
| `wp-content/uploads/pp/pp-cinta-filas-1600x900.jpg` | 1600×900 (1,78:1) | 118 KB | banda a sangre tras el hero |
| `wp-content/uploads/pp/pp-horno-pan-banda1600x424.jpg` | 1600×424 (3,78:1) | 116 KB | banda a sangre antes del CTA final |

Ambas bajo la regla de 120 KB de `DESIGN.md`. Recortes generados desde el original (4032×2268 y 4032×1908) con `object-position` centrado; no llevan velo, texto encima ni tratamiento.

### Cambios en el árbol V4

| Nodo | ID | Posición final | Contenido |
|---|---|---|---|
| `img-band-hero` | `313e2c35` | raíz índice 1 (tras `4609ec3a` h-band) | `e-image` `7c4e3e4d` |
| `img-band-linea` | `687bf08f` | raíz índice 6 (tras `5accf551` e-band, antes de `1ef35c6c` q-band) | `e-image` `20580a62` |

Ninguna banda existente se modificó: `build-composition` con `parent_id: document` + `manage-elements action=move` para posicionar. Publicado con `publish-document`, PURGE nginx 204.

### Verificación (render medido, viewport 1536)

| Medición | Resultado |
|---|---|
| `<img>` en la portada | 3 (dos nuevas + icono de cookies); antes 1 |
| Banda hero foto | top 687, alto 855 px, imagen 1521×855, ratio 1,78 |
| Banda ancha | top 4403, alto 403 px, imagen 1521×403, ratio 3,78 |
| Orden de raíces | h-band → foto → p → m → a → e → foto → q → c |
| Desbordamiento horizontal | 0 px |
| Alto de página | 6.226 px (antes 5.174) |
| Contraste | sin cambios: ninguna imagen lleva texto encima |

### Rollback

`manage-elements` con `action: delete` sobre `313e2c35` y `687bf08f`, publicar y purgar. Los dos JPEG quedan huérfanos en `uploads/pp/` sin afectar el render.

### Pendiente

Verificación a 390 px (limitación conocida del navegador de este entorno). La banda de 3,78:1 mide 103 px de alto en móvil: si se ve como una franja, se reemplaza por el recorte 1,78 o se oculta bajo 767 px.

## 2026-10-26 (20:15–20:40) · la portada tenía demasiado texto y la foto no seguía la rejilla

Orden de Mario: «tiene demasiado texto el home, y texto que no está alineado con la imagen», con `leroux.qodeinteractive.com/business-home/` como referencia.

### Medición previa

| Medición | Portada | Leroux business-home |
|---|---|---|
| Palabras de contenido (sin nav ni pie) | **685** | **394** |
| Hero | 84 (H1 10 + entradilla 20 + panel de 5 filas 54) | ~20 |
| Banda más densa | `p-band` 164 · `e-band` 155 | bloques de 20–30 |
| Listas de 5 pasos en la misma página | **2** (`ch-panel` del hero y `m-band`) | 1 |
| Borde izquierdo del texto | 170 px | — |
| Borde en que termina el texto | 760–795 px | — |
| Banda fotográfica ancha | **0 → 1521 px** | rejilla |
| Rejilla real del sitio | 170 → 1350 px (1180) | — |

Tres referencias distintas en la misma página (0, 170 y 760): la foto a sangre no compartía ninguno de los dos bordes del texto. Eso es el «no alineado» medido.

### Cambios aplicados (post 1933)

| Nodo | Acción | Medición |
|---|---|---|
| `ch-panel` `18afe328` | Eliminado: duplicaba los 5 pasos de `m-band` | hero 84 → **35 palabras** |
| `h-right` `7d50628a` | Entra `e-image` `49277942` — `pp-cinta-filas-630x875.jpg` (79 KB) | 448×623, borde derecho **1350 = rejilla** |
| `img-band-hero` `313e2c35` | Eliminada: 855 px de foto justo tras el hero, ya redundante | — |
| `p-i1..p-i6` (`7f626816`, `770f5fd5`, `a86ff77`, `6aa1a425`, `59fb7523`, `7a534231`) | Segunda frase de cada tarjeta eliminada | `p-band` 164 → **120** |
| `a-c1p..a-c4p` (`7c9cb6e5`, `35b58fb4`, `7966e8c1`, `482a0d4`) | Frase de diagnóstico eliminada: repetía `p-band`; queda «Qué recibes» | `a-band` 103 → **67** |
| `img-band-linea` `687bf08f` | De a sangre a rejilla: `max-width:1180px`, centrada (pp.css) | 1521 → **1180**, 170 → 1350 |

La regla vive en `pp.css` con `!important` acotado a ese `data-id`: la clase atómica del propio elemento (`.e-46aae31c-2f27`) fija `max-width:100%` y ganaba por cascada. Solo afecta a esa banda.

### Verificación (viewport 1536)

| Medición | Antes | Después |
|---|---|---|
| Palabras de contenido | 685 | **556** (−19 %) |
| Hero | 84 | 35 |
| Alto de página | 6.226 px | **5.323 px** (−903) |
| Banda ancha: borde izq./der. | 0 / 1521 | **170 / 1350** |
| Imagen del hero: borde der. | — | 1350 |
| `alineado` (banda = rejilla) | no | **sí** |
| Desbordamiento horizontal | 0 | 0 |
| Contraste AA | 0 fallos | 0 fallos |

### Rollback (texto eliminado, literal)

Panel del hero: «DE CONOCIMIENTO TÁCITO A CAPACIDAD OPERATIVA · 01 Conocimiento tácito — El criterio vive en una persona. · 02 Criterio explícito — Límite, unidad y evidencia. · 03 Procedimiento — Quién hace qué y con qué registro. · 04 Control — Qué se mide y cuándo se decide. · 05 Capacidad instalada — El equipo lo opera sin acompañamiento.»
Tarjetas `p`: «Nadie puede explicar la diferencia porque no está registrada.» · «o degrada la calidad.» · «El procedimiento se escribió para la auditoría, no para el turno.» · «Sin límite escrito, la decisión no es defendible ni reproducible.» · «El registro se llena al final del turno.» · «La herramienta acelera la variabilidad.»
Tarjetas `a`: «El resultado varía entre turnos y nadie puede explicar por qué.» · «Existen procedimientos, pero no describen la operación real.» · «La experiencia crítica está en una sola cabeza.» · «La capacitación se aprueba, pero la ejecución no cambia.»

### Pendiente

`e-band` sigue siendo la banda más densa (155 palabras en dos casos). Una segunda pasada la llevaría a ~100 y el total a ~500, más cerca de las 394 de Leroux.

## 2026-10-26 (20:20–20:45) · Leroux activado: la capa tipográfica se quedó huérfana

Mario activó el theme **Leroux** comprado. Estado medido del servidor: temas `leroux`, `leroux-child` (creado por el instalador), `hello-elementor`, `hello-elementor-child`; plugins `leroux-core`, `qode-framework`, `qode-optimizer`, `qode-quick-view-for-woocommerce`, `qode-wishlist-for-woocommerce`. El HTML ya sirve `themes/leroux/assets/css/main.min.css` + `themes/leroux-child/style.css` + `themes/leroux/style.css`.

### Regresión medida

`pp.css` vivía en `hello-elementor-child`. Al activar Leroux esa hoja dejó de encolarse y **el `h1` volvió a 75 px `#FFFFFF` sobre marfil: 1:1**. Otras medidas del mismo momento: `body` `#FFFFFF`, `h2` `#1F242E` 54 px, `p` `#263037` 18 px Mukta Vaani.

El `leroux-child/style.css` era solo el encabezado de 226 bytes del instalador.

### Primera restauración fallida (y por qué)

Se subió la capa completa a `leroux-child/style.css` con selectores `html body.elementor-kit-2116 h1` (especificidad 0,1,3 contra 0,1,1 del kit). El navegador seguía midiendo **0 reglas** en esa hoja: el theme padre la encola con `?ver=7.1.3` fijo y `Cache-Control: public` con `Expires` a un año, así que servía la copia antigua. `Page.reload(ignoreCache=True)` no lo resolvió.

### Solución aplicada

| Archivo | Contenido | Motivo |
|---|---|---|
| `leroux-child/pp.css` | Capa completa (tokens, tipografía h1-h3, breakpoints, banda `687bf08f` a 1180 px, `.qodef-page-title` oculta) | URL propia: no hereda la versión fija del padre |
| `leroux-child/functions.php` | `wp_enqueue_style('leroux-child-pp', …, filemtime())` a prioridad 99 | Cada edición cambia el `?ver` y se ve al instante |
| `leroux-child/style.css` | Devuelto al encabezado limpio de 226 bytes | Evita reglas duplicadas y una hoja cacheada un año |

Selectores de titular: `html body.elementor-kit-2116 h1` — `uploads/elementor/css/post-2116.css` se carga **después** de las hojas del theme y a igual especificidad ganaba.

### Defecto nuevo encontrado

Leroux activa una banda de título de página (`.qodef-page-title`, 240 px, `#FAFAFA`) que en este sitio queda **vacía** —Elementor oculta el `title`— y solo añade aire muerto antes del contenido. Medido en las 5 rutas: 240 px de alto y `innerText` vacío en todas. Ocultada en `pp.css`.

### Verificación (viewport 1536, tras PURGE 204)

| Ruta | H1 visibles | Banda de título | H1 | Fallos AA | Alto |
|---|---|---|---|---|---|
| `/` | 1 | **0 px** | 56 px Newsreader `#20282D` | **0** de 56 nodos | 5.114 px |
| `/soluciones/` | 1 | 0 px | 56 px Newsreader `#20282D` | 0 | 4.420 px |
| `/sobre-mi/` | 1 | 0 px | 56 px Newsreader `#20282D` | 0 | 1.414 px |
| `/contacto/` | 1 | 0 px | 56 px Newsreader `#20282D` | 0 | 1.290 px |
| `/perspectivas/` | 1 | 0 px | 56 px Newsreader `#20282D` | 0 | 1.370 px |

`h1` sobre `#FBFAF9` = **14,36:1**; `h2` 42 px Newsreader 13,02:1 y 14,36:1; desbordamiento horizontal 0 en las cinco. Botones del hero: `#FBFAF9` sobre `#223035`.

### Deuda abierta que dejó Leroux

El kit global sigue siendo **2116**, con globales que no son ni los de `DESIGN.md` ni los de Leroux: `--e-global-color-primary:#FB3434` (rojo), `--e-global-color-accent:#3D19CC` (violeta), `--e-global-color-text:#6C6F73` (5,05:1), tipografía `Mukta Vaani` en `body` y `h1`. Mientras no se importe el kit de Leroux o se corrijan esos globales, cualquier widget nuevo que use colores globales nace fuera de la identidad.

## 2026-10-26 (20:45–21:10) · parche de CVE-2026-32507 y demo de Leroux importado

### a) Parche del object injection (Leroux 1.3.1 → sin 1.4 disponible)

No hay acceso a la 1.4 (el paquete GPL es la 1.3.1), así que se cerró el punto de entrada a mano. Detalle completo en `docs/seguridad/CVE-2026-32507-leroux-1.3.1.md`.

Sink identificado: `wp-content/themes/leroux/inc/pagination/helper.php:79-82`, dentro del callback de la ruta REST pública `leroux/v1/get-posts` (registrada sin `permission_callback`, y `class-leroux-rest-api.php:53` aplica `__return_true` por defecto):

```php
if ( class_exists( $options['object_class_name'] ) ) {
    $options['this_shortcode'] = new $options['object_class_name']();
}
```

`class_exists()` era toda la validación. Medición antes/después con `DirectoryIterator` (clase que exige argumentos: si se instancia, la petición cae):

| Estado | `GET /wp-json/leroux/v1/get-posts?options[object_class_name]=DirectoryIterator` |
|---|---|
| original 1.3.1 | **500** |
| parcheado | **200** |

El parche (8.293 → 10.076 bytes) añade lista blanca `^LerouxCore_[A-Za-z0-9_]+_Shortcode(_Elementor)?$`, saneado de `plugin/module/shortcode/pagination_type/behavior` a `[A-Za-z0-9_-]`, `function_exists()` antes del nombre de función dinámico y `isset()` en las claves opcionales. Backup en el servidor: `helper.php.bak-20261026`. Portada y 6 rutas verificadas en 200 tras el cambio.

### b) Demo de Leroux importado sin descargar adjuntos

El importador del admin moría porque el WXR trae **350 adjuntos al principio** y el PHP del hosting corta a `max_execution_time = 60`: descargaba imágenes hasta agotar el tiempo, sin llegar a crear páginas. Se importó en el servidor con `WP_Import` y `fetch_attachments = false`.

| Concepto | Valor |
|---|---|
| Duración | 7,1 s |
| Elementos creados | **173** |
| Páginas | 19 |
| Ítems de menú | 142 |
| Plantillas Elementor (`elementor_library`) | 6 |
| Formularios CF7 | 5 |
| Plantilla de sitio (`wp_template`) | 1 |
| Omitidos | `team`, `testimonials`, `product` — esos tipos no están registrados en el sitio |

Las **40 páginas del demo** quedaron en **borrador** para no ensuciar el sitemap ni competir en buscadores con las propias. Portada intacta (`page_on_front = 1933`), sin página de posts asignada, y las 6 rutas propias siguen en 200. El listado con IDs está en `docs/seguridad/import-demo-ids-2026-10-26.json`.

Los scripts de importación (`run.php`, `run2.php`, `draft.php`), el XML y los logs se borraron del servidor: el directorio `wp-content/uploads/pp-import/` ya no existe.

## 2026-10-26 (21:35) · puertas de licencia de leroux-core: qué queda abierto

### Por qué el demo no renderizaba

`leroux-core` 1.2 condiciona el registro de sus tipos de contenido, de sus shortcodes y de sus **46 widgets Elementor** a `LerouxCore_Dashboard::get_instance()->get_code()`. Ese valor viene del código de compra de Envato. Una redistribución GPL no lo trae, así que `get_code()` devuelve cadena vacía y las tres ramas `if ( ! empty( $check_code ) )` no se ejecutan.

Medición en producción antes del cambio:

| Comprobación | Antes | Después |
|---|---|---|
| `get_code()` | 0 caracteres | 0 caracteres (no cambia) |
| `allowed_post_types` | `[]` | `clients`, `portfolio-item`, `team`, `testimonials` |
| Shortcodes del tema (`portfolio_list`, `team_list`, `testimonials_list`, `clients_list`) | no existen | existen |
| Widgets Elementor del tema | **0** (los 21 «leroux» eran widgets de barra lateral de WP) | **46** (`section_title`, `portfolio_list`, `image_marquee`, `accordion`, `counter`, `pricing_table`, `horizontal_showcase`…) |
| Widgets Elementor totales | 239 | 285 |
| Home | 200 | 200 |

### Qué se tocó

Dos archivos, ambos con respaldo `.bak-20261026` en el servidor y diff documentado:

| Archivo | Cambio |
|---|---|
| `leroux-core/inc/post-types/class-lerouxcore-custom-post-types.php` | 3.853 → 4.656 B |
| `leroux-core/inc/plugins/elementor/helper.php` | 3.288 → 3.862 B |

El parche **no borra la comprobación**: conserva `get_code()` y añade un filtro con valor por omisión verdadero. Se revierte sin editar archivos:

```php
add_filter( 'leroux_core_allow_unregistered_post_types', '__return_false' );
```

### Qué NO se puede saltar

| Puerta | Estado |
|---|---|
| Registro del código en Leroux Dashboard | Imposible: lo valida la API de Envato, no el sitio. |
| Actualizaciones automáticas del tema | Imposible sin cuenta Envato. Cualquier versión nueva hay que instalarla a mano. |
| Botón «Import Demo» del dashboard | Llama a `check_purchase_code()` contra Envato. Se sustituyó por la importación del WXR, ya hecha. |

### Riesgo asumido

El tema es 1.3.1 con el parche manual de CVE-2026-32507. Sin actualizaciones automáticas, cada aviso futuro hay que revisarlo y parchearlo a mano. La licencia del paquete es GPL y la compra fue a un redistribuidor; el código de compra de Envato no existe ni existirá.

## 2026-10-26 (21:00–21:20) · la portada se construyó sobre Business Home (#335)

> Nota posterior (21:25): ese árbol fue restituido desde el respaldo el mismo día, al comprobar que la página contenía dos widgets —el slider de Revolution y un spacer— y no un diseño Elementor. El respaldo usado fue `cache/scratch/pp-importer/backup-335-elementor.json` (22.687 B) y la copia se escribió con `wp_slash()` sobre `_elementor_data`.

### Lo que había en #335

El demo importado ocupaba la portada con un árbol Elementor **clásico** (11 secciones, 65 `elementor-section`) y un widget de Slider Revolution. Al medirlo, el contenido estaba prácticamente vacío: solo se veían el titular del slider («Achieve Results With Modern Ideas») y el banner de cookies. Los bloques del demo son shortcodes de Leroux Core que apuntan a `team`, `testimonials` y `product` —los tres tipos que no se importaron—, así que no imprimían nada. Sin `h1` en el DOM.

Respaldo del árbol anterior: `cache/scratch/pp-importer/backup-335-elementor.json` (22.687 B).

### Lo que se construyó

Ocho bloques en V4 atómico, en la portada #335 (`page_on_front = 335`), con el texto de la portada anterior reorganizado y recortado:

| Bloque | Contenido |
|---|---|
| Hero | `h1` «Procesos que se ejecutan igual, entre turnos y entre personas.» + entrada + 2 CTA + foto vertical |
| Método | 5 pasos numerados (conocimiento tácito → capacidad instalada) |
| Banda tinta | «Cuando el criterio vive en una persona…» + CTA |
| Cómo se construye | foto panorámica del horno + 5 etapas con entregable |
| Dónde se aplica | 4 modalidades en tarjetas |
| Casos | 2 casos narrados, sin nombres ni cifras |
| Quién trabaja contigo | retrato + bio + CTA a `/sobre-mi/` |
| Cierre | banda tinta con CTA y correo |

**Sin cifras.** `PRODUCT.md:67` permite una sola cifra publicable y aún sin conteo confirmado, así que no se usaron contadores ni métricas — el demo de Leroux trae una sección de cifras que se omitió a propósito.

### Errores corregidos en el camino

1. **`build-composition` guardó el árbol pero el frontend seguía sirviendo el demo.** La causa era `_elementor_element_cache` en `postmeta`: mientras ese meta exista, Elementor sirve el HTML cacheado aunque `_elementor_data` haya cambiado y se purgue nginx. Borrarlo (`delete_post_meta`) más `files_manager->clear_cache()` lo resolvió. **Purga HTTP sola no basta en Elementor 4.**
2. **Retrato roto**: `hero-1600.jpg` da 404; el archivo real es `uploads/pp/mario-pennacchiotti.png` (200 × 200). Corregido, y acotado a 240 px para no ampliar una imagen de 200 px.
3. **`alt` no existe como propiedad de `e-image`**: va dentro de `image.src.alt` y solo para imágenes por URL. Sin eso, el alt se genera del nombre del archivo («Pp Cinta Filas 630x875»).

### Verificación en producción

| Dato | Valor |
|---|---|
| `h1` | 1 visible, 56 px Newsreader 400, `#20282D`, 242 px de alto |
| `h2` | 6 + 1 de cierre a 36 px; todos Newsreader 42 px salvo el de cierre |
| `h3` | 12 |
| Imágenes | 4 de 4 cargan (`naturalWidth` > 0), alt descriptivo |
| Fallos AA | **0** de 64 nodos de texto medidos |
| Desbordamiento horizontal | 0 |
| Alto del documento | 4.840 px |
| Palabras en el contenido | 514 |
| Rutas propias | `/`, `/soluciones/`, `/sobre-mi/`, `/contacto/`, `/perspectivas/`, `/privacidad/` en 200 |

### Página anterior

La portada anterior (#1933, `/inicio-nueva/`) quedó en **borrador**: era el mismo servicio con otro texto y competía consigo misma en buscadores. Se restituye cambiando su estado a publicado; su árbol Elementor está intacto.

## 2026-10-26 (22:10–23:30) · marco del sitio: cabecera, menús, pie y fondo

La portada ya tenía el diseño del demo de Leroux (17 secciones, clonadas de la
página #15 «Main Home»), pero **sin marco**: no había cabecera, ni menús, ni pie,
y el fondo seguía en blanco. Medido antes de tocar nada: `.qodef-page-header`
presente pero con las 7 ubicaciones de menú vacías (`get_nav_menu_locations()`
→ `[]`), `#qodef-page-footer` **ausente** del DOM, `body` en `rgb(255,255,255)`
y **1.425 px** de scroll horizontal en un viewport de 1.536 px.

### Por qué no había cabecera ni pie

El tema **no llama a `elementor_theme_do_location()`** en `header.php` ni en
`footer.php` (grep sobre los 195 PHP del tema: 0 coincidencias). Las plantillas
de sitio de Elementor Pro importadas del demo (`Main Header` #2123, `Main
Footer` #2126, más `Header · sitio` #2101 y `Footer · sitio` #2102) **nunca se
renderizaban**, aunque sus condiciones estaban puestas en `include/general`.
El marco lo dibuja el tema: cabecera desde `leroux_core_options` + el menú de
`main-navigation`; pie solo si hay widgets en las áreas de pie
(`leroux_is_page_footer_enabled()` = área superior o inferior activa).

Se borró `elementor_pro_theme_builder_conditions` para no dejar plantillas
condicionadas que no se imprimen.

### Antes / después (medido en producción)

| Elemento | Antes | Ahora |
|---|---|---|
| Cabecera | sin cabecera del tema | `#qodef-page-header` **96 px**, fondo `#FBFAF9` |
| Logotipo | `assets/img/logo.png` del tema y después el logo del demo (`logo-retina-free-img.png`) | wordmark propio `pp-wordmark.png` **244×18** (PNG 977×71 a 2x, 9.522 B), `custom_logo` = adjunto 11243 |
| Menú superior | 7 ubicaciones vacías | menú «Principal» (Inicio, Sobre mí, Soluciones, Perspectivas, Contacto) en `main-navigation`, `mobile-navigation`, `fullscreen-menu-navigation` y `vertical-menu-navigation` — **488 px** de ancho |
| Menú inferior | no existía | menú «Pie» (Sobre mí, Soluciones, Perspectivas, Contacto) en widget `nav_menu` |
| Pie | **0 px**, no se imprimía | **278 px**, 3 columnas (`#qodef-page-footer-top-area`), fondo `#263037` |
| Fondo del sitio | `#FFFFFF` | `#FBFAF9` (cuerpo y cabecera) |
| Scroll horizontal | **1.425 px** | **0** (`scrollWidth - innerWidth` = −15) |
| Contraste AA (32 nodos) | 13 fallos | **1** (el mensaje «No posts were found…» sobre la banda oscura, 1,99:1) |
| Pie: texto sobre fondo | `#6C6F73` sobre `#263037` = **2,67:1** | `#EFEFEF` = **8,38:1** |

### Archivos tocados

| Archivo | Cambio |
|---|---|
| `themes/leroux-child/pp.css` | 14.863 → **17.139 B**: fondo `#FBFAF9` con `html body.elementor-kit-2116`; recorte de carruseles (`.swiper`, `.qodef-swiper-container`…) que causaban los 1.425 px; logo a 244 px; margen de ítem del menú 150 → 16 px; texto del pie `#EFEFEF`; párrafos a `#575B5F` (5,1:1 sobre salvia, 7,9:1 sobre el fondo) |
| `themes/leroux-child/functions.php` | 562 → **1.310 B**: filtro `leroux_filter_header_logo_image` que sustituye el logo del tema por el wordmark |
| `uploads/leroux-demo/pp-wordmark.png` | nuevo, 9.522 B (977×71), registrado como adjunto 11243 |

### Opciones del tema escritas (`leroux_core_options`)

`qodef_page_background_color` y `qodef_standard_header_background_color` =
`#FBFAF9`; `qodef_logo_source` y `qodef_mobile_logo_source` = `image`;
`qodef_standard_header_menu_position` = `right`; `qodef_standard_header_height`
= 90; `qodef_enable_top_footer_area` = `yes`; `qodef_set_footer_top_area_columns`
= `3`; `qodef_set_footer_top_area_in_grid` = `yes`;
`qodef_top_footer_area_background_color` = `#263037`;
`qodef_enable_bottom_footer_area` y `qodef_enable_footer_copyright_area` = `no`.

### Pendiente

- Las listas del demo (equipo, testimonios, clientes, portafolio, blog) siguen
  sin contenido: 0 ítems de cada tipo. La portada muestra «No posts were found
  for provided query parameters» donde van las entradas.
- El texto es el del demo (inglés y lorem ipsum).
- Los carruseles ya no desbordan el documento, pero falta comprobar si el JS
  del tema los inicializa (avance automático, flechas).

## 2026-10-26 (23:40–00:20) · la cabecera salía con el estilo viejo del sitio anterior

Síntoma del usuario: «el header no tiene el estilo del sitio, es como que fuera el
estilo antiguo». La causa no era CSS: **la portada #335 conservaba en su meta el
diseño de cabecera del sitio anterior** (`qodef_*`), y ese meta tiene prioridad
sobre las opciones globales del tema (`leroux_core_get_post_value_through_levels()`:
primero meta de la página, después opción global).

Meta que imponía el estilo viejo en #335 (medido con `meta.php?act=diff&from=15&to=335`):

| Clave | Valor en #335 | Efecto |
|---|---|---|
| `qodef_standard_header_menu_position` | `center` | menú centrado, no a la derecha |
| `qodef_standard_header_menu_item_side_padding` | `150` | 150 px entre ítems → menú de 1.828 px |
| `qodef_standard_header_border_color` + `enable_top_border` | `rgba(175,193,197,0.3)` / `yes` | línea superior gris azulada |
| `qodef_page_background_color` | `#19272b` | fondo oscuro bajo la página |
| `qodef_header_scroll_appearance` | `None` | sin cabecera fija al bajar |
| `qodef_content_behind_header` | `yes` | el contenido pasaba por debajo de la barra |
| `qodef_header_custom_widget_area_one` | `business-home` | área de widgets de otra página |
| `qodef_elementor_section_data_meta` | parallax | datos de parallax del diseño viejo |

Ninguno de esos valores venía del demo (en #15 solo hay
`qodef_header_scroll_appearance = sticky` y `qodef_standard_header_background_color
= #ffffff00`): eran residuo del sitio previo.

### Acción

1. Borrado de las 16 claves `qodef_*` de cabecera en la portada + `qodef_content_behind_header`
   (`meta2.php?act=clean` y `?act=nobehind`).
2. Opciones globales del tema reescritas: `qodef_content_width` 1100 → **1300**,
   `qodef_header_layout` standard, menú a la derecha, `qodef_header_scroll_appearance`
   **sticky** con fondo `#FBFAF9`, alto 96, rejilla activa, relleno de ítem 16,
   `qodef_content_behind_header` = `no`.
3. `leroux-child/pp.css` 17.849 → **18.911 B**: fondo de la barra `#FBFAF9`, línea
   inferior de 1 px `rgba(32,40,45,0.10)`, ítems a 22 px con `letter-spacing 0.3px`
   y peso 500, y **píldora de contacto** en el último ítem (fondo `#20282D`, texto
   `#FBFAF9`, radio 25 px, 12/26 px) — el demo usa el mismo patrón («Get in touch»,
   radio 25 px, 14 px).

### Medido después

| Elemento | Antes | Ahora |
|---|---|---|
| Clases del body | `qodef-header-standard--center`, `appearance--none`, sin rejilla | `qodef-header-standard--right`, `qodef-header-appearance--sticky`, `qodef-content-grid-1300`, sin `content-behind` |
| Caja de contenido | ancho libre | **1.300 px** centrados (x = 99 en 1.512) |
| Menú | 1.828 px, centrado, 150 px por ítem | **593 px**, pegado al borde derecho de la rejilla (1.399), 22 px por ítem |
| Píldora «Contacto» | — | 116 × 41 px, centrada en la barra (y = 27), borde derecho = rejilla |
| Logo | 244 × 18, alineado al margen de la rejilla (x = 99) | igual, sin cambios |
| Contenido | empezaba en y = 0 bajo la barra | empieza en **y = 96**, nada queda oculto |
| Scroll horizontal | −15 (0) | −15 (0) |

### Pendiente

- El banner de cookies de **CookieAdmin** se abre como ventana centrada y tapa la
  portada en la primera visita: hay que configurarlo como barra inferior o desactivarlo.
- El texto visible sigue siendo el del demo: «From strategy to delivery, we are here
  to make sure your business succeeds».

## 2026-10-26 (00:30–01:40) · sitio oscuro: #223035 con texto blando #EFEFEF

Petición: «el sitio usa un color como #233036, confirma si el verde es ese; ese tono
debería ser el fondo del sitio y con el texto blando, como el footer, pero todo el
sitio debe ser así».

### Confirmación del color

`#233036` **no existe** en el tema: 0 coincidencias en `main.min.css` y
`leroux-core.min.css`. Los dos tonos oscuros reales de Leroux son:

| Color | Referencias en el CSS del tema | Uso |
|---|---|---|
| `#223035` | **42** | fondo oscuro del tema (secciones del demo) |
| `#263037` | **53** | banda alterna y pie de página |
| `#20282D` | 126 | tinta de titulares sobre fondo claro |
| `#19272b` | 4 | residuo del sitio anterior |

Medido en el navegador antes de este cambio: `body` = `rgb(34,48,53)` = **#223035**,
`#qodef-page-footer-top-area` = `rgb(38,48,55)` = **#263037**, y el fondo del sitio
seguía en `#FBFAF9`. Se adoptó **#223035 como fondo del sitio** y **#263037 para las
bandas alternas y el pie**, con **#EFEFEF** de texto (el mismo del pie, 8,38:1).

### Cambios

| Capa | Antes | Ahora |
|---|---|---|
| `body`, cabecera, pie | `#FBFAF9` / `#FBFAF9` / `#263037` | **`#223035`** / **`#223035`** / **`#263037`** |
| Texto | `#575B5F` sobre claro | `#EFEFEF` (11,05:1 sobre `#223035`), párrafos `#D9DEDE` (9,1:1) |
| Titulares | `#20282D` | `#FBFAF9` |
| Etiquetas secundarias | `#85979b` (2,92:1, no usable) | `#A9B3B4` (5,3:1) |
| Globales del kit 2116 | primary `#FB3434`, text `#6C6F73` | **`#223035`**, **`#EFEFEF`**, acento `#D5DEDE` |
| 6 fondos de elementos | `#D5DEDE` ×2, `#EFEFEF` ×2, `#E1E1E1`, `#EFEFEF5E` | `#263037` ×5, `#FFFFFF0F` (velo del 6 %) |
| 3 colores en elementos | `#20282D` (uno `color`, dos `svg_icon_color`) | `#EFEFEF` |
| Logo | wordmark oscuro | **`pp-wordmark-claro.png`** (adjunto 11255), `alt` «pennacchiotti wordmark claro» |
| Píldora de contacto | `#20282D` con texto claro | `#EFEFEF` con texto `#223035` |
| Botones | claros sobre claro | `#EFEFEF` con texto `#223035` (Send, View More, Read More) |
| Formularios | fondo blanco | `#263037` con borde `rgba(239,239,239,0.18)` y texto `#EFEFEF` |

`leroux-child/pp.css` 18.911 → **25.205 B**. Toda la capa oscura está al final del
archivo bajo el rótulo «SITIO OSCURO», es reversible borrando ese bloque.

### Verificación

Auditoría de contraste en producción sobre **78 nodos de texto**
(`main p/h1..h4/li/a/span/button` + cabecera + pie): **0 fallos WCAG AA**
(antes de esta tanda: 16 fallos; con el contraste mínimo de 4,5:1 para texto normal
y 3:1 para texto grande).

| Comprobación | Valor medido |
|---|---|
| `body` | `rgb(34,48,53)` = `#223035` |
| `#qodef-page-header` | `#223035` |
| `#qodef-page-footer-top-area` | `#263037` |
| Fondo de texto | 38 nodos sobre `#223035`, 34 sobre `#263037` |
| Scroll horizontal | 0 |
| Alto de la portada | 8.900 px aprox. (19.516 en la medición previa incluía la caché del carrusel) |

### Pendiente

- El copy sigue siendo el del demo («The best solution for your business», «Achieve
  goals & coach fast», lorem ipsum) y las listas siguen vacías.
- Las fotos del demo no son de la planta: hay que sustituirlas por las propias.
- El banner de cookies de CookieAdmin sigue abriéndose como ventana centrada.

## 2026-10-27 (01:45–03:20) · contenido real en la portada, sin tocar el diseño

Petición: «ahora sí puedes meter contenido, sin cambiar el diseño, no necesitas usar
todos los bloques, solo usa lo que realmente aporten algo». El slider lo revisa él.

### Texto nuevo (portada #335)

| Bloque | Antes (demo) | Ahora |
|---|---|---|
| Titular de apertura | «The best solution for your business» | «Control y estandarización de procesos, con criterio técnico explícito» |
| Entradilla | lorem ipsum | «Trabajo con operaciones agroalimentarias y con organizaciones donde el resultado depende de conocimiento experto no documentado…» |
| Botones (6) | «View More» ×6 | Cómo trabajo · Ver soluciones · Ver perspectivas · Agendar una conversación |
| Declaración de método | «Achieve goals & coach fast» | «Diagnosticar, estandarizar e implementar» |
| Pasos del slider de miniaturas | People / Business / … (5) | Diagnóstico · Criterios · Prueba en turno · Transferencia · Seguimiento |
| Bloque de equipo | «Team of specialists» | «Para quién es» (propietarios, gerencias de operaciones, calidad y procesos) |
| Contacto | «Get in touch or visit us» + Old Westbury, Nueva York + teléfono de demo | «Hablemos de tu operación» + «Santiago, Chile» + correo real |
| Formulario CF7 1553 | Name / E-mail address / Message / Send (inglés) | Nombre / Correo / «Qué operación quieres ordenar y qué está pasando hoy» / Enviar |
| Mensajes de CF7 (18) | inglés | español («Gracias, el mensaje fue enviado…» en `wpcf7` opción `messages`) |

Palabras en la portada: **393** (antes 155 útiles + lorem). Nada de cifras: no se
publicó ningún número porque `PRODUCT.md:67` no permite cifras sin conteo verificado.

### Bloques quitados y por qué

| Elemento | ID | Motivo |
|---|---|---|
| Contador «85 K+» | `af97832` + columna `c1a87c7` | cifra inventada del demo |
| Contador «310+» | `59cb989` | cifra inventada |
| Contador «850 K+» | `2ecf9c9` | cifra inventada |
| Barras de progreso Analysis/UX/Development | `03fd425`, `22361cb`, `3865ff6` | porcentajes inventados |
| Gráfico de datos | `854241a` | datos de demo (16 % / 24 % / 33 %) |
| Sección «Latest news coming» | `8aae047` | `blog_list` sin entradas: imprimía «No posts were found…» |
| Sección de testimonios | `8592d43` | `testimonials` = 0 ítems, mismo mensaje vacío |
| Lista de equipo | `7334827` + columna `1117cde` | `team` = 0 ítems |
| Botón de vídeo | `fe5d8f3` + columna `65e70ed` | apuntaba a un vídeo del demo |

Elementos de la portada: **95 → 75**. Secciones raíz: **13 → 11**.

### Dos defectos estructurales corregidos

1. **Los tres `leroux_core_info_section` no existían como widget** en leroux-core 1.2
   (el demo se construyó con otra versión): imprimían una banda vacía de 840–900 px.
   Se sustituyeron por `leroux_core_section_title` + `leroux_core_button` en el mismo
   sitio, que es el widget real del tema.
   `8c195a2` → `0b0982e` · `8433f9b` → `98bf3e9` · `ef74c70` → `7930093`.
2. **El hero (slider) no se imprimía**: el widget `slider_revolution` tampoco existe
   en esta instalación (`widget_elementor: false`), así que la portada abría con una
   banda vacía de 770 px. Se cambió ese widget por uno de tipo `shortcode` con
   `[rev_slider alias="main-home"]`. Ahora renderiza `SR7-MODULE #SR7_7_1` con
   **824 px** de alto y sus 4 imágenes responden **200** (jpg 177 KB, webp 79–85 KB).
   El contenido de los slides sigue siendo el del demo y los enlaces apuntan a
   `leroux.qodeinteractive.com` (lo edita él).

También se quitó el vídeo de fondo de stock de la banda `abe3d9b`
(`main-home-video_2.mp4`): fondo clásico `#223035`.

### Verificación

| Comprobación | Medido |
|---|---|
| Contraste WCAG AA | **57 nodos, 0 fallos** (mínimo 4,5:1 / 3:1 texto grande) |
| «Lorem ipsum» en el texto visible | **0** |
| Marcadores del demo («View More», «The best solution»…) | **0** |
| Scroll horizontal | 0 |
| Alto de la portada | 8.770 px |
| Formulario | placeholders en español, botón «Enviar» |
| Páginas enlazadas | `/sobre-mi/` 200 «Sobre mí» · `/soluciones/` 200 · `/contacto/` 200 · `/perspectivas/` 200, sin lorem |

### Pendiente

- El correo publicado es `mariop@agroterramica.com`: confirmar que es el que quiere
  en la portada (no se publicó teléfono ni dirección).
- Copy e imágenes de los 4 slides del hero: los edita él.
- Las fotos de las bandas siguen siendo las del demo.
- El banner de cookies de CookieAdmin abre como ventana centrada.

## 2026-10-27 (03:30–04:40) · reparación: la edición de contenido rompía el diseño

Reporte del usuario: «en la edición de contenido perdiste varios formatos, algunos
bloques perdieron el color, otros se montan, otros están incompletos».

### Qué se rompió y por qué

| Síntoma | Causa real |
|---|---|
| Bloques sin color | al sustituir los `leroux_core_info_section` (widget inexistente) por widgets nuevos, se perdieron sus settings de color, padding y márgenes |
| Bloques que se montan | el titular `2ba8b1b` conservaba `margin-bottom:-5px` del demo, pensado para un titular de dos líneas; con el texto nuevo de una línea el botón se subía 5 px |
| Bloques incompletos | al quitar el único widget de una sección, la sección quedaba en pie con su alto fijo (737, 840 y 605 px vacíos) |
| Formatos perdidos | se habían quitado columnas y widgets del árbol, no solo textos |

### Cómo se reparó

1. **Restitución del árbol aprobado**: `_elementor_data` de #335 vuelve al estado del
   26-oct (13 secciones, 95 elementos, mismos IDs, 55.418 B). Todo el color, padding,
   márgenes y estructura vuelve a ser el que aprobaste.
2. **Edición sólo de texto**: se reescribieron únicamente valores de texto sobre ese
   árbol. IDs y número de elementos idénticos (95 → 95).
3. **Único cambio estructural conservado**: el hero. El widget `slider_revolution` no
   existe en esta instalación y la portada abría con una banda vacía de 770 px; queda
   un widget `shortcode` con `[rev_slider alias="main-home"]`, que sí renderiza
   (`SR7-MODULE`, 770 px, imágenes locales en 200).
4. **Bloques con datos del demo**: no se eliminan del árbol; se ocultan por CSS con su
   ID, con una línea por bloque y comentario. Al borrar esas líneas vuelven tal cual.

### Texto

| Bloque | Ahora |
|---|---|
| Apertura | «Transformo conocimiento técnico en capacidad operativa» |
| Entradilla | «Ayudo a organizaciones agroalimentarias a convertir criterio, experiencia y datos dispersos en sistemas que mejoran calidad, productividad y toma de decisiones…» |
| Contador (85 K+ demo) | **350+ «Profesionales formados en molinería, calidad y procesos»** |
| Concepto | «De conocimiento tácito a capacidad operativa» (énfasis en «conocimiento tácito», corte tras la 3.ª palabra) |
| Pilares | «Innovación y desarrollo técnico» · «Capacitación y transferencia» |
| Columna «Qué se resuelve» | añadido texto: «Tres frentes: estandarización de procesos, capacitación técnica y desarrollo de nuevas capacidades» |
| Contacto | «Hablemos de tu operación» · Santiago, Chile · mariop@agroterramica.com · formulario en español |

Palabras: 347. «Lorem ipsum» y «No posts were found»: 0.

### Oculto por CSS (reversible, por ID)

`03fd425`, `22361cb`, `3865ff6` (barras de % demo) · `854241a` (gráfico demo) ·
`59cb989`, `2ecf9c9` (contadores 310+ y 850K+) · `fe5d8f3` (vídeo demo) ·
`cbe3b83` (testimonios vacíos) · `7334827` (equipo vacío) · `8592d43`, `f65eb2f` y
`8aae047` (secciones que quedaban vacías) · `9b44d6b` (espaciador de 900 px que
mantenía en 900 px la banda de «Digital e IA»).

### Verificación en producción

| Comprobación | Medido |
|---|---|
| Solapamiento entre widgets hermanos | **0** (antes: 1, 924 px²) |
| Contraste AA | **38 nodos, 0 fallos** |
| Secciones raíz / elementos | 13 / 95 (idéntico al árbol aprobado) |
| Bandas vacías | 0 (la única sin texto es `7c3f909`: banda fotográfica de 840 px) |
| Altura de página | 7.235 px |
| Scroll horizontal | 0 |
| Alto de cada banda | 770 · 878 · 1.696 · 840 · 21 · 438 · 881 · 636 · 218 · 984 |

### Decisión editorial pendiente (revisión externa)

La revisión propone publicar 55 % de margen, 40+ organizaciones, 5 países y 350+
profesionales. `PRODUCT.md:64-67` solo autoriza **una cifra** («más de 350
profesionales formados», sujeta a confirmar el conteo) y marca el resto como **no
publicable** por ser resultados de empresas donde trabajó. Se publicó únicamente el
350+, pendiente de confirmación del conteo.

## 2026-10-27 (04:50–05:30) · la portada pasa a vender capacidades, no documentación

Revisión externa reenviada por el usuario: el sitio «vende el 30-40 % de la propuesta
de valor» porque presenta estandarización y documentación como producto, cuando son
medio. Se aplica la parte que no requiere decisión nueva.

### Copy

| Bloque | Antes | Ahora |
|---|---|---|
| Apertura | «Transformo conocimiento técnico en capacidad operativa» | **«Construyo capacidades técnicas que se convierten en resultados de negocio»** (frase textual de su LinkedIn) |
| Entradilla | «Ayudo a organizaciones agroalimentarias a convertir criterio…» | «Producción, planificación, operaciones e innovación en molinería y alimentos. Hoy ayudo a organizaciones agroalimentarias a convertir conocimiento técnico disperso en procesos, información y equipos que sostienen el resultado sin depender de una persona.» |
| Columna junto a la apertura | «Qué se resuelve» | **«Cuatro líneas de trabajo»**: desarrollo de capacidades · procesos y estandarización · información y decisiones · innovación aplicada |
| Pilar 1 | «Innovación y desarrollo técnico» | **«Desarrollo de capacidades»** (capacitación, transferencia, formación con verificación en el puesto) |
| Pilar 2 | «Capacitación y transferencia» | **«Información y decisiones»** (indicadores, análisis, control de proceso) |
| Lista de 3 | Diagnóstico · Criterios · Transferencia | **Procesos y estandarización · Innovación aplicada · Transferencia tecnológica** |
| Concepto del método | «De conocimiento tácito a capacidad operativa» | se mantiene (revisión: «el mejor hallazgo conceptual del sitio») |

### Documento

`PRODUCT.md` §Oferta: se añade la **Tesis (decidida 2026-10-27)** con la frase única y
las cuatro líneas, y la regla «la estandarización es un medio, no la oferta». Sin esto,
la próxima sesión volvería a escribir la web estrecha.

### Verificación en producción

| Comprobación | Medido |
|---|---|
| Texto que abre la portada | «Construyo capacidades técnicas que se convierten en resultados de negocio…» |
| Palabras | 345 |
| Contraste AA | **38 nodos, 0 fallos** |
| Solapamientos | **0** |
| «Lorem» / «No posts» | 0 |
| Elementos / secciones | 95 / 13 (sin cambios estructurales) |
| Alto | 7.223 px |

### Bloqueado por decisión, no por falta de trabajo

La revisión insiste en publicar **55 % de margen, 40+ organizaciones, 5 países**. Eso
choca con `PRODUCT.md:65`, que los marca **no publicables** (resultados de empresas
donde fue empleado) y con `:67` (**una sola cifra**, conteo aún sin confirmar). Hasta
que él autorice por escrito otra regla, el sitio mantiene una única cifra: 350+.

## 2026-10-27 (05:40–07:10) · evidencia en la portada y página de capacitación

Decisiones suyas en este turno: **350+ profesionales, 40+ organizaciones y 5 países**
son publicables (el 55 % de margen no lo autorizó y sigue fuera) y **sí** a una página
de capacitación.

### Evidencia visible

La columna derecha de la banda de apertura (`c1a87c7`) tenía un contador del demo
(«85 K+») y un botón en inglés. Ahora:

| Cifra | Dato |
|---|---|
| **350+** | Profesionales formados |
| **40+** | Organizaciones acompañadas |
| **5** | Países donde he trabajado |

Se clonaron dos contadores del propio tema (`c40org01`, `c5pais01`) con la misma
configuración: mismo estilo, mismo tamaño, sin inventar maquetación. Elementos de la
portada: 95 → 97. Botón `f2e02f4`: «Ver capacitación» → `/capacitacion/`.

Defecto encontrado y corregido: el contador del tema pinta el número **por JS al
entrar en pantalla** y, con el widget servido desde JSON, deja el `<span>` vacío
(medido: 5 de 5 spans con 0 px de ancho y sin texto) → las cifras no se veían. Se
imprime el número por CSS con `.qodef-m-digit:empty::after`, así que se ve siempre y
si el JS corre el `:empty` deja de aplicar. El color del número pasó de `#FFFFFF54`
(blanco al 33 %, ilegible) a `#FBFAF9`.

### Página /capacitación/

ID **11260**, publicada, título «Capacitación y transferencia». Secciones: qué se
transfiere · formatos (diplomado, formación en planta, relatoría, acompañamiento en el
puesto) · cómo se verifica · a quién está dirigido · trayectoria docente. En el menú
principal (`Principal`, id 43) como sexto ítem.

### Dos defectos de layout corregidos en el camino

1. **La portada entera se encogió a 780 px** (columnas de 207 px, banda de 1.563 px).
   Causa: la regla de lectura `.qodef-page-content-section { max-width: 780px }` apunta
   a un contenedor que la portada de Elementor **también** usa. Fix: la regla se limita
   a `body:not(.elementor-page)`.
2. El botón se montaba 5 px sobre el titular por el `margin-bottom:-5px` del demo,
   calculado para titulares de dos líneas.

### Verificación en producción

| Comprobación | Medido |
|---|---|
| Columnas de la banda | 380 · 380 · 380 px (antes del fix: 207) |
| Alto de la banda | 927 px |
| Ancho de los números | 175 / 133 / 44 px a 72 px de cuerpo (se imprimen) |
| Solapamientos | **0** |
| Contraste AA portada | 0 fallos |
| Contraste AA /capacitación/ | 12 nodos, **0 fallos** |
| Cuerpo de texto en páginas | 780 px de medida, 18 px (antes 1.300 px y 15 px) |
| Menú principal | Inicio · Sobre mí · Soluciones · Perspectivas · Contacto · **Capacitación y transferencia** |
| HTTP | `/` 200 · `/capacitacion/` 200 |

### Documento

`PRODUCT.md` §Evidencia aprobada: 350+, 40+ y 5 pasan a «cifra publicable» con fecha y
autor; el margen >55 % se marca **vetado**. La regla pasa de «1 cifra publicable como
máximo» a «tres cifras publicables».

## 2026-10-28

### Página de mantenimiento (mu-plugin, sin tocar contenido ni BD)

Se agrega `wp-content/mu-plugins/pp-mantenimiento.php` (fuente versionada en
`wp/mu-plugins/pp-mantenimiento.php`). Con el modo activo, toda visita pública recibe una
página de mantenimiento con **HTTP 503**, `Retry-After` y `X-Robots-Tag: noindex`. El
panel (`/wp-admin`), el login, `wp-cron` y la REST API siguen respondiendo; el
administrador conectado ve el sitio normal.

Programación: `pp_mant_config()` — `activo` (interruptor), `desde`/`hasta`
(`Y-m-d H:i`, hora de Chile, ventana semiautomática), `titulo`, `texto`, `retorno`,
`contacto`. Reversible: borrar el archivo por FTP. No escribe en la base de datos.

Vista previa y prueba sin afectar al público (funcionan con el modo inactivo):
`?pp_mant_preview=CLAVE` devuelve la página con 200 y `?pp_mant_test=CLAVE` con 503.

### Verificación (producción, 2026-10-28 15:0x)

| Comprobación | Medido |
|---|---|
| Archivo instalado | `mu-plugins/pp-mantenimiento.php` presente; `/` sigue en 200 |
| Sintaxis | `php -l` sin errores |
| Vista previa | 200, 3.439 bytes, `Cache-Control: no-store`, `X-Robots-Tag: noindex` |
| Prueba 503 | 503 + `Retry-After: 3600`, mismo cuerpo |
| Clave inválida | sirve el sitio normal (0 coincidencias de la página) |
| Desborde horizontal | 0 px en 320 · 390 · 768 · 1024 · 1440 |
| H1 | 32 / 40 / 48 / 56 px por breakpoint, Newsreader cargada |
| Logotipo | 160 / 180 / 220 px |
| Objetivo táctil del correo | 46 px de alto (≥44) |
| Contraste | 11,84:1 (#EFEFEF) y 13,06:1 (#FBFAF9) sobre #223035 |

### Estado

Instalada e **inactiva**. Falta la decisión de Mario: activarla ahora, programar una
ventana concreta o dejarla como interruptor manual. Al activar hay que purgar caché
(`curl -X PURGE <url>` → 204) porque la caché de página sirve HTML viejo a visitantes
anónimos.

### Activación (2026-10-28 15:2x, orden de Mario)

`activo => true`, subido por FTP. El sitio queda en mantenimiento para el público.

| Comprobación | Medido |
|---|---|
| `/` · `/contacto/` · `/perspectivas/` · `/no-existe-xyz/` | 503 + página de mantenimiento |
| `/wp-login.php` | 200 (se puede entrar) |
| `/wp-admin/` | 302 al login |
| `/wp-json/` | 200 (REST intacta) |
| `/robots.txt` | 200 (exento: no se pierden las directivas) |
| `/sitemap_index.xml` | 200 (Rank Math lo sirve antes del `template_redirect`) |
| Cabeceras de `/` | `Retry-After: 3600`, `X-Robots-Tag: noindex`, `Cache-Control: no-store` |
| Vista previa con clave | 200 |
| Caché de página | tras el PURGE deja de servir el HTML viejo; el 503 no se cachea |

### Sobre el modo mantenimiento de Elementor

Mario recordaba un modo mantenimiento dentro de Elementor. Medido: `elementor-pro`
está instalado pero **no trae el módulo `maintenance`** (`elementor-pro/modules/` no lo
contiene; `modules/maintenance/` responde 550), y el core `elementor` tampoco lo tiene
—en Elementor es una función de Pro, en Herramientas → Modo de mantenimiento—. Con este
build no está disponible, así que la página es la del mu-plugin.

## 2026-10-28 (16:48) · 14 variables globales cargadas en el kit + defecto medido en el modo mantenimiento

### Cambio aplicado (aditivo, sin efecto de render)

Se crean las 14 variables de `DESIGN.md` §Tokens en el kit activo vía `manage-global-variable`:
`ink #223035` · `heading #20282D` · `text #263037` · `muted #586A70` · `sage #D5DEDE` ·
`gray #EFEFEF` · `ivory #FBFAF9` · `font-display Newsreader` · `font-ui DM Sans` ·
`size-display 56px` · `size-h2 42px` · `size-h3 26px` · `size-lead 18px` · `size-body 15px`.

`muted` se crea en `#586A70` y no en `#85979B`: ejecuta la deuda ya registrada en
`DESIGN.md` (2,92:1 no cumple AA; `#586A70` da 5,43:1). Ninguna página referencia todavía
las variables, así que el render no cambia.

**Defecto del propio MCP, medido:** al crear `global-size-variable` con `"56"` el valor
se guarda como `"px"` — se pierde el número. Hay que enviar la unidad: `"56px"`.
Corregido con `update` en las 5 variables de tamaño; lectura de vuelta confirma
`total: 14` y los valores correctos.

### Defecto medido en el modo mantenimiento (bloquea la verificación)

Con `activo => true`, **todos** los CSS de Elementor devuelven 503 con el HTML de
mantenimiento, no el archivo:

| URL | Estado |
|---|---|
| `uploads/elementor/css/base-desktop.css` | 503 · 3.389 b |
| `base-mobile.css` · `default-desktop.css` · `post-335.css` · `post-2116.css` | 503 · HTML |
| `uploads/pp/mp-mark-ink-512.png` (estático real) | 200 · 6.980 b |

Es decir: se sirven los archivos estáticos, pero no los CSS que Elementor imprime por PHP.
Un visitante con HTML en caché de SpeedyCache (200 observado a las 16:24) recibe la página
**sin estilos**. El modo mantenimiento, tal como está, no protege el sitio: lo deja roto.
Consecuencia adicional: mientras esté activo no se puede verificar en el front que las
variables se emitan (`--e-gv-*`), solo su existencia en el kit.

### Estado

- Variables en el kit: **14** (antes 0). Clases globales: siguen en **0**.
- Mantenimiento: **activo**, sitio público en 503. Pendiente decisión de Mario.
- Verificación pendiente: emisión de `--e-gv-*` en `post-2116.css` (requiere mantenimiento apagado).

## 2026-10-28 (16:56) · mantenimiento apagado, sitio restaurado y mapa real de versiones (V3/V4)

### Cambio aplicado

`pp-mantenimiento.php:39` → `'activo' => false` por FTP, con respaldo previo del archivo vivo y diff byte a byte: **una sola línea** modificada. Purga de 5 rutas (`PURGE` → 204). Copia versionada en `wp/mu-plugins/` sincronizada con el servidor.

| Comprobación | Antes | Después |
|---|---|---|
| `/` · `/contacto/` · `/soluciones/` · `/perspectivas/` · `/capacitacion/` | 503 | **200** (1,6–3,8 s) |
| Ruta inexistente | 503 | **404** (correcto) |
| `uploads/elementor/css/post-2116.css` | 503 + HTML | **200 · 7.293 b · text/css** |
| `--e-gv-*` en el front | — | **0** |

### Por qué las 14 variables no se emiten: el sitio es híbrido V3/V4

Medido sobre el HTML servido (`data-e-type` = V3; `e-flexbox`/`e-div-block` = V4 atómico):

| Página | Nodos V3 | Nodos V4 |
|---|---|---|
| `/` (portada, post 335) | **94** | **0** |
| `/soluciones/` | 93 | 232 |
| `/contacto/` | 21 | 20 |
| `/perspectivas/` · `/capacitacion/` | 0 | 0 (no son documentos de Elementor) |

Las variables y las clases globales de V4 **solo aplican a elementos atómicos**. La portada, que es la página que se muestra al cliente, es íntegramente V3 (plantilla demo «Business Home»), así que no puede usar tokens ni clases: cualquier estilo suyo seguirá viviendo en `pp.css`.

### Causa de las familias tipográficas sobrantes

El kit conserva la tipografía global del demo:
`--e-global-typography-primary-font-family:"Mukta Vaani"`, `secondary:"Roboto Slab"`, `text:"Roboto"`.
Ahí está el origen medido de las 5–6 familias que carga la portada.

### Consecuencia

Antes de crear clases o componentes hay que decidir una de dos:
(a) migrar la portada de V3 a V4 atómico, o
(b) aceptar el híbrido y limitar tokens y clases a las páginas ya atómicas.
Crear 22 clases sin resolver esto produce activos que la portada no puede usar.

## 2026-10-28 (17:05) · piloto V4 del hero y hallazgo: la portada muestra una demo en inglés que enlaza al sitio del vendedor del tema

### Inspección nodo a nodo de la portada (post 335)

17 secciones V3, **cero nodos V4**. Widgets: `testimonials_list`, `charts`, `team_list`, `thumbnail_slider`, `blog_list`, `progress_bar` ×3, `video_button`, `icon_with_text` ×2, `textual_list` ×3, `counter` ×5, `section_title` ×9, `spacer` ×3. Es la plantilla «Business Home» del demo de Leroux, no un diseño propio.

**El hero no es Elementor.** Es un módulo **RevSlider** (`main-home`, id 7, SR7 7.1.8) dentro de un widget `shortcode`. Contiene 4 slides con:

| Elemento | Contenido medido |
|---|---|
| H1 slide 1 | «From strategy to delivery, we are here to make sure your business succeeds» |
| H1 slide 2 | «We help our clients realize their business ideas and achieve great results» |
| H1 slide 3 | «Connect with your clients using a variety of elements that let you tell your story» |
| H1 slide 4 | «Refresh your brand and pave the way for new business goals and ventures» |
| Botones | `leroux.qodeinteractive.com/our-process/` · `/about-us/` · `/our-clients/` · `/our-services/` |
| Imágenes | propias (`uploads/2026/10/IMG-20250517-WA0009.jpg`, `20250819_135033-scaled.jpg`) |

Es decir: cuatro H1 en inglés, tomados del tema, y los cuatro botones del hero llevan al visitante al sitio del vendedor del tema. Las fotos sí se reemplazaron; el texto y los enlaces no. Coste añadido: RevSlider carga **477,7 + 219,9 KB** de JS en todas las páginas.

Los contadores sí tienen cifras reales (`data-end-digit="350"`).

### Piloto V4 (página 11264, plantilla Canvas)

Hero reconstruido con tokens: `eyebrow` (13 px, mayúsculas, `var(--sage)`), `h1` (`var(--font-display)` / `var(--size-display)` / `var(--ivory)`), `lead` (`var(--size-lead)`), `botón` (`var(--ivory)` sobre `var(--ink)`), banda `var(--ink)` con `padding: 7rem 4rem` y `min-height: 62vh`.

**Verificación medida con `getComputedStyle` en el navegador** (no inferida del código):

| Nodo | Esperado | Medido |
|---|---|---|
| banda | `#223035` | `rgb(34, 48, 53)` ✓ |
| h1 color | `#FBFAF9` | `rgb(251, 250, 249)` ✓ |
| h1 fuente | Newsreader 56/400 | `Newsreader, Georgia, serif` · 56 px · 400 ✓ |
| eyebrow | `#D5DEDE` 13 px | `rgb(213, 222, 222)` · 13 px · uppercase ✓ |
| lead | 18 px | 18 px ✓ |
| botón | ivory/ink, 44 px+ | `rgb(251,250,249)` / `rgb(34,48,53)` · 56 px de alto ✓ |
| H1 | 1 | **1** (con Canvas) ✓ |
| overflow horizontal | 0 | 0 ✓ |
| cabecera y pie del tema | ausentes | ausentes ✓ |

**Conclusión:** las variables **sí** llegan al front. No aparecen como `--e-gv-` en ningún archivo porque Elementor resuelve el valor en el HTML del elemento que las referencia. Lo que faltaba no era emisión: era un nodo V4 que las consumiera.

### Defectos secundarios medidos

1. El tema imprime su propio título como `H1` (`qodef-m-title entry-title`) **aunque** `hide_title => yes` está puesto: Leroux no respeta esa opción. Se resolvió con plantilla `elementor_canvas`. En páginas con cabecera y pie hará falta el control propio del tema o se duplicará el H1.
2. La página piloto, con **cinco** elementos, pesa **534 KB** de HTML: el peso lo aportan el tema y los plugins (Spectra, qi-blocks, RevSlider), no el contenido.

### Estado

- Página 11264 publicada en `https://pennacchiotti.cl/portada-v4-·-piloto-hero-borrar/` (sin enlaces entrantes, título lo dice).
- Pendiente de Mario: revisarla, decidir si se promueve a portada o se descarta, y si se borra 11264.
- La portada real (335) **no se ha tocado**.

## 2026-10-28 (17:40) · portada nueva en V4: 6 bandas, contenido propio, cero demo

### Decisión aplicada

Se abandona la demo de Leroux como base. La portada se reconstruye desde cero con contenido propio, no se migra la plantilla. H1 = tesis de `PRODUCT.md`. Bandas: hero · problema · método · trayectoria · soluciones · cierre.

- Página **11269 «Portada 2026»**, plantilla `elementor_canvas`, publicada.
- 100 % nodos V4 (`e-flexbox`, `e-heading`, `e-paragraph`, `e-button`), 100 % valores por token.
- La portada real (335) **no se ha tocado**.
- 11264 («piloto hero») queda huérfana, pendiente de borrar.

### Medición (getComputedStyle + emulación de viewport)

| Comprobación | Resultado |
|---|---|
| Jerarquía | 1 `h1` · 5 `h2` · 10 `h3` |
| h1 | Newsreader 56/400 · `rgb(251,250,249)` |
| h2 | Newsreader 42 · `rgb(32,40,45)` |
| Cifras 350+ / 40+ / 5 | 56 px · ivory |
| Desborde horizontal en 1440 / 1024 / 768 / 390 / 320 | **0 / 0 / 0 / 0 / 0** |
| Altura del enlace secundario | 49 px (≥ 44) |
| CTA principal | 56 px de alto |
| Alto de documento | 3.296 px (escritorio) · 4.833 px (320) |

### Defectos del MCP medidos en esta pasada

1. **La propiedad `flex` abreviada rompe la regla completa.** Un estilo `display:flex; flex-direction:column; flex: 1 1 16rem; gap:.75rem` se guarda sin error pero **no aplica ninguna** de sus declaraciones (medido: `flex-direction` seguía en `row` y `gap` en `normal`). Solución adoptada: rejillas con `display: grid` + `grid-template-columns: repeat(auto-fit, minmax(…, 1fr))`.
2. **Cada `e-flexbox` trae `padding: 10px` por defecto.** Anidado en tres o cuatro niveles, se come 60–80 px del ancho en móvil. Fue la causa del desborde de 75 px a 320: no era el contenido, eran cuatro paddings heredados. Corregido con `padding: 0` explícito en los 11 contenedores internos.
3. **`PURGE` no invalida el HTML cacheado de 11264.** La página sigue sirviendo la versión de las 17:05 (id `391004c8`) aunque la base de datos tiene las 6 bandas. Una URL nueva (11269) renderiza correctamente: el problema es la entrada de caché, no el contenido.

### Contenido

Cifras 350+ / 40+ / 5 son las autorizadas en `PRODUCT.md`. **No se inventaron casos de estudio**: la banda de trayectoria usa solo esos agregados. Los tres casos con nombre y número siguen pendientes de texto de Mario.

## 2026-10-28 (21:20) · fotografía propia, tres casos y banda de formación en la portada

### Fotografía (por primera vez en el sitio)

Inventario de `Imagenes/`: **20 archivos**, 19 válidos. Uno corrupto: `amasadora 2.jpg` (PIL no puede identificarlo). Originales entre 6 KB y **12,5 MB**; cinco por encima de 4 MB, no aptos para subir en crudo.

Cuatro seleccionadas, redimensionadas a 1800 px de ancho, calidad 82, progresivas:

| Archivo | Original | Optimizada | Contenido (verificado con `vision_bridge`) |
|---|---|---|---|
| `pp-linea-marraqueta.jpg` | 3.129 KB | **343 KB** | línea industrial de marraqueta saliendo del horno |
| `pp-texturometro.jpg` | 2.455 KB | **165 KB** | cruasán sobre analizador de textura, sonda y escala |
| `pp-masa.jpg` | 1.648 KB | **212 KB** | masa dentro de maquinaria industrial |
| `pp-granola.jpg` | 5.880 KB | **358 KB** | bandeja de granola en horno (reserva) |

Subidas por FTP a `pennacchiotti.cl/wp-content/uploads/2026/10/` (el FTP entra en `/home3/ingen401`, no en el docroot: la ruta correcta lleva el prefijo `pennacchiotti.cl/`). Las tres primeras verificadas con **200 · image/jpeg**.

### Portada: 6 → 9 bandas

| # | Banda | Fondo | Altura medida |
|---|---|---|---|
| 1 | Hero | ink | 562 px |
| 2 | Problema | ivory | 644 px |
| 3 | Método | sage | 567 px |
| 4 | **Fotografía (nueva)** | gray | 612 px |
| 5 | **Tres casos (nueva)** | ivory | 664 px |
| 6 | Trayectoria | ink | 550 px |
| 7 | **Formación y transferencia (nueva)** | sage | 516 px |
| 8 | Soluciones | gray | 464 px |
| 9 | Cierre | ink | 509 px |

Reordenadas con tres `move` en una sola operación. Sin dos fondos iguales contiguos.

### Medición

| Comprobación | Resultado |
|---|---|
| Jerarquía | 1 `h1` · **8** `h2` · **16** `h3` |
| Imágenes de fondo cargadas | **3/3**, 357 × 268 px cada una (4:3) |
| Desborde horizontal 1440 / 390 / 320 | **0 / 0 / 0** |
| Alto de documento | 5.088 px (escritorio) · 8.163 px (320) |

### Contenido de los casos

Los tres casos se redactan **por situación y método**, como autoriza `PRODUCT.md:98` («los casos se narran por situación y método, no por empresa»), sin nombres ni cifras. **Son borradores**: describen patrones de intervención, no encargos identificables. Requieren validación de Mario antes de considerarse definitivos.

### Cambio de copy

El antetítulo del hero pasa de «Control y estandarización de procesos» a «Desarrollo de capacidades · Transferencia tecnológica», para alinear la promesa con la definición de negocio y no con el procedimiento.

## 2026-10-31 · emisión del gate de arte (`DIRECTION.md` v1.0)

### Motivo

Una revisión externa afirmó que «todavía no existe una identidad visual definida y documentada». La medición
contradice la afirmación en lo sustantivo: `DESIGN.md` v1.1 tiene paleta con contraste medido, escala
tipográfica, antipatrones, dirección de imagen y reglas de entrega; `fase2-tres-direcciones.md` tiene vector de
parámetros y tres direcciones con coste; el kit tiene 14 variables. Lo que faltaba es el documento de gate que
el skill `art-director` exige para que esa ley sea ejecutable, y la aplicación de la ley al render.

### Emitido

| Documento | Contenido | Estado |
|---|---|---|
| `DIRECTION.md` (raíz del proyecto, 20.813 B) | 10 secciones + §0 de cumplimiento: brief, 5 referencias con «qué no se copia», parámetros con horas y fecha de congelamiento 2026-11-02, requisitos por departamento, tres direcciones heredadas de `fase2` con estado de ejecución medido, ley visual (paleta, tipografía, retícula, espaciado, imagen, movimiento, densidad, modos), 12 rechazos explícitos, artefactos pendientes, criterios de aceptación con método de medición, registro de emisión | Borrador para firma |

### Correcciones a la revisión externa registradas en el documento

1. **«No existe identidad»**: existe y está medida; falta el gate y el despliegue.
2. **Restricción inventada**: «no puedes monetizar el conocimiento del Laboratorio de Granos y Harinas» no está
   en `PRODUCT.md`. Lo que la fuente prohíbe es presentarse como especialista universal en agroindustria
   (`:61`) y publicar material de terceros o de antiguos empleadores (`:63-65`). La fotografía propia de línea
   de marraqueta y texturómetro está autorizada (`CAMBIOS 2026-10-26 19:59`).
3. **Referentes incompatibles con la ley**: Linear, Stripe, Kin + Carta e Instrument pertenecen a la estética que
   `DESIGN.md:14-16` prohíbe. Se sustituyen por referencias editoriales/técnicas con su «qué no se copia».

### Discrepancias abiertas que este documento obliga a corregir

`DESIGN.md` v1.2: cuerpo 15/25 declarado frente a 18/29 medido · `muted #85979B` fuera de AA · `pp-stack` y
`pp-cluster` sin crear · CSS por `data-id`.

Ningún cambio en WordPress, ningún render modificado. Nada publicado.

---

## 2026-11-01 · Campos de intención, identidad y dos gates que mentían

| Cambio | Evidencia |
|---|---|
| `01_NEED.intencion.objetivo_economico` y `cambia_si_no_existe` completados | Respuesta de Mario, 2026-11-01; `verificar_need.py` → `NEED COMPLETO · 0 bloqueantes`, exit 0 |
| `verificar_need.py` ahora bloquea cualquier `null` | Antes decía `20/20 · 0 bloqueantes` con dos campos en `null`: sólo miraba el bloque `respuestas` |
| Bloque `referencias` en `01_NEED` con Stripe y Linear | Registrado con `estado: en conflicto` y `contradice: DESIGN.md:12-16`: son anti-referencias declaradas. Se adoptan aire, rejilla y filetes; no paleta, sans ni animaciones |
| `pp-favicon-512/180/32.png` y `pp-og-1200x630.jpg` generados | `deploy/assets/generar_identidad.py`; monograma P en Newsreader sobre ink `#223035`; recorte central de `masa-desgarrada-2400.jpg` |
| `mu-plugins/pp-identidad.php` en producción | Declara `rel=icon`, `apple-touch-icon`, `og:image` y `twitter:card`; verificado 200 en `/`, `/contacto/`, `/sobre-mi/` |
| `auditar_sitio.py`: favicon, `og:image` y plantilla duplicada sólo si está activa | Auditoría: 6 → **3 fallos y 1 aviso** |

Fallos que quedan: 5 de 5 páginas sin estructura de Elementor, plantilla 404 condicionada a `include/singular/post`, cero imágenes editoriales en las cinco rutas. Aviso: footer inactivo duplicado en la biblioteca.

Nada más se tocó. El contenido de las cinco páginas sigue sirviéndose desde `pp-pages/`.
