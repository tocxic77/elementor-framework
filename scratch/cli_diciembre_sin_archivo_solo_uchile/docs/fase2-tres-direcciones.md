# FASE 2 — Tres direcciones para la Home

**Fecha:** 23 de octubre de 2026
**Regla:** las tres conservan Newsreader, DM Sans, marfil `#FBFAF9`, tinta `#223035`, salvia `#D5DEDE`, el posicionamiento aprobado (oferta A como qué; digital, IA y conocimiento como cómo) y el CTA «Agendar una conversación».
**Ninguna se construye todavía.** Se elige una, se escribe su contrato y recién entonces se toca Elementor.

---

## Vector común

```yaml
sobriety: 8
modernity: 8
editorial_character: 9
technological_feel: 3
animation_intensity: 4
conversion_clarity: 9
```

| | A. Editorial contemporánea | B. Consultora boutique | C. Técnica-operacional |
|---|---|---|---|
| asymmetry | 6 | 5 | 7 |
| image_presence | 7 | 9 | 5 |
| density | media | baja | alta |

---

## A. Editorial contemporánea

**Idea:** la página es un documento bien impreso. La autoridad viene de la tipografía y del espacio, no de las imágenes.

- H1 a 80–88 px en Newsreader, tres líneas, sin imagen de fondo: texto sobre marfil.
- Bandas con mucho aire (160 px), reglas de 1 px como separadores, numeración editorial en el método.
- Dos imágenes en toda la página, ambas a sangre y en blanco y negro para que no compitan con el texto.
- Asimetría 5/7 en la banda de oferta; el resto a una columna con medida de 65 caracteres.
- Movimiento: solo revelado de texto y la línea del método que se dibuja.

**Riesgo:** sin fotografía propia puede leerse como «blog». Exige copy de altísima calidad.
**Qué necesita:** 2 fotos, ninguna adicional.
**Cuándo elegirla:** si la prioridad es autoridad técnica y el material fotográfico seguirá escaso.

---

## B. Consultora boutique

**Idea:** el sitio se parece a la memoria de una firma: fotografía tratada como material, composición con aire y detalle fino.

- Hero a sangre con fotografía contextual (planta, instrumentos, documentos) a 640 px, texto sobre velo de tinta al 55 %.
- Alternancia fuerte: marfil / tinta / salvia, con una banda a sangre de imagen por cada dos de texto.
- Asimetría 4/8 y 7/5; figuras que se salen del contenedor hacia la derecha.
- Escala tipográfica completa con `pp-h4`; numeración en método; flechas en CTA.
- Movimiento: tres momentos —revelado escalonado, zoom 1,03 en imagen, hover tipográfico.

**Riesgo:** es la dirección que más depende de fotografía real; con imágenes sintéticas se cae.
**Qué necesita:** 6–8 fotos propias.
**Cuándo elegirla:** si se consigue el banco fotográfico y se quiere la percepción más cercana a Leroux.

---

## C. Técnica-operacional

**Idea:** la página funciona como un plano de proceso: densa, precisa, con datos y estructura visible.

- H1 64 px, medida corta; el resto en rejilla de 12 columnas con asimetría 3/9.
- Bandas oscuras frecuentes; diagramas de flujo construidos con `e-grid` y reglas, no con imágenes.
- Señales cualitativas en lugar de cifras: «un turno, un criterio, una persona».
- Una sola fotografía, documental y en primer plano de material o instrumento.
- Movimiento: solo la secuencia del método por etapas.

**Riesgo:** puede volverse fría o incomprensible para un dueño de empresa que no es técnico.
**Qué necesita:** el método documentado para poder diagramarlo.
**Cuándo elegirla:** si el método existe y se quiere diferenciar por rigor, no por estética.

---

## Recomendación

**A como base, con dos préstamos de B:** el hero con fotografía a sangre y una banda de imagen en la sección de método. Razón: A no depende del banco fotográfico para sostenerse, y B aporta la única cosa que hoy no tenemos —imagen tratada como material— sin exigir seis fotos que no existen.

C y B quedan como dirección para `/sobre-mi/` y `/soluciones/` respectivamente, cuando haya material.

## Lo que falta para poder construir cualquiera de las tres

1. Decisión de dirección (esta conversación).
2. Contrato de Home con `node_tree`, `cardinalidad` y `forbidden`.
3. `pp-stack`, `pp-cluster` y `pp-h4` creadas en el kit.
4. Header y footer construidos en Theme Builder.
5. Al menos dos fotografías propias para A, seis para B.
6. Copy de la Home aprobado con evidencia validada o eliminada.
7. Regeneración de CSS y datos ejecutada por ti (sin eso el render sigue congelado).
