# 01_NEED — por qué este sitio debe existir

## Decide

- **Por qué existe**: el problema de negocio, en una frase que un tercero pueda repetir.
- **Quién compra**: el que firma, no el que navega. Nombre del rol, no demografía.
- **Acción esperada**: un verbo medible (agendar, cotizar, descargar). «Que conozca la marca» no es una acción.
- **Restricciones duras**: presupuesto, plazo, y **quién edita el sitio después de entregarlo**. Esta última decide el adaptador (HTML plano, WordPress, otro) y no tiene nada que ver con la estética.
- **Condición de no-empezar**: sin `02_MATERIAL` clasificado, no se abre `04_DIRECTION`. Sin acción esperada, no se abre nada.

## Ubicación

```
framework/01_NEED/NEED_TEMPLATE.md          plantilla
<cliente>/01_NEED.md                        instancia (una sola)
```

La instancia vive con el cliente. Aquí sólo la plantilla y lo aprendido de proyectos anteriores.

## Revisión

| Comprobación | Criterio | Bloquea |
|---|---|---|
| Los cinco campos están completos | 0 campos vacíos | sí |
| Acción esperada | es verificable con un evento que se pueda contar | sí |
| Quién edita | nombrado y con su consecuencia técnica escrita | sí |
| Restricción de plazo | fecha o rango, no «pronto» | no (se registra) |
| Coherencia con `02_MATERIAL` | ningún objetivo exige material que no existe | sí |

**Firma de esta ranura:** la revisa quien encarga el sitio. Un `01_NEED` que el cliente no reconoció como suyo produce un sitio que el cliente no reconoce.
