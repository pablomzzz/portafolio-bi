# Riesgo Financiero de Empresas

> **Pregunta de negocio:** ¿Qué empresas muestran señales de riesgo?

Análisis de ratios financieros combinados en un **score de riesgo** para
priorizar revisión de cartera, crédito o inversión.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

[Dashboard en vivo](https://pablomzzz.github.io/portafolio-bi/proyectos/finanzas-riesgo/site/)
· [Notebook de análisis](analisis_riesgo.ipynb)

## El caso de negocio

Un analista de riesgo o un comité de crédito no quiere leer 20 balances. Quiere:
1. **Un ranking** de qué empresas están en zona crítica.
2. **Por qué** (qué ratios disparan la alerta).
3. **Dónde concentrar** la revisión (sectores más expuestos).

La acción que habilita: **priorizar revisión de crédito, ajustar exposición o
condiciones** antes de que el riesgo se materialice.

## Método: ratios + score compuesto

Del último año de cada empresa se calculan:
- **margen neto** = utilidad / ingresos
- **liquidez corriente** = activo corriente / pasivo corriente (bajo 1 = no cubre deudas de corto plazo)
- **endeudamiento** = deuda / activo total
- **ROE** = utilidad / patrimonio
- **crecimiento** de ingresos (año contra año)

Se combinan en un **score de riesgo 0-100** (mayor = más riesgo). Cada dimensión
aporta hasta ~25 puntos.

## Qué demuestra

| Habilidad | Dónde |
|---|---|
| **ETL / limpieza** | `data/estados_financieros_raw.csv` (sucio) + `powerbi/ETL_POWERQUERY.md` |
| **SQL** | `analysis/consultas.sql` (window functions, self-join por MAX(anio)) |
| **Python / modelado de score** | `analysis/agregar.py`, `agregar_detalle.py` |
| **Modelado + DAX** | `powerbi/MODELO.md` + `powerbi/README.md` |
| **Conocimiento de negocio** | ratios financieros: método y recomendaciones |
| **Viz interactiva** | `site/` (filtros por sector/nivel, scatter de riesgo, ranking) |

## Cómo reproducir

```bash
python analysis/generar_datos.py    # data/estados_financieros.csv (20 empresas x 4 años)
python analysis/agregar.py          # ratios + score -> site/data.json + powerbi/ratios_riesgo.csv
python analysis/agregar_detalle.py  # detalle por empresa -> site/data_detalle.json (filtros)
python -m http.server 8100 --directory site
```

## Dashboard web

- **Banner** con los scores de riesgo de fondo.
- **Filtros**: sector, nivel de riesgo (Alto/Medio/Bajo).
- **Tabs**: Ranking de riesgo (barras por score) · Liquidez vs Endeudamiento
  (scatter, color = score) · Por sector (riesgo promedio).
- **KPIs dinámicos** + recomendaciones que cambian según los filtros.

## Datos

Hay **dos versiones**:
- `data/estados_financieros.csv` — limpio (dashboard web y notebook).
- `data/estados_financieros_raw.csv` — sucio a propósito (separador de miles,
  mayúsculas inconsistentes, nulos, duplicados) para practicar **ETL en Power
  Query** con `powerbi/ETL_POWERQUERY.md`.

Sintéticos, con perfiles de salud financiera variados (sanas, medias, en riesgo).
No representan a ninguna empresa real. Se pueden reemplazar por datos públicos
(ej: estados financieros de la CMF Chile) manteniendo el esquema.

## Power BI

1. Cargar `data/estados_financieros_raw.csv` y limpiarlo (`powerbi/ETL_POWERQUERY.md`).
2. Para el ranking usar `powerbi/ratios_riesgo.csv` (score ya calculado).
3. Medidas DAX en `powerbi/README.md`; guardar como `powerbi/finanzas.pbip` (+ capturas).

## Estructura

```
finanzas-riesgo/
├── data/          # estados_financieros.csv (limpio) + _raw.csv (sucio, ETL)
├── analysis/      # generar_datos.py, agregar.py, agregar_detalle.py, consultas.sql
├── powerbi/       # ETL_POWERQUERY.md, README.md (DAX), MODELO.md, ratios_riesgo.csv
├── site/          # dashboard web: index.html + data.json + data_detalle.json + banner.png
└── analisis_riesgo.ipynb
```
