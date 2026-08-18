"""Dataset granular de finanzas para filtros interactivos.

Como el dataset es chico (20 empresas, ultimo anio), exporta la lista completa
de empresas con sus ratios y score. El filtro (sector / nivel) se aplica
directo en el navegador sobre esta lista.
"""
from __future__ import annotations
import csv, json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "powerbi" / "ratios_riesgo.csv"  # ya trae ratios + score calculados
SALIDA = RAIZ / "site" / "data_detalle.json"


def main() -> None:
    with CSV.open(encoding="utf-8-sig") as fh:
        filas = list(csv.DictReader(fh))
    registros = [
        {
            "empresa": f["empresa"], "sector": f["sector"], "anio": int(f["anio"]),
            "margen_neto": float(f["margen_neto"]), "liquidez": float(f["liquidez"]),
            "endeudamiento": float(f["endeudamiento"]), "roe": float(f["roe"]),
            "crecimiento": float(f["crecimiento"]), "score_riesgo": int(f["score_riesgo"]),
            "nivel": f["nivel"],
        }
        for f in filas
    ]
    registros.sort(key=lambda r: r["score_riesgo"], reverse=True)
    data = {
        "dims": {
            "sectores": sorted({r["sector"] for r in registros}),
            "niveles": ["Alto", "Medio", "Bajo"],
        },
        "registros": registros,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] finanzas data_detalle.json ({len(registros)} empresas, "
          f"{len(data['dims']['sectores'])} sectores)")


if __name__ == "__main__":
    main()
