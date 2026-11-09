# Chart-Reasoning-Suite – Domain-Specific Question Sets for Chart Reasoning

## 👋 Overview

This repository provides three curated sets of chart-based questions for evaluating
and stress-testing chart reasoning across distinct domains: **Biomedical**,
**Load Testing**, and **SPC / Quality**.

Each set is stored as a standalone question collection of question–answer pairs
(or question-only prompts, depending on intended use). The suite is intended
for researchers, developers, and educators benchmarking or fine-tuning models
on domain-specific chart interpretation tasks.

## 📂 Repository Contents

| Folder | Domain | Description |
|--------|--------|-------------|
| `biomedical/` | Biomedical | Chart reasoning questions based on biomedical data, assays, and patient-related visualizations. |
| `loadtest/` | Load Testing | Questions involving load-testing metrics, performance graphs, and system behaviour charts. |
| `spc-quality/` | SPC / Quality | Questions centred on control charts, process capability, and quality-control visualizations. |
| `archive/` | – | Original ZIP archives (kept for provenance). |

## 🚀 How to Use

```bash
git clone https://github.com/yazanus94-dot/Chart-Reasoning-Suite_Projects.git
cd Chart-Reasoning-Suite_Projects
```

Each domain set is a self-contained project. Enter the domain folder you need,
install its requirements, and run its CLI to (re)generate the chart images and
the question/answer files:

```bash
# Biomedical
cd biomedical/biomedical-chart-questions
pip install -r requirements.txt
python -m biocharts.cli      # draws images/, writes output/questions.md + output/answers.json
python -m pytest -q          # 13 tests

# Load Testing
cd ../../loadtest/loadtest-chart-questions
pip install -r requirements.txt
python -m loadcharts.cli     # draws images/, writes output/questions.md + output/answers.json
python -m pytest -q          # 12 tests

# SPC / Quality
cd ../../spc-quality/spc-quality-chart-questions
pip install -r requirements.txt
python -m spccharts.cli      # draws images/, writes output/questions.md + output/answers.json
python -m pytest -q          # 12 tests
```

## 📝 Question Format

For each domain, the generated material lives in `output/`:

- `output/questions.md` — the chart-reading questions together with computed
  answers, step-by-step solutions, and an ambiguity check.
- `output/answers.json` — the machine-readable answer key.
- `images/` — the chart images the questions refer to.

All data is **synthetic (seeded)** — no real patient, employer, or client data
is used. Questions and answers are generated and verified by code.

## 📄 License

Each domain set ships with its own `LICENSE` file. See the `LICENSE` inside the
respective domain folder for details.
