"""python -m loadcharts.cli  -> draws charts, writes questions.md / answers.json / robustness report."""
import argparse
import csv
import json
import os
import sys

from .ambiguity import check_question
from .charts import draw_all
from .data import build_data
from .questions import FRAGILE_EXAMPLE, QUESTIONS


def write_csv(data, folder):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "load_test_results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["users", "throughput_rps", "avg_response_ms", "error_rate_pct"])
        w.writerows(zip(data["users"], data["throughput"], data["avg_rt"], data["error_rate"]))
    with open(os.path.join(folder, "percentiles.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["users", "p50_ms", "p90_ms", "p99_ms"])
        w.writerows(zip(data["pct_levels"], data["p50"], data["p90"], data["p99"]))


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate load-test charts and chart-reading questions.")
    p.add_argument("--seed", type=int, default=11)
    p.add_argument("--images", default="images")
    p.add_argument("--out", default="output")
    p.add_argument("--data", default="data")
    a = p.parse_args(argv)

    data = build_data(a.seed)
    draw_all(data, a.images)
    write_csv(data, a.data)
    os.makedirs(a.out, exist_ok=True)

    answers, md = [], ["# Chart questions and answer key", "", "All data is synthetic. Answers are computed from the data, not typed by hand.", ""]
    all_ok = True
    for q in QUESTIONS:
        check = check_question(q, data)
        all_ok &= check["ok"]
        ans = q.compute(data)
        answers.append({"id": q.id, "chart": q.chart, "question": q.text, "answer": ans, "unit": q.unit,
                        "difficulty": q.difficulty, "steps": q.steps(data), "robustness": check["robustness"], "flags": check["flags"]})
        md += [f"## {q.id} (difficulty {q.difficulty})", f"**Chart:** `{q.chart}`", "", f"**Question:** {q.text}", "",
               f"**Answer:** {ans}  _(unit: {q.unit})_", "", "**Solution:**", ""] + [f"{i}. {s}" for i, s in enumerate(q.steps(data), 1)]
        md += ["", f"_Reading-error robustness: {check['robustness']:.0%}_", ""]
    frag = check_question(FRAGILE_EXAMPLE, data)
    md += ["## Ambiguity check demo", "",
           f"The question \"{FRAGILE_EXAMPLE.text}\" was **flagged** and should not be submitted: " + "; ".join(frag["flags"]), ""]
    with open(os.path.join(a.out, "questions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    with open(os.path.join(a.out, "answers.json"), "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)
    print(f"charts -> {a.images}/  |  {len(QUESTIONS)} questions -> {a.out}/questions.md  |  all robust: {all_ok}")
    print(f"fragile demo flagged: {not frag['ok']}")
    return 0 if all_ok and not frag["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
