# Piloto de reparación de Contacto — registro Gate 4A

**Fecha:** 23 de octubre de 2026
**Ejecutado sobre:** copia de trabajo `2095` (`/contacto-piloto-final-qovu/`), publicada solo para medición.
**`/contacto/` (página 14) no se tocó:** verificado, sigue con `pp-stack: 0` en su HTML.

## Línea base registrada (antes de tocar)

| Dato | Valor |
|---|---|
| ID / estado | 14 · publish |
| Raíces | 1 |
| Nodos | 31 |
| Hijos de la columna editorial | 5 |
| Formularios | 1 |
| Campos | 8 |
| Clases globales | 22 |
| Respaldo | `baseline_contacto_*.json` (página + árbol + clases) |

## Acciones ejecutadas (las siete autorizadas)

1. Clases creadas en el kit: `pp-stack` (`g-0e352b6`), `pp-stack--sm` (`g-f7e2c51`), `pp-stack--md` (`g-a5de0ae`), `pp-stack--lg` (`g-0e7aa16`), `pp-cluster` (`g-b8d3344`). Kit: 22 → 27 clases, sin prefijo `DUP_`.
2. `pp-stack` aplicada a banda, wrap, columna editorial y columna del formulario (con `--md` y `--sm` para el gap).
3. Ocho propiedades declaradas en los cuatro contenedores mediante la clase: `display`, `flex-direction`, `flex-wrap`, `align-items`, `justify-content`, `gap`, `width`, `min-width`.
4. Retirados dos bloques: «No vendo software ni licencias…» (`9ba6c954`) y «Si tu desafío no es lo que hago…» (`4b05edba`). Columna editorial: 5 → 3 hijos.
5. Conservados: un formulario, ocho campos, correo, consentimiento, opciones del selector.
6. Breakpoint: dos columnas solo con ancho suficiente; una columna en 1024 e inferiores (regla `pp.css` acotada a `.pp-grid2:has(form)`).
7. CSS correctivo retirado: ninguno todavía; la regla `[data-id="63deb5ba"]` del hero no aplica a esta página y se evalúa en la Home.

Nodos: 31 → 29. Raíces: 1.

## Gate 4A — resultado medido

| Bloque | Requisito | Estado | Evidencia |
|---|---|---|---|
| Estructura | una raíz | ✅ | 1 raíz en `_elementor_data` |
| Estructura | un formulario | ✅ | `<form>` = 1 en HTML servido |
| Estructura | ocho campos | ✅ | 8 controles, nombres `nombre, organizacion, cargo, correo, telefono, area, e-form-textarea-13, consentimiento` |
| Estructura | flexboxes con dirección explícita | ✅ | `.pp-stack{display:flex;flex-direction:column;…}` compilado en `global-2095-frontend-desktop.css` |
| Estructura | columnas con `pp-stack` | ✅ | 4 nodos con la clase |
| Estructura | sin clases ad hoc | ✅ | clases por id `g-*` resueltas contra `elementor://global-classes` |
| Estructura | sin nodos duplicados | ✅ | 3 hijos en la columna, 1 `e-form` |
| Editor | contenido editable y orden comprensible | ⏳ | no verificado visualmente; el árbol conserva jerarquía y orden |
| Frontend | 1440: dos columnas equilibradas | ✅ | col 568 px / form 568 px, gap 24/16, `overflow: -15` (nulo) |
| Frontend | 1024: una columna | ✅ | inputs a 860 px de ancho útil (antes 390 en dos columnas) |
| Frontend | 390: una columna, sin desborde | ✅ | orden vertical texto → formulario, sin contenido cortado |
| Frontend | 320: sin desborde | ⚠️ | captura sin desborde, pero el ancho útil medido (155 px) es menor al esperado; medir en dispositivo real |
| Frontend | contraste AA | ✅ | `#586A70` = 5,43:1 sobre marfil |
| Funcional | envío aceptado | ✅ | `form-state-success` tras `requestSubmit()` |
| Funcional | mensaje de éxito visible | ✅ | «Recibido. Te respondo personalmente en un día hábil.» |
| Funcional | consentimiento obligatorio | ✅ | checkbox `required`, bloquea el envío sin marcar |
| Funcional | validación de campos | ✅ | 4 requeridos bloquean el envío vacío |
| Funcional | **opción inicial del selector inválida** | ❌ | «Selecciona un área» se envía como valor: el `value` renderizado es la etiqueta, no vacío |
| Funcional | correo entregado / Reply-To | ⏳ | verificación manual del usuario |

**Resultado: 16 de 18 cumplen, 1 falla, 1 pendiente de verificación manual, 1 con reserva de medición.**

## Dos hallazgos técnicos que cambian el método

1. **Las clases globales se referencian por `id`, no por etiqueta.** Escribir `"pp-stack"` en `_elementor_data` produce el atributo `class="pp-stack"` en el HTML pero **ninguna regla CSS**: el compilador resuelve ids (`g-0e352b6`) y descarta etiquetas. Síntoma exacto: la clase aparece en el DOM y el layout no cambia.
2. **El CSS y el HTML de cada página se compilan y congelan en el primer render.** Escribir `_elementor_data` por REST no invalida ni el CSS ni la caché de elementos, y publicar el kit tampoco. Una página nueva con los datos corregidos nace con CSS limpio: eso permitió validar el piloto sin depender de la regeneración manual.

Corolario operativo: para pilotos, construir en página nueva y medir ahí; para reparar en el lugar, la regeneración de Elementor es obligatoria.

## Errores propios durante el piloto

- La primera inserción de la regla de 1024 px se hizo con búsqueda de la primera llave de cierre y **rompió el bloque `@media` de `pp.css`** (dejó `.pp-grid3` fuera del media y una llave huérfana). Detectado al leer el bloque servido, corregido con reconstrucción explícita del bloque y verificación de balance de llaves (48/48).
- La regla de 1024 se había acotado al `page-id-2093`, una copia ya eliminada. Sustituida por `.pp-grid2:has(form)`, que no depende de ids ni de páginas.
- Se crearon cinco copias sucesivas durante el diagnóstico (2088, 2090, 2091, 2092, 2093); todas borradas. Queda solo `2095`.

## Decisión pendiente

La opción inicial del selector no es inválida. Tres salidas:

| Salida | Efecto | Coste |
|---|---|---|
| Quitar `required` del selector | se puede enviar sin área; pierdes la clasificación del lead | cero |
| Sustituir el selector por campo de texto libre | siempre válido, sin clasificación | bajo |
| Aceptar el defecto | un visitante puede enviar «Selecciona un área» | cero, deuda visible |

## Estado de `/contacto/` (página 14)

Reparada y **publicada el 23-10-2026** tras la aprobación del gate. Respaldo previo en `backup_14_antes_piloto.json`.

Verificación en el navegador sobre la URL pública:

| Dato | Antes | Ahora |
|---|---|---|
| `pp-stack` en el HTML | 0 | 6 |
| Controles | 8 (uno era `<select>`) | 8, `area` como texto libre |
| `<select>` | 1 | 0 |
| `flex-direction` de la columna editorial | row (heredado) | column |
| Columnas | desbordaban a 1024 | 568 / 568 px, gap 20 px |
| Texto de los dos bloques retirados | presente | 0 apariciones |
| Desborde horizontal | sí en móvil | no |
| Envío | sin verificar | `form-state-success` ×3 |

El desbloqueo no fue la regeneración manual: **`elementor-update-page-settings` del MCP invalida la caché de elementos**. Con eso la transferencia desde la copia quedó completa, sin un clic del usuario. Registrado en `elementor-mcp-design/references/class-and-cache-traps.md`.

Reserva: el gap medido es 20 px y el contrato pedía 24/16. Se deja como está y se corrige al construir la Home, para no reabrir el piloto.
