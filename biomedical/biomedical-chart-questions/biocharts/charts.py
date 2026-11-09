"""Draw the three biostatistics charts as PNG images (matplotlib, headless)."""
import os
import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .stats import linear_fit  # noqa: E402

BLUE, ORANGE, GREY, GREEN = "#1F5FA8", "#E07B1A", "#555555", "#2E8B57"


def chart_dose_response(data, path):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    xs = list(range(len(data["doses"])))
    ax.errorbar(xs, data["group_mean"], yerr=data["ci_half"], fmt="o", color=BLUE, ecolor=BLUE,
                capsize=6, markersize=8, linewidth=1.8, label="Mean reduction with 95% CI")
    ax.set_xticks(xs)
    ax.set_xticklabels(["0 (placebo)" if d == 0 else str(d) for d in data["doses"]])
    ax.set_xlabel("Dose (mg)")
    ax.set_ylabel("Reduction in systolic blood pressure (mmHg)")
    ax.set_title(f"Dose-response: mean reduction by dose group (n = {data['n']} per group)")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(loc="upper left")
    ax.text(0.99, 0.03, "Error bars show 95% confidence intervals", transform=ax.transAxes, ha="right", fontsize=9, color=GREY)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_heart_rate(data, path):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    ax.plot(data["hours"], data["hr_treatment"], "-o", color=BLUE, label="Treatment group")
    ax.plot(data["hours"], data["hr_placebo"], "-s", color=ORANGE, label="Placebo group")
    ax.axvline(0, color=GREY, linestyle="--", linewidth=1)
    ax.annotate("first dose", (0, min(data["hr_treatment"]) + 0.5), xytext=(0.3, 62.0), color=GREY, fontsize=9)
    ax.set_xlabel("Hours since first dose")
    ax.set_ylabel("Mean heart rate (beats per minute, bpm)")
    ax.set_xticks(data["hours"])
    ax.set_title("Mean heart rate over time: treatment vs placebo")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_scatter(data, path):
    rng = random.Random(5)
    jitter = [d + rng.uniform(-1.2, 1.2) for d in data["patient_dose"]]
    slope, intercept = linear_fit(data["patient_dose"], data["patient_reduction"])
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    ax.scatter(jitter, data["patient_reduction"], s=18, alpha=0.55, color=GREEN, label="Individual patients")
    xs = [0, 40]
    ax.plot(xs, [intercept + slope * x for x in xs], color=BLUE, linewidth=2.2, label="Fitted line (least squares)")
    ax.set_xlabel("Dose (mg)  [points jittered horizontally for visibility]")
    ax.set_ylabel("Reduction in systolic blood pressure (mmHg)")
    ax.set_title(f"Individual response vs dose (n = {len(data['patient_dose'])} patients) with fitted line")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def draw_all(data, folder):
    os.makedirs(folder, exist_ok=True)
    charts = {
        "fig1_dose_response_error_bars.png": chart_dose_response,
        "fig2_heart_rate_over_time.png": chart_heart_rate,
        "fig3_dose_vs_reduction_scatter.png": chart_scatter,
    }
    for name, fn in charts.items():
        fn(data, os.path.join(folder, name))
    return list(charts)
