# Auditoría de capacidad — Pennacchiotti Web

**Fecha:** 28 de octubre de 2026, 16:24–16:40 (America/Santiago)
**Método:** medición en vivo (curl, MCP de Elementor, MCP de WordPress, sistema de archivos). No hay estimaciones donde dice «medido».
**Alcance:** todo lo que hoy existe para construir sitios: producción, kit de Elementor, biblioteca de medios, documentación, skills y Hermes.

> **Regla de esta auditoría:** un dato sin instrumento se marca `N/A`, no se rellena. Los porcentajes y los puntajes son juicio experto aplicado a datos medidos, y cada uno declara en qué se apoya.

---

## 0. Tres hechos que invalidan el resto del informe si no se corrigen

| # | Hecho medido | Evidencia | Consecuencia |
|---|---|---|---|
| 1 | **El sitio público está en 503.** `activo => true` en `wp/mu-plugins/pp-mantenimiento.php:39`. `/`, `/contacto/`, `/soluciones/` y cualquier ruta devuelven 503; `/wp-login.php` y `/wp-json/` responden 200. El primer `curl` (16:24) devolvió 200 con 649 KB: era **caché**. | `curl -D -` sobre `/` → `HTTP/1.1 503`. `docs/CAMBIOS.md` (última entrada) dice «Instalada e **inactiva**. Falta la decisión de Mario». | La web del estudio no está observable. Cualquier benchmark visual, Lighthouse o CRO sobre el sitio es hoy imposible. |
| 2 | **El design system no está en el kit.** `elementor://global-variables` → `{"variables":{},"total":0}`. `elementor://global-classes` → `{"classes":[]}`. | `docs/DESIGN.md:6` afirma «Verificado contra: kit activo de Elementor V4 (**14 variables, 22 clases globales**)». `docs/SISTEMA-DISENO-CONSTRUCCION-v1.1.md:115` lista 22 clases «registradas». | El sistema vive en documentos y en un `pp.css` de 301 líneas escrito a mano. En la herramienta que produce las páginas: **cero**. Cada página nueva se resuelve improvisando, que es exactamente lo que el sistema existía para evitar. |
| 3 | **No hay una sola métrica de conversión.** Medido en el HTML servido: `googletagmanager` 0 · `gtag(` 0 · `google-analytics` 0 · `clarity` 0 · `hotjar` 0 · `plausible` 0 · `matomo` 0 · `fbq(` 0. | `pp_home.html` (649 KB descargados a las 16:24). | No se puede afirmar nada sobre conversión, ni mejorarla, ni vender CRO. El sitio es un folleto a ciegas. |

---

## FASE 1 · Inventario completo

### 1.1 Plataforma de producción (medido)

| Dato | Valor medido | Instrumento |
|---|---|---|
| WordPress | 7.1.3 | `<meta name="generator">` |
| Elementor | 4.3.5 · Elementor Pro 4.3.0 | meta generator + asset `?ver=` |
| Tema | `leroux` + `leroux-child` | rutas `wp-content/themes/` |
| Plugins con peso en el front | 12: elementor, elementor-pro, leroux-core, qi-addons-for-elementor, qi-blocks, spectra-blocks, revslider, contact-form-7, cookieadmin, cookieadmin-pro, custom-twitter-feeds, instagram-feed | grep sobre el HTML |
| Contenido | 7 páginas · 12 entradas · 332 archivos en medios | `X-WP-Total` de la REST API |
| Servidor | nginx 1.29.8 (HostGator) | cabecera `Server` |
| Caché | SpeedyCache (sirvió HTML viejo con 200 mientras el origen daba 503) | comportamiento observado |

### 1.2 Matriz de aprovechamiento

Nivel de aprovechamiento = uso real medido / capacidad demostrada por la herramienta. Impacto = cuánto mueve la calidad percibida o la capacidad de producir.

| Plataforma | Herramienta | Uso actual | Uso potencial | Aprovechamiento | Impacto |
|---|---|---|---|---|---|
| Elementor V4 | `build-composition` (58 tipos de widget, XML + CSS + clases + interacciones) | Portada y páginas internas armadas a mano, sección por sección | Fábrica de páginas desde contratos: una llamada = una sección completa | **45 %** | Alto |
| Elementor V4 | `manage-global-variable` (tokens) | **0 variables** en el kit | 8–14 tokens de color/tipografía/espaciado que gobiernan todo el sitio | **0 %** | Muy alto |
| Elementor V4 | `manage-classes` | **0 clases** en el kit | Las 22 clases de `pp-*` + `pp-stack`/`pp-cluster` | **0 %** | Muy alto |
| Elementor V4 | `manage-default-styles` (capa por etiqueta) | `h1` con `color:#ffffff; background-color:#233036; display:grid` | Tipografía base del sitio entera declarada una vez | **10 %** | Alto |
| Elementor Pro | `manage-component` (componentes reutilizables, `can_create: true`) | **0 componentes** | 8–10 componentes: hero, intro, problema, evidencia, método, CTA final, ficha, footer | **0 %** | Muy alto |
| Elementor Pro | Site parts / Theme Builder | 29 documentos, **los 29 con `is_active:false`** | Header/footer/404/archive gobernados por plantilla | **0 %** (el tema no llama `elementor_theme_do_location`, documentado en la skill) | Medio |
| Elementor | `create-preview-link` | Sin registro de uso | Bucle de verificación propio antes de publicar | **~20 %** | Alto |
| Elementor | `manage-elements` (edición quirúrgica masiva, 50 ops) | Uso correctivo cuando algo se rompe | Corrección por lote tras cada QA | **50 %** | Medio |
| Medios | Biblioteca (332 archivos) | 22 imágenes en portada; **1 SVG** (`default.svg`); 5 vídeos, **los 5 del demo de Leroux** | Sistema de imágenes propio, iconografía, diagramas | **15 %** | Alto |
| Medios | `/video` del proyecto (8 renders: `pp-hero-flujo`, `pp-hero-linea`, `pp-mascara-*`, 1080p y 9x16 + pósters + máscaras alfa/luma) | **Ninguno está en la biblioteca** (verificado por `list-assets type:video`) | Hero en vídeo real, no stock | **0 %** | Alto |
| Hosting | HostGator cPanel, ea-php83 | Producción de un sitio | Multisitio gestionado, staging por cliente | **10 %** | Alto |
| Rendimiento | 42 CSS/JS = **2.25 MB**; 20 medios = **2.85 MB**; HTML **634 KB**; TTFB **3.05 s**; 44 `<link rel=stylesheet>` | Sin política de peso | Presupuesto por página (< 1.2 MB) y plugin de critical CSS | **10 %** | Muy alto |
| Tipografía | **5 familias** cargadas: DM Sans, Heebo, Mukta Vaani, Roboto, Roboto Slab. **Newsreader no se carga.** | Herencia del demo | 2 familias (Newsreader + DM Sans) según `DESIGN.md` | **20 %** | Alto |
| Analítica | — | **Nada instalado** | GA4 + evento de envío + Search Console | **0 %** | Muy alto |
| SEO | Rank Math / Yoast no aparecen en el front | meta description 1, canonical 1, og:title 1, 1 `ld+json`, 0 `hreflang` | Schema `Organization`/`Service`, sitemap verificado, canibalización | **25 %** | Alto |
| Documentación | 3.599 líneas en `docs/` (PRODUCT 98, DESIGN 223, SISTEMA 343, SEO-CONTRACT 161, contrato contacto 174, checklist 107, CAMBIOS 972) | Se escribe y se actualiza | Base de un método vendible | **70 %** | Muy alto |
| Versiones | **Sin git** (`fatal: not a git repository`) | Copias manuales (`backup-pp-css-20261026.css`) | Repo con `docs/`, `wp/`, contratos y baselines | **10 %** | Alto |
| Skills | 10 skills relevantes: `pennacchiotti-web-design-system` (17.6 KB, 12 patrones, tokens, vetos), `elementor-mcp-design`, `elementor-atomic-mcp`, `elementor-atomic-builder`, `art-director` (10.8 KB), `popular-web-designs` (54 sistemas reales), `design-md`, `claude-design`, `clone-website-to-elementor`, `management-dashboards` | Se cargan cuando se construye | Convertirlas en procedimiento con checklist ejecutable | **60 %** | Alto |
| Hermes | `browser_exec` (DOM, CSS computado, contraseña de contraste, overflow, CLS) | Medición puntual | QA automatizado por breakpoint en cada entrega | **40 %** | Alto |
| Hermes | Ver | **`vision_analyze` devolvió 404** con el modelo actual | Revisión visual humana o modelo con visión | **0 %** | Muy alto |
| Automatizaciones | cron / background | Sin tareas programadas de este proyecto | Backup, purga de caché, informe semanal de leads | **15 %** | Medio |

### 1.3 Lo que no existe y se supone que existe

| Supuesto | Realidad medida |
|---|---|
| «Design system en el kit» | 0 variables, 0 clases |
| «Biblioteca de componentes» | 0 componentes `e-component` |
| «Theme Builder en uso» | 29 site parts, 0 activos |
| «Imágenes propias» | 1 SVG; 5 vídeos de demo; los 8 renders propios, fuera de la biblioteca |
| «El sitio está publicado» | 503 en este momento |
| «Medimos conversión» | 0 herramientas de analítica |

---

## FASE 2 · Capacidad real de agencia

### 2.1 ¿Puede competir con agencias de USD 1.000–5.000? **Sí en ejecución. No como negocio.**

Lo que ya está a nivel de ese tramo:

- Dirección editorial definida y aplicada (papel/tinta, sin degradados ni glassmorphism, anti-referencias explícitas en `DESIGN.md`).
- Contratos antes de construir (`SEO-CONTRACT.md`, `contrato contacto-v2.contract.yaml` con `node_tree`, `cardinality`, `frontend_acceptance`). Eso es más disciplina que la que tiene la mayoría de agencias de ese tramo.
- QA medido: 0 solapamientos, contraste AA verificado, 0 overflow en 6 anchos, baselines de captura.
- Capacidad técnica para armar secciones atómicas por API, con tokens y clases reutilizables.

Lo que lo descalifica hoy en ese tramo:

1. **Sin cartera.** No hay una sola página de caso con cliente, problema, intervención y resultado.
2. **Sin oferta.** `PRODUCT.md` vende consultoría operacional, no sitios web. No hay paquetes, precios, alcance, plazos ni contrato de servicio.
3. **Sin staging.** Se edita en producción; el propio `CAMBIOS.md` registra regresiones en vivo (titulares invisibles, portada encogida a 780 px, Leroux dejó huérfana la capa tipográfica).
4. **Sin medición.** Un cliente de USD 3.000 pide un informe mensual; no hay dato que enviar.
5. **Sin imágenes.** Un sitio de USD 3.000 con fotos de stock o del demo se percibe de USD 800.

**Veredicto:** puede entregar el artefacto de un proyecto de USD 3.000; no puede sostener la relación comercial de uno.

### 2.2 ¿Puede competir con agencias de USD 10.000+? **No.**

Brechas específicas, no genéricas:

| Brecha | Por qué es estructural |
|---|---|
| **Ojo humano sobre el resultado** | No hay revisión visual profesional en el bucle. `vision_analyze` falló; el único juez estético es Mario, que a la vez vende, escribe, construye y QA. |
| **Fotografía y dirección de imagen** | 1 SVG en biblioteca. Un sitio de USD 10.000 se juzga primero por sus fotos. No se resuelve con IA: se resuelve con un fotógrafo y una sesión. |
| **Motion design** | `DESIGN.md §11` regula el motion con criterio, pero no hay sistema: sin curvas, sin duraciones tokenizadas, sin ejemplos. Cero vídeo propio en la biblioteca. |
| **Copy nativo de conversión** | El copy actual es bueno en posicionamiento y honesto en evidencia. No hay ni un test de mensaje, ni variantes, ni jerarquía de objeciones. |
| **CRO con datos** | Cero analítica. CRO sin dato es opinión. |
| **Gestión de proyecto** | Sin repositorio, sin staging, sin pipeline, sin SLA. Un cliente de USD 10.000 audita eso antes de firmar. |
| **Escala de equipo** | Un operador. La calidad depende de que una persona no tenga un mal día. |
| **Marca propia** | No hay manual de marca: hay tokens y un wordmark. Falta lo que un cliente mira: papelería, plantillas, sistema de presentación. |

---

## FASE 3 · Auditoría de diseño (madurez 0–100)

| Activo | ¿Existe? | Estado real medido | Madurez |
|---|---|---|---|
| **Design system** | Sí, en papel | `DESIGN.md` (223 líneas): 4 modos de superficie, tokens, tipografía, deuda de contraste declarada (`muted` a 2,92:1, prohibido como texto). En el kit: **0 variables, 0 clases**. `pp.css`: 301 líneas, 76 reglas, 4 tokens | **40** |
| **Sistema de componentes** | No | 0 `e-component`. 12 patrones documentados en la skill, ninguno convertido en componente reutilizable | **10** |
| **Biblioteca visual** | No | 332 medios, 1 SVG propio, 5 vídeos de demo, 8 renders propios sin subir. Sin criterio de selección ni licencias documentadas | **15** |
| **Biblioteca UX** | Parcial | Contratos con `frontend_acceptance` y umbrales (CLS < 0,1, contraste, medida de línea, targets 44 px). Falta: estados (hover/focus/disabled/loading/error/vacío). `pp.css` tiene **0 `focus-visible`** y **0 `prefers-reduced-motion`** | **35** |
| **Guías de marca** | Parcial | Voz y lenguaje con prohibiciones explícitas (`PRODUCT.md §Lenguaje`), evidencia autorizada con fecha y autor. Falta manual visual, uso del wordmark, fotografía, ejemplos sí/no | **45** |
| **Framework de contenido** | Sí, fuerte | 4 modos de superficie, regla de un solo CTA primario, contrato SEO por página, estructura de casos «situación → intervención → resultado → límite», regla de tres cifras publicables | **65** |
| **Framework de conversión** | No | Sin analítica, sin mapa de objeciones, sin secuencia de nurturing, sin medición de formulario. El formulario de la portada es un CF7 con `class="wpcf7-form init demo"` y `aria-label="Contact form"` | **10** |

**Madurez de diseño global: 34/100.** La doctrina es de 70; la implementación es de 15. El sistema existe como documento, no como máquina.

### 3.1 Defectos medidos que un cliente de marca ve en 5 segundos

1. **Cinco familias tipográficas** cargadas (DM Sans, Heebo, Mukta Vaani, Roboto, Roboto Slab) y **Newsreader —la tipografía de los titulares— no se carga**. El CSS pide una fuente que el HTML no trae.
2. **Jerarquía rota:** 6 `<h2>`, **0 `<h3>`**. La estructura salta de nivel.
3. **Formulario de demo:** clases `demo`, etiqueta accesible en inglés, sin estados diseñados.
4. **Peso:** 5.7 MB de transferencia (634 KB HTML + 2.25 MB CSS/JS + 2.85 MB medios) con TTFB de 3,05 s. RevSlider solo aporta 697 KB de JS para nada visible en el contenido actual.
5. **Clases y variables inexistentes en el kit:** cualquier página nueva reconstruye estilos a mano; el resultado no es reproducible, que es la definición de «no es un sistema».

---

## FASE 4 · Auditoría de Hermes (sin cortesía)

### 4.1 Lo que hago bien, con evidencia de hoy

| Capacidad | Evidencia en esta sesión |
|---|---|
| Leer el estado real de WordPress por API | 58 tipos de widget, 29 site parts, 0 componentes, 0 clases, 332 medios, 7 páginas, 12 entradas |
| Medir en vez de opinar | TTFB 3,05 s, 42 assets / 2,25 MB, 5 familias tipográficas, 0 herramientas de analítica, 0 `focus-visible` |
| Detectar contradicciones entre documentación y realidad | `DESIGN.md:6` vs kit vacío; `CAMBIOS.md` «inactiva» vs 503 en vivo |
| Construir árbol V4 atómico por API | `build-composition` con XML, CSS, clases, interacciones, breakpoints |
| Gobernar tokens y clases de forma masiva | 50 operaciones por llamada en `manage-classes` y `manage-global-variable` |
| Escribir documentación operativa densa y verificable | `docs/` con 3.599 líneas, contratos y umbrales |
| QA mecánico por breakpoint | Medición de overflow, solapamiento, contraste, orden de lectura vía DOM/CSS computado |

### 4.2 Lo que hago de forma mediocre

- **Diseño visual sin referencia.** Puedo aplicar una ley visual existente; no puedo *inventar* una buena. Mis composiciones por defecto caen en el patrón que la propia skill prohíbe (hero, tres columnas, testimonios, CTA).
- **Espaciado y ritmo fino.** Acierto la escala; fallo el instinto. Un ojo humano corrige en 30 segundos lo que a mí me toma tres iteraciones medidas.
- **Copy en español de Chile.** Cumple registro y vetos de evidencia; le falta filo comercial. Escribo para no mentir, no para que el lector se mueva.
- **Responsive robusto de primera pasada.** Necesito medir y corregir; no anticipo la rotura.
- **Decisiones de foto.** No puedo juzgar recorte, mirada, luz ni encuadre.

### 4.3 Lo que no puedo hacer

| No puedo | Consecuencia práctica |
|---|---|
| **Ver.** `vision_analyze` devolvió 404 con el modelo actual | No valido estética, fotografía, composición ni «se ve bien». Solo mido geometría, contraste y jerarquía |
| Fotografiar, ilustrar a mano, grabar vídeo | Todo el material visual debe venir de Mario, un banco o un profesional |
| Hacer UX research con usuarios reales | Sin entrevistas, sin tests de usabilidad, sin dato de campo |
| Garantizar conversión | Sin analítica no hay línea base; sin línea base no hay garantía |
| Operar con responsabilidad legal | Privacidad, cookies, consentimiento, contratos: revisión humana |
| Mantener la calidad sin supervisión | No tengo criterio estético propio verificable |

### 4.4 Qué requiere supervisión humana obligatoria

1. Aprobar la dirección visual de cada página (captura → ojo humano → aprobación).
2. Aprobar cifras, casos y afirmaciones (veto de evidencia, `PRODUCT.md:69-78`).
3. Aprobar cualquier cambio en producción (hoy no hay staging: cada edición es en vivo).
4. Aprobar fotografía, vídeo y licencias.
5. Aprobar precios, alcance y contratos.

### 4.5 Qué debe hacer un diseñador profesional, no yo

- La dirección de arte de una marca nueva (no la ejecución de una ya definida).
- La selección y el retoque fotográfico.
- El motion design con criterio (curvas, duraciones, coreografía).
- La ilustración y los diagramas originales.
- La revisión final de cada entrega antes de que la vea el cliente.

**Resumen honesto:** soy un excelente contratista de ejecución y un mal director creativo. La operación funciona si el criterio visual viene de afuera y yo aporto velocidad, consistencia y medición.

---

## FASE 5 · Benchmark

Comparación por lo que el cliente **compra**, no por herramientas.

| Criterio | Webflow Agencies | Framer Agencies | Elementor Premium | Consultoras digitales | **Pennacchiotti Web hoy** |
|---|---|---|---|---|---|
| Velocidad de iteración visual | Muy alta (canvas real) | Muy alta (canvas + motion nativo) | Media (editor lento, colisiones) | Media | **Media-baja** (API potente, sin ojo) |
| Techo visual | Alto | **Muy alto** (motion de serie) | Medio-alto (depende del tema) | Alto | **Medio** |
| Fotografía/motion propio | Depende del estudio | Fuerte en motion | Débil de serie | Fuerte | **Muy débil** |
| Peso y rendimiento | Bueno (2–4 MB típico) | Excelente (< 1,5 MB) | Malo de serie (5–8 MB) | Variable | **5,7 MB** |
| Design system real | Sí (clases, variables) | Sí (tokens) | Sí, si se configura | Sí | **No en la herramienta** |
| SEO técnico | Bueno | Regular (hidratación) | Bueno con plugin | Bueno | **Parcial** (sin schema `Service`, sin GSC verificado) |
| Mantenimiento del cliente | Fácil | Fácil | **Difícil** (el cliente rompe el layout) | Media | Difícil |
| Coste de licencias | USD 23–39/mes por sitio | USD 5–30/mes | Tema + plugins ≈ USD 200–400/año | Variable | **Ya pagado** |
| Argumento de venta | «Diseño + CMS visual» | «Diseño + motion» | «Barato y editable» | «Estrategia» | **«Método y medición»** (aún no demostrado) |

**Fortalezas reales frente a los cuatro:** disciplina documental, contratos antes de construir, QA medido, y un método propio de estandarización que ninguna agencia de USD 3.000 tiene.
**Debilidades reales:** no hay imagen, no hay motion, no hay dato, no hay caso, no hay staging. Un cliente compara capturas, no documentos.

---

## FASE 6 · Capacidad de producción (operación unipersonal)

Base de cálculo medida: la evidencia del propio proyecto muestra que una página interna (portada, `/capacitacion/`) consumió **ciclos de varias horas con regresiones y correcciones** (`CAMBIOS.md`, entradas 2026-10-26 y 2026-10-27). Un sitio de 6 páginas con el proceso actual no baja de 4–6 jornadas reales.

| Escenario | Alcance | Páginas/sitio | Hoy (sin biblioteca) | Con biblioteca de componentes + tokens | Condición para que se cumpla |
|---|---|---|---|---|---|
| **Básico** | 4–5 páginas, plantilla, 1 sección de foto, sin copy nuevo | 5 | **4–6 / mes** | 10–14 / mes | Un componente por patrón + textos del cliente |
| **Profesional** | 6–8 páginas, dirección de arte por página, fotografía provista, contrato y QA 5 anchos | 7 | **2 / mes** (techo real) | 4–5 / mes | Ojo humano en el bucle + biblioteca + staging |
| **Escalable** | 12+ páginas, multi-idioma, integraciones, mantenimiento mensual | 12+ | **No viable** | 2–3 / mes con 2º operador | Componentes + pipeline + segundo par de manos |

**Conclusión:** hoy la operación aguanta **2 sitios profesionales al mes** con calidad defendible y **uno más** si algo falla. El cuello no es la herramienta: es el ojo y la ausencia de componentes. Convertir 12 patrones en componentes sube el techo de 2 a 4–5 sin contratar.

---

## FASE 7 · Lo que falta para sitios «de otro mundo», por impacto

| # | Falta | Por qué va primero | Coste | Retorno |
|---|---|---|---|---|
| 1 | **Ojo / dirección de arte en el bucle** | Sin juicio visual, todo lo demás se construye a ciegas. Es la única brecha que no se compra con software | 2–4 h por entrega de un diseñador, o modelo con visión | Muy alto |
| 2 | **Biblioteca de componentes real** (12 patrones → `e-component`) + tokens en el kit | Convierte 3 horas por sección en 20 minutos, y hace la calidad reproducible | 2–3 días | Muy alto |
| 3 | **Medición** (GA4 + evento de formulario + Search Console) | Sin dato no hay CRO, ni informe, ni renovación de contrato | 2 h | Muy alto |
| 4 | **Fotografía propia** (una sesión: retrato, planta, detalle, textura) | El 70 % de la calidad percibida de un sitio corporativo es su imagen | 1 sesión + selección | Muy alto |
| 5 | **Casos con estructura** (situación → intervención → resultado → límite) | Es lo que convierte un folleto en autoridad; `PRODUCT.md` ya tiene la estructura, faltan 3 casos | 1 día por caso | Alto |
| 6 | **Presupuesto de rendimiento** (CSS crítico, quitar RevSlider y feeds no usados, 2 familias) | 5,7 MB → 1,2 MB es una mejora percibida inmediata y medible | 1 día | Alto |
| 7 | **Staging + git + deploy** | Hoy cada error es público y no hay rollback más que FTP manual | 1 día | Alto |
| 8 | **Motion design con sistema** (duraciones, curvas, coreografía) | Sube la percepción de modernidad; mal hecho, la baja | 3–5 días | Medio |
| 9 | **Ilustración / diagramas originales** | La oferta es abstracta (procesos, conocimiento); un diagrama propio la vuelve concreta | 2 días | Medio |
| 10 | **UX research ligero** (5 entrevistas a gerentes de operaciones) | Con 5 conversaciones se corrigen las hipótesis de mensaje | 1 semana | Medio |
| 11 | **Oferta y precio** (paquetes, alcance, SLA) | Sin esto no hay negocio, solo favores | 1 día | Muy alto (comercial) |
| 12 | **Marco legal** (privacidad, cookies, contrato de servicio) | Obligatorio si se recogen datos y hay clientes | 1 día + abogado | Alto (riesgo) |

---

## FASE 8 · Roadmap 90 días

Criterio de orden: primero lo que multiplica el resto, después lo que se ve, al final lo que se vende.

### Días 1–30 · «Que la máquina exista»

| Semana | Acción | Entregable verificable |
|---|---|---|
| 1 | Decidir mantenimiento (apagarlo y purgar caché), poner el sitio en 200, instalar GA4 + evento `generate_lead` + GSC | `/` = 200 · evento visible en tiempo real · propiedad verificada |
| 1 | Repo git con `docs/`, `wp/`, `video/` y baselines de captura | `git log` con el primer commit |
| 2 | Cargar en el kit las **8 variables** y las **22 clases** de `DESIGN.md` (§5), más `pp-stack`, `pp-stack--sm/md/lg`, `pp-cluster` | `elementor://global-variables` = 8+ · `global-classes` = 27 |
| 2 | Declarar la capa tipográfica en `manage-default-styles` (h1–h4, p, a) | `get-default-styles(h1)` sin `display:grid` heredado |
| 3 | Convertir 6 patrones en componentes: `hero-editorial`, `intro-dos-columnas`, `problema-sintomas`, `evidencia`, `metodo-secuencial`, `cta-final` | `list-components` = 6, cada uno con `overridable_props` |
| 4 | Recortar: RevSlider, Twitter feeds, Instagram feed, Spectra, 3 familias tipográficas | Peso de portada < 2,5 MB · TTFB < 1,2 s |
| 4 | Reconstruir la portada **sobre componentes**, con captura en 5 anchos y auditoría AA | 0 overflow · 0 solapamiento · contraste 0 fallos · captura aprobada por ojo humano |

### Días 31–60 · «Que se vea»

| Semana | Acción | Entregable verificable |
|---|---|---|
| 5 | Sesión fotográfica: retrato, planta/proceso, detalle de producto, textura | 15–20 originales con licencia propia, en biblioteca con alt |
| 5 | Subir los 8 renders de `/video` y usarlos en el hero (con `pp-stack` y poster) | `list-assets type:video` incluye los propios; hero con vídeo y `prefers-reduced-motion` |
| 6 | Tres casos de estudio con la estructura de `PRODUCT.md` | 3 páginas `/casos/…` con evidencia autorizada, sin cifras vetadas |
| 7 | Sistema de motion mínimo: 3 duraciones y 2 curvas tokenizadas; animación de entrada solo en hero y CTA final | Documentado + aplicado en 2 secciones |
| 8 | Staging en subdominio + flujo «contrato → preview link → aprobación → publicar» | Ningún cambio llega a producción sin preview aprobado |

### Días 61–90 · «Que se venda»

| Semana | Acción | Entregable verificable |
|---|---|---|
| 9 | Oferta: 3 paquetes con alcance, plazo, precio y qué no incluye; SLA de respuesta | Documento de oferta de 2 páginas |
| 10 | Página `/servicios/` con la oferta, no con la consultoría | 1 CTA primario, formulario con estados y medición |
| 11 | Plantilla de propuesta y de informe mensual (con datos de GA4) | 1 propuesta generada en < 1 h |
| 12 | Segunda pasada de QA sobre el sitio completo + baseline de capturas por página | Informe con métricas antes/después: peso, TTFB, contraste, overflow |

---

## FASE 9 · Scorecard

| Dimensión | Puntaje | Base de la nota |
|---|---|---|
| **Diseño** | **38/100** | Dirección y tokens definidos (70) · 0 variables/0 clases en el kit, 5 familias tipográficas, jerarquía h2 sin h3, 1 SVG propio, sin motion ni ilustración (15) |
| **UX** | **42/100** | Contratos, 5 breakpoints y umbrales medidos (65) · 0 `focus-visible`, 0 `prefers-reduced-motion`, formulario de demo, sin estados, sin research (15) |
| **Automatización** | **50/100** | MCP de altísima capacidad: 58 widgets, 50 operaciones por lote, preview links (85) · sin git, sin staging, sin pipeline, sin cron, proceso manual (20) |
| **Escalabilidad** | **20/100** | Un operador, sin componentes, sin repo, sin staging, edición en producción (10) · 12 patrones documentados como base (30) |
| **Conversión** | **15/100** | Copy con un solo CTA y destino válido (40) · cero analítica, cero tests, cero nurturing, formulario sin estados (0) |
| **Marca** | **45/100** | Voz, vetos y evidencia autorizada con fecha (75) · sin manual visual, sin fotografía, sin papelería, sin presentación (20) |
| **Oferta comercial** | **20/100** | `PRODUCT.md` define la consultoría con precisión (60) · no existe oferta web, ni precio, ni cartera, ni SLA (5) |
| **Capacidad total** | **33/100** | Media ponderada: el techo de ejecución es alto, la operación comercial es incipiente |

**Lectura del comité:** no es una agencia; es un excelente taller de ejecución con doctrina y sin activos. El puntaje no mide talento, mide activos reutilizables y evidencia comercial, que es lo que compra un cliente y lo que mira un inversor.

---

## La pregunta: «¿qué haría mañana a las 08:00 para duplicar la calidad percibida en 30 días?»

No abriría un Figma. No aprendería Framer. No contrataría a nadie todavía. La calidad percibida de un sitio corporativo se decide en cuatro cosas, en este orden: **tipografía, fotografía, espacio y velocidad**. Tres de las cuatro están rotas y ninguna requiere talento nuevo, solo ejecución.

**08:00 — Apagar el 503 y purgar caché.** Un sitio en mantenimiento no tiene calidad percibida: tiene 503. `activo => false`, purga en las 5 rutas, verificar 200 y peso real.

**08:30 — Una sola pareja tipográfica.** Eliminar Heebo, Mukta Vaani, Roboto y Roboto Slab. Cargar Newsreader (que hoy se usa y no se carga) y DM Sans. Es el cambio con mayor retorno por minuto de todo el informe: el sitio cambia de cara sin tocar una sola sección.

**09:30 — Meter el design system en la herramienta.** 8 variables y 22 clases en el kit, y la capa tipográfica en `manage-default-styles`. Sin esto, todo lo que se construya después vuelve a ser improvisación.

**11:00 — Recortar 3 MB.** Fuera RevSlider (697 KB de JS para contenido que no lo usa), feeds sociales y Spectra. Objetivo: portada < 2 MB. La velocidad es la calidad que el visitante siente antes de leer.

**13:00 — Un solo componente bien hecho.** El hero. Sobre la foto propia, con velo, `min-height` en el contenedor raíz, texto en `pp-stack`, un CTA, y captura aprobada en 5 anchos. Ese componente define el nivel de todo lo demás.

**15:00 — Medir.** GA4 + evento de envío + Search Console. A partir de mañana, cada decisión de diseño tiene un número detrás. Sin esto, dentro de 30 días no se podrá decir si la calidad subió; solo si *parece* que subió.

**16:00 — Conseguir la foto.** Llamar y agendar la sesión para esta semana: retrato de Mario, planta o proceso real, detalle de producto. Es la única partida que exige a otra persona y la que más mueve la percepción. Un sitio impecable con fotos del demo se lee como plantilla; un sitio correcto con fotos propias se lee como empresa.

**Y lo que no haría:** rediseñar el sitio entero, escribir un documento más, ni añadir una función nueva. El problema no es de ideas. Es que hay treinta y tres de cien y las palancas que faltan son aburridas, baratas y medibles.

---

## Anexo · Aprobar / Rechazar

**Aprobar**

1. Apagar mantenimiento y purgar caché (impacto inmediato, reversible).
2. Cargar tokens y clases en el kit (2–3 h, desbloquea todo lo demás).
3. Reducir a 2 familias tipográficas (1 h, máximo retorno).
4. Instalar analítica con evento de conversión (2 h).
5. Crear 6 componentes desde los 12 patrones (2–3 días).
6. Sesión fotográfica propia (esta semana).
7. Repo git + staging (1 día).

**Rechazar**

1. Rediseñar antes de tener tokens y componentes en el kit.
2. Contratar un diseñador para «hacer el sitio» antes de tener la oferta definida.
3. Adoptar Framer o Webflow: cambia la herramienta, no la brecha (que es ojo, foto y dato).
4. Añadir otro plugin de página builder: hay 4 builders/bloques cargados y el peso ya es 5,7 MB.
5. Escribir otro documento de método antes de que el kit tenga 0 variables convertidas en 8.
6. Prometer CRO a un cliente antes de tener una línea base medida.

---

*Documento generado a partir de medición en vivo. Si un dato aquí contradice un documento previo, gana esta medición y el documento previo se corrige: `DESIGN.md:6` (14 variables/22 clases) y la última entrada de `CAMBIOS.md` (mantenimiento «inactiva») quedan desmentidos por lo medido el 2026-10-28.*
