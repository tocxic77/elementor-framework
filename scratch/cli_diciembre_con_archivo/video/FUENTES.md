# Hero en video — PENNACCHIOTTI

Reemplazo del video demo del slider `business-home` (Slider Revolution 7.x) que hoy
sirve la portada. El original (`business-rev-video.mp4`, 1920×1080, 10 s) trae una
marca de agua horneada en el píxel —un logotipo de banco de imágenes que los lectores
ópticos transcriben como «L8RX» / «LiRX»— y por eso no se puede «personalizar» con
una capa de texto encima: hay que sustituir el metraje.

## Entregables

| Archivo | Formato | Duración | Peso | Uso |
|---|---|---|---|---|
| `pp-hero-flujo-1080p.mp4` | 1920×1080, 30 fps, H.264 | 10,0 s | 2,97 MB | Opción A: granos cayendo sobre cinta |
| `pp-hero-flujo-9x16.mp4` | 1080×1920, 30 fps | 10,0 s | 3,23 MB | Opción A en móvil |
| `pp-hero-linea-1080p.mp4` | 1920×1080, 30 fps | 12,0 s | 1,74 MB | Opción B: masa cruda avanzando en la línea |
| `pp-hero-linea-9x16.mp4` | 1080×1920, 30 fps | 12,0 s | 1,52 MB | Opción B en móvil |
| `pp-hero-*-poster.jpg` | 1920×1080 / 1080×1920 | — | 50–70 KB | Póster (primer fotograma visible) |

Sin audio: el video del hero se reproduce silenciado y en bucle.

## Construcción

1. **Metraje**: Pexels, licencia Pexels (uso comercial permitido, modificación
   permitida, sin atribución obligatoria).
   - A — `https://www.pexels.com/video/efficient-conveyor-system-sorting-grains-39146545/`
     (3840×2160, 24 fps, 10 s) — granos cayendo sobre cinta, descarga de tolva.
   - B — `https://www.pexels.com/video/raw-dough-on-a-conveyor-belt-6560778/`
     (1920×1080, 25 fps, 23,5 s; se usan 6,0–18,0 s) — masa cruda en cinta azul.
2. **Gradación**: duotono al token `ink` — sombras `#0E1418`, altas luces `#ECE6DA`
   (`hue=s=0` + `lutrgb` con `k=0,72`, `gamma=1,25`), más `vignette` suave. Luminancia
   media resultante 52/255 (A) y 60/255 (B); el original estaba en 45/255.
3. **Tipografía**: `PENNACCHIOTTI` en Newsreader 400, optical size 72, tracking +0,02 em,
   `ivory #FBFAF9`, 1130 px de ancho (16:9) y 870 px (9:16), centrado óptico.
   Contraste medido texto/fondo: 246 vs 52 de luminancia ≈ 11:1.
4. **Movimiento**: entrada de 750 ms (opacidad 0→1, desplazamiento 24 px, ease-out),
   sostén y salida de 900 ms para que el bucle cierre sin salto. Cumple la regla de
   Motion del sistema de diseño (sin rebote, sin marquesina, 600–750 ms, 20–28 px).
5. **Encode**: `libx264`, CRF 25, `preset slower`, `+faststart`, `yuv420p`, sin audio.

Comando reproducible (opción A):

```bash
LUT=$(python -c "import grade; print(grade.lut(0.72,1.25))")
ffmpeg -i dl_39146545.mp4 -loop 1 -i layer_16x9_mark.png -t 10 -filter_complex "
[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,hue=s=0,$LUT,vignette=angle=PI/4.6[bg];
[1:v]format=rgba,fade=t=in:st=0.35:d=0.75:alpha=1,fade=t=out:st=8.95:d=0.90:alpha=1[ov];
[bg][ov]overlay=x=0:y='24*(1-pow(1-min(1,max(0,(t-0.35)/0.75)),3))':format=auto,format=yuv420p[v]" \
 -map "[v]" -c:v libx264 -preset slower -crf 25 -profile:v high -movflags +faststart -an pp-hero-flujo-1080p.mp4
```

## Cómo entra en el sitio

Inventario medido en la portada publicada (2026-10-26, navegador real, 1512×770):

- **Un solo slider**: módulo `SR7_7_1`, alias **`main-home`**, `y=0`, alto 770 px
  (100 % del viewport), 5 slides, sin video.
- El slider **`business-home`** —el de la demo, el que trae `business-rev-video.mp4`—
  **no está publicado** en la página: sus archivos siguen en
  `uploads/revslider/business-home/` (video, globo y flecha responden 200) pero no
  hay ninguna instancia en el DOM.

Pasos para que el video entre:

1. Subir el `.mp4` y su póster (biblioteca de medios o
   `wp-content/uploads/revslider/<alias>/`).
2. Slider Revolution → el slider publicado (`main-home`) → la slide que se quiera →
   **Slide BG Layer → HTML5 video**: URL del mp4, póster, `autoplay`, `loop`,
   `muted`, `cover`, 16:9.
3. Publicar el slider y purgar caché.

## Pendiente: por qué el hero no se parece a la demo

1. Los 5 slides de `main-home` publican titulares de la plantilla en inglés y cuatro
   botones que enlazan a `https://leroux.qodeinteractive.com/{our-process,our-clients,
   our-services,about-us}/`.
2. Tipografías del slider: Roboto y Heebo con `#AFC1C5`; fuera del sistema
   (`Newsreader` + `DM Sans`, `ivory`/`ink`/`sage`).
3. La portada devuelve **4 `h1`** (uno por slide del slider): el hero ocupa el lugar
   del H1 con copy de demo. Debe quedar un solo `h1` con el mensaje propio.
4. El mensaje propio de la portada («Procesos que se ejecutan igual, entre turnos y
   entre personas») vive más abajo, no en el hero.

## Versión máscara (2026-10-26)

La palabra como ventana: el cuadro queda en un color plano y solo las letras dejan
ver el metraje. Tres archivos:

| Archivo | Fondo | Uso |
|---|---|---|
| `pp-mascara-tinta-1080p.mp4` | `ink #223035` | publicable tal cual, 12 s, 224 KB |
| `pp-mascara-tinta-9x16.mp4` | `ink #223035` | móvil, 1080×1920, 105 KB |
| `pp-mascara-verde-1080p.mp4` | chroma `#00B140` | placa para keying, sin fundidos, 231 KB |

Medido sobre el render: 3,4 % de los píxeles son imagen (las letras), el resto es
color plano exacto; movimiento dentro de la ventana (diferencia media 10,0 entre t=2 s
y t=10 s) y cero movimiento fuera de ella.

Letra: Newsreader 500, optical 72, tracking +0,02 em, 1700 px de ancho (16:9) y 920 px
(9:16), centrada. Peso 500 en vez del 400 del sistema porque a 145 px de altura de
mayúscula el trazo de 400 deja pasar demasiado poco metraje.

Máscaras sueltas, para hacerlo en HTML en vez de en el video:
`pp-mascara-alfa-1920x1080.png` (alfa), `pp-mascara-luma-1920x1080.png` (blanco sobre
negro), `pp-mascara-alfa-1080x1920.png`.

```css
/* el video se ve solo a través de las letras; el resto es la banda ink */
.pp-hero-mascara video{
  -webkit-mask-image:url(/wp-content/uploads/pp-mascara-alfa-1920x1080.png);
          mask-image:url(/wp-content/uploads/pp-mascara-alfa-1920x1080.png);
  -webkit-mask-size:100% 100%; mask-size:100% 100%;
  -webkit-mask-repeat:no-repeat; mask-repeat:no-repeat;
}
```

Para chroma: el verde `#00B140` es plano y sin fundidos, así que keyea con tolerancia
baja; conviene dejar 1–2 px de contracción de matte para no comerse el borde del
serif.

## Versión borde (2026-10-26, corrección de Mario)

Placa `#233036`, palabra **DM Sans Black** (peso 1000, optical 40, tracking −0,03 em),
pegada al borde inferior y cortada por él.

| Archivo | Composición | Peso |
|---|---|---|
| `pp-mascara-borde-1080p.mp4` | 1856×179 px, 35 % de la altura fuera del cuadro | 183 KB |
| `pp-mascara-borde-entera-1080p.mp4` | misma letra, completa, a 36 px del borde | 265 KB |
| `pp-mascara-borde-9x16.mp4` | 1283×123 px, sangra 100 px por lado, 35 % fuera | 83 KB |

Medido sobre el render: 93,8 % de los píxeles son placa, 6,2 % imagen (las letras),
movimiento 24,0 dentro de la banda inferior y 0,0000 por encima de ella.

**Límite honesto:** un MP4 no puede garantizar el hex exacto. Con YUV 4:2:0 de 8 bits
la placa `#233036` se decodifica como `(32,45,51)`, dos o tres niveles abajo; no es un
error del archivo sino cuantización del códec. Si la placa tiene que coincidir
pixel a pixel con una sección CSS `#233036`, la vía es la máscara en HTML
(`pp-mascara-alfa-1920x1080.png` sobre un `div` con ese color) y no el video.

**Sobre la tipografía:** la del video original no es identificable con certeza —está
horneada en un clip de banco de imágenes, no declarada en ninguna hoja de estilo. Lo
medido sobre el fotograma: mayúsculas de al menos 492 px cortadas por el borde y trazo
horizontal mediano de 24 px (≈ 0,05 del alto), sobre un grotesco sin remates. DM Sans
Black es el grotesco más pesado del sistema propio y el que más se acerca; si aparece
el nombre real, el cambio es de minutos.

