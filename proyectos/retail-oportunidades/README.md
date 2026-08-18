# Oportunidades de Venta Cruzada (Market Basket Analysis)

> **Pregunta de negocio:** ¿Dónde está la mayor oportunidad de venta cruzada?

Proyecto de analítica comercial que detecta qué productos se compran juntos
para priorizar **promociones, bundles y ubicación en góndola**.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

[Dashboard en vivo](https://pablomzzz.github.io/portafolio-bi/proyectos/retail-oportunidades/site/)
· [Notebook de análisis](analisis_market_basket.ipynb)

## El caso de negocio

Un gerente comercial no quiere "un reporte de ventas". Quiere saber:
1. **Qué productos impulsan la compra de otros** (venta cruzada).
2. **Dónde armar bundles o promos** que suban el ticket.
3. **Qué ubicar junto en góndola** para aprovechar la afinidad natural.

La acción que habilita: **bundles, promos cruzadas y recomendaciones** tipo
"clientes que compraron X también llevaron Y".

## Método: Market Basket Analysis

Por cada par de productos se calcula:
- **soporte**: cuán frecuente es la combinación (boletas con ambos / total).
- **confianza (A->B)**: probabilidad de comprar B dado que se compró A.
- **lift**: cuántas veces más se compran juntos vs por azar. `lift > 1` = afinidad real.

El ranking por **lift** revela las oportunidades más fuertes. Hallazgo del
dataset sintético: *Pañales + Toallitas húmedas* (lift 4.7, confianza 76%).

## Qué demuestra

| Habilidad | Dónde |
|---|---|
| **ETL / limpieza** | `data/transacciones_raw.csv` (sucio) + `powerbi/ETL_POWERQUERY.md` |
| **SQL avanzado** | `analysis/consultas.sql` (self-join para pares, CTEs, lift) |
| **Python / analítica** | `analysis/agregar.py` (market basket end-to-end), `agregar_detalle.py` |
| **Modelado + DAX** | `powerbi/MODELO.md` + `powerbi/README.md` |
| **Viz interactiva** | `site/` (filtros por período/tienda/categoría, tabs, KPIs dinámicos) |

## Cómo reproducir

```bash
python analysis/generar_datos.py    # genera data/transacciones.csv (5000 boletas)
python analysis/agregar.py          # calcula market basket -> site/data.json
python analysis/agregar_detalle.py  # detalle granular -> site/data_detalle.json (filtros)
python -m http.server 8100 --directory site   # abrir http://localhost:8100/
```

## Dashboard web

- **Banner** con las ventas mensuales de fondo.
- **Filtros**: mes desde/hasta, tienda, categoría (recalculan KPIs y gráficos).
- **Tabs**: Resumen (ventas por categoría y tienda) · Productos (top 10) ·
  Oportunidades (market basket por lift; se calcula sobre todas las boletas, no
  depende de los filtros).

## Datos

Hay **dos versiones**:
- `data/transacciones.csv` — limpio (dashboard web y notebook).
- `data/transacciones_raw.csv` — sucio a propósito (separador de miles, mayúsculas
  inconsistentes, fechas en formato mixto, nulos, duplicados) para practicar
  **ETL en Power Query** con `powerbi/ETL_POWERQUERY.md`.

Sintéticos, con afinidades de compra inyectadas. No representan a ninguna empresa real.

## Power BI

1. Cargar `data/transacciones_raw.csv` y limpiarlo (`powerbi/ETL_POWERQUERY.md`).
2. Para las oportunidades usar `powerbi/oportunidades_cross_sell.csv` (ya calculado).
3. Medidas DAX en `powerbi/README.md`; guardar como `powerbi/retail.pbip` (+ capturas).

## Estructura

```
retail-oportunidades/
├── data/          # transacciones.csv (limpio) + _raw.csv (sucio, ETL)
├── analysis/      # generar_datos.py, agregar.py, agregar_detalle.py, consultas.sql
├── powerbi/       # ETL_POWERQUERY.md, README.md (DAX), MODELO.md, oportunidades_cross_sell.csv
├── site/          # dashboard web: index.html + data.json + data_detalle.json + banner.png
└── analisis_market_basket.ipynb
```
