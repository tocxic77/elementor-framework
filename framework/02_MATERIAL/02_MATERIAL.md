# 02_MATERIAL — qué existe, en qué estado y qué falta

## Decide

Qué material hay y **en qué clase cae cada pieza**, con criterio medible:

| Clase | Criterio objetivo |
|---|---|
| Usable | ≥2400 px de ancho, ratio entre 16:9 y 21:9, abre sin error |
| Usable con edición | abre, pero exige recorte, reencuadre o reescalado declarado |
| No usable como imagen | sirve como documento (captura, planilla) o es un icono |
| Faltante / defectuoso | no abre, o no existe y el `01_NEED` lo exige |

Una pieza sin medidas no está clasificada. «Se ve bien» no es una clase.

## Ubicación

```
framework/02_MATERIAL/MATERIAL_TEMPLATE.md   plantilla y criterios
<cliente>/02_MATERIAL.md                     instancia medida
<cliente>/Imagenes/ · <cliente>/video/       archivos originales, nunca movidos
```

Los originales no se tocan: se clasifican. La copia optimizada va en el sitio, no aquí.

## Evidencia (afirmaciones)

La ranura guarda dos cosas distintas y las dos se miden:

| Qué | Archivo | Puerta |
|---|---|---|
| Activos: fotos, video, documentos, con medidas | `<cliente>/02_MATERIAL.md` | este archivo |
| Afirmaciones publicables, con fuente y autorización | `<cliente>/02_EVIDENCE.yaml` | `tools/verificar_evidencia.py` |

Una cifra vive en `02_EVIDENCE.yaml` con `estado: validada`, `fuente` y fecha de
autorización; o vive como `rechazada` con su motivo. No existe una tercera categoría.
La puerta comprueba además que la página no publique ninguna cifra rechazada y que toda
cifra publicada tenga afirmación validada.

## Revisión

| Comprobación | Criterio | Bloquea |
|---|---|---|
| Cada ítem tiene medidas | ancho × alto y peso en KB | sí |
| Clase coherente con la medida | un «usable» <2400 px es un error de clasificación | sí |
| Archivos que no abren | listados con nombre y peso | sí (se reexportan) |
| Faltantes explícitos | ≥1 nombrado, o «sin faltantes» con razón | no |
| Video | resolución, duración y formatos por clip | no |
| Afirmaciones validadas con fuente | archivo existente o fuente citable | sí |
| Cifras rechazadas publicadas | 0 en la página | sí |

**Regla de derivación:** cada banda prevista en `04_DIRECTION` debe poder señalar el archivo que la llena. Banda sin archivo es banda sin imagen, y eso se decide en `03_CURATION`, no al final.
