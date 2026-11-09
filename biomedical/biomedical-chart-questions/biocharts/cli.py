"""python -m biocharts.cli  -> draws charts, writes questions.md / answers.json and the ambiguity report."""
import argparse
import csv
import json
import os
import sys

from .ambiguity import check_question
from .charts import draw_all
from .data import build_data
from .questions import FRAGILE_EXAMPLES, QUESTIONS


def write_csv(data, folder):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "group_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mg", "n", "mean_reduction_mmHg", "sd_mmHg", "ci95_half_width_mmHg"])
        w.writerows((d, data["n"], m, s, c) for d, m, s, c in zip(data["doses"], data["group_mean"], data["group_sd"], data["ci_half"]))
    with open(os.path.join(folder, "heart_rate.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["hour", "treatment_bpm", "placebo_bpm"])
        w.writerows(zip(data["hours"], data["hr_treatment"], data["hr_placebo"]))


def main(argv=None):
    p = argparse.ArgumentParser(description="Generate biostatistics charts and chart-reading questions.")
    p.add_argument("--seed", type=int, default=21)
    p.add_argument("--images", default="images")
    p.add_argument("--out", default="output")
    p.add_argument("--data", default="data")
    a = p.parse_args(argv)

    data = build_data(a.seed)
    draw_all(data, a.images)
    write_csv(data, a.data)
    os.makedirs(a.out, exist_ok=True)

    answers, md, all_ok = [], ["# Chart questions and answer key", "",
                               "All data is synthetic (not clinical data). Answers are computed from the data.", ""], True
    for q in QUESTIONS:
        check = check_question(q, data)
        all_ok &= check["ok"]
        ans = q.compute(data)
        answers.append({"id": q.id, "chart": q.chart, "question": q.text, "answer": ans, "unit": q.unit,
                        "difficulty": q.difficulty, "steps": q.steps(data), "robustness": check["robustness"], "flags": check["flags"]})
        md += [f"## {q.id} (difficulty {q.difficulty})", f"**Chart:** `{q.chart}`", "", f"**Question:** {q.text}", "",
               f"**Answer:** {ans}  _(unit: {q.unit})_", "", "**Solution:**", ""] + [f"{i}. {s}" for i, s in enumerate(q.steps(data), 1)]
        md += ["", f"_Reading-error robustness: {check['robustness']:.0%}_", ""]
    md += ["## Ambiguity check demos (flagged, not for submission)", ""]
    demos_flagged = True
    for q in FRAGILE_EXAMPLES:
        res = check_question(q, data)
        demos_flagged &= not res["ok"]
        md.append(f"- \"{q.text}\" -> " + "; ".join(res["flags"]))
    with open(os.path.join(a.out, "questions.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    with open(os.path.join(a.out, "answers.json"), "w", encoding="utf-8") as f:
        json.dump(answers, f, indent=2)
    print(f"charts -> {a.images}/  |  {len(QUESTIONS)} questions -> {a.out}/questions.md  |  all robust: {all_ok}  |  demos flagged: {demos_flagged}")
    return 0 if all_ok and demos_flagged else 1


if __name__ == "__main__":
    sys.exit(main())
