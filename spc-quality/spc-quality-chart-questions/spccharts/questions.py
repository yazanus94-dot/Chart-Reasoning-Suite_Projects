"""Chart-reading questions for the quality charts. Answers are computed; solutions are written out."""
from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class Question:
    id: str
    chart: str
    text: str
    unit: str
    unit_words: List[str]
    difficulty: int
    compute: Callable
    steps: Callable
    tolerance_rel: float = 0.0
    tags: List[str] = field(default_factory=list)


def count_above_ucl(d):
    return sum(1 for v in d["defect_rate"] if v > d["ucl"])


def run_day(d, length=8):
    run = 0
    for day, v in zip(d["days"], d["defect_rate"]):
        run = run + 1 if v < d["center"] else 0
        if run == length:
            return day
    return None


def causes_for_share(d, share=0.80):
    total, cum = sum(d["counts"]), 0.0
    for i, c in enumerate(d["counts"], 1):
        cum += c
        if cum / total >= share:
            return i
    return len(d["counts"])


def top_two_share(d):
    return round(sum(d["counts"][:2]) / sum(d["counts"]) * 100)


def cpk(d):
    m, s = d["diam_mean"], d["diam_sd"]
    return round(min((d["usl"] - m) / (3 * s), (m - d["lsl"]) / (3 * s)), 2)


def q1_steps(d):
    over = [(day, v) for day, v in zip(d["days"], d["defect_rate"]) if v > d["ucl"]]
    return [f"UCL = center line + 3 sigma = {d['center']} + 3 x {d['sigma']} = {d['ucl']} percent (limits use days 1 to {d['baseline_days']}).",
            f"Points above {d['ucl']}: " + ", ".join(f"day {day} ({v} percent)" for day, v in over) + ".",
            f"Count = {count_above_ucl(d)}."]


def q2_steps(d):
    day = run_day(d)
    return [f"Center line = {d['center']} percent. Count consecutive points strictly below it, resetting at any point on or above it.",
            f"The last point above the line before the run is day {day - 8}; days {day - 7} to {day} are all below.",
            f"The 8th consecutive point below the center line is day {day}."]


def q3_steps(d):
    total, cum, out = sum(d["counts"]), 0, []
    for name, c in zip(d["causes"], d["counts"]):
        cum += c
        out.append(f"{name}: cumulative {cum} of {total} = {cum / total:.1%}")
    return ["Add the bars from the largest down and track the cumulative share (the cumulative line on the right axis)."] + out + \
        [f"The 80% mark is first reached with {causes_for_share(d)} causes."]


def q4_steps(d):
    t = sum(d["counts"])
    return [f"Total defects = {t}.", f"Top two causes = {d['counts'][0]} + {d['counts'][1]} = {d['counts'][0] + d['counts'][1]}.",
            f"Share = {d['counts'][0] + d['counts'][1]} / {t} x 100 = {top_two_share(d)} percent (nearest whole percent)."]


def q5_steps(d):
    m, s = d["diam_mean"], d["diam_sd"]
    up, lo = (d["usl"] - m) / (3 * s), (m - d["lsl"]) / (3 * s)
    return [f"Read from the chart: mean = {m} mm, sample standard deviation s = {s} mm, LSL = {d['lsl']} mm, USL = {d['usl']} mm.",
            f"Upper side: (USL - mean) / (3s) = ({d['usl']} - {m}) / (3 x {s}) = {up:.3f}.",
            f"Lower side: (mean - LSL) / (3s) = ({m} - {d['lsl']}) / (3 x {s}) = {lo:.3f}.",
            f"Cpk is the smaller value = {cpk(d)}."]


QUESTIONS = [
    Question("spc-q01", "fig1_control_chart.png",
             "How many points on the control chart fall above the upper control limit (UCL)? Answer as a number of points.",
             "points", ["points"], 1, count_above_ucl, q1_steps, 0.0, ["threshold"]),
    Question("spc-q02", "fig1_control_chart.png",
             "On which day is the 8th consecutive point below the center line reached? Answer as a day number.",
             "day", ["day"], 3, run_day, q2_steps, 0.0, ["run rule"]),
    Question("spc-q03", "fig2_pareto_defect_causes.png",
             "Starting with the largest cause, what is the smallest number of defect causes whose combined share of all defects reaches at least 80 percent? Answer as a number of causes.",
             "causes", ["causes"], 2, causes_for_share, q3_steps, 0.0, ["cumulative"]),
    Question("spc-q04", "fig2_pareto_defect_causes.png",
             "What percent of all defects are caused by the top two causes combined? Give the answer in percent to the nearest whole percent.",
             "percent", ["percent", "%"], 2, top_two_share, q4_steps, 0.04, ["calculation"]),
    Question("spc-q05", "fig3_capability_histogram.png",
             "Using the mean and the sample standard deviation printed on the histogram and the specification limits (LSL and USL), what is the process capability index Cpk? Give the answer to two decimal places.",
             "index", ["cpk", "index"], 3, cpk, q5_steps, 0.05, ["multi-step"]),
]


def points_near_center(d, band=0.05):
    return sum(1 for v in d["defect_rate"] if abs(v - d["center"]) <= band)


FRAGILE_EXAMPLES = [
    Question("spc-fragile-1", "fig1_control_chart.png",
             "How many points lie within 0.05 percentage points of the center line? Answer as a number of points.",
             "points", ["points"], 2, points_near_center, lambda d: ["Count points close to the line."], 0.0, ["demo: threshold-sensitive"]),
    Question("spc-fragile-2", "fig3_capability_histogram.png",
             "Using the standard deviation shown, what is Cpk? Give the index to two decimal places.",
             "index", ["cpk", "index"], 3, cpk, lambda d: ["Compute Cpk."], 0.05, ["demo: sample vs population SD not stated"]),
]
