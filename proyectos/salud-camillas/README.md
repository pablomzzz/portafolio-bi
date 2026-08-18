# Ocupación de Camillas Hospitalarias

> **Pregunta de negocio:** ¿Qué pabellón se va a quedar sin camillas este turno?

Proyecto de Business Intelligence orientado a la **gestión de recursos
hospitalarios**. Convierte datos de ocupación en una decisión accionable:
dónde falta capacidad AHORA y dónde va a faltar.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

 [Dashboard en vivo](https://pablomzzz.github.io/portafolio-bi/proyectos/salud-camillas/site/)
·  [Notebook de análisis](analisis_ocupacion.ipynb)

---

## El caso de negocio

Un jefe de turno o un gestor de red asistencial no quiere "un dashboard de
ocupación". Quiere responder, en segundos:

1. **Qué pabellón está en rojo este turno** (ocupación crítica).
2. **Dónde hay pacientes en espera** sin camilla disponible.
3. **Qué servicio va a saturarse** según la tendencia.

La acción que habilita: **reasignar camillas / derivar pacientes / reforzar
personal** antes de que el pabellón colapse.

---

## Qué demuestra este proyecto

| Habilidad | Dónde se ve |
|---|---|
| **ETL / limpieza** | `data/ocupacion_camillas_raw.csv` (datos sucios) + `powerbi/ETL_POWERQUERY.md` (Power Query) |
| **Python** | `analysis/generar_datos.py`, `analysis/agregar.py`, `analysis/agregar_detalle.py` |
| **SQL** | `analysis/consultas.sql` (queries de las métricas clave) |
| **Modelado + DAX** | `powerbi/MODELO.md` (modelo semántico) + `powerbi/README.md` (medidas DAX) |
| **Data viz interactiva** | `site/index.html` (filtros por período/hospital/servicio/turno, tabs, KPIs dinámicos) |
| **Storytelling** | este README + el dashboard: pregunta → hallazgo → acción |

---

## Datos

Los datos son **sintéticos** (generados por `analysis/generar_datos.py`). No
provienen de ninguna institución real ni contienen información de pacientes.
Están diseñados para parecerse a un patrón realista de ocupación hospitalaria
chilena (campaña de invierno, picos por turno de noche en urgencias).

> Cuando consigas datos reales públicos (ej: Minsal DEIS), se reemplaza el CSV
> manteniendo el mismo esquema y todo lo demás sigue funcionando.

Hay **dos versiones** del dataset:
- `data/ocupacion_camillas.csv` — **limpio**, alimenta el dashboard web y el notebook.
- `data/ocupacion_camillas_raw.csv` — **sucio a propósito** (espacios, mayúsculas
  inconsistentes, fechas en formato mixto, nulos, duplicados) para practicar
  **ETL en Power Query** siguiendo `powerbi/ETL_POWERQUERY.md`.

### Esquema del dataset limpio (`data/ocupacion_camillas.csv`)

| Columna | Tipo | Descripción |
|---|---|---|
| `fecha` | date | Día de la medición |
| `hospital` | str | Nombre del establecimiento (ficticio) |
| `servicio` | str | Pabellón / servicio clínico |
| `turno` | str | Mañana / Tarde / Noche |
| `camillas_totales` | int | Capacidad instalada |
| `camillas_ocupadas` | int | Camillas en uso |
| `tasa_ocupacion` | float | ocupadas / totales (0-1) |
| `pacientes_en_espera` | int | Pacientes sin camilla asignada |
| `tiempo_espera_min_prom` | int | Espera promedio en minutos |

### Modelo
Modelo de **tabla única** (el grano —hospital × servicio × turno × día— es
suficiente para todos los análisis; una estrella añadiría complejidad sin
beneficio). Detalle completo en [`powerbi/MODELO.md`](powerbi/MODELO.md).

---

## Cómo reproducir

```bash
# 1. Generar el dataset sintético (solo stdlib)
python analysis/generar_datos.py

# 2. Agregar datos para el dashboard web
python analysis/agregar.py          # totales para las vistas base
python analysis/agregar_detalle.py  # detalle granular para los filtros

# 3. Servir el dashboard localmente (fetch no funciona con file://)
python -m http.server 8099 --directory site
# abrir http://localhost:8099/
```

## Dashboard web

Vive en `site/` (HTML + Chart.js, sin dependencias ni cuentas externas):
- **Banner** con la ocupación mensual real de fondo
- **Filtros**: mes desde/hasta, hospital, servicio, turno (recalculan todo en vivo)
- **Tabs**: Resumen · Pabellones críticos · Temporada
- **KPIs dinámicos** + recomendaciones que cambian según los filtros

## Power BI

Para construir el reporte en Power BI Desktop:
1. Cargar `data/ocupacion_camillas_raw.csv` y limpiarlo con `powerbi/ETL_POWERQUERY.md`.
2. Crear las medidas DAX de `powerbi/README.md`.
3. Guardar como `powerbi/camillas.pbip` (+ capturas).

## Estructura

```
salud-camillas/
├── data/          # ocupacion_camillas.csv (limpio) + _raw.csv (sucio, ETL)
├── analysis/      # generar_datos.py, agregar.py, agregar_detalle.py, consultas.sql
├── powerbi/       # ETL_POWERQUERY.md, README.md (DAX), MODELO.md (+ tu .pbip)
├── site/          # dashboard web: index.html + data.json + data_detalle.json + banner.png
└── analisis_ocupacion.ipynb
```
