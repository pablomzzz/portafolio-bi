# Ocupación de Camillas Hospitalarias

> **Pregunta de negocio:** ¿Qué pabellón se va a quedar sin camillas este turno?

Proyecto de Business Intelligence orientado a la **gestión de recursos
hospitalarios**. Convierte datos de ocupación en una decisión accionable:
dónde falta capacidad AHORA y dónde va a faltar.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

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
| **Python / ETL** | `analysis/generar_datos.py` (generación + lógica de métricas) |
| **SQL** | `analysis/consultas.sql` (queries de las métricas clave) |
| **Modelado de datos** | esquema estrella simple (hechos: ocupación; dimensiones: hospital, servicio, tiempo) |
| **Power BI** | `powerbi/` (.pbix + capturas del reporte) |
| **Storytelling** | este README + el dashboard: pregunta → hallazgo → acción |

---

## Datos

**IMPORTANTE:** los datos son **sintéticos** (generados por
`analysis/generar_datos.py`). No provienen de ninguna institución real ni
contienen información de pacientes. Están diseñados para parecerse a un patrón
realista de ocupación hospitalaria chilena (campaña de invierno, picos por
turno de noche en urgencias, fines de semana distintos).

> Cuando consigas datos reales públicos (ej: Minsal DEIS), se reemplaza el CSV
> manteniendo el mismo esquema y todo lo demás sigue funcionando.

### Esquema del dataset (`data/ocupacion_camillas.csv`)

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

---

## Cómo reproducir

```bash
# 1. Generar el dataset sintético (solo stdlib, no requiere instalar nada)
python analysis/generar_datos.py

# 2. Agregar los datos para el dashboard web
python analysis/agregar.py

# 3. Servir el dashboard localmente (fetch no funciona con file://)
python -m http.server 8099 --directory site
# abrir http://localhost:8099/

# 4. (opcional) Abrir data/ocupacion_camillas.csv en Power BI Desktop
```

## Dashboard web (GitHub Pages)

El dashboard interactivo vive en `site/` (HTML + Chart.js, sin dependencias ni
cuentas externas). Para publicarlo gratis:

1. Sube el repo a GitHub (`pablomzzz/portafolio-bi`).
2. Settings → Pages → Source: rama `main`, carpeta `/site`.
3. Tu dashboard queda en `https://pablomzzz.github.io/portafolio-bi/proyectos/salud-camillas/site/`.

## Estructura

```
salud-camillas/
├── data/          # dataset sintético (CSV generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # camillas.pbix + capturas (lo creas en tu PC)
└── site/          # dashboard web (index.html + data.json) → GitHub Pages
```
