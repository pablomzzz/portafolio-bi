# Oportunidades de Venta Cruzada (Market Basket Analysis)

> **Pregunta de negocio:** ¿Dónde está la mayor oportunidad de venta cruzada?

Proyecto de analítica comercial que detecta qué productos se compran juntos
para priorizar **promociones, bundles y ubicación en góndola**.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

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
- **confianza (A→B)**: probabilidad de comprar B dado que se compró A.
- **lift**: cuántas veces más se compran juntos vs por azar. `lift > 1` = afinidad real.

El ranking por **lift** revela las oportunidades más fuertes. Hallazgo del
dataset sintético: *Pañales + Toallitas húmedas* (lift 4.7, confianza 76%).

## Qué demuestra

| Habilidad | Dónde |
|---|---|
| SQL avanzado | `analysis/consultas.sql` (self-join para pares, CTEs, lift) |
| Python / analítica | `analysis/agregar.py` (market basket end-to-end) |
| Modelado | transacciones → reglas de asociación |
| Viz web | `site/` (Chart.js, dashboard interactivo) |

## Cómo reproducir

```bash
python analysis/generar_datos.py    # genera data/transacciones.csv (5000 boletas)
python analysis/agregar.py          # calcula market basket → site/data.json
python -m http.server 8100 --directory site   # abrir http://localhost:8100/
```

## Datos

Sintéticos (generados por `analysis/generar_datos.py`), con afinidades de compra
inyectadas para que el análisis las detecte. No representan a ninguna empresa real.

## Estructura

```
retail-oportunidades/
├── data/          # transacciones.csv (generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # .pbix + capturas (en tu PC)
└── site/          # dashboard web (index.html + data.json)
```
