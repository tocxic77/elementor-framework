# RUNBOOK · publicación pennacchiotti.cl · 2026-10-31

Ejecutable hoy, en este orden. Cada bloque termina en una comprobación que se mide, no se supone.
No contiene decisiones de diseño: todas están tomadas y firmadas.

Rutas de este paquete:

```
deploy/assets/   siete archivos listos para subir (2400 px de ancho, 2,5 MB en total)
deploy/html/     los cinco cuerpos de página, listos para pegar en Elementor
```

---

## Bloque 0 · copia de seguridad (bloqueante)

1. `https://pennacchiotti.cl/wp-admin/plugin-install.php?s=backuply` → instalar y activar **Backuply**.
2. Backuply → *Create Backup* → descargar el `.zip` al disco.
3. Comprobar el archivo, no el botón: abrir el zip y verificar que contiene `wp-content/uploads` y un `.sql` de base de datos del tamaño esperado.

**Verificación:** el zip existe en disco, pesa >50 MB y contiene el dump. Sin esto no se ejecuta el Bloque 1.

---

## Bloque 1 · rutas

| Página actual | Acción | Slug destino |
|---|---|---|
| `our-services` | Páginas → Editar → Enlace permanente | `soluciones` |
| `our-story` | idem | `sobre-mi` |
| `contact-us` | idem | `contacto` |
| — | Páginas → Añadir nueva, título «Perspectivas» | `perspectivas` |

**Verificación (la corro yo):** `/`, `/soluciones/`, `/perspectivas/`, `/sobre-mi/`, `/contacto/` → 200, y los cuatro `404` de hoy desaparecen.

---

## Bloque 2 · demo

1. Entradas → seleccionar las 12 (todas del 2023-02-06) → *Papelera* → vaciar papelera.
2. Páginas → `global-styles` → estado **Borrador**.

**Verificación:** `/global-styles/` deja de responder 200, el feed queda sin elementos y el sitemap baja a 5 URLs.

---

## Bloque 3 · media

1. Subir los siete archivos de `deploy/assets/` (Medios → Añadir nuevo).
   `texturometro-medicion-2400.jpg` es vertical de origen (2400×4266): la versión `-16x9` (2400×1350) es la que
   usa la banda P2; la vertical queda por si se necesita el instrumento completo.
2. Borrar los **119 placeholders** de `media_clasificado.csv` (columna `final` = `C_placeholder` y `en_uso` ≠ True).
3. No borrar todavía los 166 de kit: siguen en uso por las páginas demo hasta que estén intervenidas.

**Verificación:** biblioteca por debajo de 190 archivos, y ninguna página con imagen rota.

---

## Bloque 4 · contenido

1. **CSS:** subir `tokens.css`, `theme.css`, `utilities.css` e `instance.css` de `deploy/theme/` a
   `wp-content/themes/hello-elementor-child/`
   (cPanel → Administrador de archivos), y añadir a `functions.php` del child theme:

   ```php
   add_action('wp_enqueue_scripts', function () {
       foreach (['tokens','theme','utilities'] as $f) {
           wp_enqueue_style("pp-$f", get_stylesheet_directory_uri() . "/$f.css", [], '1.0');
       }
   });
   ```

2. **Plantillas:** por cada una de las 5 páginas → Elementor → *Configuración de página* → plantilla **Elementor Canvas**.
3. **Contenido:** un único widget **HTML** por página, con el archivo correspondiente de `deploy/html/`.
4. **Activos:** reemplazar `__UPLOADS__/` por la URL real de cada archivo subido en el Bloque 3
   (típicamente `https://pennacchiotti.cl/wp-content/uploads/2026/11/`).
5. **Formulario:** en `/contacto/`, sustituir el `<form>` estático por el widget **Form** de Elementor Pro,
   con destino `mario@pennacchiotti.cl`, y probar un envío real.

**Verificación:** las cinco rutas responden 200 con `h1` único, cero desborde a 390 px, contraste ≥4,5:1 medido
sobre lo publicado, y un correo de prueba recibido.

---

## Bloque 5 · medición a 30 días

Un contador de envíos del formulario, con fecha de inicio = fecha de publicación. Sin eso, `d4` no se puede cumplir.

---

## Lo que queda fuera, con motivo

| Pieza | Motivo |
|---|---|
| Retrato en `/contacto/` | no existe; la página funciona sin él y se agrega cuando haya sesión |
| Caso documentado #01 | no existe y no se inventa; la banda de casos se retiró |
| `linea marraqueta.jpg` | autorización pendiente con la planta |
| `indicadores nir.jpeg` | valores de lote legibles: anonimizar antes de publicar |
| 166 activos de kit | se borran cuando las páginas demo dejen de usarlos |
