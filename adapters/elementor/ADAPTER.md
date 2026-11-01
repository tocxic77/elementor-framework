# Adaptador · Elementor V4 (atómica)

Traduce el sistema de diseño del framework a objetos nativos de Elementor: variables
globales del kit, clases globales y componentes reutilizables. Sin HTML propio, sin
mu-plugin, sin CSS inyectado por fuera del kit.

Verificado contra **Elementor 4.3.5 / Pro 4.3.0**, kit `11286`.

## Qué entra y qué sale

| Entra (framework) | Sale (Elementor) | Dónde vive |
|---|---|---|
| `05_SYSTEM/tokens.css` | variables globales del kit | post 11286, `_elementor_page_settings` |
| reglas de `05_SYSTEM/theme.css` | clases globales `pp-*` | kit, gestor de clases |
| bandas y patrones de página | componentes `e-component` | documentos de componente (11377…) |
| contenido de `05_NEED` + `04_DIRECTION` | composición atómica por página | `_elementor_data` de cada página |

## Reglas V4 que el adaptador respeta

1. La estructura externa de una banda es **`e-flexbox`** o **`e-div-block`**; nunca
   `container` (V3).
2. Todo texto es **`e-heading`** o **`e-paragraph`**. El widget `text-editor` existe
   pero es legado: no se usa en composición nueva.
3. El estilo se declara **una vez** en una clase global. El valor local sólo se admite
   para lo que es único de esa instancia.
4. Colores y tamaños se referencian con `var(--token)`. Prohibido hex en el estilo de
   un elemento.
5. Anidación máxima: 4 niveles. Espaciado uniforme con `gap` en el padre, no con
   márgenes en los hijos.
6. Cada elemento necesita un `configuration-id` único dentro de la composición.
7. Breakpoints reales del kit: `--tablet` = 1025 px, `--mobile` = 768 px (máximo
   inclusivo). No se usan 1024/767.

## Procedimiento

1. `elementor/manage-global-variable` — crear las variables que falten (ver `sistema.yaml`).
2. `elementor/manage-classes` — crear las clases con sus declaraciones CSS.
3. `elementor/manage-component` — crear el componente con `xml_structure` + `classes`.
   Exponer como `overridable_props` sólo lo que cambia por instancia (textos, imagen).
4. `elementor/build-composition` en una página — instanciar componentes con
   `<e-component configuration-id="…"/>` y `element_config: {component_id, overrides}`.
5. `elementor/publish-document` sólo con autorización explícita.
6. `verificar_sistema.py` — comprueba que el sistema sigue en pie.

## Límites conocidos

- `list-components` devuelve los componentes publicados, no sus overrides; para saber
  qué expone cada uno hay que leerlo en el editor.
- Las clases globales no se pueden enumerar por herramienta: se validan al aplicarlas
  (un label inexistente devuelve error con la lista disponible). El gate no las cubre.
- Un componente no acepta contenido arbitrario: si la instancia necesita estructura
  distinta, se crea otro componente, no se parchea la instancia.
- `e-form` (formulario nativo) existe en 4.3.5 pero este adaptador todavía no lo emite.
