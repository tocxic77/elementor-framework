# Elementor Framework

[![License: MIT](https://img.shields.io/badge/license-MIT-223035.svg)](LICENSE)
[![Elementor](https://img.shields.io/badge/Elementor-4.3.5%20%2B%20Pro%204.3.0-223035.svg)](https://elementor.com)
[![WordPress](https://img.shields.io/badge/WordPress-6.x-223035.svg)](https://wordpress.org)

Un método para producir sitios editoriales en WordPress donde cada decisión visual
tiene una fuente, cada afirmación se puede medir y el sistema de diseño vive **dentro de
Elementor** —variables globales, clases globales y componentes reutilizables— en lugar
de en hojas de estilo sueltas.

No es una plantilla ni un tema. Es la cadena que va de una necesidad comercial a una
publicación verificada, con seis puertas que se pueden ejecutar.

> *A method for building editorial WordPress sites with Elementor. The design system is
> materialised as Elementor global variables, global classes and components — not as
> ad-hoc CSS — and every gate is an executable script, not a checklist.*

---

## Índice

- [Qué es y qué no es](#qué-es-y-qué-no-es)
- [Los tres principios](#los-tres-principios)
- [Cómo funciona](#cómo-funciona)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Inicio rápido](#inicio-rápido)
- [Verificadores](#verificadores)
- [Adaptador de Elementor](#adaptador-de-elementor)
- [Estado: qué está verificado](#estado-qué-está-verificado)
- [Lo que falta](#lo-que-falta)
- [Licencia](#licencia)

---

## Qué es y qué no es

**Es** un orden de decisiones. Cada fase tiene una pregunta que la cierra, un artefacto
que la demuestra y un verificador que la comprueba sin pedir permiso a nadie.

**No es** una biblioteca de secciones bonitas. Si un componente no responde a una
necesidad escrita en `01_NEED`, no entra.

## Los tres principios

1. **Nada se publica sin evidencia.** Toda afirmación con fuente, toda decisión visual
   con referencia, todo componente con un objetivo declarado.
2. **El problema no es el material, es la decisión.** Un sitio mediocre con buen material
   sigue siendo mediocre: lo que falta es criterio explícito, no más fotos.
3. **Si una decisión no desbloquea una página, no puede bloquear una página.** No se
   abren fases, gates ni verificadores nuevos mientras no desbloqueen entrega.

## Cómo funciona

| Fase | Decide | Artefacto | Puerta |
|---|---|---|---|
| `01_NEED` | por qué el sitio debe existir; qué lo haría falso | `01_NEED.md` + cuestionario de 9 preguntas | `verificar_need.py` |
| `02_MATERIAL` | qué existe, en qué estado y qué falta | inventario medido + registro de afirmaciones | `inventario_activos.py`, `verificar_evidencia.py` |
| `03_CURATION` | qué entra, qué sale y con qué criterio se juzga | biblioteca de gusto medida a 1440 y 390 | `verificar_activos.py` |
| `04_DIRECTION` | la ley visual, y sólo eso | tesis, estrategia de imagen, prompts | revisión con capturas |
| `05_SYSTEM` | el código que se reutiliza | `tokens.css`, `theme.css`, `utilities.css` | gate estático y renderizado |
| `06_DEPLOYMENT` | dos puertas: QA de lanzamiento y medición a 30 días | runbook y mediciones | contraste, H1 único, desbordes |

Las fases no son carpetas de documentación: son puertas. Si una fase no puede cerrarse,
el proyecto no avanza, y eso se ve en el verificador, no en una reunión.

## Estructura del repositorio

```
.
├── framework/
│   ├── 01_NEED/          la necesidad y su cuestionario
│   ├── 02_MATERIAL/      lo que existe, medido
│   ├── 03_CURATION/      biblioteca de gusto: 54 especímenes HTML + índice YAML
│   │   └── gusto/        gen_specimen.py · gen_doble.py · index.yaml
│   ├── 04_DIRECTION/     tesis visual, estrategia de imagen, prompts
│   ├── 05_SYSTEM/        tokens.css · theme.css · utilities.css
│   ├── 06_DEPLOYMENT/    puesta en producción
│   ├── tools/            cinco verificadores ejecutables
│   └── README.md         qué contiene cada ranura y su deuda declarada
└── adapters/
    └── elementor/        el sistema materializado en Elementor V4 (atómica)
        ├── ADAPTER.md          contrato y reglas V4
        ├── sistema.yaml        variables, clases y componentes
        └── verificar_sistema.py gate contra una instalación viva
```

## Inicio rápido

```bash
git clone https://github.com/tocxic77/elementor-framework.git
cd elementor-framework

# 1 · el framework no puede nombrar a ningún cliente
python framework/tools/verificar_independencia.py

# 2 · la puerta de la fase 1
python framework/tools/verificar_need.py clients/<proyecto>/01_NEED.yaml

# 3 · el sistema sigue existiendo en el sitio
export ELEMENTOR_MCP_URL="https://<sitio>/wp-json/elementor/mcp/"
export ELEMENTOR_MCP_KEY="<credencial Basic>"
python adapters/elementor/verificar_sistema.py
```

Cada verificador imprime cuántas comprobaciones corrió, cuántas fallaron y cuántas no pudo
medir. Ninguno imprime credenciales.

Códigos de salida, iguales en todas las puertas:

| Código | Significado |
|---|---|
| `0` | todo lo que la puerta mide se midió y pasó |
| `1` | algo medido incumple la regla |
| `2` | error de uso: argumentos inválidos o documento vacío/ilegible (no se midió nada) |
| `3` | **NO MEDIDO**: la puerta corrió y no había nada que medir, o faltó el instrumento |

`3` existe para que «no lo comprobé» no pueda leerse como «está bien»: un registro vacío, un
documento en blanco o un repositorio sin `clients/` ya no salen `0`.

## Verificadores

| Script | Comprueba | Salida |
|---|---|---|
| `verificar_independencia.py` | que el framework **y el adaptador** no nombren a ningún cliente, por token completo | `ACOPLA archivo:línea` |
| `verificar_need.py` | las 20 preguntas respondidas con fuente y que **ningún campo quede en `null`** | recuento + rutas en null |
| `verificar_evidencia.py` | fuente de cada afirmación **resuelta contra el YAML, no contra el cwd**; cada cifra publicada respaldada | huérfanas, sin fuente, cifras sin respaldo |
| `verificar_activos.py` | nivel y procedencia, `seleccionado` vs `publicado_en`, ancho medido, generada que no reemplace real, ≥2400 px si va a sangre, autorización declarada | conflictos, medidas faltantes y derechos sin declarar |
| `verificar_tokens.py` | `tokens.css` ↔ `sistema.yaml`: mismo color, tamaño y familia; sin hex nuevos fuera de tokens | divergencias |
| `verificar_estatico.py` · `verificar.js` | capa estática y capa renderizada de la calidad (18 comprobaciones estáticas + las renderizadas) | `N comprobaciones · 0 bloqueantes` |
| `verificar_servido.py` | inventario ↔ HTML publicado (y el CSS que ese HTML carga): lo servido está declarado, está autorizado, y lo declarado en uso se publicó | `páginas leídas` · fallas |
| `verificar_404.py` | pide una URL inexistente y exige **404**: un `200` es soft-404, un `301` es redirección silenciosa | `códigos` |
| `verificar_release.py` | **la secuencia**: corre todas las puertas en orden, corta en la primera FALLA y no declara publicable lo que quedó sin medir | tabla + `PUBLICABLE` / `NO PUBLICABLE` |
| `adapters/elementor/auditar_estructura.py` | **ADAPTER.md reglas 1-7 sobre `_elementor_data`**: estructura, widget de texto, estilo local, hex, profundidad ≤4, `configuration-id` único, breakpoints, `spacer`/`divider` prohibidos | `R1…R7` + recuento |
| `framework/tools/verificar_arquitectura.py` | **arquitectura de sitio**: cabecera y pie repetidos en 3+ páginas, plantillas globales (NO MEDIDO sin kit), bloques repetidos como REVISAR | FALLA por copia, aviso por candidato |
| `framework/tools/medir_material.py` | **material disponible**: qué mecanismos de `MECANISMOS.yaml` habilita el material real del cliente; lo que no tiene dónde medirse queda NO DISPONIBLE | instrumento, no puerta |
| `framework/tools/medir_referentes.py` | **referentes**: cruza los mecanismos observados en cada sitio analizado con el material del cliente; un mecanismo inventado en `REFERENTES.yaml` es error de dato | instrumento, no puerta |
| `framework/04_DIRECTION/MATERIALES.yaml` | **protocolo de material**: por cada material, a quién preguntarle, con qué pregunta, qué documento lo prueba y en qué campo se archiva | no es una guía genérica: se cruza con los huecos de un cliente |
| `framework/tools/plan_material.py` | convierte lo que falta en un **plan de entrevista** para este cliente; falla si la biblioteca usa un material sin protocolo de obtención | instrumento, no puerta |
| `framework/tools/medir_migracion.py` | Cuánta autoridad pública sigue en dominio ajeno; separa enlazar de rehospedar |
| `framework/tools/verificar_composicion.py` | La arquitectura propuesta sólo usa mecanismos disponibles, patrones reales y evidencia que existe |
| `inventario_activos.py` | inventario medido de una carpeta de material | CSV |
| `adapters/elementor/verificar_sistema.py` | variables con token de origen y componentes presentes en el kit | `SISTEMA OK · N comprobaciones, 0 fallos` |
| `adapters/elementor/auditar_sitio.py` | un sitio ya publicado: páginas con estructura de Elementor, plantillas duplicadas, 404 mal condicionado, imágenes, H1, **favicon y `og:image`** | tabla + `AUDITORÍA · N fallos` |

El operador corre **un** comando; la secuencia no se arma a mano:

```bash
python framework/tools/verificar_release.py clients/<proyecto>
```

Y los casos que prueban que las puertas fallan cuando deben fallar:

```bash
python tests/run_gates.py        # 24 casos, sin red ni credenciales
```

## Adaptador de Elementor

Elementor 4.3.5 trae la capa atómica (`e-*`) pero no un widget HTML. La consecuencia
práctica: o el sistema se materializa en el kit, o el sitio acaba siendo HTML ajeno al
editor. Este adaptador trata el segundo caso como error.

**Qué traduce**

| Entra | Sale | Dónde vive |
|---|---|---|
| `05_SYSTEM/tokens.css` | variables globales | kit, `_elementor_page_settings` |
| reglas de `theme.css` | clases globales `pp-*` | gestor de clases del kit |
| bandas y patrones | componentes `e-component` | documentos de componente |
| contenido de `01_NEED` | composición atómica | `_elementor_data` de la página |

**Reglas que respeta**

1. La estructura de una banda es `e-flexbox` o `e-div-block`, nunca `container` (V3).
2. Todo texto es `e-heading` o `e-paragraph`; `text-editor` es legado y no se usa.
3. El estilo se declara una vez, en una clase global.
4. Colores y tamaños se referencian con `var(--token)`; hex prohibido en el elemento.
5. Anidación máxima de 4 niveles; espaciado con `gap` en el padre, no con márgenes.
6. Cada elemento necesita un `configuration-id` único.
7. Breakpoints reales del kit: 1025 px (tablet) y 768 px (móvil), máximo inclusivo.

**Composición de una página**, instanciando componentes en vez de copiar subárboles:

```json
{
  "post_id": 123,
  "xml_structure": "<e-flexbox configuration-id=\"pagina\"><e-component configuration-id=\"hero\"/><e-component configuration-id=\"objecion\"/></e-flexbox>",
  "element_config": {
    "hero":     { "component_id": 11377, "overrides": { "titular": "…", "cta": "…" } },
    "objecion": { "component_id": 11380, "overrides": { "titular": "…" } }
  }
}
```

`sistema.yaml` registra los 13 tokens, las 18 clases `pp-*` y los 5 componentes con sus
propiedades expuestas. Es una instalación de referencia: en cada sitio se generan los
suyos.

## Estado: qué está verificado

- El adaptador corrió contra una instalación real: **13 variables, 18 clases globales,
  5 componentes**, gate en verde (`3 comprobaciones, 0 fallos`).
- Una página de prueba construida con `e-*` y las clases del kit renderizó a **56 px de
  titular, contraste 13,06:1 y botón sin el azul por defecto de Elementor**.
- Los verificadores del framework son ejecutables y se corrieron sobre el árbol real.
- `auditar_sitio.py` corrió contra un sitio publicado y encontró **6 fallos reales**:
  5 de 5 páginas sin estructura de Elementor, footer duplicado, plantilla 404 mal
  condicionada, cero imágenes editoriales, sin favicon y sin `og:image`. Tras declarar
  favicon y `og:image` en producción, la misma auditoría bajó a **3 fallos y 1 aviso**.
- `verificar_need.py` bloquea con `exit 1` cuando encuentra un campo en `null`, aunque
  las 20 preguntas estén respondidas: un dato ausente no puede pasar por respuesta.

**No verificado:** que las clases globales basten sin las hojas CSS del framework
cargadas aparte. Esa prueba está pendiente y es la que decide si el sistema está
completo o sólo trasladado.

## Lo que falta

- Emitir el formulario con `e-form` nativo en lugar de `wp_mail` externo.
- Componentes de cita, caso y listado (`loop-grid`).
- Un gate que lea `_elementor_data` en vez de HTML (H1 único, hex prohibido, anidación).
- Vídeo de hero con `e-background-video`.

## Licencia

MIT — ver [`LICENSE`](LICENSE). Los 64 PNG de la biblioteca de gusto no se incluyen por
peso y por derechos; se regeneran con `framework/03_CURATION/gusto/gen_specimen.py`.
