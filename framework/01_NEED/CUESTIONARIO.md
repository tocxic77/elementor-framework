# Cuestionario de descubrimiento — bloquea el avance

Se responde **antes** de escribir una línea de HTML, CSS o copy. Cada respuesta lleva
`fuente` (documento:línea, correo, acta, archivo). Una respuesta sin fuente no cuenta como
respuesta: cuenta como pendiente.

El archivo que se llena es `<cliente>/01_NEED.yaml`. La puerta es ejecutable:

```bash
python framework/tools/verificar_need.py <cliente>/01_NEED.yaml
```

Si falta una respuesta de nivel `bloquea`, el comando sale con código 1 y el proyecto no
avanza a `02`, `04` ni `05`. No es una recomendación: es una salida de proceso.

## A · Negocio — 6 preguntas

| # | Pregunta | Nivel | Por qué bloquea |
|---|---|---|---|
| A1 | ¿Qué se vende, en una frase que el comprador reconocería? | bloquea | sin esto el copy es adorno |
| A2 | ¿Qué problema resuelve y en qué se nota que existe? | bloquea | el sitio se ordena por problema, no por servicios |
| A3 | ¿Qué alternativa usa el comprador si esta organización no existiera? | bloquea | sin alternativa no hay diferenciación, sólo catálogo |
| A4 | ¿Qué debe lograr el sitio? (una acción primaria, medible) | bloquea | un sitio con dos acciones no tiene ninguna |
| A5 | ¿Qué se puede afirmar con evidencia propia? | bloquea | toda cifra necesita fuente o no se publica |
| A6 | ¿Qué está prohibido decir? | avisa | protege confidencialidad y posicionamiento |

## B · Audiencia — 5 preguntas

| # | Pregunta | Nivel | Por qué |
|---|---|---|---|
| B1 | ¿Quién firma el contrato? | bloquea | define el registro y el largo del argumento |
| B2 | ¿Quién influye y quién usa? | avisa | define qué evidencia convence |
| B3 | ¿Cuál es la objeción principal antes de escribir? | bloquea | la primera banda de la página responde a esa objeción |
| B4 | ¿Qué sabe ya el comprador? | avisa | evita explicar de más o de menos |
| B5 | ¿En qué contexto lee? (móvil, oficina, feria) | info | decide la medida de lectura y el peso |

## C · Evidencia — 5 preguntas

| # | Pregunta | Nivel | Por qué |
|---|---|---|---|
| C1 | ¿Qué fotografías y videos existen, con qué medidas? | bloquea | sin material propio la estética se vuelve préstamo |
| C2 | ¿Qué afirmaciones están autorizadas y con qué fuente? | bloquea | sin esto no hay cifras publicables |
| C3 | ¿Qué material está vetado por confidencialidad? | bloquea | el veto se declara antes, no se descubre después |
| C4 | ¿Qué falta y cuánto cuesta conseguirlo? | avisa | lo que falta con costo es una decisión, no un olvido |
| C5 | ¿Quién autoriza el uso de cada pieza? | avisa | sin autoría no hay permiso |

## D · Operación — 4 preguntas

| # | Pregunta | Nivel | Por qué |
|---|---|---|---|
| D1 | ¿Quién edita el sitio después de entregarlo? | bloquea | decide cuánto puede vivir en el builder |
| D2 | ¿Qué puede cambiar esa persona sin romper el sistema? | avisa | define el límite de los patrones |
| D3 | ¿Quién firma la dirección visual? | bloquea | sin firma no se elige tipografía ni color |
| D4 | ¿Cuándo se revisa? | info | un sistema sin fecha de revisión se vuelve fósil |

## Resultado

```
NEED COMPLETO   → se puede escribir 02 y 04
NEED BLOQUEADO  → falta: A3, B3, D3   (3 bloqueantes, 0 avisos)
```

La salida nombra cada faltante. Nunca dice «incompleto» sin decir qué falta.
