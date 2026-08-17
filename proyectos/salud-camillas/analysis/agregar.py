"""Agrega el CSV de ocupacion en un data.json liviano para el dashboard web.

Separa la logica de agregacion (Python, testeable) de la presentacion (HTML).
El dashboard `site/index.html` consume `site/data.json` via fetch.

Solo stdlib. Uso:
    python analysis/agregar.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "ocupacion_camillas.csv"
SALIDA = RAIZ / "site" / "data.json"

MESES_INVIERNO = {"05", "06", "07", "08"}
UMBRAL_ROJO = 0.95


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _prom(nums: list[float]) -> float:
    return round(sum(nums) / len(nums), 3) if nums else 0.0


def top_rojo(filas: list[dict], limite: int = 10) -> list[dict]:
    """Top pabellones criticos (ocupacion >= umbral) por espera acumulada."""
    grupos: dict[tuple, dict] = defaultdict(
        lambda: {"espera": 0, "ocup": [], "veces": 0}
    )
    for f in filas:
        if float(f["tasa_ocupacion"]) >= UMBRAL_ROJO:
            k = (f["hospital"], f["servicio"], f["turno"])
            grupos[k]["espera"] += int(f["pacientes_en_espera"])
            grupos[k]["ocup"].append(float(f["tasa_ocupacion"]))
            grupos[k]["veces"] += 1
    salida = [
        {
            "hospital": h, "servicio": s, "turno": t,
            "espera": g["espera"],
            "ocupacion": _prom(g["ocup"]),
            "veces_rojo": g["veces"],
        }
        for (h, s, t), g in grupos.items()
    ]
    salida.sort(key=lambda x: (x["espera"], x["ocupacion"]), reverse=True)
    return salida[:limite]


def por_turno(filas: list[dict]) -> list[dict]:
    grupos: dict[str, dict] = defaultdict(
        lambda: {"ocup": [], "espera_min": [], "en_espera": 0}
    )
    for f in filas:
        g = grupos[f["turno"]]
        g["ocup"].append(float(f["tasa_ocupacion"]))
        g["espera_min"].append(int(f["tiempo_espera_min_prom"]))
        g["en_espera"] += int(f["pacientes_en_espera"])
    orden = ["Mañana", "Tarde", "Noche"]
    return [
        {
            "turno": t,
            "ocupacion": _prom(grupos[t]["ocup"]),
            "espera_min": round(sum(grupos[t]["espera_min"]) / len(grupos[t]["espera_min"])),
            "en_espera": grupos[t]["en_espera"],
        }
        for t in orden if t in grupos
    ]


def por_hospital(filas: list[dict]) -> list[dict]:
    grupos: dict[str, list] = defaultdict(list)
    for f in filas:
        grupos[f["hospital"]].append(float(f["tasa_ocupacion"]))
    salida = [{"hospital": h, "ocupacion": _prom(v)} for h, v in grupos.items()]
    salida.sort(key=lambda x: x["ocupacion"], reverse=True)
    return salida


def invierno_vs_resto(filas: list[dict]) -> list[dict]:
    grupos: dict[tuple, list] = defaultdict(list)
    for f in filas:
        mes = f["fecha"][5:7]
        temporada = "Invierno" if mes in MESES_INVIERNO else "Resto"
        grupos[(f["servicio"], temporada)].append(float(f["tasa_ocupacion"]))
    servicios = sorted({f["servicio"] for f in filas})
    return [
        {
            "servicio": s,
            "invierno": _prom(grupos.get((s, "Invierno"), [])),
            "resto": _prom(grupos.get((s, "Resto"), [])),
        }
        for s in servicios
    ]


def kpis(filas: list[dict], top: list[dict]) -> dict:
    n = len(filas)
    en_rojo = sum(1 for f in filas if float(f["tasa_ocupacion"]) >= UMBRAL_ROJO)
    total_espera = sum(int(f["pacientes_en_espera"]) for f in filas)
    peor = top[0] if top else None
    return {
        "filas": n,
        "pct_rojo": round(en_rojo * 100 / n, 1),
        "total_en_espera": total_espera,
        "peor_pabellon": (
            f"{peor['servicio']} / {peor['turno']} - {peor['hospital']}"
            if peor else "N/A"
        ),
    }


def main() -> None:
    filas = leer_filas(CSV)
    top = top_rojo(filas)
    data = {
        "kpis": kpis(filas, top),
        "top_rojo": top,
        "por_turno": por_turno(filas),
        "por_hospital": por_hospital(filas),
        "invierno_vs_resto": invierno_vs_resto(filas),
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] data.json escrito -> {SALIDA}")
    print(f"     KPIs: {data['kpis']}")


if __name__ == "__main__":
    main()
