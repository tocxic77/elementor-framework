# framework — qué contiene cada ranura

## PRINCIPIO 01 — nada se publica sin evidencia

> Toda afirmación tiene una fuente. Toda decisión visual tiene una referencia.
> Todo componente responde a un objetivo. Todo sitio se puede auditar.

El principio no vive en este README: vive en dos puertas que salen con código 1.

```bash
python tools/verificar_need.py     <cliente>/01_NEED.yaml        # ¿se puede empezar?
python tools/verificar_evidencia.py <cliente>/02_EVIDENCE.yaml --html <página>
```

Sin `01_NEED` completo no se escribe `02`, ni `04`, ni `05`. Y una cifra que no está en
`02_EVIDENCE.yaml` como `validada` con fuente no se publica, aunque sea cierta.

---

## PRINCIPIO 02 — el problema no es el material, es la decisión

> Casi nunca falta material: falta la decisión de qué pieza ocupa qué banda.
> Seleccionar es un trabajo distinto de producir, y se hace antes de construir.

Por eso `02` mide y `03` decide, en ese orden. Una foto sin banda asignada es material
disponible, no material usado: no cuenta como avance.

---

Seis ranuras numeradas. Cada una **contiene un artefacto**, no un resumen: si una ranura
sólo tiene prosa, no cuenta como hecha. El estado de abajo es la verdad de hoy, no un plan.

| Ranura | Debe contener | Estado | Artefacto real |
|---|---|---|---|
| `01_NEED/` | Problema, audiencia, acción, objeción, quién firma — con fuente por respuesta | **plantilla + puerta ejecutable** | `01_NEED.md` · `CUESTIONARIO.md` 20 preguntas · `tools/verificar_need.py` · `<cliente>/01_NEED.yaml` (20/20 con fuente) |
| `02_MATERIAL/` | Evidencia y material: activos con medida + afirmaciones con fuente | **plantilla + 2 instancias** | `02_MATERIAL.md` · `<cliente>/02_EVIDENCE.yaml` 5 afirmaciones (3 validadas, 2 rechazadas) · `tools/verificar_evidencia.py` |
| `03_CURATION/` | Qué entra y qué sale + biblioteca de gusto (imagen + take/avoid) | **hecha** | `03_CURATION.md` · `gusto/index.yaml` 59 refs (54 ficha + 5 medidas) · 64 PNG (1440+390) |
| `04_DIRECTION/` | Firma visual, antirreglas, tipo, color, foto, motion + qué imagen puede ocupar qué banda | **plantilla + 1 instancia + 2 artefactos** | `04_DIRECTION.md` · `IMAGE_STRATEGY.md` (niveles A/B/C + regla ejecutable) · `prompts.yaml` 6 categorías · `<cliente>/DIRECTION.md` v1.3 · `03_ASSETS.yaml` 20 activos medidos · `tools/verificar_activos.py` |
| `05_SYSTEM/` | Tokens + patrones en código + previews | **hecha** | `tokens.css` 32 · `utilities.css` 16 · `theme.css` 159 · 11 patrones · gate estático 18 comprobaciones · `tools/verificar_tokens.py` |
| `06_DEPLOYMENT/` | QA medido, accesibilidad, SEO, analítica, lanzamiento | **plantilla, sin evidencia** | `06_DEPLOYMENT/06_DEPLOYMENT.md` |

Las seis ranuras tienen su archivo. Ninguna está llena de evidencia excepto `05_SYSTEM` y una
instancia de `02`/`04`: eso es el estado, no el plan.

## PRINCIPIO 03 — si una decisión no desbloquea una página, no puede bloquear una página

Una ranura que no cambia lo que se publica esta semana es documentación, no producción. Cada ranura
declara el artefacto visible que entrega; el documento es el registro, no el entregable.

**Congelado del 2026-10-31 al 2026-11-07:** no se agregan archivos, reglas ni verificadores al framework.
Se construyen las cinco páginas del cliente con lo que ya existe. Al volver, la evidencia de qué faltaba
sale de haber publicado, no de haber documentado.

## Por qué cada ranura contiene un artefacto y no un documento

El framework se rompe si `02_MATERIAL` es una lista de buenas intenciones y `05_SYSTEM` es un
documento sobre patrones. La prueba de que una ranura está hecha es que **otra persona pueda
usar su salida sin leer nada más**:

- `05_SYSTEM` se prueba abriendo la página del cliente en `clients/<cliente>/05_SYSTEM/`: si no
  renderiza, la ranura está vacía. El framework sólo guarda los tres CSS.
- `02_MATERIAL` se prueba contando archivos clasificados con su medida: si una foto dice
  «usable» y mide 720 px de ancho, la clasificación es falsa.
- `04_DIRECTION` se prueba midiendo contraste computado: si un criterio no se mide, no existe.
- `06_DEPLOYMENT` se prueba con capturas fechadas y un número: 1 `h1`, 0 textos bajo AA, 0 desborde.

## Lo que NO va aquí

Nada de un cliente. Ni su `DIRECTION.md`, ni su inventario de activos, ni sus cifras, ni su
página. Aquí sólo entra lo que se pueda reutilizar diez veces; si algo se usa una sola vez,
es del cliente, aunque se llame igual.

```
04_WEB/
├── framework/          6 ranuras, 3 archivos de sistema, 10 puertas — cero nombres de cliente
├── clients/
│   └── <cliente>/  01_NEED.yaml · 02_EVIDENCE.yaml · 03_ASSETS.yaml · 03_SELECCION.md
│                       DIRECTION.md · 05_SYSTEM/ (página, assets, capturas) · docs · material
└── adapters/           salida por tecnología (vacío hasta que exista E-7)
```

La prueba de independencia es un comando, no una promesa:

```bash
python framework/tools/verificar_independencia.py   # 0 = independiente · 3 = no había clientes que buscar
```

Y la secuencia completa, que es lo que corre el operador:

```bash
python framework/tools/verificar_release.py clients/<cliente>
```

## Regla de no duplicación

Un artefacto tiene una sola ubicación y las demás ranuras lo referencian por ruta. No hay
`qa.md` que repita los criterios de `DIRECTION.md`, ni `patterns.md` que describa lo que ya
está en `05_SYSTEM/theme.css`. Si dos archivos dicen lo mismo, uno de los dos miente en el
próximo cambio.

## Deuda declarada, ordenada por costo

1. `05_SYSTEM` sin página neutra: la página de referencia se movió a `<cliente>/`
   y el sistema quedó con sus tres CSS. Falta una demo sin copy de cliente para que la ranura
   se pruebe sola.
2. `06_DEPLOYMENT` sin medición en vivo: los criterios existen, la evidencia no.
3. `adapters/` vacío: los patrones son HTML/CSS y todavía no se insertan en Elementor.
   Depende de E-7 (child theme), no de más CSS.
4. `03_CURATION` con 30 referencias curadas de 59: la biblioteca está, la selección es
   declarada y revisable, no exhaustiva.
