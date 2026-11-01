# 04_DIRECTION — la ley visual (y sólo eso)

## Decide

- **Tres decisiones de firma**: restricciones verificables, no adjetivos. Ejemplo: `oversized-numerals`, `1px-dividers`, `ink-duotone`.
- **Antirreglas**: lo prohibido, con su razón. Mínimo cinco.
- **Tipografía**: una familia display y una de texto. Las declaradas deben ser las cargadas.
- **Color**: paleta con contraste computado, no con hex «elegidos».
- **Fotografía**: tratamiento (duotono, recorte, ratio) y qué se prohíbe (banco de imágenes).
- **Evidencia visual**: nivel de cada activo (real · derivada · generada), qué banda admite cada
  nivel y la regla «una generada no reemplaza un real disponible». Vive en `IMAGE_STRATEGY.md`.
- **Motion**: dónde hay movimiento y dónde no.
- **Composición**: cómo se diferencian dos bandas consecutivas.

**Lo que NO decide: la tecnología.** Elegir WordPress, Elementor o HTML plano depende de quién
edita el sitio (`01_NEED`) y del presupuesto, y se resuelve en el adaptador. Mezclar las dos
decisiones es cómo un proyecto termina con un tema comprado antes de tener ley visual.

## Ubicación

```
framework/04_DIRECTION/DIRECTION_TEMPLATE.md   plantilla de 10 secciones
framework/04_DIRECTION/firmas.md               catálogo de firmas reutilizables
framework/04_DIRECTION/IMAGE_STRATEGY.md       niveles A/B/C, prioridad por banda, regla ejecutable
framework/04_DIRECTION/prompts.yaml            base de prompts por categoría (uso nivel C)
<cliente>/DIRECTION.md                         instancia, versionada, con enmiendas fechadas
<cliente>/03_ASSETS.yaml                       inventario medido de activos con su nivel
```

El brief visual de un proyecto **no es un archivo más**: es la vista que resulta de cruzar
`03_ASSETS.yaml` (qué existe) con `IMAGE_STRATEGY.md` (qué hace falta por banda). Se genera
cuando se pide y se pega en la conversación; no se mantiene a mano.

## Revisión

| Comprobación | Criterio | Bloquea |
|---|---|---|
| Tres firmas nombradas | cada una medible en el CSS/DOM | sí |
| Antirreglas | ≥5, cada una con criterio de detección | sí |
| Familias tipográficas | declaradas == cargadas (medido en red, no en el doc) | sí |
| Contraste | 0 textos bajo 4,5:1 (3:1 si ≥24 px) **computado** | sí |
| Toda excepción | enmienda con fecha, motivo y qué se acepta perder | sí |
| Alcance de la firma | declara que congela reglas, no el estado estético | sí |
| Nivel de cada activo | real · derivada · generada, declarado en `03_ASSETS.yaml` | sí |
| Generada con hueco real libre | 0 casos; la puerta nombra el archivo desplazado | sí |
| Ancho de imagen | ≥2400 px para banda completa; si no, no va a sangre | no |

**Regla de la casa:** la ley no se rompe en silencio. Una excepción sin enmienda es un defecto,
aunque se vea mejor.
