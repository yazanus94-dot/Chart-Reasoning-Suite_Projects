"""Synthetic manufacturing data (seeded). All numbers are fabricated for demonstration."""
import random
import statistics

BASELINE_DAYS = 20
TAIL = [2.15, 1.95, 3.10, 1.85, 1.80, 1.75, 1.70, 1.80, 1.70, 1.75, 1.80, 1.70]  # days 21-32
CAUSES = ["Scratches", "Misalignment", "Missing component", "Wrong label", "Porosity", "Other"]
COUNTS = [48, 31, 12, 7, 5, 3]
LSL, USL, NOMINAL = 49.85, 50.15, 50.00


def build_data(seed: int = 31) -> dict:
    rng = random.Random(seed)
    base = []
    for _ in range(BASELINE_DAYS):
        v = rng.gauss(2.0, 0.25)
        base.append(round(min(max(v, 2.0 - 0.6), 2.0 + 0.6), 2))  # clamp so baseline stays in control
    rate = base + TAIL
    center = round(statistics.mean(base), 3)
    sigma = round(statistics.stdev(base), 3)
    diameters = [round(rng.gauss(50.012, 0.046), 3) for _ in range(200)]
    return {
        "days": list(range(1, len(rate) + 1)), "defect_rate": rate, "baseline_days": BASELINE_DAYS,
        "center": center, "sigma": sigma, "ucl": round(center + 3 * sigma, 3), "lcl": round(center - 3 * sigma, 3),
        "causes": CAUSES, "counts": COUNTS,
        "diameters": diameters, "diam_mean": round(statistics.mean(diameters), 3),
        "diam_sd": round(statistics.stdev(diameters), 3), "lsl": LSL, "usl": USL, "nominal": NOMINAL,
        # absolute reading error assumed per quantity shown on a chart (about 0.5% of its axis range, or display rounding)
        "_readable": {"defect_rate": 0.0175, "center": 0.0175, "ucl": 0.0175, "lcl": 0.0175,
                      "counts": 0.25, "diam_mean": 0.0005, "diam_sd": 0.0005},
    }
