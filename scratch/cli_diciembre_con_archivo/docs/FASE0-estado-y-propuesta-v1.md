# PENNACCHIOTTI — Fase 0
## Estado verificado, propuesta textual, matriz de evidencia y plan

**Fecha de medición:** 23 de octubre de 2026
**Versión:** 1.0 — documento de trabajo, no publicado
**Alcance:** entrega 23.A–23.E del brief de reconstrucción integral
**Regla aplicada:** no se modificó el cuerpo sustantivo de la Home en esta fase.

---

## A. Estado actual verificado

Medido hoy contra `https://pennacchiotti.cl` con user-agent de Chrome completo y query string única para forzar caché nueva. No se reutilizan conclusiones de auditorías anteriores.

### A.1 Lo que ya está cerrado

| Ítem | Estado | Evidencia |
|---|---|---|
| Portada única | **Cumple** | `page_on_front = 1933`. `/inicio/` en borrador, `/inicio-revision/` en papelera |
| Demos de plantilla | **Cumple** | 11 a papelera. `/home/`, `/about-us/`, `/contact-us/` → 404 real |
| Páginas públicas | **4** | `/` 200 · `/sobre-mi/` 200 · `/perspectivas/` 200 · `/contacto/` 200 |
| Títulos SEO | **Cumple en las 4** | Únicos, con marca: «… · PENNACCHIOTTI» |
| Metadescripciones | **Cumple en las 4** | Escritas y servidas en el `<head>` |
| Canonical | **Cumple** | Presente en las 4 páginas |
| 404 | **Cumple** | `/soluciones/` devuelve 404 real, sin contenido demo |
| Contenido demo indexable | **Cumple** | 0 páginas demo accesibles |
| Formulario | **Parcial** | 1 solo `<form>`, 8 campos, sin duplicados tras la limpieza |
| Imagen del hero | **Parcial** | Se sirve en 58 KB (JPEG) por CSS, pero el HTML sigue solicitando el PNG de 770 KB |
| Cache | **Cumple** | Purga por `/marraqueta/v1/purge`; verificación siempre con query única |

### A.2 Defectos abiertos

| # | Defecto | Evidencia medida | Severidad |
|---|---|---|---|
| 1 | **No hay navegación** | `nav: 0` en las cuatro páginas. Sin menú, el sitio no se recorre | Crítica |
| 2 | **Footer demo** | «© 2023 eramic, All Rights Reserved» + logo `logo-retina-free-img.png` + descripción «Estrategia, operaciones e innovación aplicada…» | Alta |
| 3 | **`/soluciones/` no existe** | 404. El menú propuesto la incluye | Alta |
| 4 | **H1 duplicado** | `/sobre-mi/` y `/perspectivas/`: 2 `<h1>` (título del tema + H1 del contenido) | Media |
| 5 | **Desplegable del formulario** | Las opciones se renderizan como `procesos`, `digital`, `ia` en vez de las etiquetas legibles | Media |
| 6 | **Entrega de correo sin verificar** | `form-state-success` solo prueba que el endpoint aceptó el envío. No hay confirmación de recepción en `contacto@pennacchiotti.cl` | Alta |
| 7 | **Almacenamiento de envíos sin verificar** | La acción `collect-submissions` está declarada; no se comprobó que escriba en la base | Media |
| 8 | **Peso de recursos** | 42 hojas de estilo, 15 scripts externos, HTML de 569 KB en la Home | Media |
| 9 | **Contraste insuficiente** | `#85979B` sobre `#FBFAF9` = **2,92:1**; sobre `#EFEFEF` = **2,65:1**. AA exige 4,5:1 en texto normal y 3:1 en texto grande: **no cumple ni para texto grande en marfil** | Media |
| 10 | **Sin páginas legales** | No hay privacidad ni términos. El formulario ya recoge datos personales con consentimiento | Alta |
| 11 | **Banner de cookies** | CookieAdmin activo, sin verificación visual ni de texto legal | Media |
| 12 | **Responsive incompleto** | Verificado antes a 390 y 1536 en la Home; **320, 768 y 1024 sin medir**, y no se re-verificó tras los últimos cambios | Media |
| 13 | **Rendimiento sin auditar** | LCP, CLS, INP y TTFB no medidos | Media |
| 14 | **Doble mensaje en la portada** | El `<title>` y la meta ya dicen control de proceso y agroindustria; el cuerpo sigue vendiendo transformación digital, IA y conocimiento | Alta |
| 15 | **Sitemap incompleto** | `robots.txt` apunta a `/sitemap_index.xml`, que declara 2 sub-sitemaps (páginas y `elementor_library`); no se verificó su contenido con UA válido | Baja |

### A.3 Estado del contenido

- **Artículos publicados:** 0. Hay **un borrador** (2058) de 395 palabras, sin aprobar.
- **Categorías creadas:** 4 (`transformacion-digital`, `inteligencia-artificial-aplicada`, `gestion-del-conocimiento`, `sistemas-y-decisiones`). **No coinciden** con las 5 del brief (§12): falta «Control y estandarización», «Transformación operacional» y «Formación y transferencia»; sobran «Sistemas y decisiones».
- **Bloque Perspectivas en la Home:** no existe. Debe mantenerse oculto hasta tener 3 artículos publicados, y entonces retirar «Perspectivas» del menú.
- **Evidencia publicada:** ninguna cifra. Es correcto que así sea mientras no se valide (ver C).

### A.4 Origen técnico de dos defectos

- **Footer:** no está en el child theme. Lo genera el footer dinámico de Hello Elementor (`template-parts/dynamic-footer`) y el texto de copyright viene de una opción del tema heredada de la importación del kit. Se corrige sin tocar PHP.
- **H1 duplicado:** el tema imprime el título de la página y el contenido imprime el suyo. En `/` y `/contacto/` se resolvió ocultando el del tema por CSS; en las otras dos no se aplicó.

---

## B. Propuesta textual completa (borrador v1 — no publicada)

Redactada para revisión. No se publica nada hasta aprobación. Las cifras aparecen como marcadores explícitos, no como datos.

### B.1 Navegación

`Inicio · Soluciones · Sobre Mario · Contacto` + botón **Agendar una conversación**

> «Perspectivas» **no entra** al menú hasta tener 3 artículos publicados (brief §9.9). «Soluciones» no se activa hasta que la página exista.

### B.2 Hero

**Antetítulo:** Consultoría en operaciones agroalimentarias

**H1:** Transformamos conocimiento en capacidades organizacionales.

**Bajada:** Ayudamos a organizaciones agroalimentarias a controlar y estandarizar sus procesos, reducir la dependencia de personas clave y convertir experiencia técnica en resultados sostenibles.

**CTA principal:** Agendar una conversación → `/contacto/`
**CTA secundario:** Conocer el enfoque → ancla `#enfoque`

### B.3 Problemas reconocibles

Título: **Si la operación depende de quién está ese día, el problema no es la gente.**

1. Cada persona ejecuta el proceso a su manera, y todas las versiones funcionan hasta que una falla.
2. Las decisiones críticas se consultan a una sola persona, que no tiene reemplazo.
3. Los procedimientos existen, pero describen la operación ideal, no la real.
4. Hay datos por todos lados y ningún criterio compartido para leerlos.
5. La capacitación se aprueba y la ejecución sigue igual.
6. Se digitaliza el desorden existente y se vuelve más rápido.
7. Se explora inteligencia artificial sin haber priorizado un problema operacional.

### B.4 Resultado

Título: **Qué cambia cuando el proceso se controla**

- Procesos consistentes entre turnos, plantas y personas.
- Criterios técnicos explícitos: qué se acepta, qué se rechaza y por qué.
- Responsabilidades definidas, sin zonas grises.
- Conocimiento crítico documentado y reutilizable.
- Controles verificables, no declaraciones de intención.
- Menos dependencia de expertos individuales.
- Capacidad real para formar, transferir y escalar.

### B.5 Oferta

**Servicio troncal:** Control, estandarización y desarrollo de capacidades operacionales.

**1. Diagnóstico**
- *Para quién:* quien sospecha que la operación depende de personas y no de procesos.
- *Problema:* nadie sabe con precisión dónde se pierde el criterio.
- *Incluye:* levantamiento de procesos críticos, análisis de variabilidad, mapa de conocimiento tácito, revisión documental, identificación de dependencias.
- *Entregables:* informe priorizado, mapa de procesos críticos, matriz de brechas, propuesta de hoja de ruta.
- *Resultado esperado:* una lista corta y ordenada de dónde intervenir primero.
- *Aporta el cliente:* acceso a operación, personas clave y documentación existente.
- *Siguiente paso:* definir alcance de estandarización.

**2. Diseño y estandarización**
- *Para quién:* organizaciones con procesos definidos en la cabeza de expertos.
- *Problema:* el criterio existe, pero no está escrito ni es transferible.
- *Incluye:* conversión de criterio experto en proceso, procedimientos, controles, responsabilidades y criterios de aceptación.
- *Entregables:* proceso documentado, procedimientos, puntos de control, criterios de aceptación, roles.
- *Resultado esperado:* cualquiera con la competencia técnica puede ejecutar y verificar igual.
- *Aporta el cliente:* validación de expertos y tiempo de sus equipos.
- *Siguiente paso:* plan de implementación.

**3. Implementación y adopción**
- *Para quién:* quien ya tiene el estándar escrito y no logra que se cumpla.
- *Problema:* el documento existe y la práctica no cambia.
- *Incluye:* puesta en marcha, acompañamiento, gestión del cambio, ajuste de controles, digitalización cuando aporta, IA cuando resuelve un problema definido.
- *Entregables:* plan de adopción, tablero de seguimiento, ajustes al estándar, registro de desviaciones.
- *Resultado esperado:* el estándar se cumple de forma sostenida, no por auditoría.
- *Aporta el cliente:* responsables por área y decisión sobre prioridades.
- *Siguiente paso:* medir y ampliar alcance.

**4. Formación y transferencia**
- *Para quién:* organizaciones que necesitan instalar la capacidad, no contratarla para siempre.
- *Problema:* la formación entrega contenidos y no cambia la ejecución.
- *Incluye:* cursos, talleres y programas diseñados sobre el proceso real, con evaluación de desempeño.
- *Entregables:* programa, material, evaluaciones, evidencias de aplicación.
- *Resultado esperado:* personas capaces de sostener el proceso sin acompañamiento externo.
- *Aporta el cliente:* participantes con rol operativo y tiempo protegido.
- *Siguiente paso:* definir programa y cobertura.

### B.6 Enfoque (no «framework propietario»)

Título: **Cómo trabajamos**

1. **Comprender** la operación y el resultado que se busca.
2. **Identificar** el conocimiento crítico y quién lo tiene.
3. **Estructurar** procesos, criterios y responsabilidades.
4. **Estandarizar** en documentos que reflejen la operación real.
5. **Implementar** con acompañamiento y gestión del cambio.
6. **Transferir** a las personas que quedan a cargo.
7. **Medir y mejorar** con indicadores del proceso, no de actividad.

### B.7 Aplicaciones

- Estandarización de un proceso técnico que hoy depende de un experto.
- Transferencia del conocimiento de alguien que se jubila o cambia de rol.
- Diseño de documentación operacional que se pueda usar en planta.
- Mejora del control y seguimiento de un proceso crítico.
- Digitalización de un proceso previamente rediseñado.
- Formación asociada a una capacidad concreta y evaluable.
- Selección de casos de uso de IA con criterio operacional.

### B.8 Evidencia

**Bloque vacío por ahora.** No hay una sola cifra publicable (ver C). Cuando existan dos o tres casos validados, este bloque se llena con la estructura situación → intervención → resultado → límite.

### B.9 Perspectivas

**Oculto.** Requiere 3 artículos publicados. Hoy hay 1 borrador sin aprobar.

### B.10 Sobre Mario (síntesis, no CV)

> Dos décadas en operaciones agroalimentarias y técnicas, en roles donde el resultado dependía de que el criterio estuviera donde debía estar: en el proceso y en la gente, no en una persona. Dirigí equipos, administré presupuestos y respondí por márgenes. La mayor parte de lo que sé sobre estandarización no viene de un manual, viene de operaciones que fallaban por depender de alguien irremplazable. Hoy trabajo con organizaciones que quieren lo mismo: que su conocimiento no se vaya con una persona.

### B.11 CTA final

**Título:** Conversemos sobre los procesos y conocimientos que hoy limitan tu operación.
**Botón:** Agendar una conversación → `/contacto/`

### B.12 Footer

Marca PENNACCHIOTTI · navegación · `contacto@pennacchiotti.cl` · Privacidad · Términos · año dinámico. Sin logo demo, sin «eramic», sin descripción del kit.

---

## C. Matriz de evidencia

Ninguna cifra se publica sin cerrar los diez pasos del brief §7. Estado inicial:

| # | Afirmación | Fuente declarada | Contexto | Atribución | Permiso | Estado | Redacción propuesta si se aprueba |
|---|---|---|---|---|---|---|---|
| 1 | Equipos de hasta 70 personas | Brief §7 / CV | Rol dependiente | Liderazgo directo, verificable | No verificado | **No publicable todavía** | «Equipos de hasta 70 personas» solo si se puede sostener con fuente y período |
| 2 | Presupuesto de USD 180 MM | Brief §7 | Empresa empleadora | Institucional, no personal | Riesgo alto | **No publicable** | No usar |
| 3 | Ingresos generados USD 194 MM | Brief §7 | Empresa empleadora | Institucional | Riesgo alto | **No publicable** | No usar |
| 4 | Márgenes sobre 55 % | Brief §7 | Empresa empleadora | Institucional | Riesgo alto | **No publicable** | No usar |
| 5 | Error de estimación 20 % → <5 % | Brief §7 | Proyecto con equipo | Compartida | No verificado | **No publicable todavía** | «Redujimos el error de estimación de un proceso crítico» (sin cifras) |
| 6 | Quiebres −70 % con S&OP | Brief §7 | Proyecto con equipo | Compartida | No verificado | **No publicable todavía** | «Redujimos quiebres en la cadena mediante S&OP» (sin cifras) |
| 7 | 350+ profesionales formados | Brief §7 / CV | Trayectoria acumulada | Personal, si el conteo es propio | Probable | **Utilizable como experiencia general** | «Más de 350 profesionales formados» tras verificar el conteo |
| 8 | Diplomado con USD 41,8 MM en ingresos | Brief §7 | Institución educativa | Institucional y ajena | No | **No publicable** | No usar; como mucho «diseñé y dirigí un diplomado» |

**Conclusión de C:** hoy hay **0 cifras publicables con respaldo documental**. La única defendible a corto plazo es «más de 350 profesionales formados», y solo si el conteo es propio y verificable. Las demás son resultados de organizaciones donde Mario trabajó: publicarlas requiere permiso y, en varios casos, no son atribuibles a su gestión individual. El riesgo contractual es real y aplica directo al §3 del brief.

---

## D. Plan de implementación

Orden por dependencia y riesgo. Cada fila es reversible.

| # | Cambio | Página | Herramienta | Riesgo | Depende de | Criterio de aceptación | Reversión |
|---|---|---|---|---|---|---|---|
| 1 | Copyright y datos del footer | Global | Opción del tema (Customizer) | Bajo | — | Sin «eramic», año dinámico, contacto real | Valor anterior de la opción |
| 2 | Logo demo fuera del header | Global | Ya oculto por CSS; eliminar del DOM | Bajo | — | 0 referencias a `logo-retina-free-img` | CSS |
| 3 | Menú de 4 ítems + CTA | Global | Menú WP + header de Elementor Pro | Medio | Página `/soluciones/` | Nav presente y navegable por teclado | Borrar menú |
| 4 | H1 único en `/sobre-mi/` y `/perspectivas/` | 2 páginas | CSS acotado o tema | Bajo | — | 1 `<h1>` por página | CSS |
| 5 | Desplegable del formulario con etiquetas | `/contacto/` | Edición del widget en Elementor | Bajo | — | Opciones legibles en el render | Rebuild |
| 6 | Prueba real de correo | `/contacto/` | Envío + revisión de bandeja | Bajo | GoSMTP | Correo recibido, Reply-To correcto, sin spam | — |
| 7 | Verificar almacenamiento de envíos | `/contacto/` | Elementor → Submissions | Bajo | — | Envío visible en el panel | — |
| 8 | PNG pesados fuera del árbol | Home | Reemplazo de imágenes | Bajo | — | 0 cargas del PNG de 770 KB | Datos previos |
| 9 | `/soluciones/` | Página nueva | Elementor | Medio | Copy aprobado (B.5) | Publicada con las 4 modalidades | Papelera |
| 10 | Reescritura de la Home | Home | Elementor por bandas | Alto | Copy aprobado | Cada banda validada a 1440/768/390 | Respaldo de datos |
| 11 | Categorías de Perspectivas | Blog | REST | Bajo | — | 5 categorías del brief §12 | Reasignar |
| 12 | 3 artículos | Blog | REST + revisión | Medio | Aprobación de textos | Publicados, con autor, fecha, lectura | Borrador |
| 13 | Páginas legales | Nuevas | Elementor | Medio | Texto legal revisado | Privacidad y términos publicados | Papelera |
| 14 | Contraste `#85979B` | Global | Variables del kit | Bajo | — | ≥4,5:1 en texto pequeño | Variable previa |
| 15 | Peso y rendimiento | Global | Caché, imágenes, crítico | Medio | 8 | LCP y CLS medidos y documentados | Config previa |
| 16 | Motion sobrio | Global | Elementor + CSS | Bajo | 10, 14, 15 | Respeta `prefers-reduced-motion` | Quitar animaciones |

---

## E. Recomendación crítica

**1. La oferta es defendible en el fondo y demasiado ancha en la forma.**
«Control, estandarización y desarrollo de capacidades operacionales para organizaciones agroalimentarias y técnico-operacionales intensivas en conocimiento especializado» son tres conceptos y dos públicos en una frase. Un gerente de operaciones no se reconoce en «organización técnico-operacional intensiva en conocimiento». Esa categoría es cómoda para el consultor y opaca para el comprador. Recomiendo conservarla como definición interna y usar en la web una sola frase con un solo público: *«Ordenamos y estandarizamos procesos en operaciones agroalimentarias para que no dependan de una persona.»*

**2. El H1 actual no dice qué haces.**
«Transformamos conocimiento en capacidades organizacionales» es diferenciador y es la marca, pero es una promesa abstracta: no menciona procesos, operación ni resultado. El brief pide mantenerlo, y coincido en mantenerlo como plataforma; lo que no puede es quedar solo. La bajada debe cargar todo el peso concreto, y hoy la propuesta la cumple.

**3. La evidencia no sostiene la oferta, y forzarla sería el error más caro.**
De las ocho cifras del brief, **siete son resultados de organizaciones donde Mario fue empleado**, no de su práctica consultora. Publicarlas crea tres riesgos simultáneos: confidencialidad contractual, atribución individual falsa y promesa que un cliente puede auditar. Mi recomendación es publicar **señales cualitativas verificables** («dirigí equipos», «respondí por márgenes», «formé a más de 350 profesionales») y dejar las cifras fuera hasta tener dos casos propios con autorización escrita.

**4. El método de siete pasos es correcto y no es un diferenciador.**
Comprender → estructurar → estandarizar → implementar → transferir → medir lo tiene cualquier consultora, con otros nombres. Sirve como estructura de página y como expectativa de trabajo; no sirve como argumento de venta. El argumento está en otro lugar: en que el entregable es **criterio de aceptación verificable**, no un documento.

**5. «Agendar una conversación» sin agenda es una promesa vacía.**
Hoy no hay Calendly ni equivalente. O se crea una agenda real, o el CTA dice «Escríbeme» y lleva al formulario. Un botón que promete agendar y abre un formulario produce la primera decepción del sitio.

**6. La contradicción actual es de mensaje, no de diseño.**
El `<title>` ya dice agroindustria y control de proceso; el cuerpo vende transformación digital, IA y conocimiento. Mientras eso no se resuelva, ningún ajuste visual va a arreglar la impresión de que el sitio no sabe qué vende.

**7. Hay una dependencia técnica que conviene declarar.**
Construir Elementor V4 por MCP funciona, pero es frágil: `build-composition` agrega raíces en vez de reemplazar, las opciones del desplegable no se serializan bien, y la caché de nginx sirve la versión anterior de una URL aunque se purgue. Cada fase debe empezar contando raíces y formularios, y cerrar con verificación por query única. Está documentado en el registro de cambios.

**Veredicto:** la oferta es **suficientemente defendible** como dirección y **demasiado ancha** como está escrita. Compatible con las restricciones contractuales solo si se descartan las cifras institucionales. Comprensible para el cliente objetivo solo después de bajar la formulación a una frase con un público único.

---

## Siguiente decisión pendiente

1. Aprobar o corregir la bajada del hero (B.2) y la frase de oferta de E.1.
2. Decidir qué se hace con la evidencia: publicar señales cualitativas o esperar casos propios.
3. Autorizar la creación de `/soluciones/` para poder publicar el menú.
