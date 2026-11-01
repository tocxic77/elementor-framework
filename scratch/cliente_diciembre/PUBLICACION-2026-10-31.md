# PUBLICACIÓN · pennacchiotti.cl · 2026-10-31 18:2x UTC

Ejecutado sobre producción con acceso FTP del hosting y la clave de aplicación de WordPress.
Todo lo que sigue se midió después de publicar, no antes.

## Las cuatro mediciones que deciden

| Medición | Resultado |
|---|---|
| 200 OK en las cinco rutas | ✅ `/` `/soluciones/` `/perspectivas/` `/sobre-mi/` `/contacto/` |
| H1 único por página | ✅ 1 en cada una (gate `h1-unico`) |
| Contraste real en producción | ✅ mínimo **5,44:1**, 10/10 PASS a 1440 y 390 |
| Envío exitoso del formulario | ✅ `nonce=ok mail=ok`, confirmación visible en `?enviado=1` |

Rutas retiradas: `/our-services/`, `/our-story/`, `/contact-us/`, `/global-styles/` → **404**.
Sitemap: exactamente 5 URLs. Feed: 0 elementos. 12 entradas demo a papelera.
Biblioteca: **119 adjuntos placeholder borrados**.

## Backup

`pp-backup-20261031-181857.sql` · 22,6 MB · 76 tablas · 23.604 filas, descargado y conservado.

**Restauración: no comprobada.** No existe una base de prueba donde volcarlo. El archivo prueba que hay
una copia, no que la copia levante. Es la única comprobación de la puerta que sigue abierta.

## Desvíos respecto del runbook, y por qué

1. **El HTML se sirve desde archivos, no desde Elementor.** El kit atómico de Elementor 4.3.5 no incluye
   widget HTML; las opciones eran reconstruir el diseño en widgets —prohibido por el congelamiento— o
   servir el markup propio. Las páginas son documentos de WordPress con plantilla Elementor Canvas y el
   contenido lo entrega `mu-plugins/pp-publicar.php` desde `pp-pages/`. Publicar un cambio = subir un archivo.
2. **El formulario usa `wp_mail` con GoSMTP**, no el widget Form de Elementor Pro. Mismo destino
   (`mario@pennacchiotti.cl`), sin dependencia de licencia ni de plantilla.
3. **Los siete activos viven en el child theme `/assets/`**, no en la biblioteca de medios. Se migran
   a Medios cuando haya razón para editarlos desde el panel.

## Avisos abiertos

- 13 elementos con `style=` inyectados por el contenedor de Elementor (no por el HTML propio: el gate estático sigue en 18/18).
- 2 controles por debajo de 24 px de alto.
- `pp.css` del child theme tiene reglas `page-id` del sitio anterior: se desencola, no se borra.
- El menú «Main Menu» (9 ítems) sigue apuntando a `leroux.qodeinteractive.com`: no se renderiza porque las páginas usan Canvas, pero existe en la base.

## Capturas

`05_SYSTEM/capturas/2026-10-31-publicado/publicado-1440-{inicio,soluciones,perspectivas,sobre-mi,contacto}.png`
