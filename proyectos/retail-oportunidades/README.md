# Oportunidades de Venta Cruzada (Market Basket Analysis)

> **Pregunta de negocio:** Donde esta la mayor oportunidad de venta cruzada?

Proyecto de analitica comercial que detecta que productos se compran juntos
para priorizar **promociones, bundles y ubicacion en gondola**.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

## El caso de negocio

Un gerente comercial no quiere "un reporte de ventas". Quiere saber:
1. **Que productos impulsan la compra de otros** (venta cruzada).
2. **Donde armar bundles o promos** que suban el ticket.
3. **Que ubicar junto en gondola** para aprovechar la afinidad natural.

La accion que habilita: **bundles, promos cruzadas y recomendaciones** tipo
"clientes que compraron X tambien llevaron Y".

## Metodo: Market Basket Analysis

Por cada par de productos se calcula:
- **soporte**: cuan frecuente es la combinacion (boletas con ambos / total).
- **confianza (A->B)**: probabilidad de comprar B dado que se compro A.
- **lift**: cuantas veces mas se compran juntos vs por azar. `lift > 1` = afinidad real.

El ranking por **lift** revela las oportunidades mas fuertes. Hallazgo del
dataset sintetico: *Panales + Toallitas humedas* (lift 4.64, confianza 76%).

## Que demuestra

| Habilidad | Donde |
|---|---|
| SQL avanzado | `analysis/consultas.sql` (self-join para pares, CTEs, lift) |
| Python / analitica | `analysis/agregar.py` (market basket end-to-end) |
| Modelado | transacciones -> reglas de asociacion |
| Viz web | `site/` (Chart.js, dashboard interactivo) |

## Como reproducir

```bash
python analysis/generar_datos.py    # genera data/transacciones.csv (5000 boletas)
python analysis/agregar.py          # calcula market basket -> site/data.json
python -m http.server 8100 --directory site   # abrir http://localhost:8100/
```

## Datos

Sinteticos (generados por `analysis/generar_datos.py`), con afinidades de compra
inyectadas para que el analisis las detecte. No representan a ninguna empresa real.

## Estructura

```
retail-oportunidades/
├── data/          # transacciones.csv (generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # .pbix + capturas (en tu PC)
└── site/          # dashboard web (index.html + data.json)
```
