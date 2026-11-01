# Contacto V2 — Page Design Contract

**Estado:** borrador para aprobación. No construir hasta aprobar.
**Versión:** 2.1 (23-oct-2026)
**Página:** `/contacto/` — post 14
**Modo de superficie:** Persuade

---

```yaml
page: contacto
objective: iniciar una conversación comercial calificada
audience: gerente de operaciones que sabe que su proceso depende de personas
status: draft
version: 2.1

mode: persuade

sections:
  - id: contact-main
    purpose: introducir la conversación y capturar el contacto
    pattern: contacto

node_tree:
  - type: e-flexbox
    role: section
    classes: [pp-band, pp-band--ivory]
    container_contract:
      display: flex
      direction: {desktop: column, tablet: column, mobile: column}
      wrap: nowrap
      align: stretch
      justify: flex-start
      gap: 0
      width: 100%
      min_width: 0
    children:
      - type: e-flexbox
        role: container
        classes: [pp-wrap]
        container_contract:
          display: flex
          direction: {desktop: column, tablet: column, mobile: column}
          wrap: nowrap
          align: stretch
          justify: flex-start
          gap: 0
          width: 100%
          min_width: 0
        children:
          - type: e-grid
            role: layout
            classes: [pp-grid2]
            container_contract:
              display: grid
              columns: {desktop: "5fr 7fr", tablet: "5fr 7fr", mobile: 1}
              gap: {desktop: 64, tablet: 40, mobile: 32}
              breakpoint_stack: 1024      # por debajo de 1024, una columna
              width: 100%
            children:
              - type: e-flexbox
                role: editorial-intro
                classes: [pp-stack, pp-stack--md]
                container_contract:
                  display: flex
                  direction: {desktop: column, tablet: column, mobile: column}
                  wrap: nowrap
                  align: stretch
                  justify: flex-start
                  gap: 24
                  width: 100%
                  min_width: 0
                children:
                  - type: e-heading        # h1 único de la página
                  - type: e-paragraph      # lead
                  - type: e-paragraph
                  - type: e-paragraph
              - type: e-flexbox
                role: form-wrapper
                classes: [pp-stack, pp-stack--sm]
                container_contract:
                  display: flex
                  direction: {desktop: column, tablet: column, mobile: column}
                  wrap: nowrap
                  align: stretch
                  justify: flex-start
                  gap: 16
                  width: 100%
                  min_width: 0
                children:
                  - type: e-form           # 1 formulario, 8 campos

content:
  h1: Conversemos sobre el proceso que hoy depende de personas clave.
  lead: Cuéntame qué está pasando en tu operación. Respondo personalmente en un día hábil.
  paragraphs: 3 máximo; el tercero solo si aporta condiciones del servicio.
  cta: Solicitar conversación inicial
  fields: [nombre, organizacion, cargo, correo, telefono, area, desafio, consentimiento]

cardinality:
  page_roots: 1
  sections: 1
  layout_nodes: 1
  forms: 1
  h1: 1
  intro_paragraphs: 3
  submit_buttons: 1

forbidden:
  - position_absolute
  - negative_margin
  - data_id_css
  - overflow_hidden_as_fix
  - local_width_hacks
  - unclassified_flexbox        # contenedor sin rol, dirección y clase estructural
  - ad_hoc_class                # clase solo para un nodo, sin registro global
  - eyebrow_above_heading
  - test_content

responsive:
  order_mobile: [editorial-intro, form-wrapper]
  hidden_mobile: []
  reflow:
    - "el layout pasa a una columna por debajo de 1024 px"
    - "el formulario ocupa el 100 % del contenedor"
  stack_rule: "apilar si el texto no conserva 420 px o el formulario 480 px"

tokens:
  container: default
  colors: [ivory, ink, text, "#586A70"]
  type: [pp-h1, pp-lead, pp-body]
  spacing: [16, 24, 32, 40, 64]

editor_acceptance:
  - árbol editable sin nodos huérfanos
  - sin superposición de controles
  - jerarquía visible con los paneles abiertos
  - ningún elemento inaccesible por posición
  - el formulario se selecciona y edita como una unidad

frontend_acceptance:
  - overflow_horizontal: 0 px en 1440, 1200, 1024, 768, 390, 320
  - intersección entre bloques no relacionados: 0
  - texto cortado: 0
  - controles fuera del viewport: 0
  - diferencia de ancho form vs wrapper: ≤ 1 px
  - contraste: AA en todo texto (muted #586A70)
  - una columna en 1024 y menores
  - un solo h1, un solo form
  - CLS de carga < 0,1
  - CTA principal dentro del flujo y alcanzable con teclado
  - medida de línea del cuerpo 45–75 caracteres

regression:
  baselines: [contacto-v2-1440.png, contacto-v2-1024.png, contacto-v2-768.png, contacto-v2-390.png, contacto-v2-320.png]
  rule: "toda modificación posterior se compara contra estas capturas aprobadas"

risks:
  - "el widget e-form hereda el ancho del wrapper: sin min-width 0 desborda"
  - "1024 px con 5/7 comprime el formulario: por eso apila"
  - "la caché de elementos puede congelar el render tras escribir por REST"

reversal:
  - backup_14.json antes de tocar
  - restaurar por REST + publish-document + purge
```

## Decisiones incorporadas en 2.1

1. **1024 pasa a una columna.** Con H1 de frase completa y ocho campos, 5/7 en 1024 comprime el formulario. Se apila salvo prueba visual favorable.
2. **Tres párrafos en el intro, no cinco.** La versión anterior acumulaba texto que competía con el formulario.
3. **`pp-stack` obligatorio en ambas columnas.** Hoy están sin clase: ese es el defecto real.
4. **`node_tree` y `cardinality` explícitos**, para que dos ejecuciones produzcan la misma página.
5. **Editor y frontend se aceptan por separado.** El editor no debe verse idéntico al frontend; debe ser editable, legible y sin superposición.
