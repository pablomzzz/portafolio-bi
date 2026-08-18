# Modelo semántico — Finanzas: Riesgo de empresas

Documentación del modelo de datos del reporte `finanzas.pbip` / `finanzas.pbix`.

## Fuentes de datos
1. `ratios_riesgo.csv` (en esta carpeta) — **ratios + score de riesgo ya calculados**
   por empresa (20 empresas). El análisis pesado ya está hecho en Python.
2. `../data/estados_financieros.csv` — estados crudos (80 filas = 20 empresas × 4 años).

## Arquitectura
Dos tablas:
- **resumen de riesgo**: `ratios_riesgo` (1 fila por empresa, último año)
- **serie histórica**: `estados_financieros` (para tendencias)

Relación opcional 1:N por `empresa` (si se quiere cruzar tendencia con score).

## Tabla: `ratios_riesgo`
Grano: 1 fila = 1 empresa (con sus ratios del último año y su score).

| Columna | Tipo | Descripción |
|---|---|---|
| `empresa` | Texto | Nombre (ficticio) |
| `sector` | Texto | Rubro |
| `anio` | Entero | Año del cálculo |
| `margen_neto` | Decimal | utilidad / ingresos |
| `liquidez` | Decimal | activo corriente / pasivo corriente (bajo 1 = alerta) |
| `endeudamiento` | Decimal | deuda / activo total |
| `roe` | Decimal | utilidad / patrimonio |
| `crecimiento` | Decimal | variación de ingresos año contra año |
| `score_riesgo` | Entero | Riesgo compuesto 0-100 (mayor = más riesgo) |
| `nivel` | Texto | Alto / Medio / Bajo |

## Tabla: `estados_financieros`
Grano: 1 fila = 1 empresa × año. Columnas: `empresa, sector, anio, ingresos,
utilidad_neta, activo_corriente, pasivo_corriente, deuda_total, activo_total,
patrimonio`.

## Medidas (DAX, sobre `ratios_riesgo`)
| Medida | Fórmula |
|---|---|
| `Empresas` | `DISTINCTCOUNT('ratios_riesgo'[empresa])` |
| `En riesgo` | `CALCULATE(DISTINCTCOUNT('ratios_riesgo'[empresa]), 'ratios_riesgo'[score_riesgo] >= 50)` |
| `Score maximo` | `MAX('ratios_riesgo'[score_riesgo])` |

## Score de riesgo (definición de negocio)
Compuesto 0-100, cada dimensión aporta hasta 25 puntos:
- Baja liquidez (< 1.5 empieza a sumar riesgo)
- Alto endeudamiento (> 0.4 empieza a sumar)
- Margen bajo/negativo (< 0.08 suma)
- Decrecimiento de ingresos (< 0.03 suma)

## Decisiones de modelado
- **Score pre-calculado en Python** y expuesto como CSV: la lógica de negocio vive
  en código versionado y testeable, no oculta en DAX.
- **Umbral "en riesgo" = 50**: separa cartera a revisar.
- `nivel` (Alto/Medio/Bajo) para formato condicional directo en los visuales.

## Pregunta de negocio que responde
¿Qué empresas muestran señales de riesgo? → priorizar revisión de crédito o cartera.
