"""Ambiguity checks: unit stated, standard-deviation type stated, and answer stable under small reading errors."""
import random


def equivalent(a, b, tol_rel):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= tol_rel * abs(b) if tol_rel else a == b
    return a == b


def perturb(data, rng):
    d = dict(data)
    for key, scale in data["_readable"].items():
        value = data[key]
        if isinstance(value, list):
            d[key] = [v + rng.uniform(-scale, scale) for v in value]
        else:
            d[key] = value + rng.uniform(-scale, scale)
    return d


def robustness(q, data, trials=300, seed=0):
    """Share of trials where plausible chart-reading errors still give an equivalent answer."""
    rng = random.Random(seed)
    base = q.compute(data)
    return sum(equivalent(q.compute(perturb(data, rng)), base, q.tolerance_rel) for _ in range(trials)) / trials


def check_question(q, data, min_robustness=0.95):
    flags, text = [], q.text.lower()
    if not any(w in text for w in q.unit_words):
        flags.append(f"question text does not state the unit ({q.unit})")
    if ("cpk" in text or "standard deviation" in text) and "sample" not in text and "population" not in text:
        flags.append("question uses a standard deviation without saying whether it is the sample or population value")
    score = robustness(q, data)
    if score < min_robustness:
        flags.append(f"answer is sensitive to small reading errors (stable in {score:.0%} of trials)")
    return {"id": q.id, "robustness": round(score, 3), "flags": flags, "ok": not flags}
