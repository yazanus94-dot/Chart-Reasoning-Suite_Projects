"""Draw the three load-test charts as PNG images (matplotlib, headless)."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .questions import first_plateau_level  # noqa: E402

BLUE, ORANGE, RED, GREY = "#1F5FA8", "#E07B1A", "#C0392B", "#555555"


def chart_throughput_vs_response_time(data, path):
    fig, ax1 = plt.subplots(figsize=(9, 5), dpi=150)
    (line1,) = ax1.plot(data["users"], data["throughput"], "-o", color=BLUE, label="Throughput (requests/s, left axis)")
    ax1.set_xlabel("Virtual users")
    ax1.set_ylabel("Throughput (requests per second)", color=BLUE)
    ax1.tick_params(axis="y", labelcolor=BLUE)
    ax1.set_xticks(data["users"][1::2])
    ax1.set_ylim(0, 560)
    ax1.grid(True, alpha=0.3)
    ax2 = ax1.twinx()
    (line2,) = ax2.plot(data["users"], data["avg_rt"], "-s", color=ORANGE, label="Average response time (ms, right axis)")
    ax2.set_ylabel("Average response time (ms)", color=ORANGE)
    ax2.tick_params(axis="y", labelcolor=ORANGE)
    knee = first_plateau_level(data)
    ax1.axvline(knee, color=GREY, linestyle="--", linewidth=1)
    knee_y = data["throughput"][data["users"].index(knee)]
    ax1.annotate("throughput stops growing", (knee, knee_y), xytext=(knee + 8, knee_y + 45),
                 arrowprops={"arrowstyle": "->", "color": GREY}, color=GREY, fontsize=9)
    lines = [line1, line2]
    ax1.legend(lines, [l.get_label() for l in lines], loc="upper left", fontsize=9)
    ax1.set_title("Load test: throughput and average response time vs virtual users")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_percentiles(data, path):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    levels = data["pct_levels"]
    width, xs = 0.25, range(len(levels))
    for offset, (key, label, color) in enumerate([("p50", "p50", "#7FB3E0"), ("p90", "p90", BLUE), ("p99", "p99", "#0B2A52")]):
        pos = [x + (offset - 1) * width for x in xs]
        bars = ax.bar(pos, data[key], width, label=label, color=color)
        ax.bar_label(bars, fmt="%.1f", fontsize=8, padding=2)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([f"{u} users" for u in levels])
    ax.set_ylabel("Response time (ms)")
    ax.set_title("Response-time percentiles at three load levels")
    ax.legend(title="Percentile")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def chart_error_rate(data, path):
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    ax.plot(data["users"], data["error_rate"], "-o", color=RED, label="Error rate (%)")
    ax.axhline(data["sla_error_pct"], color=GREY, linestyle="--", label=f"SLA limit ({data['sla_error_pct']:.0f}%)")
    ax.set_xlabel("Virtual users")
    ax.set_ylabel("Error rate (% of requests)")
    ax.set_xticks(data["users"][1::2])
    ax.set_title("Error rate vs virtual users, with the 1% SLA limit")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def draw_all(data, folder):
    os.makedirs(folder, exist_ok=True)
    paths = {
        "fig1_throughput_vs_response_time.png": chart_throughput_vs_response_time,
        "fig2_response_time_percentiles.png": chart_percentiles,
        "fig3_error_rate_vs_users.png": chart_error_rate,
    }
    for name, fn in paths.items():
        fn(data, os.path.join(folder, name))
    return list(paths)
