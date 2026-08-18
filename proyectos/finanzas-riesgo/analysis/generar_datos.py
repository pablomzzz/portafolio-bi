"""Generador de estados financieros sinteticos para analisis de riesgo.

Crea estados financieros anuales de empresas ficticias de varios sectores,
con perfiles de salud distintos (sanas, medias, en riesgo) para que el analisis
de ratios detecte las senales de alerta.

Datos FICTICIOS. Solo stdlib.
Uso: python analysis/generar_datos.py --empresas 20 --anios 4 --seed 42
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from pathlib import Path

SECTORES = ["Retail", "Tecnología", "Manufactura", "Servicios", "Construcción"]

# perfil de riesgo -> (margen base, endeudamiento base, liquidez base, crecimiento base)
PERFILES = {
    "sana":    (0.14, 0.35, 1.9, 0.10),
    "media":   (0.07, 0.55, 1.3, 0.04),
    "riesgo":  (-0.02, 0.78, 0.9, -0.03),
}


@dataclass(frozen=True)
class Config:
    empresas: int
    anios: int
    seed: int
    salida: Path


def _jit(rng: random.Random, base: float, pct: float = 0.15) -> float:
    return base * (1 + rng.uniform(-pct, pct))


def generar_filas(cfg: Config) -> list[dict]:
    rng = random.Random(cfg.seed)
    anio_fin = 2025
    perfiles = list(PERFILES.keys())
    filas: list[dict] = []

    for e in range(1, cfg.empresas + 1):
        nombre = f"Empresa {chr(64 + e)}" if e <= 26 else f"Empresa {e}"
        sector = rng.choice(SECTORES)
        perfil = rng.choices(perfiles, weights=[45, 35, 20])[0]
        m_base, end_base, liq_base, cre_base = PERFILES[perfil]
        ingresos = rng.uniform(5_000, 80_000) * 1_000_000  # CLP

        for a in range(cfg.anios):
            anio = anio_fin - (cfg.anios - 1) + a
            crecimiento = _jit(rng, cre_base, 0.5)
            ingresos = max(1_000_000, ingresos * (1 + crecimiento))
            margen = _jit(rng, m_base, 0.4)
            utilidad = ingresos * margen
            costos = ingresos - utilidad
            endeud = min(0.95, max(0.1, _jit(rng, end_base)))
            activo_total = ingresos * rng.uniform(0.8, 1.4)
            deuda_total = activo_total * endeud
            patrimonio = activo_total - deuda_total
            liquidez = max(0.3, _jit(rng, liq_base))
            pasivo_corriente = deuda_total * rng.uniform(0.35, 0.6)
            activo_corriente = pasivo_corriente * liquidez

            filas.append({
                "empresa": nombre,
                "sector": sector,
                "anio": anio,
                "ingresos": round(ingresos),
                "costos": round(costos),
                "utilidad_neta": round(utilidad),
                "activo_corriente": round(activo_corriente),
                "pasivo_corriente": round(pasivo_corriente),
                "activo_total": round(activo_total),
                "deuda_total": round(deuda_total),
                "patrimonio": round(patrimonio),
            })
    return filas


def escribir_csv(filas: list[dict], salida: Path) -> None:
    salida.parent.mkdir(parents=True, exist_ok=True)
    with salida.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)


def parse_args() -> Config:
    p = argparse.ArgumentParser(description="Genera estados financieros sinteticos.")
    p.add_argument("--empresas", type=int, default=20)
    p.add_argument("--anios", type=int, default=4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--salida", type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "estados_financieros.csv",
    )
    a = p.parse_args()
    return Config(empresas=a.empresas, anios=a.anios, seed=a.seed, salida=a.salida)


def main() -> None:
    cfg = parse_args()
    filas = generar_filas(cfg)
    escribir_csv(filas, cfg.salida)
    empresas = len({f["empresa"] for f in filas})
    print(f"[OK] {len(filas)} filas ({empresas} empresas x {cfg.anios} anios) -> {cfg.salida}")


if __name__ == "__main__":
    main()
