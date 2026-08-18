# ETL en Power Query — Finanzas

Guía para limpiar `../data/estados_financieros_raw.csv` en Power Query.

> Carga **`estados_financieros_raw.csv`** (el sucio). Para el ranking de riesgo
> sigue usando `ratios_riesgo.csv` (ese ya viene limpio y con el score calculado).

## Problemas del CSV crudo
1. Nombres de columna con mayúsculas: `Empresa`, `Sector`
2. `empresa` con espacios sobrantes
3. `sector` con mayúsculas inconsistentes + typo `Tecnologa` (por `Tecnologia`)
4. Columnas numéricas con separador de miles con punto: `3.139.247.101`
5. Algunas celdas numéricas vacías (nulos)
6. Filas duplicadas

## Pasos en Power Query

### 1. Cargar y transformar
Obtener datos → Texto/CSV → `estados_financieros_raw.csv` → **Transformar datos**.

### 2. Renombrar columnas
`Empresa` → `empresa`, `Sector` → `sector`.

### 3. Recortar espacios
Selecciona `empresa`, `sector` → **Transformar → Formato → Recortar** y **Limpiar**.

### 4. Normalizar mayúsculas
`sector` → **Transformar → Formato → Poner en mayúsculas cada palabra**.

### 5. Corregir typo
Clic derecho en `sector` → **Reemplazar valores** → `Tecnologa` por `Tecnologia`.

### 6. Quitar separador de miles en columnas numéricas
Selecciona TODAS las columnas de montos (ingresos, costos, utilidad_neta,
activo_corriente, pasivo_corriente, activo_total, deuda_total, patrimonio) →
**Transformar → Reemplazar valores** → `.` por `` (quita los puntos) →
luego **Detectar tipo de datos** o cambia cada una a **Número entero**.
> Nota: hazlo con las columnas seleccionadas juntas para aplicar a todas de una vez.

### 7. Manejar nulos
Las celdas vacías: selecciona las columnas numéricas → **Reemplazar valores →
null por 0** (o filtra las filas incompletas si prefieres no inventar ceros).
> Criterio de negocio: en finanzas, un 0 puede distorsionar ratios. Para un
> análisis serio conviene FILTRAR las filas con datos faltantes en vez de rellenar.
> Documenta tu decisión.

### 8. Quitar duplicados
Selecciona todas las columnas → **Inicio → Quitar filas → Quitar duplicados**.
> Importante: una empresa tiene 1 fila por año. Si hay duplicados exactos, elimínalos;
> pero NO elimines filas legítimas de años distintos.

### 9. Quitar filas en blanco
**Inicio → Quitar filas → Quitar filas en blanco**.

### 10. Aplicar
**Cerrar y aplicar**. Verifica que todas las columnas de montos quedaron como
número entero y `anio` como número entero.

## Resultado
Tabla limpia de estados financieros. Con ella puedes recrear los ratios en DAX
(o cruzarla con `ratios_riesgo.csv`). El ETL documentado demuestra criterio:
sabes cuándo rellenar y cuándo filtrar datos faltantes.
