# 03_CURATION — qué entra, qué sale y con qué criterio se juzga

La ranura más barata de llenar y la que más cambia el resultado: sin ella, cada proyecto se
juzga con el gusto del día.

## Decide

- **Qué entra**: los archivos de `02_MATERIAL` asignados a bandas concretas.
- **Qué sale**: lo que no se usará, dicho explícitamente (no borrado del cliente).
- **Qué se reescribe**: copy que existe pero no sirve.
- **Qué se fotografía**: el faltante que se resuelve produciendo, no comprando banco.
- **La biblioteca de gusto**: cada referencia con su imagen propia y dos listas cortas.

```yaml
- nombre: stripe
  categoria: premium
  imagen: gusto/stripe.png          # 1440 y 390, renderizada, no enlazada
  take: [espaciado, jerarquia-tipografica]
  avoid: [exceso-de-producto]
```

`take` y `avoid` son tres ítems como máximo. Una referencia con veinte «take» no enseña nada.

## Ubicación

```
framework/03_CURATION/gusto/<slug>.png        capturas 1440 y 390
framework/03_CURATION/gusto/index.yaml        la lista
<cliente>/03_CURATION.md                      selección: banda → archivo → tratamiento
```

## Estado de la biblioteca

54 sistemas, medidos y capturados el 2026-10-31. Una imagen por sistema con las dos
medidas en la misma pieza (escritorio 1440 y móvil 390), generada desde la ficha de tokens
del sistema, no desde el sitio publicado.

```
03_CURATION/gusto/
├── index.yaml            54 entradas · take ≤3 · avoid ≤3 · imagen
├── gen_doble.py          ficha de tokens → espécimen comparable
├── dobles/               54 especímenes HTML
└── capturas/             64 PNG · 6,0 MB (54 fichas + 10 de los 5 sitios medidos)
```

Comprobado antes de declararla hecha: 59 entradas (54 `origen: ficha` + 5 `origen: medido`),
64 imágenes existentes, 0 sin imagen, 0 con más de tres `take` o `avoid`.

**La diferencia entre las dos clases:** una referencia `medido` se midió con el mismo
instrumento que el gate (palabras, familias, contraste, recursos, MB) y puede citarse en
`04_DIRECTION` con su número. Una referencia `ficha` sólo aporta la mecánica que su sistema
declara: sirve para comparar decisiones, no para afirmar hechos sobre el sitio.

| Familia | Entradas |
|---|---|
| herramientas de desarrollo | 14 |
| IA y modelos | 12 |
| diseño y productividad | 10 |
| infraestructura | 6 |
| consumidor | 6 |
| fintech | 4 |
| enterprise | 2 |

**Cómo se usa:** se elige por `take` y se descarta por `avoid`. Una firma de `04_DIRECTION`
debe poder citar al menos una entrada que la respalde; una antirregla, al menos una que la
justifique. Si la biblioteca no alcanza para decidir, la referencia que falta se captura y
se añade: no se improvisa el criterio.

## Las 30 que cuentan

De las 59, treinta son las que se usan para decidir; las demás son archivo. Están en el bloque
`seleccion:` de `gusto/index.yaml`, con el porqué de cada una.

| Grupo | Qué se estudia en él | Cuántas |
|---|---|---|
| autoridad | claridad, estructura, credibilidad (2 familias, medida de lectura, dato que ordena) | 10 |
| innovación | fotografía, escala, movimiento, una sola ley visual | 10 |
| rechazadas | lo que el sistema prohíbe, con el motivo nombrado | 10 |

**Un rechazo vale tanto como una referencia.** Las diez rechazadas no son sitios malos: son
sitios donde el fondo hace el trabajo que debería hacer la estructura (degradados, brillo,
neón, saturación). Sirven para reconocer el atajo antes de tomarlo.

La selección es **declarada y revisable**, no exhaustiva: si una decisión necesita una
referencia que no está en las treinta, se cita desde el archivo o se captura una nueva.

## Revisión

| Comprobación | Criterio | Bloquea |
|---|---|---|
| Cada entrada tiene PNG | la imagen abre y mide ≥390 px de ancho | sí |
| `take`/`avoid` acotados | ≤3 ítems por lista | no |
| Toda banda del sitio tiene material asignado | 0 bandas sin archivo | sí |
| Toda firma de `04_DIRECTION` cita una referencia | 3 de 3 | no |
| Lo que sale está nombrado | lista explícita | no |

**Prueba de que la ranura sirve:** con `index.yaml` y las capturas, otra persona debe poder
elegir entre dos composiciones sin preguntarte. Si necesita preguntar, la biblioteca no se
transfirió: se quedó en tu cabeza.
