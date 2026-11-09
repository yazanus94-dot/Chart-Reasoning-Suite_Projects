"""Deterministic synthetic load-test results (seeded). All numbers are fabricated for demonstration."""
import random

PERCENTILE_LEVELS = [60, 120, 180]


def build_data(seed: int = 11) -> dict:
    rng = random.Random(seed)
    users = list(range(10, 201, 10))
    throughput, avg_rt, error_rate = [], [], []
    for u in users:
        base = 4.0 * u if u <= 120 else 480.0 - 0.4 * (u - 120)
        throughput.append(round(base * (1 + rng.uniform(-0.012, 0.012)), 1))
        rt = 110 + 0.5 * u + (max(0, u - 120) ** 1.5) * 0.35
        avg_rt.append(round(rt * (1 + rng.uniform(-0.01, 0.01)), 1))
        err = 0.1 + max(0, u - 100) * 0.04
        error_rate.append(round(max(0.0, err + rng.uniform(-0.03, 0.03)), 2))
    rt_at = {u: avg_rt[users.index(u)] for u in PERCENTILE_LEVELS}
    p50 = [round(rt_at[u] * 0.80, 1) for u in PERCENTILE_LEVELS]
    p90 = [round(rt_at[u] * 1.60, 1) for u in PERCENTILE_LEVELS]
    p99 = [round(rt_at[u] * 3.00, 1) for u in PERCENTILE_LEVELS]
    return {
        "users": users, "throughput": throughput, "avg_rt": avg_rt, "error_rate": error_rate,
        "pct_levels": PERCENTILE_LEVELS, "p50": p50, "p90": p90, "p99": p99,
        "sla_error_pct": 1.0,
        # series a reader would estimate from the plot; the ambiguity check perturbs these
        "_readable": ["throughput", "avg_rt", "error_rate", "p50", "p90", "p99"],
    }
