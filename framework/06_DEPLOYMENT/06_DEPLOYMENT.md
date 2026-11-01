# 06_DEPLOYMENT — dos puertas, no una

Publicar y medir son dos momentos distintos. Mezclarlos produce sitios que nunca lanzan o que
lanzan sin evidencia.

## Decisión 1 · QA de lanzamiento (bloquea publicar)

| Comprobación | Criterio | Herramienta |
|---|---|---|
| Un `h1` por página | exactamente 1 en todas las publicadas | `framework/tools/verificar.js` |
| Accesibilidad de color | 0 textos bajo AA computado | `framework/tools/verificar.js` |
| Responsive | 0 desborde a 390/768/1440 | `framework/tools/verificar.js` |
| Peso y medios | imágenes servidas ≤ 2× el ancho de uso, formato moderno | `framework/tools/verificar_estatico.py` |
| Navegación | toda página alcanzable desde la cabecera y el pie | manual, con captura |
| Metadatos | `title`, descripción y OpenGraph únicos por página | revisión de HTML servido |
| Formularios | envío real probado, respuesta registrada | manual |
| Consentimiento | nada de analítica antes del aviso | revisión de red |

**Regla:** si un bloqueante falla, no se publica. No existe «se arregla en producción».

## Decisión 2 · Medición (30 días después)

- **GA4** o equivalente: eventos de la acción esperada de `01_NEED`, no pageviews sueltos.
- **Search Console**: consultas y páginas indexadas.
- **Clarity** o mapa de calor: scroll y clics reales de la primera pantalla.
- **Un número por objetivo**: el que se declaró en `01_NEED`, con su valor a 30 días.

Sin consentimiento configurado, la segunda puerta no existe: medir sin aviso es un defecto legal,
no un detalle técnico.

## Ubicación

```
framework/06_DEPLOYMENT/QA.md                 esta puerta, genérica
<cliente>/06_DEPLOYMENT.md                    evidencia fechada, capturas y números
```

## Revisión de esta ranura

| Comprobación | Criterio |
|---|---|
| Cada bloqueante tiene su salida medida | número o captura fechada, no «ok» |
| Capturas por ancho | 390, 768 y 1440 por página publicada |
| Analítica instalada | sí/no, y si está detrás del consentimiento |
| Baseline a 30 días | agendado con fecha, no prometido |
