# Riesgo Financiero de Empresas

> **Pregunta de negocio:** ¿Qué empresas muestran señales de riesgo?

Análisis de ratios financieros combinados en un **score de riesgo** para
priorizar revisión de cartera, crédito o inversión.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

## El caso de negocio

Un analista de riesgo o un comité de crédito no quiere leer 20 balances. Quiere:
1. **Un ranking** de qué empresas están en zona crítica.
2. **Por qué** (qué ratios disparan la alerta).
3. **Dónde concentrar** la revisión (sectores más expuestos).

La acción que habilita: **priorizar revisión de crédito, ajustar exposición o
condiciones** antes de que el riesgo se materialice.

## Método: ratios + score compuesto

Del último año de cada empresa se calculan:
- **margen neto** = utilidad / ingresos
- **liquidez corriente** = activo corriente / pasivo corriente (bajo 1 = no cubre deudas de corto plazo)
- **endeudamiento** = deuda / activo total
- **ROE** = utilidad / patrimonio
- **crecimiento** de ingresos (año contra año)

Se combinan en un **score de riesgo 0-100** (mayor = más riesgo). Cada dimensión
aporta hasta ~25 puntos.

## Qué demuestra

| Habilidad | Dónde |
|---|---|
| SQL (window functions, self-join por MAX(anio)) | `analysis/consultas.sql` |
| Python / modelado de score | `analysis/agregar.py` |
| Conocimiento de negocio (ratios financieros) | método y recomendaciones |
| Viz web (scatter de riesgo, ranking) | `site/` |

## Cómo reproducir

```bash
python analysis/generar_datos.py    # data/estados_financieros.csv (20 empresas x 4 años)
python analysis/agregar.py          # ratios + score → site/data.json
python -m http.server 8100 --directory site
```

## Datos

Sintéticos, con perfiles de salud financiera variados (sanas, medias, en riesgo).
No representan a ninguna empresa real. Cuando quieras, se pueden reemplazar por
datos públicos (ej: estados financieros de la CMF Chile) manteniendo el esquema.

## Estructura

```
finanzas-riesgo/
├── data/          # estados_financieros.csv (generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # .pbix + capturas (en tu PC)
└── site/          # dashboard web (index.html + data.json)
```
