# Modelo semántico — Retail: Oportunidades de venta cruzada

Documentación del modelo de datos del reporte `retail.pbip` / `retail.pbix`.

## Fuentes de datos
1. `oportunidades_cross_sell.csv` (en esta carpeta) — **market basket ya calculado**
   (148 pares con soporte, confianza y lift). El análisis pesado ya está hecho en
   Python; Power BI solo lo visualiza.
2. `../data/transacciones.csv` — transacciones crudas (14.5k líneas, 5.000 boletas).

## Arquitectura
Dos tablas independientes (no requieren relación para los visuales base):
- **hechos de venta**: `transacciones`
- **reglas de asociación**: `oportunidades_cross_sell`

## Tabla: `transacciones`
Grano: 1 fila = 1 línea de boleta (un producto dentro de una boleta).

| Columna | Tipo | Descripción |
|---|---|---|
| `boleta_id` | Texto/Entero | Identificador de la boleta |
| `fecha` | Fecha | Día de la compra |
| `tienda` | Texto | Local |
| `producto` | Texto | Producto vendido |
| `categoria` | Texto | Categoría del producto |
| `cantidad` | Entero | Unidades |
| `precio_unit` | Entero | Precio unitario (CLP) |
| `monto` | Entero | cantidad × precio_unit |

## Tabla: `oportunidades_cross_sell`
Grano: 1 fila = 1 par de productos que se compran juntos.

| Columna | Tipo | Descripción |
|---|---|---|
| `producto_a` / `producto_b` | Texto | Los dos productos del par |
| `soporte` | Decimal | P(A y B): frecuencia del par |
| `confianza_a_b` | Decimal | P(B \| A) |
| `lift` | Decimal | afinidad real; > 1 = se compran juntos más que por azar |
| `boletas` | Entero | Nº de boletas con el par |

## Columna calculada (opcional, etiqueta legible)
```dax
Par = 'oportunidades_cross_sell'[producto_a] & " + " & 'oportunidades_cross_sell'[producto_b]
```

## Medidas (DAX, sobre `transacciones`)
| Medida | Fórmula |
|---|---|
| `Ventas totales` | `SUM('transacciones'[monto])` |
| `Boletas` | `DISTINCTCOUNT('transacciones'[boleta_id])` |
| `Ticket promedio` | `DIVIDE([Ventas totales], [Boletas])` |

## Decisiones de modelado
- **Market basket pre-calculado en Python** (soporte, confianza, lift) y expuesto
  como CSV: separa el cálculo (reproducible, testeable) de la visualización.
- **Umbral de soporte = 1%**: descarta pares triviales o ruido.
- Se prioriza **lift** para el ranking: mide afinidad real, no solo popularidad.

## Pregunta de negocio que responde
¿Dónde está la mayor oportunidad de venta cruzada? → bundles, promos y ubicación
en góndola sobre los pares de mayor lift.
