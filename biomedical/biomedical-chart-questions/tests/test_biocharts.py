import json
import math
import os
import statistics

import numpy as np
import pytest

from biocharts.ambiguity import check_question, robustness
from biocharts.charts import draw_all
from biocharts.cli import main
from biocharts.data import build_data
from biocharts.questions import FRAGILE_EXAMPLES, QUESTIONS
from biocharts.stats import linear_fit

D = build_data()
BY_ID = {q.id: q for q in QUESTIONS}


def test_data_reproducible_and_group_sizes():
    assert build_data(21) == build_data(21) and build_data(21) != build_data(22)
    assert len(D["patient_dose"]) == len(D["patient_reduction"]) == 150
    assert D["patient_dose"].count(20) == 30


def test_group_statistics_are_computed_correctly():
    for i, dose in enumerate(D["doses"]):
        vals = [r for d, r in zip(D["patient_dose"], D["patient_reduction"]) if d == dose]
        assert D["group_mean"][i] == pytest.approx(statistics.mean(vals), abs=0.006)
        assert D["group_sd"][i] == pytest.approx(statistics.stdev(vals), abs=0.006)
        assert D["ci_half"][i] == pytest.approx(1.96 * statistics.stdev(vals) / math.sqrt(30), abs=0.006)


def test_linear_fit_matches_numpy():
    slope, intercept = linear_fit(D["patient_dose"], D["patient_reduction"])
    ref_slope, ref_intercept = np.polyfit(D["patient_dose"], D["patient_reduction"], 1)
    assert slope == pytest.approx(ref_slope) and intercept == pytest.approx(ref_intercept)


def test_q1_difference_of_means():
    assert BY_ID["bio-q01"].compute(D) == pytest.approx(D["group_mean"][3] - D["group_mean"][0], abs=0.06)


def test_q2_non_overlapping_intervals_independent_check():
    hi0 = D["group_mean"][0] + D["ci_half"][0]
    expected = [d for i, d in enumerate(D["doses"]) if i and (D["group_mean"][i] - D["ci_half"][i] > hi0)]
    assert BY_ID["bio-q02"].compute(D) == expected == [10, 20, 40]
    assert 5 not in expected  # the 5 mg interval overlaps the placebo interval


def test_q3_percentage_fall_and_q4_first_hour():
    a, b = D["hr_treatment"][2], D["hr_treatment"][6]
    assert BY_ID["bio-q03"].compute(D) == round((a - b) / a * 100)
    first = next(h for h, t, p in zip(D["hours"], D["hr_treatment"], D["hr_placebo"]) if p - t >= 10)
    assert BY_ID["bio-q04"].compute(D) == first == 4


def test_q5_slope_per_10mg_matches_numpy():
    ref = np.polyfit(D["patient_dose"], D["patient_reduction"], 1)[0] * 10
    assert BY_ID["bio-q05"].compute(D) == pytest.approx(ref, abs=0.06)


def test_every_question_has_steps_and_passes_ambiguity_check():
    for q in QUESTIONS:
        assert len(q.steps(D)) >= 2
        res = check_question(q, D)
        assert res["ok"], (q.id, res)


def test_error_bar_questions_state_what_the_bars_show():
    assert "95%" in BY_ID["bio-q02"].text


def test_fragile_demos_are_flagged_for_the_right_reasons():
    by = {q.id: check_question(q, D) for q in FRAGILE_EXAMPLES}
    assert any("sensitive" in f for f in by["bio-fragile-1"]["flags"])
    assert any("error bars" in f for f in by["bio-fragile-2"]["flags"])


def test_robustness_is_one_for_stable_question():
    assert robustness(BY_ID["bio-q04"], D, trials=50) == 1.0


def test_images_created_and_valid_png(tmp_path):
    names = draw_all(D, str(tmp_path))
    for n in names:
        path = os.path.join(tmp_path, n)
        assert open(path, "rb").read(8) == b"\x89PNG\r\n\x1a\n" and os.path.getsize(path) > 20000


def test_cli_end_to_end(tmp_path):
    assert main(["--images", str(tmp_path / "i"), "--out", str(tmp_path / "o"), "--data", str(tmp_path / "d")]) == 0
    answers = json.loads((tmp_path / "o" / "answers.json").read_text())
    assert [a["id"] for a in answers] == [q.id for q in QUESTIONS]
    assert (tmp_path / "d" / "group_summary.csv").exists()
