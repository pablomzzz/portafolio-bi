"""Generador de transacciones sinteticas de retail para market basket analysis.

Crea boletas (transacciones) con canastas realistas: ciertos productos
co-ocurren mas de lo esperado por azar (pan+mantequilla, cerveza+snacks,
cafe+azucar...), que es justo lo que un analisis de venta cruzada debe detectar.

Datos FICTICIOS. No representan a ninguna empresa real.
Solo stdlib. Uso:
    python analysis/generar_datos.py --boletas 5000 --seed 42
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

# --- Catalogo de productos (categoria -> productos) -------------------------

CATALOGO = {
    "Panaderia": ["Pan molde", "Pan hallulla", "Croissant"],
    "Lacteos": ["Leche", "Mantequilla", "Yogurt", "Queso"],
    "Bebidas": ["Bebida cola", "Agua mineral", "Jugo naranja"],
    "Alcohol": ["Cerveza", "Vino tinto"],
    "Snacks": ["Papas fritas", "Mani", "Galletas"],
    "Cafe/Te": ["Cafe", "Te", "Azucar"],
    "Bebe": ["Panales", "Toallitas humedas"],
    "Limpieza": ["Detergente", "Cloro", "Esponjas"],
}
PRODUCTOS = [p for prods in CATALOGO.values() for p in prods]

# --- Reglas de co-ocurrencia (afinidades) -----------------------------------
# Si la canasta ya tiene A, sube la probabilidad de agregar B.
AFINIDADES = {
    "Pan molde": [("Mantequilla", 0.55), ("Queso", 0.35)],
    "Pan hallulla": [("Mantequilla", 0.50), ("Queso", 0.30)],
    "Cerveza": [("Papas fritas", 0.60), ("Mani", 0.45)],
    "Vino tinto": [("Queso", 0.50)],
    "Cafe": [("Azucar", 0.65), ("Galletas", 0.30)],
    "Te": [("Azucar", 0.55)],
    "Panales": [("Toallitas humedas", 0.70), ("Cerveza", 0.25)],
    "Detergente": [("Cloro", 0.40), ("Esponjas", 0.35)],
    "Bebida cola": [("Papas fritas", 0.35)],
}

PRECIOS = {  # precio unitario aproximado en CLP
    "Pan molde": 1800, "Pan hallulla": 1500, "Croissant": 900,
    "Leche": 1200, "Mantequilla": 2500, "Yogurt": 800, "Queso": 4500,
    "Bebida cola": 1500, "Agua mineral": 900, "Jugo naranja": 1600,
    "Cerveza": 3500, "Vino tinto": 5000,
    "Papas fritas": 1800, "Mani": 1200, "Galletas": 1000,
    "Cafe": 4000, "Te": 2500, "Azucar": 1300,
    "Panales": 8000, "Toallitas humedas": 2200,
    "Detergente": 5500, "Cloro": 1400, "Esponjas": 1200,
}

TIENDAS = ["Tienda Centro", "Tienda Norte", "Tienda Sur", "Tienda Mall"]


@dataclass(frozen=True)
class Config:
    boletas: int
    seed: int
    salida: Path


def generar_canasta(rng: random.Random) -> list[str]:
    """Arma una canasta: productos semilla + productos por afinidad."""
    n_semillas = rng.choices([1, 2, 3, 4], weights=[20, 40, 30, 10])[0]
    canasta: set[str] = set(rng.sample(PRODUCTOS, n_semillas))
    # aplicar afinidades (venta cruzada natural)
    for producto in list(canasta):
        for asociado, prob in AFINIDADES.get(producto, []):
            if rng.random() < prob:
                canasta.add(asociado)
    return sorted(canasta)


def generar_filas(cfg: Config) -> list[dict]:
    rng = random.Random(cfg.seed)
    inicio = date.today() - timedelta(days=89)
    filas: list[dict] = []
    for i in range(1, cfg.boletas + 1):
        dia = inicio + timedelta(days=rng.randint(0, 89))
        tienda = rng.choice(TIENDAS)
        canasta = generar_canasta(rng)
        for producto in canasta:
            cantidad = rng.choices([1, 2, 3], weights=[70, 22, 8])[0]
            filas.append({
                "boleta_id": i,
                "fecha": dia.isoformat(),
                "tienda": tienda,
                "producto": producto,
                "categoria": next(c for c, ps in CATALOGO.items() if producto in ps),
                "cantidad": cantidad,
                "precio_unit": PRECIOS[producto],
                "monto": cantidad * PRECIOS[producto],
            })
    return filas


def escribir_csv(filas: list[dict], salida: Path) -> None:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)


def parse_args() -> Config:
    p = argparse.ArgumentParser(description="Genera transacciones de retail.")
    p.add_argument("--boletas", type=int, default=5000)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--salida", type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "transacciones.csv",
    )
    a = p.parse_args()
    return Config(boletas=a.boletas, seed=a.seed, salida=a.salida)


def main() -> None:
    cfg = parse_args()
    filas = generar_filas(cfg)
    escribir_csv(filas, cfg.salida)
    boletas = len({f["boleta_id"] for f in filas})
    print(f"[OK] {len(filas)} lineas en {boletas} boletas -> {cfg.salida}")
    print(f"     Productos: {len(PRODUCTOS)} | Tiendas: {len(TIENDAS)} | 90 dias")


if __name__ == "__main__":
    main()
