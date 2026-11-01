# Checklist de validación Impeccable — aplicado al MCP de Elementor

**Función:** capa de diseño y auditoría del sistema. No escribe en Elementor; dictamina antes (shape) y después (critique, audit, polish).
**Fuente:** doctrina Impeccable (pbakaus/impeccable, Apache 2.0) + guía propia del MCP (`elementor://style/best-practices`).
**Uso:** se ejecuta sobre el contrato (antes) y sobre el render (después). Cada casilla se responde con evidencia: nodo, clase, medida o captura.

---

## A. Antes de construir — shape

- [ ] Modo de superficie declarado (Persuade / Operate / Read / Experience).
- [ ] Objetivo del visitante en una frase, con la acción primaria.
- [ ] Inventario de secciones: una responsabilidad por sección.
- [ ] `node_tree` completo con rol, clases y `container_contract` por nodo.
- [ ] `cardinality` declarada (raíces, secciones, layouts, formularios, h1, botones).
- [ ] `forbidden` explícito.
- [ ] Breakpoints con decisión de apilado y umbral de ancho por columna.
- [ ] Copy revisado contra PRODUCT.md (lenguaje, cifras publicables).
- [ ] Evidencia: toda cifra tiene fuente propia o se elimina.

## B. Después de construir — critique

- [ ] Squint test: se distinguen primario, secundario y grupos en orden.
- [ ] Jerarquía con escalón ≥ 1,25× entre roles (ideal ≥ 3× titular/cuerpo).
- [ ] Densidad y ritmo: hay intervalos apretados y generosos, no un solo valor.
- [ ] La página no es solo texto y bandas: hay imagen, figura o diagrama pertinente.
- [ ] Cada sección cumple una sola responsabilidad.
- [ ] El copy nombra problemas concretos; cero buzzwords.
- [ ] Cadencia: no todas las secciones cierran con la misma fórmula («X. No Y.»).

## C. Después de construir — audit (medible)

| Comprobación | Umbral | Instrumento |
|---|---|---|
| Overflow horizontal | 0 px en 1440/1200/1024/768/390/320 | navegador |
| Intersección de bloques no relacionados | 0 | captura + medición |
| Texto cortado u ocluido | 0 | captura |
| Controles fuera del viewport | 0 | medición |
| Ancho form vs wrapper | ≤ 1 px de diferencia | medición |
| Contraste cuerpo | ≥ 4,5:1 | cálculo |
| Contraste texto grande | ≥ 3:1 | cálculo |
| Medida de línea | 45–75 caracteres | medición |
| Interlínea de cuerpo | ≥ 1,5× | clase/variable |
| Tamaño mínimo de cuerpo | ≥ 15 px | clase/variable |
| Tracking de cuerpo | ≤ 0,05em | clase/variable |
| CLS en carga | < 0,1 | navegador |
| Un solo h1 / un solo form | exacto | árbol + HTML |
| Contenedores sin dirección | 0 | `get-page-structure` |
| Nodos de columna sin clase estructural | 0 | `get-page-structure` |
| Clases no registradas en el kit | 0 | `elementor://global-classes` |
| Estados del formulario | hover, focus, error, éxito, disabled | render |
| Browser surfaces | selección, caret, focus-visible, scrollbar | CSS/captura |
| Reduced motion | respetado | CSS |

## D. Antipatrones Impeccable — verificación puntual

Prohibiciones duras (si aparecen, la sección se rechaza):

- [ ] Sin etiqueta pequeña sobre un titular (`kicker-above-heading`, `hero-eyebrow-chip`).
- [ ] Sin texto con degradado (`gradient-text`).
- [ ] Sin halos ni focos radiales (`dark-glow`, `radial-halo`).
- [ ] Sin tarjetas anidadas ni icono en tile sobre título (`nested-cards`, `icon-tile-stack`).
- [ ] Sin marquesina, cursor parpadeante ni punto pulsante decorativo.
- [ ] Sin superficies de rayas o rejilla (`repeating-stripes-gradient`, `codex-grid-background`).
- [ ] Sin emoji como iconos.
- [ ] Sin imágenes rotas ni contenido invisible al cargar.

Defaults a justificar por escrito si se usan:

- [ ] Fuente sobreusada (Inter, Roboto, Fraunces, Geist, Plus Jakarta, Space Grotesk).
- [ ] Paleta morada/cian; crema por reflejo.
- [ ] Espaciado monótono; jerarquía tipográfica plana.
- [ ] Titular serif itálico gigante; números de sección sin información.
- [ ] Borde de 1px + sombra difusa ancha en cada tarjeta.
- [ ] H1 de frase completa a tamaño display.
- [ ] Buzzwords, cadencia aforística, saturación de guiones largos.

## E. Después de corregir — polish

- [ ] Foco visible y con orden lógico.
- [ ] Selección de texto y caret con color de la paleta.
- [ ] Subrayados con offset legible.
- [ ] Numerales tabulares donde hay datos.
- [ ] Transiciones de 180–250 ms en controles, sin rebote.
- [ ] Imágenes: peso objetivo (hero ≤ 120 KB), `alt` correcto.
- [ ] Textos de error que nombran el problema y la recuperación.
- [ ] Sin placeholders, sin datos de prueba, sin «Lorem».

## F. Cierre de la sección

- [ ] Captura 1440 y 390 archivadas como baseline.
- [ ] Comparación con la baseline anterior sin diferencias no intencionadas.
- [ ] Checklist del contrato punto por punto.
- [ ] Registro de cambio escrito con reversión posible.
- [ ] Aprobación humana antes de la sección siguiente.

---

## Quién hace qué

| Capa | Rol | No hace |
|---|---|---|
| Impeccable (esta checklist) | shape, critique, audit, polish | no escribe en Elementor |
| `pennacchiotti-web-design-system` | identidad, tokens, patrones, aceptación | no traduce a nodos |
| `elementor-atomic-builder` | traduce el contrato a nodos y clases | no decide estética |
| `elementor-mcp-design` | traduce doctrina a acciones de las 22 abilities | no diseña la página |
| MCP de Elementor | ejecuta | no juzga |
