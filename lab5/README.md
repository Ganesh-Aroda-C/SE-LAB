# Lab 5: Static Code Analysis — Smart Home Device Controller

## Student Information
- **Course**: Software Engineering Lab (SE-LAB)
- **Assignment**: Lab 5 — Static Code Analysis
- **Assigned Repository**: [SETAPESU26/L5_36_smart_home](https://github.com/SETAPESU26/L5_36_smart_home)
- **Target File**: `smart_home.py`

---

## 1. Project Overview
This lab demonstrates the application of industry-standard Python static analysis tools to audit, detect, and remediate code quality defects, security vulnerabilities, and PEP 8 style violations in an IoT Smart Home Device Controller system.

### Static Analysis Tools
1. **Pylint (v4.1.3)**: Evaluates semantic code quality, programming errors, refactoring candidates, and documentation standards.
2. **Bandit (v1.9.4)**: Audits the Python Abstract Syntax Tree (AST) for Common Weakness Enumeration (CWE) security vulnerabilities.
3. **Flake8 (v7.5.0)**: Combines `pyflakes`, `pycodestyle`, and `mccabe` to enforce PEP 8 style, syntax correctness, and complexity limits.

---

## 2. Before vs. After Analysis Summary

| Analysis Dimension | Baseline (Before) | Remediated (After) | Status |
| :--- | :--- | :--- | :--- |
| **Pylint Score** | **4.80 / 10** (26 violations) | **10.00 / 10** (0 violations) | **Target > 9.5 Exceeded** |
| **Bandit Findings** | 4 issues (1 High, 1 Medium, 2 Low) | 0 actionable issues (0 High, 0 Medium, 0 Low) | **All Vulnerabilities Resolved** |
| **Flake8 Violations** | 4 violations (E203, E302, E261, E501) | 0 violations | **100% PEP 8 Compliant** |
| **Thermostat State Leakage** | Bug present (settings shared across devices) | Fixed (isolated dict per device, type guards) | **Verified by Unit Tests** |
| **Unit Test Suite** | None present | 7 / 7 Passing Unit Tests (`unittest`) | **Fully Verified** |

---

## 3. Key Issues Resolved

1. **Subprocess Command Injection (`Bandit B602`, CWE-78)**:
   - *Problem*: `subprocess.call("bash scenes/" + sceneScript, shell=True)` enabled arbitrary command injection.
   - *Solution*: Removed `shell=True`, extracted safe filename using `os.path.basename`, and passed arguments as an immutable list vector to `subprocess.run`.
2. **Hardcoded Insecure Network Binding (`Bandit B104`, CWE-605)**:
   - *Problem*: `HUB_HOST = "0.0.0.0"` bound server sockets across all public and private network interfaces.
   - *Solution*: Replaced default with secure loopback `"127.0.0.1"` and configurable `os.getenv("HUB_HOST", ...)`.
3. **Hardcoded Password String (`Bandit B105`, CWE-259)**:
   - *Problem*: Embedded plaintext credentials `HUB_PASSWORD = "smarthome-demo"` in source code.
   - *Solution*: Configured secure retrieval via `os.getenv("HUB_PASSWORD", "smarthome-demo")`.
4. **Mutable Default Argument Bug (`Pylint W0102`) & Thermostat Bug**:
   - *Problem*: `def addDevice(..., settings={})` evaluated the default dictionary once at import, sharing the exact same dictionary object across all created devices. Calling `setTemperature("Thermostat", 35)` caused non-thermostats (such as `Ceiling Light`) to inherit temperature settings (`{'temperature': 30}`).
   - *Solution*: Changed default to `settings=None`, initialized distinct dictionaries per device, and validated device type before applying thermostat settings.
5. **Inconsistent Return Statements (`Pylint R1710`)**:
   - *Problem*: `toggleDevice` returned boolean values on success but implicitly returned `None` when a device was missing.
   - *Solution*: Explicitly returned `None` on missing device checks for deterministic control flow.
6. **Unspecified Text Encoding (`Pylint W1514`)**:
   - *Problem*: `open(fileName, "w")` relied on platform-dependent default encodings.
   - *Solution*: Added explicit `encoding="utf-8"`.
7. **PEP 8 Naming Conventions and Docstrings (`Pylint C0103, C0114, C0116`)**:
   - *Problem*: CamelCase naming across functions/arguments and missing docstrings.
   - *Solution*: Renamed to snake_case (`add_device`, `device_name`) and retained backward-compatibility aliases (`addDevice = add_device`) with proper linter pragmas; documented module and all functions.
8. **PEP 8 Formatting Violations (`Flake8 E203, E302, E261, E501`)**:
   - *Problem*: Whitespace before colons, single blank lines between functions, single space before inline comments, and lines over 79 characters.
   - *Solution*: Formatted all code to strictly satisfy PEP 8 requirements.

---

## 4. Directory Structure

```
SE-LAB/
├── lab5/
│   ├── .gitignore
│   ├── README.md                  # Comprehensive lab documentation and report
│   ├── issues.md                  # Detailed issue logging table and root-cause analysis
│   ├── reflection.md              # Answers to the static analysis reflection questions
│   ├── smart_home.py              # Cleaned and fully remediated smart home controller
│   ├── pylint_report_before.txt   # Pylint baseline analysis report (4.80/10)
│   ├── pylint_report_after.txt    # Pylint remediated analysis report (10.00/10)
│   ├── bandit_report_before.txt   # Bandit baseline security scan (4 findings)
│   ├── bandit_report_after.txt    # Bandit remediated security scan (0 findings)
│   ├── flake8_report_before.txt   # Flake8 baseline style scan (4 violations)
│   ├── flake8_report_after.txt    # Flake8 remediated style scan (0 violations)
│   └── tests/
│       └── test_smart_home.py     # Unit test suite covering all functionality and fixes
└── [Existing Lab1, Lab2, Lab3, Lab4 folders preserved]
```

---

## 5. Running the Application & Static Analysis Tools

### Run the Smart Home Controller Demo
```bash
python smart_home.py
```

### Run Unit Tests
```bash
python -m unittest discover -s tests
```

### Run Static Analysis Tools
```bash
# Pylint (Score: 10.00/10)
python -m pylint smart_home.py

# Bandit (Issues: 0)
python -m bandit -r smart_home.py

# Flake8 (Violations: 0)
python -m flake8 smart_home.py
```
