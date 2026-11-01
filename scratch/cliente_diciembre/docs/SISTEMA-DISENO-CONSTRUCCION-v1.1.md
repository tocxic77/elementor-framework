# Sistema de diseño y construcción — v1.1

**Fecha de creación:** 23 de octubre de 2026
**Última actualización:** 23 de octubre de 2026, 23:40 (America/Santiago)
**Versión:** 1.1
**Estado:** borrador técnico para aprobación.

**Estado de las skills:**
- creadas y documentadas;
- revisión documental completada;
- integración de la capa Impeccable: hecha (dentro de `elementor-mcp-design`);
- piloto: **pendiente**;
- **no aptas todavía para construcción autónoma de páginas públicas**.

Sustituye a `SISTEMA-DISENO-CONSTRUCCION-v1.md`. Ninguna página pública fue modificada.

---

## 1. Diagnóstico (verificado, no inferido)

`/contacto/` (post 14) tiene un árbol de tres niveles y un `e-form` con 18 hijos. La jerarquía es correcta.

Lo que está mal, medido en los settings de los cinco `e-flexbox`:

| Hecho | Evidencia |
|---|---|
| Los contenedores **no declaran `flex-direction`** | `props: {}` en los cinco nodos |
| Los dos nodos de columna **no tienen ninguna clase** | `clases = []` en `1f557501` (texto) y `2c0536c4` (formulario) |
| Las clases del kit **sí están aplicadas** | `g-e75c1b0`=`pp-band`, `g-c030200`=`pp-wrap`, `g-166b808`=`pp-grid2`, `g-fc5a2a0`=`pp-h1` |
| El motor usa `row` por defecto | `elementor://style/best-practices`: «set `flex-direction` explicitly on every multi-child container» |

**Consecuencia:** cinco bloques editoriales se reparten en fila y compiten por el ancho. Ese es el descuadre de la captura, y se ve igual en el editor porque está en el árbol.

### 1.1 La regla, ahora verificable

> Todo `e-flexbox` declara explícitamente `display`, `flex-direction`, `flex-wrap`, `align-items`, `justify-content`, `gap`, ancho y el breakpoint donde cambia de dirección — **incluso cuando coincide con el valor por defecto**.

**Criterio de detención:** un contenedor sin dirección explícita impide aprobar la sección. No se compensa con CSS.

```yaml
# columna editorial
container_contract:
  display: flex
  direction: {desktop: column, tablet: column, mobile: column}
  wrap: nowrap
  align: stretch
  justify: flex-start
  gap: 24
  width: 100%
  min_width: 0

# grupo de acciones
container_contract:
  display: flex
  direction: {desktop: row, tablet: row, mobile: column}
  wrap: wrap
  align: center
  justify: flex-start
  gap: 16
  width: auto
```

---

## 2. Arquitectura de responsabilidades

Cinco capas, cada una con una decisión distinta. Ninguna puede tomar la decisión de otra.

| Capa | Dónde vive | Responsable de | No hace |
|---|---|---|---|
| **Impeccable** | `elementor-mcp-design` → `references/design-rules.md` + checklist de validación | shape, critique, audit, adapt, polish; umbrales medibles | no escribe en Elementor |
| **Design system PENNACCHIOTTI** | skill `pennacchiotti-web-design-system` | identidad, tokens, patrones autorizados, responsive, motion, aceptación visual | no traduce a nodos |
| **Builder Elementor** | skill `elementor-atomic-builder` | traducir el contrato a nodos, definir contenedores, aplicar clases, controlar dirección y wrapping, evitar duplicaciones | no decide estética |
| **Manual del MCP** | skill `elementor-mcp-design` | schemas, wrappers, comandos, caché, publicación, trampas | no diseña páginas |
| **MCP de Elementor** | 22 abilities | ejecutar lo aprobado | no juzga |

**Integración de Impeccable:** no es una capa separada que decide diseño, sino la **vara de medir** del sistema: entra antes de construir (shape) y después de construir (critique, audit, polish), siempre sobre el render. Se eliminó el skill genérico que la contenía por separado; su doctrina vive dentro del sistema exclusivo del MCP.

### Pipeline

```
PRODUCT.md → DESIGN.md → shape (Impeccable) → Page Design Contract
→ elementor-atomic-builder → MCP Elementor → publish + purge
→ captura → critique/audit (Impeccable) → corrección estructural
→ polish → aprobación humana → baseline
```

---

## 3. Fuentes canónicas

| Documento | Contiene | No contiene |
|---|---|---|
| `PRODUCT.md` | oferta, clientes, problemas, resultados, lenguaje, evidencia aprobada, CTA, límites contractuales | decisiones visuales |
| `DESIGN.md` | dirección editorial, tokens, tipografía, layout, patrones, motion, imágenes, accesibilidad, responsive, antipatrones, deuda | copy comercial |
| `contacto-v2.contract.yaml` | la página concreta: `node_tree`, `container_contract`, `cardinality`, `forbidden`, aceptación | reglas generales |
| skills | procedimiento y reglas de construcción | duplicar PRODUCT/DESIGN |

Las skills **consultan** estos documentos y no los copian. Si un dato aparece en dos sitios y difieren, gana el código hasta que se corrija uno de los dos, y la discrepancia se registra.

---

## 4. Diagnóstico, norma y procedimiento (separados)

- **Diagnóstico:** qué está roto hoy, con evidencia medida. Vive en este documento y caduca al repararse.
- **Norma:** qué debe cumplirse siempre. Vive en PRODUCT.md, DESIGN.md y en las reglas de las skills.
- **Procedimiento:** cómo se ejecuta y se verifica. Vive en el builder y en los checklists.

Un diagnóstico no se convierte en norma sin generalizarse. «Faltaba `flex-direction` en Contacto» (diagnóstico) se convirtió en «todo contenedor declara dirección» (norma).

---

## 5. Clases estructurales

### 5.1 Inventario real (22 clases globales registradas)

`pp-wrap`, `pp-band`, `pp-band--ink`, `pp-band--ivory`, `pp-band--sage`, `pp-band--gray`, `pp-eyebrow`, `pp-h1`, `pp-h2`, `pp-h3`, `pp-lead`, `pp-body`, `pp-cta`, `pp-cta--ghost`, `pp-cta-row`, `pp-card`, `pp-grid2`, `pp-grid3`, `pp-muted`, `pp-ink-band-text`, `pp-hero-img`, `pp-figure`.

### 5.2 Clases que faltan y hay que crear antes del piloto

| Clase | Definición | Estado |
|---|---|---|
| `pp-stack` | `display:flex; flex-direction:column; align-items:stretch; justify-content:flex-start; min-width:0; width:100%` | **no existe** |
| `pp-stack--sm` | solo `gap: 16px` | **no existe** |
| `pp-stack--md` | solo `gap: 24px` | **no existe** |
| `pp-stack--lg` | solo `gap: 40px` | **no existe** |
| `pp-cluster` | `display:flex; flex-direction:row; flex-wrap:wrap; align-items:center; gap:16px` | **no existe** |

Las variantes **solo cambian el gap**. No duplican las propiedades del stack: se aplican junto a `pp-stack`, que es la que declara la dirección.

### 5.3 Regla semántica (corregida)

- Contenido editorial vertical → **stack**.
- Acciones, metadatos, piezas de ancho intrínseco, filas que deben envolver → **cluster** (flex row con wrap).
- Columnas estructurales de contenido → **grid**.
- Un flex row libre nunca simula un grid.

La versión anterior decía «dos o más columnas siempre grid». Era una barrera contra el error, no una norma de diseño: navegación, grupos de botones y metadatos son legítimamente rows.

---

## 6. Los `g-*`: id interno, no clase ad hoc

Contradicción corregida. Hay dos cosas distintas:

| Concepto | Ejemplo | Veredicto |
|---|---|---|
| **Id interno de una clase global registrada** | `g-e75c1b0` → `pp-band` | **Válido.** Es cómo Elementor guarda el árbol |
| **Clase ad hoc no registrada** | una clase que solo existe para un nodo, sin nombre semántico, sin registro global, o duplicando otra | **Inválida** |

**Regla:** no se rechaza una clase por empezar con `g-`. Se resuelve el id contra `elementor://global-classes` y se valida que corresponda a una clase compartida y aprobada. Validar con el registro, nunca por la forma del id.

---

## 7. Page Design Contract ampliado

Campos obligatorios (plantilla en `pennacchiotti-web-design-system/templates/page-design-contract.md`, ejemplo aplicado en `contratos/contacto-v2.contract.yaml`):

- `node_tree` — cada nodo con `role`, `classes`, `container_contract` e hijos.
- `container_contract` — las ocho propiedades por breakpoint.
- `cardinality` — raíces, secciones, layouts, formularios, h1, botones.
- `forbidden` — prohibiciones explícitas, incluida `unclassified_flexbox`.
- `editor_acceptance` — criterios del editor.
- `frontend_acceptance` — umbrales medibles.
- `regression` — baselines por viewport.

Sin `node_tree` y `cardinality`, dos ejecuciones producen páginas distintas. Con ellos, el resultado es reproducible.

---

## 8. Responsive: 1024 se apila

El contrato anterior mantenía 5/7 en 1024. Con un H1 de frase completa y ocho campos, esa anchura comprime el formulario. Corregido:

| Ancho | Contacto |
|---|---|
| 1440 | 2 columnas 5/7 |
| 1200 | 2 columnas 5/7 |
| 1024 | **1 columna** |
| 768 | 1 columna |
| 390 | 1 columna |
| 320 | 1 columna |

**Regla de apilado basada en contenido:** se apila cuando el texto no conserva 420 px o el formulario 480 px. Más robusta que depender solo del viewport.

---

## 9. QA en tres capas

| Capa | Pregunta | Instrumento |
|---|---|---|
| **Estructura** | ¿árbol, clases y cardinalidad correctos? | `get-page-structure`, `elementor://global-classes` |
| **Editor** | ¿editable, legible, sin superposición, sin elementos inaccesibles? | Elementor con paneles abiertos |
| **Frontend** | ¿composición, responsive, estilo, interacción, rendimiento? | navegador + captura |

Se jubiló la fórmula «captura = editor»: el editor reduce el ancho y añade paneles. Exigir identidad píxel a píxel era un criterio falso. El editor debe conservar estructura, orden, legibilidad y ausencia de superposición; el frontend debe coincidir con el diseño aprobado en el ancho objetivo.

### 9.1 Umbrales de aceptación

| Métrica | Umbral |
|---|---|
| Overflow horizontal | 0 px en 1440/1200/1024/768/390/320 |
| Intersección de bloques no relacionados | 0 |
| Texto cortado u ocluido | 0 |
| Controles fuera del viewport | 0 |
| Ancho form vs wrapper | ≤ 1 px de diferencia |
| Contraste | AA (4,5:1 cuerpo, 3:1 grande) |
| Cambio de layout | en el breakpoint declarado |
| CLS en carga | < 0,1 |
| Medida de línea | 45–75 caracteres |
| H1 en escritorio | 12–15 palabras por línea como máximo |

### 9.2 Regresión visual

Cada viewport aprobado deja baseline: `contacto-v2-1440.png`, `-1024`, `-768`, `-390`, `-320`. Toda modificación posterior se compara contra esas capturas. «Sin captura no hay aprobación» se mantiene, ahora con umbrales que dicen **cómo** se evalúa la captura.

### 9.3 Rendimiento — cómo se mide

Un umbral sin instrumento no es criterio de aprobación. Los tres se miden con la misma corrida:

| Métrica | Umbral | Instrumento | Condición |
|---|---|---|---|
| LCP | < 2,5 s | Lighthouse móvil (preset *mobile*, throttling por defecto) sobre la URL productiva | p75 de 3 corridas; se descarta la primera |
| INP | < 200 ms | Datos de campo (CrUX / Search Console) | solo con tráfico suficiente para no ser ruido; mientras no lo haya, `N/A` |
| CLS | < 0,1 | Lighthouse móvil + inspección del árbol | obligatorio siempre |

`N/A` es un resultado válido cuando el instrumento no aplica; una cifra de laboratorio presentada como dato de campo no lo es. El informe de la corrida se archiva junto a las capturas de baseline (§9.2).

---

## 10. Estilos locales: excepción justificada, no lista cerrada

Los estilos locales están prohibidos por defecto. Toda excepción exige: justificación escrita, registro en el log de cambio y demostración de que no corresponde crear una clase reutilizable.

Casos típicos que pueden justificarse: posición de recorte y `object-position` de una imagen, orden responsive excepcional, ancho máximo único de una ilustración, relación de aspecto de un gráfico puntual.

La lista cerrada de tres excepciones era dogmática; el criterio de justificación registrada protege el sistema sin bloquear casos legítimos.

---

## 11. Gate: reparar o reconstruir

### 11.1 Criterio

**Reparar** si: hay una raíz, el anidamiento es correcto, no hay duplicados, las clases globales están aplicadas y basta corregir dirección y contenido.

**Reconstruir** si: hay estilos locales irreconciliables, el widget está en una rama incorrecta, las propiedades están corruptas, el editor no permite trabajar, hay múltiples raíces, o la reparación exigiría CSS compensatorio.

**Aplicado a `/contacto/`:** una raíz, tres niveles, un formulario, clases aplicadas, sin duplicados. El criterio apunta a **reparación**, no a reconstrucción.

### 11.2 Reparación mínima (borrador)

1. Crear `pp-stack`, `pp-stack--sm`, `pp-stack--md`, `pp-cluster` con `manage-classes`.
2. Aplicar `pp-stack` + `pp-stack--md` a la columna editorial (`1f557501`).
3. Aplicar `pp-stack` + `pp-stack--sm` al wrapper del formulario (`2c0536c4`).
4. Declarar `flex-direction: column` explícito en los cinco contenedores.
5. Reducir los párrafos del intro de cinco a tres.
6. Retirar de `pp.css` los selectores por `data-id`.
7. Regenerar, capturar, medir y comparar contra el contrato.

Si el resultado cumple, no se reconstruye nada y la configuración del formulario se conserva intacta.

---

## 12. Plan piloto v2

| Paso | Acción | Gate |
|---|---|---|
| **0** | Decidir reparar o reconstruir con la evidencia del §11 | decisión escrita |
| 1 | Congelar: `backup_14.json` + capturas 1440/390 del estado actual | respaldo verificado |
| 2 | Auditar clases: registro global, `DUP_`, huecos (`pp-stack`, `pp-cluster`) | inventario |
| 3 | Crear las clases estructurales faltantes | `manage-classes` sin `DUP_` |
| 4A | Reparación mínima del §11.2 | **Gate 4A**: si cumple, saltar a 6; si falla, revertir y pasar a 4B |
| 4B | Reconstrucción de Contacto V2 según `node_tree` | solo si 4A falla |
| 5 | Regenerar CSS y datos desde la interfaz y verificar el render | HTML refleja los datos |
| 6 | Medir 1440/1200/1024/768/390/320 con umbrales del §9.1 | tabla de medición |
| 7 | Critique + audit + polish con checklist Impeccable | checklist completo |
| 8 | Prueba funcional: envío, almacenamiento, correo (verificación humana) | envío + correo |
| 9 | Baseline de capturas y registro de cambio | aprobación humana |

**Dos puntos de parada obligatorios:** el Gate 4A y el paso 7. Ninguno se salta por prisa.

---

## 13. Condiciones antes de reconstruir la Home

1. Contacto aprobada con el método completo (pasos 0–9).
2. `pp-stack`, `pp-cluster` y variantes creadas, con CSS verificado en el render.
3. Sin contenedores sin dirección en ninguna página.
4. CSS compensatorio eliminado de `pp.css` (selectores por `data-id`).
5. Variable `muted` corregida o reemplazada en la práctica por `#586A70`.
6. Copy de la Home aprobado, con evidencia validada o eliminada.
7. `/soluciones/` aprobada y publicada: sin ella no hay menú de cinco ítems.
8. Footer definitivo definido.
9. Regresión visual operativa: baseline por viewport en las páginas publicadas.

---

## 14. Gobernanza de tokens, patrones y skills

| Qué | Quién decide | Cómo se cambia |
|---|---|---|
| Token (color, tamaño, fuente) | Mario | se cambia en el kit por `manage-global-variable` y se refleja en DESIGN.md el mismo día |
| Clase estructural | Mario | se crea/actualiza por `manage-classes` con justificación; se registra en DESIGN.md |
| Patrón de composición | Mario | se documenta en `patterns.md` antes de usarse dos veces |
| Regla de construcción | derivada de un defecto medido | se añade al builder solo si generaliza un diagnóstico |
| Contrato de una página | Mario aprueba | se versiona; cambiar el contrato invalida las capturas baseline |

Regla: **ningún cambio de token o clase entra por CSS del theme ni por estilo local.** Si no cabe en el kit, la decisión no está tomada.

---

## 15. Diff conceptual frente a v1

| # | v1 | v1.1 | Motivo |
|---|---|---|---|
| 1 | Impeccable ausente de la arquitectura | capa de shape/critique/audit/polish dentro de `elementor-mcp-design` | evita cuatro capas decidiendo diseño |
| 2 | Diagnóstico narrado | regla verificable + `container_contract` de 8 propiedades | un diagnóstico no impide repetir el error |
| 3 | «Dos o más columnas → grid» | grid para columnas, stack para flujo, cluster para acciones | flex es semánticamente correcto en varios casos |
| 4 | `pp-stack` mencionada sin definir | definida, con variantes de gap y `pp-cluster`, marcadas como **no existentes** | no se puede aplicar una clase que no existe |
| 5 | `g-*` tratado ambiguamente | id interno válido vs clase ad hoc inválida | evitar el error de diagnóstico que ya cometí |
| 6 | Contrato con layout y contenido | + `node_tree`, `cardinality`, `forbidden`, aceptación por capa | dos ejecuciones deben producir la misma página |
| 7 | 5/7 en 1024 | 1 columna en 1024 + regla de 420/480 px | riesgo real de compresión |
| 8 | «captura = editor» | QA separado: estructura / editor / frontend | el criterio anterior era falso |
| 9 | Aprobación por captura | umbrales numéricos + baselines por viewport | «se ve bien» no es verificable |
| 10 | Tres excepciones fijas a estilos locales | excepción justificada y registrada | la lista cerrada bloquea casos legítimos |
| 11 | Reconstruir el árbol | gate reparar/reconstruir + reparación mínima primero | menor riesgo, conserva el formulario |
| 12 | Sin PRODUCT.md ni DESIGN.md | ambos creados como fuentes canónicas | las skills no deben duplicar la verdad |
| 13 | Fecha 24-oct (futura) | 23-oct, versión 1.1, hora | registro técnico no se fecha adelante |
| 14 | «skills creadas» | «creadas, no validadas; piloto pendiente» | no afirmar operatividad sin prueba |
| 15 | Plan de 9 pasos | + Paso 0, 4A y 4B con gates | decisión explícita antes de tocar |
| 16 | Gobernanza ausente | tabla de quién decide y cómo se cambia | sin gobernanza, el sistema se desalinea |

---

## 16. Lo que no se hizo

- No se modificó ninguna página pública.
- No se construyó Contacto V2.
- No se crearon todavía `pp-stack`, `pp-cluster` ni sus variantes: requieren aprobación del contrato.
- No se eliminó el CSS por `data-id`: se hace en la reparación mínima, con respaldo.

**Pendiente que no depende de mí:** la regeneración de CSS y datos desde la interfaz de Elementor sigue siendo el interruptor que destraba el render.
