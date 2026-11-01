# Sistema de diseño y construcción — entrega A–H

**Fecha:** 24 de octubre de 2026
**Estado:** skills creadas; ninguna página pública modificada.
**Skills:** `pennacchiotti-web-design-system` · `elementor-atomic-builder` · `elementor-atomic-mcp` (técnica, existente)

---

## Diagnóstico nuevo: la causa real del descuadre

Revisé el árbol actual de `/contacto/` (post 14) antes de escribir nada. El diagnóstico del brief acierta en el síntoma y **no** en la causa: el árbol **no está plano**.

```
e-flexbox                    (1 hijo)
└── e-flexbox                (1 hijo)
    └── e-flexbox            (2 hijos: texto | formulario)
        ├── e-flexbox        (5 hijos: eyebrow, h1, p, p, p)
        └── e-flexbox        (1 hijo: e-form con 18 hijos)
```

Es un layout de dos columnas con tres niveles. **Corrección (24-oct):** la primera lectura de este diagnóstico fue errónea. El árbol guarda las clases por `id`, y `elementor://global-classes` confirma que `g-e75c1b0` = `pp-band`, `g-c030200` = `pp-wrap`, `g-166b808` = `pp-grid2`, `g-fc5a2a0` = `pp-h1`. Las 22 clases del kit existen y están aplicadas. La tabla siguiente compara etiqueta esperada con id almacenado, no con una ausencia:

Lo que sí está roto, verificado en los settings de los cinco `e-flexbox` de la página: **ninguno declara `flex-direction`**, y los dos nodos de columna (texto y formulario) **no tienen ninguna clase**. Como `e-flexbox` nace en `row`, los cinco hijos de la columna de texto (eyebrow, h1, tres párrafos) se reparten en fila y compiten por el ancho. Eso es exactamente lo que muestra la captura.

| Nodo | Clases que debería tener | Clases que tiene |
|---|---|---|
| sección | `pp-band`, `pp-band--ivory` | `g-e75c1b0`, `g-57286d5` |
| contenedor | `pp-wrap` | `g-c030200` |
| layout | `pp-grid2` | `g-166b808` |
| columna de texto | — | *(vacía)* |
| eyebrow | `pp-eyebrow` | `g-1208f77` |
| h1 | `pp-h1` | `g-fc5a2a0` |
| párrafos | `pp-body` | `g-7233314`, `g-c855423` |
| botón | `pp-cta` | `g-9dfc77b` |

**Cada nodo usa una clase global del kit, almacenada por id.** El sistema sí está aplicado; lo que falta es la propiedad que resuelve la dirección del flujo. Ahí está el descuadre: `e-flexbox` sin `flex-direction` es una fila, y una fila de cinco bloques de texto no es una columna editorial.

Esto también explica por qué terminé escribiendo CSS con `[data-id="…"]`: estaba compensando una dirección no declarada, exactamente lo que el brief prohíbe. Ese CSS debe retirarse cuando el árbol se reconstruya con `pp-stack` en las columnas.

**Consecuencia para el método:** el punto de control no es solo «¿hay tres niveles?», sino **«¿cada contenedor declara su dirección, y cada columna lleva su clase?»**. Un árbol con niveles correctos, clases aplicadas y contenedores en fila por defecto sigue siendo un árbol inválido.

---

## A. Índice de las skills

### `pennacchiotti-web-design-system`

| Archivo | Contenido |
|---|---|
| `SKILL.md` | 14 secciones: regla 0 (contrato obligatorio), marca, paleta con contrastes medidos, tipografía, espaciado, contenedores, grid, breakpoints, clases, patrones, componentes, accesibilidad, motion, antipatrones, criterios de aceptación, flujo |
| `references/tokens.md` | Tokens reales del kit, deuda registrada (`muted #85979B` a 2,92:1), escala tipográfica, espaciado, contenedores, breakpoints, convención de nombres |
| `references/patterns.md` | Los 12 patrones con su árbol nodo por nodo y su comportamiento móvil |
| `templates/page-design-contract.md` | Plantilla YAML del contrato, con reglas de uso |

### `elementor-atomic-builder`

| Archivo | Contenido |
|---|---|
| `SKILL.md` | 12 secciones: inspección previa, estructura obligatoria, nombres, variables y clases, widgets complejos, modificación localizada, raíces duplicadas, responsive, verificación posterior, gate por sección, reversión, prohibiciones |
| `references/writing.md` | Formas JSON exactas (wrappers `$$type`), orden de operaciones, trampas comprobadas, pseudocódigo de verificación |
| `references/qa-checklist.md` | Checklist por sección y por página, y señales de detenerse |
| `templates/section-build-log.md` | Registro de cambio sin git |

`elementor-atomic-mcp` se mantiene como manual técnico del MCP; el builder lo referencia y no lo duplica.

---

## B. Reglas obligatorias

1. Ninguna página se construye sin Page Design Contract aprobado.
2. Una sección, una responsabilidad.
3. Tres niveles mínimos: sección → contenedor → layout.
4. Dos o más columnas → grid; una dirección → stack. Flex-row solo para acciones.
5. Toda clase usada existe en el kit y es **compartida**, no generada por nodo.
6. Cero estilos locales salvo las tres excepciones registradas (fondo del hero, `aspect-ratio` de una imagen, color del velo).
7. Sin CSS nuevo para corregir una sección: si hace falta, el árbol está mal.
8. Móvil se define por orden de lectura, no reduciendo tamaños.
9. Una sección por gate: construir → regenerar → capturar → comparar → aprobar.
10. Sin captura no hay aprobación.
11. Si el render no refleja los datos, se regenera; no se sigue construyendo.
12. Todo cambio deja registro con respaldo y forma de reversión.

---

## C. Antipatrones

- Texto, imagen o formulario sueltos en la raíz.
- Clases generadas por nodo en lugar de clases del sistema.
- `position: absolute` o márgenes negativos para resolver solapamiento.
- `overflow: hidden` como arreglo.
- Reducir fuente para que quepa.
- CSS dirigido a `data-id` o a un ID.
- `display: none` para esconder lo que no se supo maquetar.
- Reglas globales sobre `.entry-title` que rompen los artículos.
- Contenido en `::after` para evitar el árbol.
- Duplicar una sección para «probar».
- Reconstruir con `build-composition` sobre una página existente (agrega raíces).
- Publicar con placeholders, cifras sin validar o marcas demo.
- Construir siete secciones y revisar al final.

---

## D. Estructura de archivos

```
skills/devops/
├── pennacchiotti-web-design-system/
│   ├── SKILL.md
│   ├── references/
│   │   ├── tokens.md
│   │   └── patterns.md
│   └── templates/
│       └── page-design-contract.md
├── elementor-atomic-builder/
│   ├── SKILL.md
│   ├── references/
│   │   ├── writing.md
│   │   └── qa-checklist.md
│   └── templates/
│       └── section-build-log.md
└── elementor-atomic-mcp/
    └── SKILL.md
```

Documentos de proyecto:

```
03_Desarrollo/04_WEB/Pennacchiotti.cl/docs/
├── FASE0-estado-y-propuesta-v1.md
├── SOLUCIONES-copy-v1.md
├── SISTEMA-DISENO-CONSTRUCCION-v1.md
└── contratos/
    ├── contacto-v2.contract.yaml
    └── registro-de-cambios.yaml
```

---

## E. Checklist de QA

Por sección: raíces del contrato, tres niveles, clases del kit compartidas, sin estilos locales, un `h1`, jerarquía sin saltos, 1440/1024/768/390/320 sin desborde ni solapamiento, contraste AA, foco visible, capturas tomadas, captura = editor, registro escrito.

Por página: un formulario, campos con etiqueta y `name`, envío almacenado, correo verificado por una persona, CTA con destino real, footer sin marcas demo, menú navegable, título/descripción/canonical únicos, sin placeholders, imágenes < 200 KB en hero, caché regenerada y verificada con query única.

Señales para detenerse: el HTML no refleja lo guardado; dos formularios; hay que agregar CSS por `data-id`; hay que ocultar algo con `display:none`.

---

## F. Page Design Contract — Contacto V2

```yaml
page: contacto
objective: iniciar una conversación comercial calificada
audience: gerente de operaciones que ya sabe que su proceso depende de personas
status: draft
version: 2

sections:
  - id: contact-main
    purpose: presentar el contexto de la conversación y capturar el contacto
    pattern: contacto
    layout:
      1440: two-columns-5-7
      1024: two-columns-5-7
      768: one-column
      390: one-column
      320: one-column
    components: [editorial-intro, contact-form]
    content:
      h1: Conversemos sobre el proceso que hoy depende de personas clave.
      lead: Cuéntame qué está pasando en tu operación. Respondo personalmente en un día hábil.
      cta: Solicitar conversación inicial → envío del formulario
    assets:
      image: ninguna
      alt: —

responsive:
  order_mobile: [intro, form]
  hidden_mobile: []
  reflow: [el formulario pasa a ancho completo tras el intro]

tokens:
  container: default
  colors: pp-band--ivory, color-text, color-text-muted
  type: pp-h1, pp-lead, pp-body, pp-eyebrow
  spacing: banda 112/80/64, gap 64 (escritorio) / 32 (móvil)

acceptance:
  - no-horizontal-scroll (1440, 1024, 768, 390, 320)
  - no-overlap
  - one-h1
  - form-usable-with-keyboard
  - contrast-aa
  - spacing-on-scale
  - screenshot-matches-editor
  - un-solo-form
  - area-de-interes-con-etiquetas-legibles
  - primera-opcion-no-valida

risks:
  - el widget e-form exige hijos de mensaje; sin ellos no renderiza
  - la caché de render puede congelar el frontend tras escribir por REST

reversal:
  - backup_14.json
  - restaurar por REST + publish-document + purge
```

---

## G. Plan piloto — Contacto V2

**Objetivo:** reconstruir una sola sección con el método completo y demostrar que el sistema funciona antes de tocar cualquier otra página.

| Paso | Acción | Evidencia de cierre |
|---|---|---|
| 1 | Congelar `/contacto/`: respaldo de `_elementor_data`, captura 1440 y 390 del estado actual | `backup_14.json`, dos capturas |
| 2 | Auditar clases del kit: cuáles existen, cuáles están vacías, cuáles son generadas (`g-*`) | listado de clases con su definición |
| 3 | Ejecutar la acción pendiente de regeneración (CSS y datos) y confirmar que el frontend refleja los datos | HTML con etiquetas legibles y placeholders |
| 4 | Reconstruir el árbol con clases del kit: sección → `pp-wrap` → `pp-grid2` → intro / form-wrapper | árbol con clases compartidas, 1 raíz |
| 5 | Retirar del child las reglas con `[data-id]` que compensaban el árbol roto | `pp.css` sin selectores por ID |
| 6 | Medir 1440/1024/768/390/320: ancho de columnas, overflow, `h1`, formulario | tabla de medición |
| 7 | Capturas y auditoría visual contra el contrato | capturas aprobadas |
| 8 | Prueba funcional: envío real, almacenamiento, correo (verificación humana) | envío visible en Elementor + correo recibido |
| 9 | Registro de cambio y aprobación | entrada en `registro-de-cambios.yaml` |

**Duración estimada:** una sesión de trabajo, con dos puntos de parada obligatorios (paso 3 y paso 7).

**Criterio de fracaso:** si en el paso 3 el frontend no refleja los datos, el piloto se detiene y no se reconstruye nada hasta que la regeneración sea verificable.

---

## H. Condiciones antes de reconstruir la Home

1. `/contacto/` aprobada como piloto: árbol con clases del kit, cinco anchos validados, formulario funcionando.
2. Clases del kit auditadas: sin duplicados, sin clases generadas por nodo, `muted` corregido o reemplazado por `#586A70` en la práctica.
3. CSS compensatorio eliminado del child (selectores por `data-id`, `display:none` de relleno).
4. Copy de la Home aprobado por escrito, con la evidencia validada o excluida.
5. `/soluciones/` aprobada y publicada: el menú de cinco ítems no puede existir antes.
6. Footer definitivo definido (marca, navegación, contacto, legal, año).
7. Caché y regeneración bajo control: procedimiento probado al menos dos veces.
8. Registro de cambios en uso, con un piloto ya documentado.

Ninguna de estas condiciones es técnica en sentido estricto: todas son de método. La Home es la página más visible; reconstruirla con el sistema sin probar es repetir el error en cuatro veces más superficie.

---

## Lo que no hice

- No modifiqué ninguna página pública mientras diseñaba las skills.
- No construí Contacto V2.
- No creé el menú ni el footer.
- No publiqué `/soluciones/`.

Lo que sí está pendiente y fuera de mi alcance: la regeneración de CSS y datos desde la interfaz de Elementor, que sigue siendo el interruptor que destraba el render.
