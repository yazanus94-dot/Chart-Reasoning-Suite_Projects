import json
import os

import pytest

from loadcharts.ambiguity import check_question, equivalent, robustness
from loadcharts.charts import draw_all
from loadcharts.cli import main
from loadcharts.data import build_data
from loadcharts.questions import FRAGILE_EXAMPLE, QUESTIONS, first_plateau_level

DATA = build_data()
BY_ID = {q.id: q for q in QUESTIONS}


def test_data_is_reproducible_and_well_formed():
    assert build_data(11) == build_data(11)
    assert build_data(11) != build_data(12)
    assert len(DATA["users"]) == len(DATA["throughput"]) == len(DATA["avg_rt"]) == len(DATA["error_rate"]) == 20


def test_q1_matches_independent_calculation():
    t, u = DATA["throughput"], DATA["users"]
    expected = next(u[i] for i in range(1, len(t)) if (t[i] - t[i - 1]) / t[i - 1] <= 0.02)
    assert BY_ID["lt-q01"].compute(DATA) == expected == first_plateau_level(DATA) == 130


def test_q2_percentage_change_matches_manual_formula():
    a = DATA["avg_rt"][DATA["users"].index(100)]
    b = DATA["avg_rt"][DATA["users"].index(160)]
    assert BY_ID["lt-q02"].compute(DATA) == pytest.approx((b - a) / a * 100, abs=0.06)


def test_q3_highest_level_within_sla():
    ok_levels = []
    for i, u in enumerate(DATA["users"]):
        if all(x <= 1.0 for x in DATA["error_rate"][: i + 1]):
            ok_levels.append(u)
    assert BY_ID["lt-q03"].compute(DATA) == max(ok_levels) == 120


def test_q4_and_q5_ratios():
    i = DATA["pct_levels"].index(120)
    assert BY_ID["lt-q04"].compute(DATA) == pytest.approx(DATA["p99"][i] / DATA["p50"][i], abs=0.006)
    assert BY_ID["lt-q04"].compute(DATA) == pytest.approx(3.75, abs=0.01)  # p99 = 3.0x avg, p50 = 0.8x avg
    assert BY_ID["lt-q05"].compute(DATA) > 1.0


def test_every_question_has_steps_and_states_its_unit():
    for q in QUESTIONS:
        assert len(q.steps(DATA)) >= 2
        assert any(w in q.text.lower() for w in q.unit_words), q.id


def test_all_shipped_questions_pass_the_ambiguity_check():
    for q in QUESTIONS:
        result = check_question(q, DATA)
        assert result["ok"], (q.id, result)


def test_fragile_question_is_flagged():
    result = check_question(FRAGILE_EXAMPLE, DATA)
    assert not result["ok"] and any("sensitive" in f for f in result["flags"])


def test_missing_unit_is_flagged():
    q = BY_ID["lt-q02"]
    bad = type(q)(**{**q.__dict__, "text": "How much does the response time change between 100 and 160 users?",
                     "unit_words": ["percent", "%"]})
    assert any("unit" in f for f in check_question(bad, DATA)["flags"])


def test_equivalence_rules():
    assert equivalent(100.0, 101.0, 0.02) and not equivalent(100.0, 110.0, 0.02)
    assert equivalent("a", "a", 0.0) and not equivalent(1, 2, 0.0)
    assert robustness(BY_ID["lt-q03"], DATA, trials=50) == 1.0


def test_images_are_created_and_are_real_png(tmp_path):
    names = draw_all(DATA, str(tmp_path))
    assert len(names) == 3
    for n in names:
        path = os.path.join(tmp_path, n)
        assert open(path, "rb").read(8) == b"\x89PNG\r\n\x1a\n" and os.path.getsize(path) > 20000


def test_cli_writes_all_outputs(tmp_path):
    code = main(["--images", str(tmp_path / "img"), "--out", str(tmp_path / "out"), "--data", str(tmp_path / "d")])
    assert code == 0
    answers = json.loads((tmp_path / "out" / "answers.json").read_text())
    assert len(answers) == 5 and all(a["steps"] for a in answers)
    assert (tmp_path / "out" / "questions.md").exists() and (tmp_path / "d" / "load_test_results.csv").exists()
