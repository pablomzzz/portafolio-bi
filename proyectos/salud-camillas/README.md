# Ocupacion de Camillas Hospitalarias

> **Pregunta de negocio:** Que pabellon se va a quedar sin camillas este turno?

Proyecto de Business Intelligence orientado a la **gestion de recursos
hospitalarios**. Convierte datos de ocupacion en una decision accionable:
donde falta capacidad AHORA y donde va a faltar.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

---

## El caso de negocio

Un jefe de turno o un gestor de red asistencial no quiere "un dashboard de
ocupacion". Quiere responder, en segundos:

1. **Que pabellon esta en rojo este turno** (ocupacion critica).
2. **Donde hay pacientes en espera** sin camilla disponible.
3. **Que servicio va a saturarse** segun la tendencia.

La accion que habilita: **reasignar camillas / derivar pacientes / reforzar
personal** antes de que el pabellon colapse.

---

## Que demuestra este proyecto

| Habilidad | Donde se ve |
|---|---|
| **Python / ETL** | `analysis/generar_datos.py` (generacion + logica de metricas) |
| **SQL** | `analysis/consultas.sql` (queries de las metricas clave) |
| **Modelado de datos** | esquema estrella simple (hechos: ocupacion; dimensiones: hospital, servicio, tiempo) |
| **Power BI** | `powerbi/` (.pbix + capturas del reporte) |
| **Storytelling** | este README + el dashboard: pregunta -> hallazgo -> accion |

---

## Datos

**IMPORTANTE:** los datos son **sinteticos** (generados por
`analysis/generar_datos.py`). No provienen de ninguna institucion real ni
contienen informacion de pacientes. Estan disenados para parecerse a un patron
realista de ocupacion hospitalaria chilena (campana de invierno, picos por
turno de noche en urgencias, fines de semana distintos).

> Cuando consigas datos reales publicos (ej: Minsal DEIS), se reemplaza el CSV
> manteniendo el mismo esquema y todo lo demas sigue funcionando.

### Esquema del dataset (`data/ocupacion_camillas.csv`)

| Columna | Tipo | Descripcion |
|---|---|---|
| `fecha` | date | Dia de la medicion |
| `hospital` | str | Nombre del establecimiento (ficticio) |
| `servicio` | str | Pabellon / servicio clinico |
| `turno` | str | Manana / Tarde / Noche |
| `camillas_totales` | int | Capacidad instalada |
| `camillas_ocupadas` | int | Camillas en uso |
| `tasa_ocupacion` | float | ocupadas / totales (0-1) |
| `pacientes_en_espera` | int | Pacientes sin camilla asignada |
| `tiempo_espera_min_prom` | int | Espera promedio en minutos |

---

## Como reproducir

```bash
# 1. Generar el dataset sintetico (solo stdlib, no requiere instalar nada)
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

1. Sube el repo a GitHub (`pablomzzz/salud-camillas`).
2. Settings -> Pages -> Source: rama `main`, carpeta `/site`.
3. Tu dashboard queda en `https://pablomzzz.github.io/salud-camillas/`.

> No necesitas cerrar tu GitHub Pages actual: cada repo tiene su propio sitio.

## Estructura

```
salud-camillas/
├── data/          # dataset sintetico (CSV generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # camillas.pbix + capturas (lo creas en tu PC)
└── site/          # dashboard web (index.html + data.json) -> GitHub Pages
```
