"""Generador de datos sinteticos de ocupacion de camillas hospitalarias.

Crea un CSV realista para el proyecto de BI "Ocupacion de Camillas".
Los datos son FICTICIOS: no representan a ninguna institucion ni paciente real.

Diseno de realismo:
- Campana de invierno chilena (mayo-agosto): mas ocupacion en servicios
  respiratorios y urgencias.
- Turno noche: urgencias mas saturadas; servicios electivos mas tranquilos.
- Fin de semana: cirugia electiva baja, urgencias sube.
- Cada hospital tiene una capacidad y una presion base distinta.

Solo usa la libreria estandar (random, csv, datetime). No requiere instalar nada.

Uso:
    python analysis/generar_datos.py
    python analysis/generar_datos.py --dias 120 --seed 7 --salida data/mi.csv
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

# --- Configuracion del dominio (dimensiones) --------------------------------

HOSPITALES = [
    # (nombre ficticio, factor de presion base 0.55-0.80)
    ("Hospital Regional Norte", 0.74),
    ("Hospital Metropolitano Central", 0.80),
    ("Hospital del Valle", 0.58),
    ("Hospital Costa Poniente", 0.66),
]

# servicio -> (camillas base, sensibilidad al invierno 0-1, factor turno noche)
SERVICIOS = {
    "Urgencias": (40, 0.9, 1.25),
    "UCI": (16, 0.7, 1.05),
    "Medicina Interna": (60, 0.8, 1.0),
    "Cirugía": (45, 0.2, 0.75),
    "Pediatría": (30, 0.85, 1.0),
    "Maternidad": (25, 0.1, 1.0),
}

TURNOS = ["Mañana", "Tarde", "Noche"]
MESES_INVIERNO = {5, 6, 7, 8}  # campana de invierno en Chile


@dataclass(frozen=True)
class Config:
    dias: int
    seed: int
    salida: Path


# --- Logica pura de metricas ------------------------------------------------

def factor_invierno(dia: date, sensibilidad: float) -> float:
    """Multiplicador de presion segun temporada de invierno."""
    if dia.month in MESES_INVIERNO:
        return 1.0 + 0.22 * sensibilidad
    return 1.0


def factor_finde(dia: date, servicio: str) -> float:
    """Cirugía electiva baja el fin de semana; urgencias sube."""
    es_finde = dia.weekday() >= 5
    if not es_finde:
        return 1.0
    if servicio == "Cirugia":
        return 0.55
    if servicio == "Urgencias":
        return 1.15
    return 0.95


def factor_turno(turno: str, factor_noche: float) -> float:
    """Ajuste por turno. Noche usa el factor propio del servicio."""
    if turno == "Noche":
        return factor_noche
    if turno == "Tarde":
        return 1.05
    return 0.95  # Mañana


def calcular_ocupadas(totales: int, presion: float, rng: random.Random) -> int:
    """Camillas ocupadas dada una presion (0-1.4+). Se satura en totales."""
    ruido = rng.uniform(-0.08, 0.08)
    tasa = max(0.15, min(1.15, presion + ruido))
    return min(totales, round(totales * tasa))


def calcular_espera(totales: int, ocupadas: int, presion: float,
                    rng: random.Random) -> tuple[int, int]:
    """Pacientes en espera y tiempo promedio. Solo hay espera si esta lleno."""
    disponibles = totales - ocupadas
    if disponibles > 2 and presion < 1.0:
        return 0, rng.randint(5, 25)
    exceso = round((presion - 0.95) * totales * rng.uniform(0.3, 0.7))
    en_espera = max(0, exceso)
    if en_espera == 0:
        return 0, rng.randint(10, 30)
    tiempo = rng.randint(45, 180) + en_espera * rng.randint(3, 8)
    return en_espera, tiempo


# --- Generacion del dataset -------------------------------------------------

def generar_filas(cfg: Config) -> list[dict]:
    rng = random.Random(cfg.seed)
    inicio = date.today() - timedelta(days=cfg.dias - 1)
    filas: list[dict] = []

    for d in range(cfg.dias):
        dia = inicio + timedelta(days=d)
        for hospital, presion_hosp in HOSPITALES:
            for servicio, (base, sens, noche) in SERVICIOS.items():
                # capacidad instalada con pequena variacion por hospital
                totales = max(4, round(base * rng.uniform(0.85, 1.1)))
                for turno in TURNOS:
                    presion = (
                        presion_hosp
                        * factor_invierno(dia, sens)
                        * factor_finde(dia, servicio)
                        * factor_turno(turno, noche)
                    )
                    ocupadas = calcular_ocupadas(totales, presion, rng)
                    en_espera, t_espera = calcular_espera(
                        totales, ocupadas, presion, rng
                    )
                    filas.append({
                        "fecha": dia.isoformat(),
                        "hospital": hospital,
                        "servicio": servicio,
                        "turno": turno,
                        "camillas_totales": totales,
                        "camillas_ocupadas": ocupadas,
                        "tasa_ocupacion": round(ocupadas / totales, 3),
                        "pacientes_en_espera": en_espera,
                        "tiempo_espera_min_prom": t_espera,
                    })
    return filas


def escribir_csv(filas: list[dict], salida: Path) -> None:
    salida.parent.mkdir(parents=True, exist_ok=True)
    campos = list(filas[0].keys())
    with salida.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)


def parse_args() -> Config:
    p = argparse.ArgumentParser(description="Genera datos sinteticos de camillas.")
    p.add_argument("--dias", type=int, default=90, help="Dias de historia (def 90)")
    p.add_argument("--seed", type=int, default=42, help="Semilla aleatoria (def 42)")
    p.add_argument(
        "--salida", type=Path,
        default=Path(__file__).resolve().parent.parent / "data" / "ocupacion_camillas.csv",
        help="Ruta del CSV de salida",
    )
    a = p.parse_args()
    return Config(dias=a.dias, seed=a.seed, salida=a.salida)


def main() -> None:
    cfg = parse_args()
    filas = generar_filas(cfg)
    escribir_csv(filas, cfg.salida)
    en_rojo = sum(1 for f in filas if f["tasa_ocupacion"] >= 0.95)
    print(f"[OK] {len(filas)} filas generadas -> {cfg.salida}")
    print(f"     Rango: {cfg.dias} dias | {len(HOSPITALES)} hospitales | "
          f"{len(SERVICIOS)} servicios | {len(TURNOS)} turnos")
    print(f"     Filas en ocupacion critica (>=95%): {en_rojo} "
          f"({en_rojo * 100 // len(filas)}%)")


if __name__ == "__main__":
    main()
