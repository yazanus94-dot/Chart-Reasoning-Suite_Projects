"""Ambiguity checks: would the answer change if a reader misjudged the chart slightly?"""
import random


def equivalent(a, b, tol_rel):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol_rel * abs(b) if tol_rel else a == b
    return a == b


def robustness(q, data, rel_noise=0.005, trials=300, seed=0):
    """Share of trials where a +/-0.5% misreading of the plotted values still gives an equivalent answer."""
    rng = random.Random(seed)
    base = q.compute(data)
    ok = 0
    for _ in range(trials):
        d = dict(data)
        for key in data["_readable"]:
            d[key] = [v * (1 + rng.uniform(-rel_noise, rel_noise)) for v in data[key]]
        ok += equivalent(q.compute(d), base, q.tolerance_rel)
    return ok / trials


def check_question(q, data, min_robustness=0.95):
    score = robustness(q, data)
    flags = []
    if not any(w in q.text.lower() for w in q.unit_words):
        flags.append(f"question text does not state the unit ({q.unit})")
    if score < min_robustness:
        flags.append(f"answer is sensitive to small reading errors (stable in {score:.0%} of trials)")
    return {"id": q.id, "robustness": round(score, 3), "flags": flags, "ok": not flags}
