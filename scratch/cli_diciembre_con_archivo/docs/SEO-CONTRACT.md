# SEO-CONTRACT.md — PENNACCHIOTTI

**Estado:** borrador para aprobación. Fuente canónica de SEO por página.
**Última actualización:** 24 de octubre de 2026
**Subordina a:** `PRODUCT.md` (oferta, clientes, evidencia, CTA) y `DESIGN.md` (modo de superficie, tokens).
**Precede a:** el Page Design Contract (`templates/page-design-contract.md` de la skill). Sin SEO Contract no se escribe el contrato de diseño.

---

## 1. Por qué existe

El Page Design Contract describe **qué se construye**. No dice **para qué consulta existe la página, a quién le habla, ni si compite consigo misma**. Ese hueco ya produjo un defecto medido: `/inicio/` y `/contact/` responden 200 con el mismo contenido que `/` y `/contacto/`, con canonical correcto pero indexables (`CAMBIOS.md:11`).

Canonical no arregla canibalización si la URL duplicada sigue siendo indexable y enlazada: solo consolida señales. La decisión de indexar o no debe estar escrita antes de construir.

## 2. Reglas duras

1. **Una página, un contrato.** Se completa antes de cualquier llamada al MCP.
2. **Una sola acción primaria** (`PRODUCT.md:73`). Si el contrato propone dos CTA primarios, está mal.
3. **`canonical_url` es obligatorio en toda página**, incluidas las legales. Nunca se deja al valor por defecto del tema.
4. **`robots` explícito.** `index,follow` solo en páginas publicadas, con H1 único y sin duplicado de contenido. Borradores y páginas de estado: `noindex,follow`.
5. **URL duplicada con contenido idéntico:** la duplicada se marca `noindex` o se redirige 301 a la buena. Se elige una y se registra en `CAMBIOS.md`. No se resuelve solo con canonical.
6. **`faq_required: true` obliga a FAQ visible** en la página y a `FAQPage` con **exactamente** las preguntas visibles. Al revés no: FAQ visible sin schema es válido; `FAQPage` sin preguntas visibles es penalizable y se rechaza.
7. **`schema` es una lista cerrada** de tipos aplicables: `FAQPage`, `Article`, `BreadcrumbList`, `Organization`. No se inventan tipos fuera de esa lista sin aprobación.
8. **Cero volúmenes inventados.** Si no hay medición (Search Console, Keyword Planner, herramienta con fecha), se escribe `volume: N/A`. La keyword se elige por intención declarada, no por una cifra inventada.
9. **Ninguna keyword del centro de la oferta puede ser un método.** `PRODUCT.md:55`: digital, IA y gestión del conocimiento son métodos. No se posiciona sobre «transformación digital» ni «IA para empresas».
10. **Todo CTA apunta a una URL que existe** (`PRODUCT.md:81`). Si el destino es 404, el contrato no se aprueba.
11. **Enlaces entrantes declarados:** una página nueva no se publica si no tiene al menos un enlace real desde una página existente (menú o enlace contextual). Publicar una huérfana y esperar a que la descubra Google es una decisión, no un descuido.
12. **El contrato no redacta el copy.** Fija la intención, la persona y la acción; el texto se escribe contra el lenguaje de `PRODUCT.md:44-50`.

## 3. Plantilla

```yaml
seo_contract:
  page: <slug>
  post_id: <id WordPress | null si no existe>
  status: draft | approved
  version: 1.0

  # --- intención ---
  primary_keyword: <una sola>
  secondary_keywords: [<3–6>]
  search_intent: informational | commercial | navigational | transactional
  intent_note: <qué pregunta trae al visitante, en una frase>
  volume: <N/A si no hay medición, con herramienta y fecha>

  # --- destinatario ---
  target_persona: <rol y tipo de empresa, según PRODUCT.md:15-21>
  not_for: <quién no debe llegar o no debe convertir>

  # --- indexación ---
  canonical_url: <absoluta>
  robots: index,follow | noindex,follow

  # --- conversión ---
  cta_primary:   {label: <>, target: </ruta/>}
  cta_secondary: {label: <>, target: </ruta/>}

  # --- estructura de enlaces ---
  internal_links:
    - {from_section: <id>, to: </ruta/>, anchor: <texto>}
  inbound_links:
    - {from: </ruta/ | menú>, anchor: <texto>}

  # --- preguntas y datos estructurados ---
  faq_required: true | false
  faq_visible_count: <n | 0>
  schema: [FAQPage | Article | BreadcrumbList | Organization]  # subconjunto; FAQPage exige faq_visible_count > 0

  # --- metadatos ---
  title_tag:        {value: <>, max_chars: 60}
  meta_description: {value: <>, max_chars: 155}
  h1: <texto exacto, único en la página>

  # --- posicionamiento ---
  positioning_check: <cómo la página sostiene el posicionamiento de PRODUCT.md:52-58>
  evidence_used: [<dato de PRODUCT.md:60-67, o "ninguno">]
```

## 4. Contrato completado — `/soluciones/`

Página existente como borrador: post **2076**, 11 bandas, 1 H1, 6 preguntas frecuentes (`CAMBIOS.md:26`). Hoy **no está enlazada ni indexada**. Los valores marcados *(propuesta)* requieren aprobación de Mario antes de publicar.

```yaml
seo_contract:
  page: /soluciones/
  post_id: 2076
  status: draft
  version: 1.0

  primary_keyword: estandarización de procesos          # (propuesta)
  secondary_keywords:
    - consultoría de procesos agroalimentarios
    - procedimientos operativos estándar
    - control de procesos industria alimentaria
    - criterios de aceptación de producto
  search_intent: commercial
  intent_note: >-
    Un gerente de operaciones busca cómo dejar de depender de personas clave:
    quiere un método, no una herramienta ni una capacitación.
  volume: N/A   # sin medición; no se elige keyword por cifra inventada

  target_persona: >-
    Gerente de operaciones, calidad o procesos de empresa agroalimentaria
    (PRODUCT.md:15-21)
  not_for: >-
    Quien busca licencia de software, subir producción sin cambiar el proceso
    o un informe sin implementación (PRODUCT.md:22)

  canonical_url: https://pennacchiotti.cl/soluciones/
  robots: noindex,follow   # borrador; pasa a index,follow solo al publicar

  cta_primary:   {label: Agendar una conversación, target: /contacto/}
  cta_secondary: {label: Ver perspectivas,          target: /perspectivas/}

  internal_links:
    - {from_section: alcance,  to: /contacto/,    anchor: Agendar una conversación}
    - {from_section: cierre,   to: /perspectivas/, anchor: Ver perspectivas}
    - {from_section: metodo,   to: /sobre-mi/,    anchor: cómo trabajo}
  inbound_links:
    - {from: menú principal, anchor: Soluciones}
    - {from: /,              anchor: Ver soluciones}   # pendiente: hoy el menú propuesto la incluye, la página no existe enlazada

  faq_required: true
  faq_visible_count: 6
  schema: [FAQPage, BreadcrumbList]

  title_tag:
    value: Estandarización de procesos operacionales · PENNACCHIOTTI
    max_chars: 60
  meta_description:
    value: >-
      Procesos que se ejecutan igual entre turnos y personas: criterios
      explícitos, responsabilidades definidas y evidencia para decidir.
    max_chars: 155
  h1: <texto exacto del H1 del post 2076, verificado en el árbol antes de publicar>

  positioning_check: >-
    Vende control y estandarización operacional. Los métodos (digital, IA,
    conocimiento) aparecen subordinados; ninguna sección se titula
    «transformación digital» ni «soluciones de IA» (PRODUCT.md:54-55).
  evidence_used: ["ninguno"]   # solo la cifra publicable de PRODUCT.md:64, y aún no confirmada
```

### Bloqueos de publicación (medidos, abiertos)

| # | Bloqueo | Evidencia |
|---|---|---|
| 1 | URL duplicada indexable | `/inicio/` y `/contact/` sirven el mismo contenido que `/` y `/contacto/` (`CAMBIOS.md:11`) → decidir `noindex` o 301 antes de publicar `/soluciones/` |
| 2 | Página sin enlaces entrantes | 2076 no está enlazada; el sitio no tiene `<nav>` renderizado (`CAMBIOS.md`, defecto 1) |
| 3 | CTA sin destino | Los botones del sitio se renderizan como `<button>` sin `href` (defecto 2); el CTA primario de `/soluciones/` hoy no navega |
| 4 | FAQ sin schema | 6 preguntas visibles y ningún `FAQPage` declarado |
| 5 | H1 sin verificar | El H1 del post 2076 no está transcrito en este contrato; se copia del árbol, no de memoria |

## 5. Relación con el resto del sistema

```
PRODUCT.md → SEO-CONTRACT.md (esta página) → Page Design Contract → Elementor
```

En conflicto entre reglas, gana el escalón superior. Los vetos absolutos (evidencia verificable, confidencialidad, veracidad, WCAG AA) están fuera de la jerarquía: si fallan, la página se rechaza sin importar el objetivo comercial. Ver `pennacchiotti-web-design-system` §0.1.
