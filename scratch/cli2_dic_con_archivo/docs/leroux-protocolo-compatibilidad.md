# Protocolo de compatibilidad Leroux ↔ Elementor MCP

**Estado:** no ejecutado. Requiere WordPress temporal con acceso SSH o panel de staging.
**Regla:** no se compra ni se instala Leroux en producción. Este protocolo decide con datos, no con impresiones.

---

## Hipótesis a refutar

> «Un theme de ThemeForest con widgets propios puede ser gobernado por el MCP de Elementor igual que Hello Elementor.»

Tres niveles que hay que separar, porque el marketing del theme solo responde al primero:

| Nivel | Pregunta | Cómo se verifica |
|---|---|---|
| 1 | ¿Funciona con Elementor? | Declarado por el autor: sí. No se verifica, se asume |
| 2 | ¿El MCP lee sus páginas? | `elementor-get-page-structure` sobre la demo importada |
| 3 | ¿El MCP edita sus widgets? | `list-widget-schemas` + `manage-elements` sobre cada sección crítica |

**El nivel 3 es el único que importa.** «Compatible con Elementor» no significa «controlable por MCP».

## Montaje

1. WordPress limpio (subdominio o contenedor), sin plugins previos.
2. Instalar Leroux + `leroux-core` + Qi Addons + cualquier plugin requerido por la demo.
3. Importar la demo completa.
4. Elementor Pro (misma versión que producción: 4.3.5) + Hello Elementor desactivado, no eliminado.
5. Activar el MCP de Elementor y el adaptador de WordPress.
6. Conectar Hermes con una app password **de staging**, nunca la de producción.

## Inventario de widgets

```
1. total de widgets en el demo
2. widgets nativos Elementor V4
3. widgets de Qi Addons
4. widgets de Leroux/Qode
5. widgets de terceros (sliders, portfolios, banners)
6. widgets con schema expuesto por list-widget-schemas
7. widgets sin schema       ← el número que decide la compra
```

**Umbral:** si los widgets sin schema superan el 10 % de los elementos críticos, no comprar.

## Cinco secciones críticas a probar

Header, hero, servicios/oferta, método, footer.

Para cada una, ejecutar en este orden y anotar resultado binario:

| Operación | Herramienta | Éxito |
|---|---|---|
| Leer estructura | `get-page-structure` | la sección aparece con nodos |
| Cambiar texto | `manage-elements` update | persiste tras publish |
| Cambiar imagen | `manage-elements` update (`image.src.id`) | renderiza el adjunto nuevo |
| Modificar columnas | `manage-elements` (grid/flex) | cambia sin romper |
| Aplicar clase del kit | `manage-classes` + update | clase visible en HTML |
| Cambiar responsive | `manage-classes` con `@media(--bp)` | cambia solo en ese breakpoint |
| Modificar animación | settings del widget | se guarda y se ve |
| Duplicar sección | `manage-elements` duplicate | duplica con ids nuevos |
| Crear componente | `manage-component` | aparece en la librería |
| Publicar copia | `publish-document` | commitea sin mover `page_on_front` |

## Criterios de compra (todos obligatorios)

- [ ] ≥ 90 % de los elementos críticos editables por MCP.
- [ ] Ninguna dependencia estructural de widgets sin schema.
- [ ] Header y footer reemplazables por Theme Builder sin pelear con el theme.
- [ ] Páginas siguen editables en el editor de Elementor después de aplicar cambios por MCP.
- [ ] Actualización del theme no sobrescribe personalizaciones (probar con un update simulado).
- [ ] No obliga a mantener dos sistemas visuales en paralelo.
- [ ] Rendimiento: no añade más de 200 KB de JS ni duplica jQuery.
- [ ] Responsive propio no compite con el de Elementor.
- [ ] Calificación y soporte del autor aceptables (hoy ≈ 4,02/5: no es un argumento a favor).

## Riesgos de lock-in a documentar

1. **Widgets propietarios en secciones centrales** → si el theme se abandona, esas secciones no se pueden editar.
2. **Opciones de theme** que solo existen en su panel y no en variables de Elementor.
3. **CSS del theme con `!important`** que gana sobre las clases del kit.
4. **Dependencia de Qi Addons** para animaciones o layouts.
5. **Importador de demo** que crea páginas con plantillas propias, no con el árbol de Elementor.
6. **Actualizaciones** que reintroducen estilos sobrescritos.

## Costo real

| Concepto | Estimación |
|---|---|
| Licencia | ~USD 60–80 |
| Staging | 2–4 horas de montaje |
| Prueba de las 5 secciones | 2–3 horas |
| Rehacer el sistema en sus componentes | 3–5 días |
| Riesgo de lock-in | permanente |

Frente a: **cero costo** por extraer escala, aire, asimetría y ritmo con grid y clases del kit —que es lo que la matriz de FASE 1 muestra como brecha real.

## Decisión por defecto

**No comprar.** Se reevalúa solo si el protocolo demuestra que la calidad visual no se puede reproducir con widgets nativos, y que al menos el 90 % de los elementos críticos es editable por MCP.
