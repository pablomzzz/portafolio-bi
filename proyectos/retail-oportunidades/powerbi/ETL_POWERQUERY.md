# ETL en Power Query — Retail

Guía para limpiar `../data/transacciones_raw.csv` en Power Query.

> Carga **`transacciones_raw.csv`** (el sucio). Para las oportunidades de venta
> cruzada sigue usando `oportunidades_cross_sell.csv` (ese ya viene limpio).

## Problemas del CSV crudo
1. Nombres de columna con mayúsculas: `Tienda`, `Categoria`, `Monto`
2. Fechas en formato mixto (texto): `2025/08/19`, `19/8/2025`, `19-8-2025`
3. `tienda` y `producto` con espacios sobrantes
4. `categoria` con mayúsculas inconsistentes + typo `Lacteo` (por `Lacteos`)
5. `monto` con separador de miles con punto: `1.234.567`
6. `cantidad` con algunos nulos
7. Filas duplicadas

## Pasos en Power Query

### 1. Cargar y transformar
Obtener datos → Texto/CSV → `transacciones_raw.csv` → **Transformar datos**.

### 2. Renombrar columnas
`Tienda` → `tienda`, `Categoria` → `categoria`, `Monto` → `monto`.

### 3. Recortar espacios
Selecciona `tienda`, `producto`, `categoria` → **Transformar → Formato →
Recortar** y **Limpiar**.

### 4. Normalizar mayúsculas
`categoria` → **Transformar → Formato → Poner en mayúsculas cada palabra**.

### 5. Corregir typo
Clic derecho en `categoria` → **Reemplazar valores** → `Lacteo` por `Lacteos`
(marca "coincidir contenido completo de la celda").

### 6. Arreglar el separador de miles en `monto`
Clic derecho en `monto` → **Reemplazar valores** → `.` por `` (nada, para quitar
los puntos de miles) → luego cambia el tipo a **Número entero**.
> Si algún monto tuviera decimales reales, primero maneja esos; en este dataset
> los montos son enteros en CLP.

### 7. Convertir fecha (formato mixto)
Igual que en salud:
1. Reemplaza `/` por `-` en `fecha`.
2. Columna personalizada con lógica M:
   ```
   = let p = Text.Split([fecha], "-") in
     if Text.Length(p{0}) = 4
     then #date(Number.From(p{0}), Number.From(p{1}), Number.From(p{2}))
     else #date(Number.From(p{2}), Number.From(p{1}), Number.From(p{0}))
   ```
   Nómbrala `fecha_ok`, tipo **Fecha**, elimina la original.

### 8. Nulos en `cantidad`
Selecciona `cantidad` → **Reemplazar valores → null por 1** (o filtra si prefieres)
→ tipo **Número entero**.

### 9. Quitar duplicados y filas en blanco
**Inicio → Quitar filas → Quitar duplicados** y **Quitar filas en blanco**.

### 10. (Opcional) Recalcular `monto`
Si quieres asegurar consistencia: **Agregar columna → Columna personalizada** →
`[cantidad] * [precio_unit]` → reemplaza `monto`.

### 11. Aplicar
**Cerrar y aplicar**. Verifica tipos: `fecha_ok` = fecha, `monto` y `cantidad` = enteros.

## Resultado
Tabla limpia lista para las medidas DAX (`README.md`). El ETL queda documentado
en "Pasos aplicados".
