# Elementor Framework

Un método para producir sitios editoriales en WordPress con Elementor, donde cada
decisión visual tiene una fuente y cada afirmación se puede medir.

No es una plantilla. Es la cadena que va de una necesidad comercial a un sistema de
diseño materializado en Elementor —variables, clases globales y componentes— y de ahí
a una publicación verificada.

> A method for building editorial WordPress sites with Elementor: every visual decision
> has a source, every claim is measured, and the design system lives inside Elementor
> — global variables, global classes and reusable components — not in ad-hoc CSS.

## Principios

1. **Nada se publica sin evidencia.** Toda afirmación con fuente, toda decisión visual
   con referencia, todo componente con un objetivo.
2. **El problema no es el material, es la decisión.** El framework ordena decisiones,
   no acumula archivos.
3. **Si una decisión no desbloquea una página, no puede bloquear una página.** No se
   abren fases ni verificadores que no desbloqueen entrega.

## Estructura

```
framework/
├── 01_NEED/          la necesidad: a quién le sirve, qué problema resuelve, qué la haría falsa
├── 02_MATERIAL/      lo que existe: activos, textos, cifras, fuentes
├── 03_CURATION/      la biblioteca de gusto: referencias medidas, no impresiones
├── 04_DIRECTION/     la dirección: tesis visual, estrategia de imagen, prompts
├── 05_SYSTEM/        el sistema: tokens.css, theme.css, utilities.css
├── 06_DEPLOYMENT/    la puesta en producción y sus comprobaciones
└── tools/            verificadores ejecutables (need, evidencia, activos, independencia)

adapters/
└── elementor/        cómo el sistema se materializa en Elementor V4 (atómica)
```

Las seis fases son puertas: cada una deja por escrito qué entra, qué sale y qué la
invalida. Nada se da por bueno porque «se ve bien».

## Adaptador de Elementor

`adapters/elementor/` traduce el sistema a objetos nativos: variables del kit, clases
globales `pp-*` y componentes reutilizables con propiedades expuestas. Sin HTML propio,
sin `mu-plugin`, sin CSS inyectado fuera del kit.

- `ADAPTER.md` — contrato y reglas V4 que respeta.
- `sistema.yaml` — registro de variables, clases y componentes.
- `verificar_sistema.py` — gate: comprueba contra una instalación viva que el sistema
  sigue existiendo (MCP respondiendo, componentes presentes, cada variable con su token
  de origen).

```bash
export ELEMENTOR_MCP_URL="https://<sitio>/wp-json/elementor/mcp/"
export ELEMENTOR_MCP_KEY="<credencial Basic>"
python adapters/elementor/verificar_sistema.py
```

Los identificadores de kit y de componentes en `sistema.yaml` son de una instalación de
referencia: en cada sitio se generan los propios.

## Requisitos

- WordPress 6.x con **Elementor 4.3.5** y **Elementor Pro 4.3.0** (probado).
- Python 3.10+ para los verificadores.
- Para el adaptador, un endpoint MCP de Elementor accesible con cabecera `Basic`.

## Qué está verificado

- `framework/tools/verificar_independencia.py` → el framework no menciona a ningún
  cliente: `exit 0`.
- El adaptador corrió contra una instalación real: 13 variables, 18 clases globales,
  5 componentes, gate en verde.
- Los verificadores de `framework/tools/` son ejecutables, no documentación.

## Qué no está incluido

- `03_CURATION/gusto/capturas/` — 64 capturas de sitios de terceros. Se excluyen por
  peso y por derechos; se regeneran con `framework/03_CURATION/gusto/gen_specimen.py`.
- Ningún proyecto de cliente. El framework es independiente por diseño.

## Licencia

MIT — ver `LICENSE`.
