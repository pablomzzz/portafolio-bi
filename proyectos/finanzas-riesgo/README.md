# Riesgo Financiero de Empresas

> **Pregunta de negocio:** Que empresas muestran senales de riesgo?

Analisis de ratios financieros combinados en un **score de riesgo** para
priorizar revision de cartera, credito o inversion.

**Autor:** Pablo Morales ([@pablomzzz](https://github.com/pablomzzz))

## El caso de negocio

Un analista de riesgo o un comite de credito no quiere leer 20 balances. Quiere:
1. **Un ranking** de que empresas estan en zona critica.
2. **Por que** (que ratios disparan la alerta).
3. **Donde concentrar** la revision (sectores mas expuestos).

La accion que habilita: **priorizar revision de credito, ajustar exposicion o
condiciones** antes de que el riesgo se materialice.

## Metodo: ratios + score compuesto

Del ultimo anio de cada empresa se calculan:
- **margen neto** = utilidad / ingresos
- **liquidez corriente** = activo corriente / pasivo corriente (bajo 1 = no cubre deudas de corto plazo)
- **endeudamiento** = deuda / activo total
- **ROE** = utilidad / patrimonio
- **crecimiento** de ingresos (anio contra anio)

Se combinan en un **score de riesgo 0-100** (mayor = mas riesgo). Cada dimension
aporta hasta ~25 puntos.

## Que demuestra

| Habilidad | Donde |
|---|---|
| SQL (window functions, self-join por MAX(anio)) | `analysis/consultas.sql` |
| Python / modelado de score | `analysis/agregar.py` |
| Conocimiento de negocio (ratios financieros) | metodo y recomendaciones |
| Viz web (scatter de riesgo, ranking) | `site/` |

## Como reproducir

```bash
python analysis/generar_datos.py    # data/estados_financieros.csv (20 empresas x 4 anios)
python analysis/agregar.py          # ratios + score -> site/data.json
python -m http.server 8100 --directory site
```

## Datos

Sinteticos, con perfiles de salud financiera variados (sanas, medias, en riesgo).
No representan a ninguna empresa real. Cuando quieras, se pueden reemplazar por
datos publicos (ej: estados financieros de la CMF Chile) manteniendo el esquema.

## Estructura

```
finanzas-riesgo/
├── data/          # estados_financieros.csv (generado)
├── analysis/      # generar_datos.py, agregar.py, consultas.sql
├── powerbi/       # .pbix + capturas (en tu PC)
└── site/          # dashboard web (index.html + data.json)
```
