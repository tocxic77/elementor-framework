# 05_SYSTEM — el código que se reutiliza

Esta ranura no es un documento sobre patrones: es el código. Si no renderiza, la ranura está vacía.

## Decide

- **Tokens**: una sola fuente de valores. Si un valor no está en `tokens.css`, no se usa.
- **Patrones**: qué banda cubre qué necesidad, con nombre y número estables (`P1 hero`, `P10 pie`). Un patrón no es un componente suelto: es una banda completa con su ritmo vertical.
- **Versión de la biblioteca**: qué cambió y qué baseline medido se conserva por patrón.
- **Lo que NO entra**: CSS por identificador de página, estilos en línea, dependencias de un constructor.

## Ubicación

```
framework/05_SYSTEM/tokens.css               valores
framework/05_SYSTEM/theme.css                base + patrones
framework/05_SYSTEM/index.html               composición de referencia
framework/05_SYSTEM/articulo.html            plantilla de página interior
framework/05_SYSTEM/assets/                  material usado por la referencia
framework/05_SYSTEM/capturas/patrones/       preview por patrón, 1440 y 390
```

## Revisión

Se corre siempre, antes de declarar nada:

```bash
python framework/tools/verificar_estatico.py 05_SYSTEM
```

```javascript
// en el navegador, sobre la página servida
js(<contenido de framework/tools/verificar.js>)
```

| Comprobación | Criterio | Bloquea |
|---|---|---|
| Renderiza | abre sin error de consola y sin solicitudes fallidas | sí |
| Un solo `h1` por página | `document.querySelectorAll('h1').length === 1` | sí |
| Contraste computado | 0 textos bajo 4,5:1 (3:1 si ≥24 px) | sí |
| Desborde horizontal | 0 px a 390 y 1440 | sí |
| `page-id` en CSS | 0 ocurrencias | sí |
| Estilos en línea | 0 (salvo excepción registrada) | no |
| Preview por patrón | todos los patrones con 1440 y 390 | sí |
| Rejilla repetida | ≤1 rejilla de tres iguales por página, y nunca dos bandas seguidas con la misma | no |

## Regla de deriva

Un patrón sin baseline medido se degrada sin que nadie lo note. Cada captura de
`capturas/patrones/` es el baseline: si el patrón cambia, la captura se regenera **y se dice
qué cambió**. Cambiar el CSS y dejar la captura vieja es documentación que miente.
