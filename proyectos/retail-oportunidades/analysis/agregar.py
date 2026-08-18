"""Market basket analysis: detecta oportunidades de venta cruzada.

Lee las transacciones y calcula, para cada par de productos:
- support(A,B): cuan frecuente es la combinacion (boletas con ambos / total)
- confidence(A->B): P(comprar B | compro A)
- lift: cuanto mas se compran juntos vs por azar. lift > 1 = afinidad real.

Salida: site/data.json con top oportunidades + ventas por producto/categoria/tienda.
Solo stdlib. Uso: python analysis/agregar.py
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "transacciones.csv"
SALIDA = RAIZ / "site" / "data.json"
POWERBI_CSV = RAIZ / "powerbi" / "oportunidades_cross_sell.csv"

SOPORTE_MIN = 0.01   # el par debe aparecer en al menos 1% de las boletas
TOP_N = 10


def leer_filas(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def canastas(filas: list[dict]) -> list[set[str]]:
    por_boleta: dict[str, set[str]] = defaultdict(set)
    for f in filas:
        por_boleta[f["boleta_id"]].add(f["producto"])
    return list(por_boleta.values())


def market_basket(cestas: list[set[str]]) -> list[dict]:
    total = len(cestas)
    cont_item: dict[str, int] = defaultdict(int)
    cont_par: dict[tuple, int] = defaultdict(int)
    for cesta in cestas:
        for item in cesta:
            cont_item[item] += 1
        for a, b in combinations(sorted(cesta), 2):
            cont_par[(a, b)] += 1

    reglas: list[dict] = []
    for (a, b), n_ab in cont_par.items():
        soporte = n_ab / total
        if soporte < SOPORTE_MIN:
            continue
        sup_a, sup_b = cont_item[a] / total, cont_item[b] / total
        lift = soporte / (sup_a * sup_b)
        reglas.append({
            "producto_a": a,
            "producto_b": b,
            "soporte": round(soporte, 4),
            "confianza_a_b": round(n_ab / cont_item[a], 3),
            "lift": round(lift, 2),
            "boletas": n_ab,
        })
    reglas.sort(key=lambda r: r["lift"], reverse=True)
    return reglas


def _sum_por(filas: list[dict], clave: str) -> list[dict]:
    tot: dict[str, int] = defaultdict(int)
    for f in filas:
        tot[f[clave]] += int(f["monto"])
    out = [{clave: k, "monto": v} for k, v in tot.items()]
    out.sort(key=lambda x: x["monto"], reverse=True)
    return out


def kpis(filas: list[dict], top: list[dict]) -> dict:
    total_ventas = sum(int(f["monto"]) for f in filas)
    boletas = len({f["boleta_id"] for f in filas})
    mejor = top[0] if top else None
    return {
        "ventas_total": total_ventas,
        "boletas": boletas,
        "ticket_promedio": round(total_ventas / boletas),
        "mejor_oportunidad": (
            f"{mejor['producto_a']} + {mejor['producto_b']}" if mejor else "N/A"
        ),
        "mejor_lift": mejor["lift"] if mejor else 0,
    }


def exportar_powerbi(pares: list[dict]) -> None:
    """Exporta TODAS las reglas de asociacion a un CSV listo para Power BI."""
    POWERBI_CSV.parent.mkdir(parents=True, exist_ok=True)
    campos = ["producto_a", "producto_b", "soporte", "confianza_a_b", "lift", "boletas"]
    with POWERBI_CSV.open("w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(pares)
    print(f"[OK] CSV Power BI -> {POWERBI_CSV} ({len(pares)} pares)")


def main() -> None:
    filas = leer_filas(CSV)
    cestas = canastas(filas)
    todos = market_basket(cestas)
    top = todos[:TOP_N]
    exportar_powerbi(todos)
    data = {
        "kpis": kpis(filas, top),
        "top_oportunidades": top,
        "top_productos": _sum_por(filas, "producto")[:10],
        "por_categoria": _sum_por(filas, "categoria"),
        "por_tienda": _sum_por(filas, "tienda"),
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] data.json -> {SALIDA}")
    print(f"     KPIs: {data['kpis']}")
    print("     Top 3 oportunidades (lift):")
    for r in top[:3]:
        print(f"       {r['producto_a']} + {r['producto_b']}: "
              f"lift={r['lift']} confianza={r['confianza_a_b']}")


if __name__ == "__main__":
    main()
