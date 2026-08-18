# Power BI — Salud: Ocupación de camillas

Guía para armar `camillas.pbix` en **Power BI Desktop** (gratis, sin cuenta, solo Windows).

## 1. Cargar datos
1. **Inicio → Obtener datos → Texto o CSV**
2. Selecciona `../data/ocupacion_camillas.csv` (está en UTF-8, las tildes se ven bien)
3. Revisa la vista previa → **Cargar**
4. Si `fecha` no quedó tipo Fecha: **Transformar datos** → click derecho en `fecha` → Tipo → Fecha

## 2. Medidas DAX (Inicio → Nueva medida, una por una)

```dax
Mediciones = COUNTROWS('ocupacion_camillas')
```
```dax
% Critico =
DIVIDE(
    CALCULATE(COUNTROWS('ocupacion_camillas'), 'ocupacion_camillas'[tasa_ocupacion] >= 0.95),
    COUNTROWS('ocupacion_camillas')
)
```
> Formato de `% Critico`: pestaña **Herramientas de medida → %**.

```dax
Pacientes en espera = SUM('ocupacion_camillas'[pacientes_en_espera])
```
```dax
Ocupacion promedio = AVERAGE('ocupacion_camillas'[tasa_ocupacion])
```
> Formato de `Ocupacion promedio`: **%**.

## 3. Columna calculada (Modelado → Nueva columna)

```dax
Temporada =
IF(
    MONTH('ocupacion_camillas'[fecha]) >= 5 && MONTH('ocupacion_camillas'[fecha]) <= 8,
    "Invierno",
    "Resto del año"
)
```

## 4. Visuales (replica la historia del dashboard web)

| Visual | Tipo | Campos |
|---|---|---|
| KPI crítico | Tarjeta | `% Critico` |
| Pacientes en espera | Tarjeta | `Pacientes en espera` |
| Top pabellones críticos | Barras horizontales | Eje: `hospital`, `servicio`, `turno` · Valor: `Pacientes en espera` (orden desc) |
| Presión por turno | Columnas | Eje: `turno` · Valor: `Ocupacion promedio` |
| Invierno vs Resto | Columnas agrupadas | Eje: `servicio` · Leyenda: `Temporada` · Valor: `Ocupacion promedio` |

## 5. Toques pro
- **Ver → Temas →** elige uno oscuro (combina con el portafolio web)
- Título de página: *"¿Qué pabellón se queda sin camillas este turno?"*
- Guarda como **`camillas.pbix`** en esta carpeta
- Exporta 2-3 capturas PNG (Archivo → Exportar → PDF, o recorte de pantalla) a esta carpeta

> No uses tu cuenta/tenant de Walmart. Power BI Desktop no requiere cuenta.
