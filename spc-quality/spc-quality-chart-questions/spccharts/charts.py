"""Draw the three quality-control charts as PNG images (matplotlib, headless)."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLUE, RED, GREY, ORANGE = "#1F5FA8", "#C0392B", "#555555", "#E07B1A"


def chart_control(data, path):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.plot(data["days"], data["defect_rate"], "-o", color=BLUE, markersize=5, label="Defect rate (% of units)")
    ax.axhline(data["center"], color="#2E8B57", linewidth=1.6, label=f"Center line = {data['center']}%")
    ax.axhline(data["ucl"], color=RED, linestyle="--", label=f"UCL = {data['ucl']}%")
    ax.axhline(data["lcl"], color=RED, linestyle="--", label=f"LCL = {data['lcl']}%")
    over = [(d, v) for d, v in zip(data["days"], data["defect_rate"]) if v > data["ucl"]]
    ax.scatter([d for d, _ in over], [v for _, v in over], color=RED, s=90, zorder=5, label="Above UCL")
    ax.axvline(data["baseline_days"] + 0.5, color=GREY, linestyle=":", linewidth=1)
    ax.text(data["baseline_days"] + 0.8, data["lcl"] + 0.03, "limits calculated from days 1-20", fontsize=8.5, color=GREY)
    ax.set_xlabel("Day")
    ax.set_ylabel("Defect rate (% of units inspected)")
    ax.set_xticks(data["days"][::2])
    ax.set_title("Control chart of daily defect rate (UCL and LCL = center line +/- 3 sigma)")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=8.5, ncol=2)
    ax.set_ylim(data["lcl"] - 0.15, data["ucl"] + 0.55)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_pareto(data, path):
    total = sum(data["counts"])
    cum, run = [], 0
    for c in data["counts"]:
        run += c
        cum.append(run / total * 100)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    bars = ax.bar(data["causes"], data["counts"], color=BLUE)
    ax.bar_label(bars, padding=2, fontsize=9)
    ax.set_ylabel("Number of defects")
    ax.set_xlabel("Defect cause")
    ax2 = ax.twinx()
    ax2.plot(data["causes"], cum, "-o", color=ORANGE, label="Cumulative share (%)")
    ax2.axhline(80, color=GREY, linestyle="--", linewidth=1, label="80% line")
    ax2.set_ylim(0, 112)
    ax2.set_ylabel("Cumulative share of all defects (%)")
    for x, c in zip(data["causes"], cum):
        ax2.annotate(f"{c:.0f}%", (x, c), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8.5, color=ORANGE)
    ax.set_title(f"Pareto chart of defect causes (total = {total} defects)")
    ax2.legend(loc="center right")
    plt.setp(ax.get_xticklabels(), rotation=15)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_capability(data, path):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    ax.hist(data["diameters"], bins=22, color="#7FB3E0", edgecolor="white")
    ax.axvline(data["lsl"], color=RED, linewidth=2, label=f"LSL = {data['lsl']} mm")
    ax.axvline(data["usl"], color=RED, linewidth=2, label=f"USL = {data['usl']} mm")
    ax.axvline(data["nominal"], color="#2E8B57", linestyle="--", label=f"Nominal = {data['nominal']} mm")
    ax.set_xlabel("Part diameter (mm)")
    ax.set_ylabel("Number of parts")
    ax.set_title(f"Part diameter distribution with specification limits (n = {len(data['diameters'])})")
    ax.text(0.02, 0.95, f"mean = {data['diam_mean']:.3f} mm\nsample standard deviation s = {data['diam_sd']:.3f} mm",
            transform=ax.transAxes, va="top", fontsize=10, bbox={"boxstyle": "round", "facecolor": "white", "alpha": 0.9})
    ax.legend(loc="upper right")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def draw_all(data, folder):
    os.makedirs(folder, exist_ok=True)
    charts = {"fig1_control_chart.png": chart_control, "fig2_pareto_defect_causes.png": chart_pareto,
              "fig3_capability_histogram.png": chart_capability}
    for name, fn in charts.items():
        fn(data, os.path.join(folder, name))
    return list(charts)
