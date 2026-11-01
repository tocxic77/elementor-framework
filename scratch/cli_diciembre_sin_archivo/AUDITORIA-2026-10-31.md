# AUDITORÍA · pennacchiotti.cl · 2026-10-31

Medido sobre el sitio en vivo, sin tocar nada. Lo que sigue son hechos con su evidencia, no
impresiones.

## Veredicto

**La instalación está limpia. El contenido no.** Se pasó de 11 plugins y 73 recursos a 4
plugins y 46 recursos, y el tema ya es `hello-elementor` + `hello-elementor-child` — es decir,
E-7 no hay que construirla, ya existe. Pero lo que hay publicado es el contenido de
demostración de un kit de Elementor, con la navegación en español apuntando a páginas que no
existen.

## Medido

```
WordPress 7.1.4 · Elementor 4.3.5 + Pro · CookieAdmin + Pro
tema        hello-elementor + hello-elementor-child v2.0.1 (style.css 603 B, sin CSS propio)
home        200 · 144.925 B · 533 palabras visibles · 1 h1 · 0 style="" · 32 CSS · 14 JS
páginas     5 publicadas: home, our-story, our-services, contact-us, global-styles
entradas    12 publicadas, todas del 2023-02-06, ~701 palabras, en inglés (demo)
media       314 archivos · 93 en la primera página: 52 jpeg, 36 png, 1 mp4, 1 webp, 1 svg
sitemap     wp-sitemap.xml + sitemap_index.xml, 200
```

## Defectos, por gravedad

| # | Defecto | Evidencia | Efecto |
|---|---|---|---|
| 1 | **Hero de demostración publicado** | «This Headline Grabs Visitors' Attention · A short description of your business» en `/` | la portada no dice nada y está indexada |
| 2 | **4 enlaces de navegación muertos** | `/soluciones/` `/perspectivas/` `/sobre-mi/` `/contacto/` → **404** | la navegación en español no lleva a ninguna parte; las páginas reales son `our-services`, `our-story`, `contact-us` |
| 3 | **12 entradas demo publicadas** | 2023-02-06, ~701 palabras, inglés, «Business & plan scheming» | contenido ajeno indexable, en el sitemap |
| 4 | **Sin formulario en contacto** | `/contact-us/` = 0 `<form>`, 3 `<input>` | A4 es imposible: no hay acción primaria ejecutable |
| 5 | **314 archivos de media, mayoría de kit** | `image_placeholder-13122021`, `hero-bg-image`, `our-story-400_380`, `placeholder-png-7` | 20 fotos propias sepultadas entre placeholders |
| 6 | **`global-styles` publicada** | `/global-styles/` → 200 | documento interno de Elementor expuesto e indexable |
| 7 | **Sin copia de seguridad** | no hay Backuply ni plugin equivalente entre los 4 | cualquier intervención en producción es irreversible |
| 8 | **Sin plugin SEO** | no aparece ninguno en el HTML | títulos y descripciones dependen de Elementor |

## Lo que sí está bien y no hay que deshacer

- 4 plugins: el ruido anterior (`revslider`, `custom-twitter-feeds`, `instagram-feed`, `qi-addons`, `leroux-core`, `spectra-blocks`) desapareció.
- 32 CSS + 14 JS, contra 41 + 32 medidos el 28-oct.
- `hello-elementor-child` presente: es el lugar de `tokens.css`, `theme.css` y `utilities.css` (E-7).
- 1 `h1` por página y 0 estilos en línea: la disciplina del sistema se sostiene sola.
- Sitemap y `robots.txt` correctos.

## Limpieza, en este orden

1. **Borrar las 12 entradas demo** (papelera + vaciar). Antes, comprobar que ninguna tiene contenido propio: las fechas son todas 2023-02-06 y el texto es de kit.
2. **Despublicar `global-styles`** (borrador o privada).
3. **Renombrar las tres páginas demo** a las rutas decididas: `our-services` → `/soluciones/`, `our-story` → `/sobre-mi/`, `contact-us` → `/contacto/`. `Perspectivas` no existe como página: se crea. Esto elimina los 4 × 404 de una vez.
4. **Vaciar la biblioteca de media de placeholders** — no a ciegas: primero listar los 314 y conservar los que tengan EXIF de cámara o nombre propio (`img-20240420-wa0039`, `sourdough_bread*`).
5. **Instalar Backuply y hacer una copia con restauración comprobada** antes de cualquier otra cosa en producción.
6. **Formulario**: usar el widget Form de Elementor Pro (ya está licenciado) en `/contacto/`, con destino `mario@pennacchiotti.cl`. No hace falta reinstalar Contact Form 7.

## Lo que esto cambia en el framework

El hallazgo 2 es un defecto de proceso, no de contenido: la navegación y las páginas se
editaron por separado y nadie midió el resultado. `06_DEPLOYMENT` gana una comprobación
permanente: **0 enlaces internos con 404 en la navegación y en el pie**, medida antes de
publicar.
