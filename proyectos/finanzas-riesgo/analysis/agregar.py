"""Analisis de riesgo financiero: ratios + score compuesto por empresa.

Lee estados financieros y calcula, para el ultimo anio de cada empresa:
- margen_neto, liquidez corriente, endeudamiento, ROE y crecimiento de ingresos.
Luego combina esas senales en un score de riesgo 0-100 (mayor = mas riesgo).

Salida: site/data.json. Solo stdlib. Uso: python analysis/agregar.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "estados_financieros.csv"
SALIDA = RAIZ / "site" / "data.json"
POWERBI_CSV = RAIZ / "powerbi" / "ratios_riesgo.csv"

UMBRAL_RIESGO = 50  # score >= 50 se considera "en riesgo"


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig") as fh:
        filas = list(csv.DictReader(fh))
    for f in filas:
        for k in ("anio", "ingresos", "costos", "utilidad_neta", "activo_corriente",
                  "pasivo_corriente", "activo_total", "deuda_total", "patrimonio"):
            f[k] = float(f[k])
    return filas


def por_empresa(filas: list[dict]) -> dict[str, list[dict]]:
    d: dict[str, list[dict]] = defaultdict(list)
    for f in filas:
        d[f["empresa"]].append(f)
    for lst in d.values():
        lst.sort(key=lambda x: x["anio"])
    return d


def _score_riesgo(margen: float, liquidez: float, endeud: float, crec: float) -> int:
    """0-100, mayor = mas riesgo. Cada dimension aporta hasta ~25 pts."""
    s = 0.0
    # liquidez < 1 es alarma; > 1.8 es sano
    s += max(0, min(25, (1.5 - liquidez) / 1.5 * 25))
    # endeudamiento > 0.7 alarma
    s += max(0, min(25, (endeud - 0.4) / 0.4 * 25))
    # margen negativo alarma
    s += max(0, min(25, (0.08 - margen) / 0.15 * 25))
    # decrecimiento alarma
    s += max(0, min(25, (0.03 - crec) / 0.1 * 25))
    return round(max(0, min(100, s)))


def analizar(filas: list[dict]) -> list[dict]:
    resultados: list[dict] = []
    for empresa, hist in por_empresa(filas).items():
        ult = hist[-1]
        prev = hist[-2] if len(hist) > 1 else ult
        margen = ult["utilidad_neta"] / ult["ingresos"]
        liquidez = ult["activo_corriente"] / ult["pasivo_corriente"]
        endeud = ult["deuda_total"] / ult["activo_total"]
        roe = ult["utilidad_neta"] / ult["patrimonio"] if ult["patrimonio"] else 0
        crec = (ult["ingresos"] - prev["ingresos"]) / prev["ingresos"] if prev["ingresos"] else 0
        score = _score_riesgo(margen, liquidez, endeud, crec)
        resultados.append({
            "empresa": empresa,
            "sector": ult["sector"],
            "anio": int(ult["anio"]),
            "margen_neto": round(margen, 3),
            "liquidez": round(liquidez, 2),
            "endeudamiento": round(endeud, 3),
            "roe": round(roe, 3),
            "crecimiento": round(crec, 3),
            "score_riesgo": score,
            "nivel": "Alto" if score >= 65 else "Medio" if score >= UMBRAL_RIESGO else "Bajo",
        })
    resultados.sort(key=lambda x: x["score_riesgo"], reverse=True)
    return resultados


def por_sector(res: list[dict]) -> list[dict]:
    d: dict[str, list[int]] = defaultdict(list)
    for r in res:
        d[r["sector"]].append(r["score_riesgo"])
    out = [{"sector": s, "riesgo_prom": round(sum(v) / len(v))} for s, v in d.items()]
    out.sort(key=lambda x: x["riesgo_prom"], reverse=True)
    return out


def kpis(res: list[dict]) -> dict:
    en_riesgo = [r for r in res if r["score_riesgo"] >= UMBRAL_RIESGO]
    return {
        "empresas": len(res),
        "en_riesgo": len(en_riesgo),
        "pct_riesgo": round(len(en_riesgo) * 100 / len(res), 1),
        "mas_riesgosa": res[0]["empresa"] if res else "N/A",
        "score_max": res[0]["score_riesgo"] if res else 0,
    }


def exportar_powerbi(res: list[dict]) -> None:
    """Exporta ratios + score ya calculados a un CSV listo para Power BI."""
    POWERBI_CSV.parent.mkdir(parents=True, exist_ok=True)
    campos = ["empresa", "sector", "anio", "margen_neto", "liquidez",
              "endeudamiento", "roe", "crecimiento", "score_riesgo", "nivel"]
    with POWERBI_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(res)
    print(f"[OK] CSV Power BI -> {POWERBI_CSV} ({len(res)} empresas)")


def main() -> None:
    filas = leer_filas(CSV)
    res = analizar(filas)
    exportar_powerbi(res)
    data = {
        "kpis": kpis(res),
        "ranking_riesgo": res,
        "por_sector": por_sector(res),
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] data.json -> {SALIDA}")
    print(f"     KPIs: {data['kpis']}")
    print("     Top 3 en riesgo:")
    for r in res[:3]:
        print(f"       {r['empresa']} ({r['sector']}): score={r['score_riesgo']} "
              f"liq={r['liquidez']} end={r['endeudamiento']} margen={r['margen_neto']}")


if __name__ == "__main__":
    main()
