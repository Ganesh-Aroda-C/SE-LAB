# Lab 5: Static Code Analysis — Smart Home Device Controller

## Student Details
- **Course**: Software Engineering Lab (SE-LAB)
- **Lab Assignment**: Lab 5 — Static Code Analysis
- **Assigned Repository**: [SETAPESU26/L5_36_smart_home](https://github.com/SETAPESU26/L5_36_smart_home)
- **Target File**: `smart_home.py`

---

## 1. Overview
This laboratory assignment focuses on static code analysis using three industry-standard Python tools:
1. **Pylint**: Evaluates code quality, conventions, potential bugs, docstrings, and design smells.
2. **Bandit**: Scans Python source code to detect security vulnerabilities and unsafe coding patterns.
3. **Flake8**: Enforces PEP 8 style guidelines, formatting, line length, and syntax correctness.

The assigned project is a Smart Home Device Controller system (`smart_home.py`) managing home appliances (lights, fans, thermostats, televisions), rooms, power usage calculations, and state persistence.

---

## 2. Baseline Static Analysis Reports
Before applying any fixes, the original code was analyzed using all three tools:
- `pylint_report_before.txt`: Initial score of **4.80/10** with 26 violations (missing docstrings, non-standard naming, mutable default arguments, inconsistent return statements, unspecified file encoding).
- `bandit_report_before.txt`: 4 issues flagged (1 High severity shell injection risk, 1 Medium severity network interface binding, 2 Low severity findings).
- `flake8_report_before.txt`: 4 PEP 8 style violations (E203 whitespace before colon, E302 missing blank lines, E261 inline comment spacing, E501 line length > 79 chars).

---

## 3. Plan of Execution
1. **Commit 1**: Add original codebase and initial static analysis baseline reports (`feat(lab5)`).
2. **Commit 2**: Fix critical Pylint warnings, mutable default argument bugs, thermostat state isolation, and all Bandit security vulnerabilities (`fix(lab5)`).
3. **Commit 3**: Fix all Flake8 PEP 8 styling issues, generate final verification reports, add comprehensive unit tests, and provide detailed issue and reflection documentation (`style(lab5)`).
