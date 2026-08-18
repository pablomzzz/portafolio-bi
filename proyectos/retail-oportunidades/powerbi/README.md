# Power BI — Retail: Oportunidades de venta cruzada

Guía para armar `retail.pbix` en **Power BI Desktop**.

Tienes **2 archivos** para cargar:
- `oportunidades_cross_sell.csv` (en esta carpeta) — **el market basket YA calculado** (148 pares con soporte, confianza, lift). Lo difícil ya está hecho.
- `../data/transacciones.csv` — las transacciones crudas, para ventas por producto/categoría/tienda.

## 1. Cargar datos
1. **Obtener datos → Texto o CSV** → carga `oportunidades_cross_sell.csv`
2. Repite y carga `../data/transacciones.csv`
3. (Ambos en UTF-8, las tildes se ven bien)

## 2. Columna calculada (opcional, para etiquetas lindas)
En la tabla `oportunidades_cross_sell`, **Modelado → Nueva columna**:
```dax
Par = 'oportunidades_cross_sell'[producto_a] & " + " & 'oportunidades_cross_sell'[producto_b]
```

## 3. Medidas DAX (sobre transacciones)
```dax
Ventas totales = SUM('transacciones'[monto])
```
```dax
Boletas = DISTINCTCOUNT('transacciones'[boleta_id])
```
> Ajusta `boleta_id` al nombre real de la columna de boleta en tu CSV.
```dax
Ticket promedio = DIVIDE([Ventas totales], [Boletas])
```

## 4. Visuales

| Visual | Tipo | Campos |
|---|---|---|
| Top oportunidades por lift | Barras horizontales | Eje: `Par` · Valor: `lift` (de oportunidades, orden desc) |
| Confianza de la regla | Tabla | `producto_a`, `producto_b`, `confianza_a_b`, `lift`, `boletas` |
| Top productos | Barras | Eje: `producto` · Valor: `Ventas totales` |
| Ventas por categoría | Anillo/Treemap | `categoria` · `Ventas totales` |
| Ticket por tienda | Columnas | Eje: `tienda` · Valor: `Ticket promedio` |

## 5. Toques pro
- Tema oscuro (Ver → Temas)
- Título: *"¿Dónde está la mayor oportunidad de venta cruzada?"*
- Filtra el visual de lift a `lift > 1` (afinidades reales)
- Guarda como **`retail.pbix`** aquí + capturas PNG

> No uses tu cuenta/tenant de Walmart. Power BI Desktop no requiere cuenta.
