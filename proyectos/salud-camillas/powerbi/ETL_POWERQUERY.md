# ETL en Power Query — Salud

Guía para limpiar `../data/ocupacion_camillas_raw.csv` en Power Query antes de
modelar. Cada paso queda registrado en "Pasos aplicados" (el reclutador ve tu
proceso de limpieza en el `.pbip`).

> Carga el archivo **`ocupacion_camillas_raw.csv`** (el sucio), NO el limpio.
> El objetivo es demostrar que sabes transformar datos crudos.

## Problemas que tiene el CSV crudo
1. Nombres de columna con espacios y mayúsculas: `Hospital `, `Turno`, `Tasa Ocupacion`
2. Fechas en formato mixto (texto): `2025/08/19`, `19/8/2025`, `19-8-2025`
3. Texto con espacios y mayúsculas inconsistentes en `servicio`, `turno`, `hospital`
4. Typo real: `Urgencia` en vez de `Urgencias`
5. `tasa_ocupacion` con coma decimal: `"0,775"`
6. `pacientes_en_espera` con celdas vacías (nulos)
7. Filas duplicadas

## Pasos en Power Query (Transformar datos)

### 1. Cargar
Inicio → Obtener datos → Texto/CSV → `ocupacion_camillas_raw.csv` →
**Transformar datos** (NO "Cargar" todavía).

### 2. Recortar espacios (Trim) en columnas de texto
Selecciona `Hospital `, `servicio`, `Turno` (Ctrl+clic) →
**Transformar → Formato → Recortar**. Repite **Formato → Limpiar** (quita
caracteres invisibles).

### 3. Renombrar columnas
Doble clic en cada encabezado:
- `Hospital ` → `hospital`
- `Turno` → `turno`
- `Tasa Ocupacion` → `tasa_ocupacion`

### 4. Normalizar mayúsculas
Selecciona `servicio`, `turno`, `hospital` →
**Transformar → Formato → Poner en mayúsculas cada palabra** (Capitalize Each Word).
Así `URGENCIAS`, `urgencias` → `Urgencias`.

### 5. Corregir el typo
Clic derecho en `servicio` → **Reemplazar valores** → Buscar `Urgencia` →
Reemplazar por `Urgencias`.
> Ojo: marca "Coincidir con el contenido completo de la celda" para no romper
> "Urgencias" (que contiene "Urgencia").

### 6. Arreglar el decimal con coma
Clic derecho en `tasa_ocupacion` → **Reemplazar valores** → `,` por `.` →
luego clic en el ícono de tipo de la columna → **Número decimal**.
> Alternativa robusta: usa la **configuración regional** al cambiar tipo
> (Tipo de datos con configuración regional → Español).

### 7. Convertir la fecha (formato mixto)
Las fechas vienen en formatos distintos, así que "Detectar tipo" falla. Solución:
1. Clic derecho en `fecha` → **Reemplazar valores** → `/` por `-` (unifica separador)
2. Ahora tienes `2025-08-19`, `19-8-2025`, etc. — aún mixto.
3. **Reto avanzado (recomendado):** agrega una **Columna personalizada** con lógica M:
   ```
   = let p = Text.Split([fecha], "-") in
     if Text.Length(p{0}) = 4
     then #date(Number.From(p{0}), Number.From(p{1}), Number.From(p{2}))
     else #date(Number.From(p{2}), Number.From(p{1}), Number.From(p{0}))
   ```
   Llama la columna `fecha_ok`, cambia su tipo a **Fecha**, elimina la `fecha` vieja.

### 8. Rellenar o filtrar nulos
`pacientes_en_espera`: clic derecho → **Reemplazar valores** → deja "Buscar"
vacío no funciona; mejor: selecciona la columna → **Transformar → Reemplazar
valores → null por 0** (o filtra los null si prefieres descartarlos).
Luego cambia el tipo a **Número entero**.

### 9. Quitar duplicados
Selecciona todas las columnas (clic en la esquina superior izquierda de la tabla) →
**Inicio → Quitar filas → Quitar duplicados**.

### 10. Quitar filas vacías
**Inicio → Quitar filas → Quitar filas en blanco**.

### 11. Aplicar
**Inicio → Cerrar y aplicar**. Verifica que los tipos quedaron correctos
(fecha = calendario, tasa_ocupacion = decimal, pacientes_en_espera = entero).

## Resultado
Una tabla limpia lista para las medidas DAX del `README.md`. Tus "Pasos aplicados"
documentan todo el ETL — justo lo que un reclutador quiere ver.
