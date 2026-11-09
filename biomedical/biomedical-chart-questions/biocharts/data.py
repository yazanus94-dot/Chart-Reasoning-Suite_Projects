"""Synthetic trial data (seeded). All numbers are fabricated for demonstration; this is not clinical data."""
import math
import random
import statistics

DOSES = [0, 5, 10, 20, 40]
N_PER_GROUP = 30
TRUE_MEAN = {0: 2.0, 5: 5.5, 10: 9.5, 20: 14.0, 40: 17.0}  # systolic BP reduction, mmHg
TRUE_SD = 6.0
HOURS = list(range(0, 9))
HR_TREATMENT = [78.0, 74.2, 70.1, 67.5, 64.3, 63.0, 62.4, 62.0, 61.8]
HR_PLACEBO = [77.0, 76.8, 76.5, 76.3, 76.0, 75.8, 75.7, 75.5, 75.4]


def build_data(seed: int = 21) -> dict:
    rng = random.Random(seed)
    patient_dose, patient_reduction = [], []
    means, sds, ci_half = [], [], []
    for d in DOSES:
        values = [round(rng.gauss(TRUE_MEAN[d], TRUE_SD), 1) for _ in range(N_PER_GROUP)]
        patient_dose += [d] * N_PER_GROUP
        patient_reduction += values
        m, s = statistics.mean(values), statistics.stdev(values)
        means.append(round(m, 2))
        sds.append(round(s, 2))
        ci_half.append(round(1.96 * s / math.sqrt(N_PER_GROUP), 2))
    hr_t = [round(v + rng.uniform(-0.2, 0.2), 1) for v in HR_TREATMENT]
    hr_p = [round(v + rng.uniform(-0.2, 0.2), 1) for v in HR_PLACEBO]
    return {
        "doses": DOSES, "n": N_PER_GROUP, "group_mean": means, "group_sd": sds, "ci_half": ci_half,
        "patient_dose": patient_dose, "patient_reduction": patient_reduction,
        "hours": HOURS, "hr_treatment": hr_t, "hr_placebo": hr_p,
        "_readable": ["group_mean", "ci_half", "hr_treatment", "hr_placebo", "patient_reduction"],
    }
