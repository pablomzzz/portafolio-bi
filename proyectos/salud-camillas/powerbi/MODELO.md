# Modelo semántico — Salud: Ocupación de camillas

Documentación del modelo de datos del reporte `camillas.pbip` / `camillas.pbix`.

## Fuente de datos
`../data/ocupacion_camillas.csv` (UTF-8, datos sintéticos). 26.280 filas =
365 días × 4 hospitales × 6 servicios × 3 turnos.

## Arquitectura
Modelo de **tabla única** (flat table). El grano de la tabla de hechos es
suficientemente fino para todos los análisis, no requiere dimensiones separadas.

**Grano:** 1 fila = 1 medición de ocupación (hospital × servicio × turno × día).

## Tabla: `ocupacion_camillas`

| Columna | Tipo | Descripción |
|---|---|---|
| `fecha` | Fecha | Día de la medición |
| `hospital` | Texto | Establecimiento (ficticio) |
| `servicio` | Texto | Pabellón / servicio clínico |
| `turno` | Texto | Mañana / Tarde / Noche |
| `camillas_totales` | Entero | Capacidad instalada |
| `camillas_ocupadas` | Entero | Camillas en uso |
| `tasa_ocupacion` | Decimal | ocupadas / totales (0-1) |
| `pacientes_en_espera` | Entero | Pacientes sin camilla asignada |
| `tiempo_espera_min_prom` | Entero | Espera promedio (minutos) |

## Columnas calculadas

**`Temporada`** — clasifica invierno (mayo-agosto) vs resto del año:
```dax
Temporada =
IF(
    MONTH('ocupacion_camillas'[fecha]) >= 5 && MONTH('ocupacion_camillas'[fecha]) <= 8,
    "Invierno",
    "Resto del año"
)
```

## Medidas (DAX)

| Medida | Fórmula | Uso de negocio |
|---|---|---|
| `Mediciones` | `COUNTROWS('ocupacion_camillas')` | Volumen de datos analizado |
| `% Critico` | `DIVIDE(CALCULATE(COUNTROWS(...), tasa_ocupacion >= 0.95), COUNTROWS(...))` | % de turnos en ocupación crítica |
| `Pacientes en espera` | `SUM('ocupacion_camillas'[pacientes_en_espera])` | Demanda insatisfecha total |
| `Ocupacion promedio` | `AVERAGE('ocupacion_camillas'[tasa_ocupacion])` | Presión media de capacidad |

```dax
% Critico =
DIVIDE(
    CALCULATE(COUNTROWS('ocupacion_camillas'), 'ocupacion_camillas'[tasa_ocupacion] >= 0.95),
    COUNTROWS('ocupacion_camillas')
)
```

## Decisiones de modelado
- **Umbral crítico = 95%** de ocupación: por encima, el pabellón no absorbe más demanda.
- **Tabla única** en vez de estrella: el dataset es pequeño y de un solo grano; una
  estrella añadiría complejidad sin beneficio (YAGNI).
- `% Critico` y `Ocupacion promedio` formateadas como porcentaje.

## Pregunta de negocio que responde
¿Qué pabellón se queda sin camillas este turno? → priorizar refuerzo de capacidad
y anticipar la campaña de invierno.
