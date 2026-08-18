"""Agrega el CSV a un dataset GRANULAR para filtros interactivos en el dashboard.

A diferencia de agregar.py (que produce totales fijos), este genera registros
por mes x hospital x servicio x turno con metricas ADITIVAS. Asi el dashboard
puede re-agregar en el navegador segun los filtros que elija el usuario
(rango de meses, hospital, servicio, turno) sin backend.

Solo stdlib. Uso: python analysis/agregar_detalle.py
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "ocupacion_camillas.csv"
SALIDA = RAIZ / "site" / "data_detalle.json"
UMBRAL_ROJO = 0.95
MESES_INVIERNO = {"05", "06", "07", "08"}


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    filas = leer_filas(CSV)
    # grano: (mes 'YYYY-MM', hospital, servicio, turno) -> metricas aditivas
    grupos: dict[tuple, dict] = defaultdict(
        lambda: {"n": 0, "suma_ocup": 0.0, "suma_espera": 0,
                 "n_rojo": 0, "suma_espera_min": 0}
    )
    for f in filas:
        mes = f["fecha"][:7]  # YYYY-MM
        k = (mes, f["hospital"], f["servicio"], f["turno"])
        g = grupos[k]
        ocup = float(f["tasa_ocupacion"])
        g["n"] += 1
        g["suma_ocup"] += ocup
        g["suma_espera"] += int(f["pacientes_en_espera"])
        g["suma_espera_min"] += int(f["tiempo_espera_min_prom"])
        if ocup >= UMBRAL_ROJO:
            g["n_rojo"] += 1

    registros = [
        {
            "mes": mes, "hospital": h, "servicio": s, "turno": t,
            "temporada": "Invierno" if mes[5:7] in MESES_INVIERNO else "Resto",
            "n": g["n"],
            "suma_ocup": round(g["suma_ocup"], 4),
            "suma_espera": g["suma_espera"],
            "n_rojo": g["n_rojo"],
            "suma_espera_min": g["suma_espera_min"],
        }
        for (mes, h, s, t), g in grupos.items()
    ]
    registros.sort(key=lambda r: (r["mes"], r["hospital"], r["servicio"], r["turno"]))

    data = {
        "dims": {
            "meses": sorted({r["mes"] for r in registros}),
            "hospitales": sorted({r["hospital"] for r in registros}),
            "servicios": sorted({r["servicio"] for r in registros}),
            "turnos": ["Mañana", "Tarde", "Noche"],
        },
        "umbral_rojo": UMBRAL_ROJO,
        "registros": registros,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] data_detalle.json -> {SALIDA}")
    print(f"     {len(registros)} registros | {len(data['dims']['meses'])} meses | "
          f"{len(data['dims']['hospitales'])} hospitales")


if __name__ == "__main__":
    main()
