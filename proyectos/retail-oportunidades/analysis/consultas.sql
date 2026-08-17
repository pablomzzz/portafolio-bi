-- ============================================================================
-- Market Basket Analysis en SQL: oportunidades de venta cruzada
-- ----------------------------------------------------------------------------
-- Tabla `transacciones` con el esquema del CSV (una fila por producto/boleta).
-- Cargar en SQLite:
--   sqlite3 retail.db
--   .mode csv
--   .import data/transacciones.csv transacciones
-- ============================================================================


-- 1. LA ESTRELLA: top pares de productos por lift (venta cruzada)
--    lift > 1 = se compran juntos mas de lo esperado por azar.
WITH total AS (
    SELECT COUNT(DISTINCT boleta_id) AS n FROM transacciones
),
items AS (  -- soporte individual
    SELECT producto, COUNT(DISTINCT boleta_id) AS n_item
    FROM transacciones GROUP BY producto
),
pares AS (  -- co-ocurrencias (self-join, a < b para no duplicar)
    SELECT a.producto AS prod_a, b.producto AS prod_b,
           COUNT(DISTINCT a.boleta_id) AS n_ab
    FROM transacciones a
    JOIN transacciones b
      ON a.boleta_id = b.boleta_id AND a.producto < b.producto
    GROUP BY a.producto, b.producto
)
SELECT
    p.prod_a, p.prod_b,
    p.n_ab AS boletas_juntos,
    ROUND(1.0 * p.n_ab / t.n, 4)                       AS soporte,
    ROUND(1.0 * p.n_ab / ia.n_item, 3)                 AS confianza_a_b,
    ROUND((1.0 * p.n_ab / t.n) /
          ((1.0 * ia.n_item / t.n) * (1.0 * ib.n_item / t.n)), 2) AS lift
FROM pares p
CROSS JOIN total t
JOIN items ia ON ia.producto = p.prod_a
JOIN items ib ON ib.producto = p.prod_b
WHERE 1.0 * p.n_ab / t.n >= 0.01   -- soporte minimo 1%
ORDER BY lift DESC
LIMIT 10;


-- 2. Top productos por venta (monto total)
SELECT producto, SUM(monto) AS ventas, SUM(cantidad) AS unidades
FROM transacciones
GROUP BY producto
ORDER BY ventas DESC
LIMIT 10;


-- 3. Ventas por categoria (participacion del mix)
SELECT categoria,
       SUM(monto) AS ventas,
       ROUND(100.0 * SUM(monto) / (SELECT SUM(monto) FROM transacciones), 1) AS pct
FROM transacciones
GROUP BY categoria
ORDER BY ventas DESC;


-- 4. Ticket promedio por tienda
SELECT tienda,
       COUNT(DISTINCT boleta_id) AS boletas,
       SUM(monto) AS ventas,
       ROUND(1.0 * SUM(monto) / COUNT(DISTINCT boleta_id)) AS ticket_promedio
FROM transacciones
GROUP BY tienda
ORDER BY ticket_promedio DESC;
