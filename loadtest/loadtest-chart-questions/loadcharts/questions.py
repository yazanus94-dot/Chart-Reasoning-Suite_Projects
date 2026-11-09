"""Chart-reading questions. Each answer is COMPUTED from the data, with the reasoning written out step by step."""
from dataclasses import dataclass, field
from typing import Callable, List, Union

Answer = Union[float, int, str]


@dataclass
class Question:
    id: str
    chart: str
    text: str
    unit: str
    unit_words: List[str]
    difficulty: int
    compute: Callable[[dict], Answer]
    steps: Callable[[dict], List[str]]
    tolerance_rel: float = 0.0  # acceptable relative reading error for numeric answers
    decimals: int = 1
    tags: List[str] = field(default_factory=list)


def idx(data, users_value):
    return data["users"].index(users_value)


def first_plateau_level(data, growth=0.02):
    t, u = data["throughput"], data["users"]
    for i in range(1, len(t)):
        if (t[i] - t[i - 1]) / t[i - 1] <= growth:
            return u[i]
    return None


def highest_level_within_sla(data):
    last = None
    for u, e in zip(data["users"], data["error_rate"]):
        if e > data["sla_error_pct"]:
            return last
        last = u
    return last


def first_level_over_sla(data):
    for u, e in zip(data["users"], data["error_rate"]):
        if e > data["sla_error_pct"]:
            return u
    return None


def q1(d):
    return first_plateau_level(d)


def q1_steps(d):
    u = q1(d)
    i = d["users"].index(u)
    t = d["throughput"]
    return [f"Compare each throughput point with the previous one (10-user steps); growth = (new - old) / old.",
            f"Growth up to {d['users'][i - 1]} users is above 2% at every step.",
            f"From {d['users'][i - 1]} to {u} users: ({t[i]} - {t[i - 1]}) / {t[i - 1]} = {(t[i] - t[i - 1]) / t[i - 1]:.1%}, which is 2% or less.",
            f"So throughput first stops growing by more than 2% at {u} users."]


def q2(d):
    a, b = d["avg_rt"][idx(d, 100)], d["avg_rt"][idx(d, 160)]
    return round((b - a) / a * 100, 1)


def q2_steps(d):
    a, b = d["avg_rt"][idx(d, 100)], d["avg_rt"][idx(d, 160)]
    return [f"Read average response time at 100 users: {a} ms; at 160 users: {b} ms.",
            f"Change = {b} - {a} = {round(b - a, 1)} ms.",
            f"Percentage increase = {round(b - a, 1)} / {a} x 100 = {q2(d)} percent."]


def q3(d):
    return highest_level_within_sla(d)


def q3_steps(d):
    u = q3(d)
    nxt = first_level_over_sla(d)
    e = d["error_rate"]
    return [f"The SLA line is at {d['sla_error_pct']} percent error rate.",
            f"Error rate at {u} users is {e[idx(d, u)]} percent, which is at or below the line.",
            f"Error rate at {nxt} users is {e[idx(d, nxt)]} percent, which is above the line.",
            f"So the highest level that still meets the SLA is {u} users."]


def q4(d):
    i = d["pct_levels"].index(120)
    return round(d["p99"][i] / d["p50"][i], 2)


def q4_steps(d):
    i = d["pct_levels"].index(120)
    return [f"In the grouped bars at 120 users, p99 = {d['p99'][i]} ms and p50 = {d['p50'][i]} ms.",
            f"Ratio = {d['p99'][i]} / {d['p50'][i]} = {q4(d)}."]


def q5(d):
    u = first_level_over_sla(d)
    return round(d["avg_rt"][idx(d, u)] / d["avg_rt"][idx(d, 10)], 2)


def q5_steps(d):
    u = first_level_over_sla(d)
    return [f"Find the first user level where the error rate is above the SLA line: {u} users (third chart).",
            f"Read average response time at {u} users: {d['avg_rt'][idx(d, u)]} ms (first chart).",
            f"Read average response time at 10 users: {d['avg_rt'][idx(d, 10)]} ms.",
            f"Ratio = {d['avg_rt'][idx(d, u)]} / {d['avg_rt'][idx(d, 10)]} = {q5(d)} times."]


QUESTIONS = [
    Question("lt-q01", "fig1_throughput_vs_response_time.png",
             "On the throughput line, at which number of virtual users does throughput first stop growing by more than 2 percent compared with the previous 10-user step?",
             "users", ["users"], 2, q1, q1_steps, 0.0, 0, ["trend"]),
    Question("lt-q02", "fig1_throughput_vs_response_time.png",
             "By what percentage does the average response time (right axis, in ms) increase between 100 users and 160 users? Give the answer in percent to one decimal place.",
             "percent", ["percent", "%"], 2, q2, q2_steps, 0.03, 1, ["calculation"]),
    Question("lt-q03", "fig3_error_rate_vs_users.png",
             "What is the highest user level, in steps of 10, at which the error rate is still at or below the 1 percent SLA line?",
             "users", ["users", "user level"], 1, q3, q3_steps, 0.0, 0, ["threshold"]),
    Question("lt-q04", "fig2_response_time_percentiles.png",
             "At 120 users, how many times larger is the p99 response time than the p50 response time? Give the ratio to two decimal places.",
             "ratio", ["ratio", "times"], 2, q4, q4_steps, 0.03, 2, ["comparison"]),
    Question("lt-q05", "fig1_throughput_vs_response_time.png + fig3_error_rate_vs_users.png",
             "Using the error-rate chart, find the first user level at which the error rate is above the 1 percent SLA line. How many times larger is the average response time at that level than at 10 users? Give the ratio to two decimal places.",
             "ratio", ["ratio", "times"], 3, q5, q5_steps, 0.03, 2, ["combined series"]),
]


def peak_throughput_level(d):
    t = d["throughput"]
    return d["users"][t.index(max(t))]


# Deliberately fragile: throughput is flat after ~120 users, so the "peak" depends on tiny reading differences.
FRAGILE_EXAMPLE = Question(
    "lt-fragile", "fig1_throughput_vs_response_time.png",
    "At how many users is throughput at its highest point? Answer in users.",
    "users", ["users"], 2, peak_throughput_level,
    lambda d: ["Find the highest point of the throughput line."], 0.0, 0, ["demo: should be flagged"])
