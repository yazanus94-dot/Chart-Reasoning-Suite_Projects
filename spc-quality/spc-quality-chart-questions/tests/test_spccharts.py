import json
import os
import statistics

import pytest

from spccharts.ambiguity import check_question, equivalent, robustness
from spccharts.charts import draw_all
from spccharts.cli import main
from spccharts.data import build_data
from spccharts.questions import FRAGILE_EXAMPLES, QUESTIONS

D = build_data()
BY_ID = {q.id: q for q in QUESTIONS}


def test_data_reproducible_and_limits_use_the_baseline():
    assert build_data(31) == build_data(31) and build_data(31) != build_data(32)
    base = D["defect_rate"][:20]
    assert D["center"] == pytest.approx(statistics.mean(base), abs=0.001)
    assert D["sigma"] == pytest.approx(statistics.stdev(base), abs=0.001)
    assert D["ucl"] == pytest.approx(D["center"] + 3 * D["sigma"], abs=0.002)
    assert D["lcl"] == pytest.approx(D["center"] - 3 * D["sigma"], abs=0.002)


def test_baseline_is_in_control_and_one_point_breaks_the_limit():
    assert all(D["lcl"] < v < D["ucl"] for v in D["defect_rate"][:20])
    assert [d for d, v in zip(D["days"], D["defect_rate"]) if v > D["ucl"]] == [23]
    assert BY_ID["spc-q01"].compute(D) == 1


def test_q2_run_of_eight_matches_independent_loop():
    run, answer = 0, None
    for day, v in enumerate(D["defect_rate"], 1):
        run = run + 1 if v < D["center"] else 0
        if run == 8:
            answer = day
            break
    assert BY_ID["spc-q02"].compute(D) == answer == 31


def test_q3_and_q4_pareto():
    total = sum(D["counts"])
    assert total == 106
    cumulative = [sum(D["counts"][: i + 1]) / total for i in range(6)]
    assert BY_ID["spc-q03"].compute(D) == next(i + 1 for i, c in enumerate(cumulative) if c >= 0.8) == 3
    assert BY_ID["spc-q04"].compute(D) == round((48 + 31) / 106 * 100) == 75


def test_q5_cpk_matches_manual_formula():
    m, s = D["diam_mean"], D["diam_sd"]
    expected = round(min((50.15 - m) / (3 * s), (m - 49.85) / (3 * s)), 2)
    assert BY_ID["spc-q05"].compute(D) == expected
    assert expected == pytest.approx(0.93, abs=0.01)


def test_diameter_summary_matches_the_raw_data():
    assert D["diam_mean"] == pytest.approx(statistics.mean(D["diameters"]), abs=0.0006)
    assert D["diam_sd"] == pytest.approx(statistics.stdev(D["diameters"]), abs=0.0006)
    assert len(D["diameters"]) == 200


def test_every_shipped_question_is_robust_and_has_steps():
    for q in QUESTIONS:
        assert len(q.steps(D)) >= 2
        res = check_question(q, D)
        assert res["ok"], (q.id, res)


def test_q5_states_that_sd_is_the_sample_value():
    assert "sample standard deviation" in BY_ID["spc-q05"].text.lower()


def test_fragile_demos_flagged_for_the_right_reasons():
    by = {q.id: check_question(q, D) for q in FRAGILE_EXAMPLES}
    assert any("sensitive" in f for f in by["spc-fragile-1"]["flags"])
    assert any("sample or population" in f for f in by["spc-fragile-2"]["flags"])


def test_equivalence_and_robustness_helpers():
    assert equivalent(10.0, 10.3, 0.04) and not equivalent(10.0, 11.0, 0.04)
    assert equivalent(3, 3, 0.0) and not equivalent(3, 4, 0.0)
    assert robustness(BY_ID["spc-q01"], D, trials=50) == 1.0


def test_images_created_and_valid_png(tmp_path):
    names = draw_all(D, str(tmp_path))
    assert len(names) == 3
    for n in names:
        path = os.path.join(tmp_path, n)
        assert open(path, "rb").read(8) == b"\x89PNG\r\n\x1a\n" and os.path.getsize(path) > 20000


def test_cli_end_to_end(tmp_path):
    assert main(["--images", str(tmp_path / "i"), "--out", str(tmp_path / "o"), "--data", str(tmp_path / "d")]) == 0
    answers = json.loads((tmp_path / "o" / "answers.json").read_text())
    assert [a["id"] for a in answers] == [q.id for q in QUESTIONS]
    assert (tmp_path / "d" / "pareto.csv").exists()
