-- ============================================================================
-- Analisis de riesgo financiero: ratios por empresa (ultimo anio)
-- ----------------------------------------------------------------------------
-- Tabla `estados` con el esquema del CSV. Cargar en SQLite:
--   .mode csv
--   .import data/estados_financieros.csv estados
-- ============================================================================


-- 1. Ratios clave del ultimo anio de cada empresa (senales de riesgo)
WITH ult AS (  -- ultimo anio por empresa
    SELECT e.*
    FROM estados e
    JOIN (SELECT empresa, MAX(anio) AS max_anio FROM estados GROUP BY empresa) m
      ON e.empresa = m.empresa AND e.anio = m.max_anio
)
SELECT
    empresa, sector, anio,
    ROUND(1.0 * utilidad_neta / ingresos, 3)          AS margen_neto,
    ROUND(1.0 * activo_corriente / pasivo_corriente, 2) AS liquidez,
    ROUND(1.0 * deuda_total / activo_total, 3)         AS endeudamiento,
    ROUND(1.0 * utilidad_neta / patrimonio, 3)         AS roe
FROM ult
ORDER BY endeudamiento DESC, liquidez ASC;


-- 2. Empresas con senales de alerta combinadas (candidatas a riesgo)
WITH ult AS (
    SELECT e.* FROM estados e
    JOIN (SELECT empresa, MAX(anio) AS max_anio FROM estados GROUP BY empresa) m
      ON e.empresa = m.empresa AND e.anio = m.max_anio
)
SELECT empresa, sector,
    ROUND(1.0 * activo_corriente / pasivo_corriente, 2) AS liquidez,
    ROUND(1.0 * deuda_total / activo_total, 3)          AS endeudamiento,
    ROUND(1.0 * utilidad_neta / ingresos, 3)           AS margen_neto
FROM ult
WHERE 1.0 * activo_corriente / pasivo_corriente < 1.1      -- baja liquidez
   OR 1.0 * deuda_total / activo_total > 0.75              -- alto endeudamiento
   OR 1.0 * utilidad_neta / ingresos < 0                   -- perdidas
ORDER BY liquidez ASC;


-- 3. Crecimiento de ingresos anio contra anio (window function)
SELECT
    empresa, anio, ingresos,
    LAG(ingresos) OVER (PARTITION BY empresa ORDER BY anio) AS ingresos_prev,
    ROUND(100.0 * (ingresos - LAG(ingresos) OVER (PARTITION BY empresa ORDER BY anio))
          / LAG(ingresos) OVER (PARTITION BY empresa ORDER BY anio), 1) AS crecimiento_pct
FROM estados
ORDER BY empresa, anio;


-- 4. Riesgo promedio por sector (endeudamiento y margen)
WITH ult AS (
    SELECT e.* FROM estados e
    JOIN (SELECT empresa, MAX(anio) AS max_anio FROM estados GROUP BY empresa) m
      ON e.empresa = m.empresa AND e.anio = m.max_anio
)
SELECT sector,
    COUNT(*) AS empresas,
    ROUND(AVG(1.0 * deuda_total / activo_total), 3) AS endeudamiento_prom,
    ROUND(AVG(1.0 * utilidad_neta / ingresos), 3)   AS margen_prom
FROM ult
GROUP BY sector
ORDER BY endeudamiento_prom DESC;
