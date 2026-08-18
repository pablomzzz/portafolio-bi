# Power BI — Finanzas: Riesgo de empresas

Guía para armar `finanzas.pbix` en **Power BI Desktop**.

Tienes **2 archivos**:
- `ratios_riesgo.csv` (en esta carpeta) — **ratios + score de riesgo YA calculados** por empresa (margen, liquidez, endeudamiento, ROE, crecimiento, score, nivel). Lo difícil ya está hecho.
- `../data/estados_financieros.csv` — estados crudos (20 empresas × 4 años), para tendencias.

## 1. Cargar datos
1. **Obtener datos → Texto o CSV** → carga `ratios_riesgo.csv`
2. Repite y carga `../data/estados_financieros.csv`

## 2. Medidas DAX (sobre ratios_riesgo)
```dax
Empresas = DISTINCTCOUNT('ratios_riesgo'[empresa])
```
```dax
En riesgo = CALCULATE(DISTINCTCOUNT('ratios_riesgo'[empresa]), 'ratios_riesgo'[score_riesgo] >= 50)
```
```dax
Score maximo = MAX('ratios_riesgo'[score_riesgo])
```

## 3. Visuales

| Visual | Tipo | Campos |
|---|---|---|
| Empresas en riesgo | Tarjeta | `En riesgo` |
| Ranking de riesgo | Barras horizontales | Eje: `empresa` · Valor: `score_riesgo` (orden desc) · color por `nivel` |
| Liquidez vs Endeudamiento | Dispersión (scatter) | X: `endeudamiento` · Y: `liquidez` · Detalles: `empresa` · Tamaño: `score_riesgo` |
| Riesgo por sector | Columnas | Eje: `sector` · Valor: promedio de `score_riesgo` |
| Detalle | Tabla | `empresa`, `sector`, `liquidez`, `endeudamiento`, `margen_neto`, `score_riesgo`, `nivel` |

## 4. Formato condicional (recomendado)
En el ranking de barras: **Formato → Colores de datos → fx** → por `nivel`
(Alto = rojo, Medio = ámbar, Bajo = verde).

## 5. Toques pro
- Tema oscuro (Ver → Temas)
- Título: *"¿Qué empresas muestran señales de riesgo?"*
- Guarda como **`finanzas.pbix`** aquí + capturas PNG

> No uses tu cuenta/tenant de Walmart. Power BI Desktop no requiere cuenta.
