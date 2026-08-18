# Portafolio de Business Intelligence — Pablo Morales

Portafolio de proyectos de BI enfocados en **resolver problemas de negocio**,
no en gráficos decorativos. Cada proyecto identifica un problema real, lo
cuantifica y termina en una recomendación accionable.

**Dominios:** Retail · Finanzas · Salud
**Stack:** Power BI (Power Query/ETL, DAX, modelo semántico), SQL, Python
(pandas), modelado de datos y data storytelling.

 **Portafolio en vivo:** https://pablomzzz.github.io/portafolio-bi/
 **CV:** https://pablomzzz.github.io/pablomcv.github.io/

---

## Proyectos

| Proyecto | Dominio | Pregunta de negocio | Dashboard en vivo |
|---|---|---|---|
| [Ocupación de camillas](proyectos/salud-camillas/) | Salud | ¿Qué pabellón se queda sin camillas este turno? | [ver](https://pablomzzz.github.io/portafolio-bi/proyectos/salud-camillas/site/) |
| [Oportunidades de venta cruzada](proyectos/retail-oportunidades/) | Retail | ¿Dónde está la mayor oportunidad comercial? | [ver](https://pablomzzz.github.io/portafolio-bi/proyectos/retail-oportunidades/site/) |
| [Salud financiera de empresas](proyectos/finanzas-riesgo/) | Finanzas | ¿Qué empresas muestran señales de riesgo? | [ver](https://pablomzzz.github.io/portafolio-bi/proyectos/finanzas-riesgo/site/) |

## Qué demuestra el portafolio

| Habilidad | Dónde se ve |
|---|---|
| **ETL / limpieza de datos** | Datos crudos (`*_raw.csv`) + guías `powerbi/ETL_POWERQUERY.md` (Power Query: trim, tipos, nulos, duplicados, fechas en formato mixto) |
| **Modelado + DAX** | `powerbi/MODELO.md` (modelo semántico documentado) + `powerbi/README.md` (medidas DAX) |
| **Python / pandas** | Notebooks `.ipynb` con EDA y gráficos incrustados |
| **SQL** | `analysis/consultas.sql` en cada proyecto |
| **Data viz interactiva** | Dashboards web con filtros, tabs y KPIs que recalculan en vivo |
| **Storytelling** | Cada proyecto: pregunta de negocio → hallazgo → acción |

## Dashboards interactivos (sin backend)

Cada proyecto tiene un dashboard web (HTML + Chart.js) con:
-  **Banner** temático por dominio
-  **Filtros interactivos** (período, y dimensiones propias de cada caso)
-  **KPIs dinámicos** que se recalculan en el navegador al filtrar
-  **Tabs** para organizar las vistas

Se sirven como sitios estáticos en GitHub Pages: sin servidor, sin cuentas,
sin dependencias. La agregación granular vive en `site/data_detalle.json` y
se re-agrega client-side según los filtros.

## Análisis reproducible (Jupyter Notebooks)

Cada proyecto incluye un notebook con el análisis completo en **pandas +
matplotlib** (GitHub los renderiza con los gráficos incrustados):

| Notebook | Qué muestra |
|---|---|
| [salud](proyectos/salud-camillas/analisis_ocupacion.ipynb) | EDA de ocupación, pabellones críticos, efecto invierno |
| [retail](proyectos/retail-oportunidades/analisis_market_basket.ipynb) | Market basket: soporte, confianza, lift |
| [finanzas](proyectos/finanzas-riesgo/analisis_riesgo.ipynb) | Ratios financieros + score de riesgo |

## Power BI

Cada proyecto trae un **kit para construir el reporte en Power BI**:
- `data/*_raw.csv` — datos crudos para practicar **ETL en Power Query**
- `powerbi/ETL_POWERQUERY.md` — pasos de limpieza clic por clic
- `powerbi/README.md` — medidas **DAX** y visuales
- `powerbi/MODELO.md` — modelo semántico documentado
- (Pablo agrega el `.pbip`/`.pbix` + capturas al construir el reporte)

## Estructura del repo

```
portafolio-bi/
├── index.html                 # landing del portafolio
├── proyectos/
│   ├── salud-camillas/
│   ├── retail-oportunidades/
│   └── finanzas-riesgo/
│       ├── data/              # CSV limpio + *_raw.csv (sucio para ETL)
│       ├── analysis/          # generar_datos.py, agregar*.py, consultas.sql
│       ├── powerbi/           # ETL_POWERQUERY.md, README.md (DAX), MODELO.md
│       ├── site/              # dashboard web (index.html + data*.json + banner)
│       └── analisis_*.ipynb   # notebook
└── README.md
```

## Cómo ejecutar localmente

```bash
# Notebooks (pandas + matplotlib)
uv venv && uv pip install pandas matplotlib seaborn notebook
jupyter notebook   # abre el .ipynb del proyecto que quieras

# Dashboards web (fetch no funciona con file://, hay que servir)
python -m http.server 8100
# abrir http://localhost:8100/
```

## Nota sobre los datos

Todos los proyectos usan **datos sintéticos o públicos**. Ninguno contiene
información confidencial, de pacientes ni de terceros.
