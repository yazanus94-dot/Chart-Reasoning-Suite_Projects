"""Ambiguity checks: unit stated, error-bar type stated, and answer stable under small misreadings."""
import random

ERROR_BAR_TYPES = ("95%", "standard deviation", "standard error", "sem", "confidence interval")


def equivalent(a, b, tol_rel):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(a - b) <= tol_rel * abs(b) if tol_rel else a == b
    return a == b


def robustness(q, data, rel_noise=0.005, trials=300, seed=0):
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
    flags, text = [], q.text.lower()
    score = robustness(q, data)
    if not any(w in text for w in q.unit_words):
        flags.append(f"question text does not state the unit ({q.unit})")
    if "error bar" in text and not any(t in text for t in ERROR_BAR_TYPES):
        flags.append("question mentions error bars without saying what they show (SD, SEM or 95% CI)")
    if score < min_robustness:
        flags.append(f"answer is sensitive to small reading errors (stable in {score:.0%} of trials)")
    return {"id": q.id, "robustness": round(score, 3), "flags": flags, "ok": not flags}
