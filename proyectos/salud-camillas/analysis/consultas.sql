-- ============================================================================
-- Consultas clave: Ocupacion de Camillas Hospitalarias
-- ----------------------------------------------------------------------------
-- Dialecto: ANSI SQL (probado mentalmente para SQLite / BigQuery / Postgres).
-- Asume una tabla `ocupacion` con el mismo esquema que el CSV.
--
-- Cargar el CSV en SQLite para probar:
--   sqlite3 camillas.db
--   .mode csv
--   .import data/ocupacion_camillas.csv ocupacion
-- ============================================================================


-- 1. LA PREGUNTA ESTRELLA: que pabellon se queda sin camillas este turno?
--    Ranking de servicios en ocupacion critica, priorizados por espera.
WITH criticos AS (
    SELECT
        hospital,
        servicio,
        turno,
        fecha,
        camillas_totales,
        camillas_ocupadas,
        tasa_ocupacion,
        pacientes_en_espera,
        tiempo_espera_min_prom
    FROM ocupacion
    WHERE tasa_ocupacion >= 0.95
)
SELECT
    hospital,
    servicio,
    turno,
    ROUND(AVG(tasa_ocupacion), 3)       AS ocupacion_prom,
    SUM(pacientes_en_espera)            AS total_en_espera,
    ROUND(AVG(tiempo_espera_min_prom))  AS espera_prom_min,
    COUNT(*)                            AS veces_en_rojo
FROM criticos
GROUP BY hospital, servicio, turno
ORDER BY total_en_espera DESC, ocupacion_prom DESC
LIMIT 10;


-- 2. Ranking de servicios mas presionados dentro de cada hospital
--    (window function: RANK por hospital).
SELECT
    hospital,
    servicio,
    ROUND(AVG(tasa_ocupacion), 3) AS ocupacion_prom,
    RANK() OVER (
        PARTITION BY hospital
        ORDER BY AVG(tasa_ocupacion) DESC
    ) AS ranking_presion
FROM ocupacion
GROUP BY hospital, servicio
ORDER BY hospital, ranking_presion;


-- 3. Efecto de la campana de invierno (mayo-agosto) vs resto del ano.
SELECT
    servicio,
    CASE
        WHEN CAST(strftime('%m', fecha) AS INT) BETWEEN 5 AND 8
        THEN 'Invierno' ELSE 'Resto'
    END AS temporada,
    ROUND(AVG(tasa_ocupacion), 3) AS ocupacion_prom,
    SUM(pacientes_en_espera)      AS pacientes_en_espera
FROM ocupacion
GROUP BY servicio, temporada
ORDER BY servicio, temporada;


-- 4. Perfil por turno: donde y cuando se concentra la saturacion.
SELECT
    turno,
    ROUND(AVG(tasa_ocupacion), 3)      AS ocupacion_prom,
    ROUND(AVG(tiempo_espera_min_prom)) AS espera_prom_min,
    SUM(pacientes_en_espera)           AS total_en_espera
FROM ocupacion
GROUP BY turno
ORDER BY ocupacion_prom DESC;


-- 5. Alerta operacional: dias-turno con dEFICIT real de camillas
--    (mas pacientes en espera que camillas libres proyectables).
SELECT
    fecha,
    hospital,
    servicio,
    turno,
    camillas_totales,
    camillas_ocupadas,
    pacientes_en_espera,
    tiempo_espera_min_prom
FROM ocupacion
WHERE pacientes_en_espera > 0
  AND tasa_ocupacion = 1.0
ORDER BY pacientes_en_espera DESC, tiempo_espera_min_prom DESC
LIMIT 20;
