"""Chart-reading questions for the biostatistics charts. Answers are computed; solutions are written out."""
from dataclasses import dataclass, field
from typing import Callable, List

from .stats import linear_fit


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


def i_of(d, dose):
    return d["doses"].index(dose)


def interval(d, dose):
    i = i_of(d, dose)
    return d["group_mean"][i] - d["ci_half"][i], d["group_mean"][i] + d["ci_half"][i]


def q1(d):
    return round(d["group_mean"][i_of(d, 20)] - d["group_mean"][i_of(d, 0)], 1)


def q1_steps(d):
    a, b = d["group_mean"][i_of(d, 20)], d["group_mean"][i_of(d, 0)]
    return [f"Read the mean reduction (the dot) for 20 mg: {a} mmHg, and for placebo (0 mg): {b} mmHg.",
            f"Difference = {a} - {b} = {q1(d)} mmHg."]


def q2(d):
    lo0, hi0 = interval(d, 0)
    out = []
    for dose in d["doses"][1:]:
        lo, hi = interval(d, dose)
        if lo > hi0 or hi < lo0:
            out.append(dose)
    return out


def q2_steps(d):
    lo0, hi0 = interval(d, 0)
    steps = [f"Placebo 95% CI = {round(lo0, 2)} to {round(hi0, 2)} mmHg (mean +/- the error bar).",
             "A dose group does not overlap placebo if its lower limit is above the placebo upper limit."]
    for dose in d["doses"][1:]:
        lo, hi = interval(d, dose)
        steps.append(f"{dose} mg: {round(lo, 2)} to {round(hi, 2)} -> " + ("no overlap" if dose in q2(d) else "overlaps"))
    steps.append(f"Dose groups with no overlap: {q2(d)} mg.")
    return steps


def q3(d):
    a, b = d["hr_treatment"][2], d["hr_treatment"][6]
    return round((a - b) / a * 100)


def q3_steps(d):
    a, b = d["hr_treatment"][2], d["hr_treatment"][6]
    return [f"Treatment mean heart rate at hour 2: {a} bpm; at hour 6: {b} bpm.",
            f"Fall = {round(a - b, 1)} bpm. Percentage fall = {round(a - b, 1)} / {a} x 100 = {round((a - b) / a * 100, 2)} percent, "
            f"which is {q3(d)} percent to the nearest whole percent."]


def q4(d):
    for h, t, p in zip(d["hours"], d["hr_treatment"], d["hr_placebo"]):
        if p - t >= 10:
            return h
    return None


def q4_steps(d):
    h = q4(d)
    return ["Gap = placebo mean heart rate minus treatment mean heart rate, hour by hour.",
            f"At hour {h - 1} the gap is {round(d['hr_placebo'][h - 1] - d['hr_treatment'][h - 1], 1)} bpm (below 10).",
            f"At hour {h} the gap is {round(d['hr_placebo'][h] - d['hr_treatment'][h], 1)} bpm (10 or more).",
            f"So the gap first reaches 10 bpm at hour {h}."]


def q5(d):
    slope, _ = linear_fit(d["patient_dose"], d["patient_reduction"])
    return round(slope * 10, 1)


def q5_steps(d):
    slope, intercept = linear_fit(d["patient_dose"], d["patient_reduction"])
    return [f"The fitted line over all {len(d['patient_dose'])} patients has slope {round(slope, 3)} mmHg per mg "
            f"(intercept {round(intercept, 2)} mmHg).",
            f"For each extra 10 mg: {round(slope, 3)} x 10 = {q5(d)} mmHg additional reduction."]


QUESTIONS = [
    Question("bio-q01", "fig1_dose_response_error_bars.png",
             "What is the difference in mean systolic blood-pressure reduction between the 20 mg group and the placebo (0 mg) group? Give the answer in mmHg to one decimal place.",
             "mmHg", ["mmhg"], 1, q1, q1_steps, 0.03, ["comparison"]),
    Question("bio-q02", "fig1_dose_response_error_bars.png",
             "The error bars show 95% confidence intervals. Which dose groups (in mg) have a 95% confidence interval that does not overlap the placebo group's interval?",
             "mg", ["mg"], 3, q2, q2_steps, 0.0, ["statistical feature"]),
    Question("bio-q03", "fig2_heart_rate_over_time.png",
             "Between hour 2 and hour 6, by what percentage does the treatment group's mean heart rate (bpm) fall? Give the answer in percent, to the nearest whole percent.",
             "percent", ["percent", "%"], 2, q3, q3_steps, 0.10, ["calculation"]),
    Question("bio-q04", "fig2_heart_rate_over_time.png",
             "At which hour (counting from the first dose at hour 0) does the placebo group's mean heart rate first exceed the treatment group's by at least 10 bpm?",
             "hour", ["hour"], 3, q4, q4_steps, 0.0, ["two series"]),
    Question("bio-q05", "fig3_dose_vs_reduction_scatter.png",
             "Using the fitted line through all patients, how many mmHg of additional systolic blood-pressure reduction does the line predict for each extra 10 mg of dose? Give the answer in mmHg to one decimal place.",
             "mmHg", ["mmhg"], 3, q5, q5_steps, 0.05, ["regression"]),
]


def largest_gap_hour(d):
    gaps = [p - t for t, p in zip(d["hr_treatment"], d["hr_placebo"])]
    return d["hours"][gaps.index(max(gaps))]


# Deliberately flawed examples that the ambiguity check must flag.
FRAGILE_EXAMPLES = [
    Question("bio-fragile-1", "fig2_heart_rate_over_time.png",
             "At which hour is the gap between the placebo and treatment heart rates largest? Answer as an hour.",
             "hour", ["hour"], 2, largest_gap_hour, lambda d: ["Find the largest gap."], 0.0, ["demo: late-hour plateau"]),
    Question("bio-fragile-2", "fig1_dose_response_error_bars.png",
             "Do the error bars of the 5 mg group and the placebo group overlap? Answer with the number of mg of the group.",
             "mg", ["mg"], 2, lambda d: 5, lambda d: ["Compare the bars."], 0.0, ["demo: error-bar type not stated"]),
]
