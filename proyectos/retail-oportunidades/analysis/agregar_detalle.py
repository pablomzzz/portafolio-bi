"""Dataset granular de retail para filtros interactivos.

Grano: mes x tienda x categoria x producto, con metricas aditivas (monto,
cantidad, lineas). Permite re-agregar en el navegador segun filtros.
"""
from __future__ import annotations
import csv, json
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSV = RAIZ / "data" / "transacciones.csv"
SALIDA = RAIZ / "site" / "data_detalle.json"


def main() -> None:
    with CSV.open(encoding="utf-8-sig") as fh:
        filas = list(csv.DictReader(fh))
    g: dict[tuple, dict] = defaultdict(lambda: {"monto": 0, "cantidad": 0, "lineas": 0})
    for f in filas:
        mes = f["fecha"][:7]
        k = (mes, f["tienda"], f["categoria"], f["producto"])
        g[k]["monto"] += int(float(f["monto"]))
        g[k]["cantidad"] += int(float(f["cantidad"] or 0))
        g[k]["lineas"] += 1
    registros = [
        {"mes": m, "tienda": t, "categoria": c, "producto": p,
         "monto": v["monto"], "cantidad": v["cantidad"], "lineas": v["lineas"]}
        for (m, t, c, p), v in g.items()
    ]
    registros.sort(key=lambda r: (r["mes"], r["tienda"], r["categoria"]))
    data = {
        "dims": {
            "meses": sorted({r["mes"] for r in registros}),
            "tiendas": sorted({r["tienda"] for r in registros}),
            "categorias": sorted({r["categoria"] for r in registros}),
        },
        "registros": registros,
    }
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] retail data_detalle.json ({len(registros)} registros, "
          f"{len(data['dims']['meses'])} meses)")


if __name__ == "__main__":
    main()
