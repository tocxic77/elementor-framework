# FASE 1 — Matriz comparativa PENNACCHIOTTI ↔ Leroux

**Fecha:** 23 de octubre de 2026
**Base:** mediciones propias del demo público de Leroux (23-oct) y del sitio actual.
**Criterio:** se compara el **lenguaje**, no el theme. Nada de Leroux se copia literalmente.

## Matriz

| # | Elemento | Estado en PENNACCHIOTTI | Principio observado en Leroux | Diferencia | Impacto visual | Viabilidad con Elementor nativo | Riesgo | Recomendación |
|---|---|---|---|---|---|---|---|---|
| 1 | Escala tipográfica | H1 64, H2 42, H3 26, cuerpo 15 | H1 56, H2 42, H3 32, H4 25, cuerpo 15: escalones intermedios | Falta el escalón 25–32; el salto 42→26 es brusco | La página se lee en dos registros, sin matices | Alta (`pp-h4`, variable de tamaño) | Bajo | Crear `pp-h4` 25/35 y usarlo en listas y pasos |
| 2 | Ancho de contenedor | 940 px útil | 1521 px | **−38 %** | Todo se siente comprimido y centrado, sin tensión lateral | Alta (token `container-wide`) | Medio: textos largos se estiran | Subir bandas anchas a 1320–1400 y mantener 760 en lectura |
| 3 | Aire vertical | Padding 112 uniforme | 150 px | −25 % | Ritmo monótono; ninguna banda respira distinto | Alta (clase `pp-band`) | Bajo | 160 en bandas de declaración, 112 en el resto |
| 4 | Hero | 771 px, foto + velo, 2 CTA | 643 px (42 % viewport) | +20 % de altura | El hero ocupa más que la promesa | Alta | Bajo | Bajar a 620–660 y quitar un CTA del hero |
| 5 | Asimetría | grid3 3×372 y grid2 2×568 simétricos | Repartos irregulares por banda | **Ausencia total de asimetría** | Es la causa principal de la sensación «plana» | Alta (`e-grid` con `5fr 7fr`, `4fr 8fr`) | Bajo | Introducir asimetría en 3 de 7 bandas |
| 6 | Ritmo de bandas | 7 bandas con padding y estructura equivalentes | Alternancia denso/abierto, oscuro/claro | Monotonía de arquetipo | El ojo no encuentra puntos de descanso ni de tensión | Alta (contrato de arquetipos) | Bajo | Prohibir arquetipos consecutivos iguales |
| 7 | Imágenes | 2 generadas, ambas del hero/figura | Fotografía contextual a sangre, varias por página | **Brecha principal de credibilidad** | Sin fotografía propia, cualquier maqueta parece plantilla | Media: requiere banco de fotos reales | Alto: imagen sintética de «IA» es peor que nada | Priorizar 6–8 fotos reales antes de seguir construyendo |
| 8 | Detalle editorial | Reglas de 1 px, radio 0, borde 1 px | Igual, más flechas, numeración y subrayados | Faltan microdetalles | Sin ellos la página es correcta pero anónima | Alta (clases del kit) | Bajo | Numeración en método, flechas en CTA, subrayado con offset |
| 9 | Contraste de fondos | Marfil/tinta/salvia/gris | Igual | Equivalente | — | Ya resuelto | — | Mantener; agregar una banda oscura intermedia en el método |
| 10 | Tipografía | Newsreader + DM Sans | DM Sans + Heebo | Nuestra elección es más editorial; la suya, más neutra | A favor nuestro | — | — | Conservar Newsreader: es el diferencial de marca |
| 11 | Botones | `pp-cta` borde 1 px radio 0 | 162 controles, borde 1 px radio 0 | Equivalente | — | Ya resuelto | — | Añadir estado hover con desplazamiento de 2 px y flecha |
| 12 | Header | Oculto por CSS | Header transparente que cambia al hacer scroll | **No existe header** | Sin navegación no hay sitio, solo página | Alta (Theme Builder de Elementor Pro) | Medio: no tocar `functions.php` | Construir header de 5 ítems tras aprobar `/soluciones/` |
| 13 | Footer | Oculto («© 2023 eramic») | Footer con marca, navegación, contacto, legal | **No existe footer** | La página termina en seco | Alta (Theme Builder) | Medio | Construir footer definitivo con año dinámico |
| 14 | Movimiento | Ninguno | Discreto y consistente | Ausencia total | Está bien no animar, pero falta un momento autoral | Alta (clases + interacciones nativas) | Bajo | 2–3 momentos: revelado escalonado, regla del método, hover de imagen |
| 15 | Fotografía tratada como composición | Imagen como bloque | Recortes intencionales, a sangre, superpuestos | Diferencia de tratamiento | Sin esto, la foto sigue siendo adorno | Media | Medio: superposición mal hecha rompe accesibilidad | Recorte y `object-position` decididos; sin superposición hasta validar |

## Lectura de conjunto

La paleta, los botones y el registro tipográfico **ya están alineados** —se copiaron del mismo lenguaje. La distancia se concentra en cinco puntos: **ancho de contenedor, aire, asimetría, fotografía propia y ritmo de bandas**. Ninguno exige comprar un theme; cuatro se resuelven con grid, clases y contrato, y el quinto (fotografía) es un insumo que falta.

## Lo que no se puede cerrar con CSS

- Fotografía real: sin ella, la modernidad se queda en maqueta.
- Header y footer: son estructura del sitio, no estilo.
- Método documentado: sin etapas y entregables, la banda de método no se puede diagramar.

## Conclusión

La brecha es de **composición y contenido**, no de theme. Leroux se usa como vara, no como compra.
