# Lab 7: Fuzz Testing for Input Validation Bugs

## Student Details
- **Course**: Software Engineering Lab (SE-LAB)
- **Lab Assignment**: Lab 7 — Fuzz Testing for Input Validation Bugs
- **Assigned Repository**: [SETAPESU26/L6_L7_36_highway_toll](https://github.com/SETAPESU26/L6_L7_36_highway_toll)
- **Destination Repository**: [Ganesh-Aroda-C/SE-LAB](https://github.com/Ganesh-Aroda-C/SE-LAB)
- **Target Application**: `processor.py` (and `highway_toll.py`)
- **Test Suite**: `test_processor.py` (and `test_highway_toll.py`)

---

## 1. Lab Objectives
- Explore **fuzz testing (fuzzing)** as an automated dynamic security and quality assurance technique.
- Utilize the **Hypothesis** property-based testing framework to generate diverse, unexpected, boundary, and malformed inputs.
- Uncover unhandled runtime crashes, type errors, unpacking defects, and domain logic vulnerabilities.
- Implement defensive programming and input validation to harden the application while strictly preserving all valid business logic.

---

## 2. Application Overview (`processor.py` / `highway_toll.py`)
The target application performs vehicle and toll management through three core functions:
1. `parse_plate(plate)`:
   - Parses license plates formatted as `STATE-DISTRICT-SERIES-NUMBER` (e.g. `KA-05-AB-1234`).
   - Returns a 3-tuple: `(state.upper(), int(district), int(number))`.
2. `trip_cost(text)`:
   - Computes trip charges from a `countxrate` format expression (e.g. `3x150`).
   - Returns total cost as `int(count) * int(rate)`.
3. `axle_class(axles)`:
   - Classifies vehicles based on axle count:
     - 2 axles $\rightarrow$ `'car'`
     - 3 to 4 axles $\rightarrow$ `'truck'`
     - $\ge 5$ axles $\rightarrow$ `'heavy'`

---

## 3. What is Fuzz Testing?
**Fuzz testing (or fuzzing)** is an automated dynamic testing technique that feeds pseudo-random, unexpected, malformed, or boundary-breaking data into software interfaces.
- **Why use fuzzing?**
  - Unit tests verify expected inputs based on developer assumptions ("testing what you think could go wrong").
  - Fuzzers explore the input space orthogonally to human bias, exposing defects developers never anticipated.
  - Detects unhandled crashes (`AttributeError`, `TypeError`), memory issues, injection vulnerabilities, and denial-of-service risks.

---

## 4. Introduction to Hypothesis
[Hypothesis](https://hypothesis.readthedocs.io/) is an industry-standard property-based testing library for Python.
- Instead of testing individual static examples, developers define **invariants (properties)** that must hold across all valid and invalid inputs.
- **Key Features**:
  - `st.*` Strategies: Generators for arbitrary text, integers, floats, booleans, collections, dictionaries, and nulls.
  - **Shrinking**: Automatically minimizes failing test inputs to find the smallest reproducible counterexample (e.g. `s=None` or `s=''`).
  - **Replay & Flaky Detection**: Persists failing examples in a local cache to prevent regressions.

---

## 5. Software Requirements & Setup
- Python 3.8+ (Tested on Python 3.11.9)
- `hypothesis`: 6.170.15
- `pytest`: 9.2.0

### Installation
```bash
python -m pip install hypothesis pytest
```

---

## 6. Execution Commands

### Run the Interactive Application
```bash
python processor.py
# or
python highway_toll.py
```

### Run Hypothesis Fuzz Tests
```bash
python -m pytest -v test_processor.py
# or
pytest -v
```

---

## 7. Defects Discovered via Fuzz Testing

Running Hypothesis against the original implementation uncovered 7 distinct failures:

| Bug # | Function | Failing Input | Failure Type | Root-Cause Analysis |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `parse_plate` | `None`, non-str | `AttributeError` | Unconditionally called `.split('-')` on `None`, crashing immediately. |
| **2** | `parse_plate` | `""`, `"KA05AB1234"` | `ValueError` | Direct tuple unpacking `state, district, series, number = ...` failed when parts $\ne 4$. |
| **3** | `parse_plate` | `"KA-XX-AB-1234"` | `ValueError` | Calling `int(district)` or `int(number)` failed on non-numeric strings. |
| **4** | `trip_cost` | `None`, non-str | `AttributeError` | Called `.lower()` on `None` without type validation. |
| **5** | `trip_cost` | `""`, `"3x"` | `ValueError` | Direct unpack on split tokens failed when `'x'` was missing or non-numeric. |
| **6** | `axle_class` | `None`, `[]`, `{}` | `TypeError` | Direct call `int(axles)` crashed on null or collection types. |
| **7** | `axle_class` | `0`, `-1`, `1` | **Logic Bug** | Condition `if n <= 4: return 'truck'` evaluated to True for non-positive axles, falsely classifying negative/zero axles as trucks. |

---

## 8. Defensive Fixes Implemented

The application was hardened defensively without altering original valid behavior:
1. **Type & Null Verification**: Added `isinstance()` checks across all functions; null, boolean, or unexpected collection types return `None` safely.
2. **Delimiter & Token Validation**: `parse_plate` strictly verifies that exactly 4 hyphen-delimited tokens exist, state is alphabetic, district is numeric, and registration number is numeric.
3. **Safe Numeric Conversion**: `trip_cost` verifies digits before converting to integers and rejects negative values.
4. **Domain Boundary Enforcement**: `axle_class` rejects axle counts $< 2$, booleans (`True/False`), and non-numeric types, ensuring invalid axles never classify as valid vehicles.

---

## 9. Final Testing Results

Rerunning `python -m pytest -v test_processor.py` against the remediated application achieves a **100% pass rate**:

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.2.0, pluggy-1.7.0
rootdir: C:\Users\gani4\OneDrive\Desktop\SE\SE-LAB\lab7
plugins: anyio-4.16.0, hypothesis-6.170.15, platformdirs-4.14.5
collected 11 items

test_processor.py::test_parse_plate_no_crash PASSED                      [  9%]
test_processor.py::test_trip_cost_no_crash PASSED                        [ 18%]
test_processor.py::test_axle_class_no_crash PASSED                       [ 27%]
test_processor.py::test_parse_plate_diverse_types PASSED                 [ 36%]
test_processor.py::test_trip_cost_diverse_types PASSED                   [ 45%]
test_processor.py::test_axle_class_diverse_types PASSED                  [ 54%]
test_processor.py::test_axle_class_invalid_boundaries PASSED             [ 63%]
test_processor.py::test_trip_cost_negative_inputs PASSED                 [ 72%]
test_processor.py::test_parse_plate_valid_format_preservation PASSED     [ 81%]
test_processor.py::test_trip_cost_valid_multiplication PASSED            [ 90%]
test_processor.py::test_axle_class_valid_ranges PASSED                   [100%]

============================= 11 passed in 0.97s ==============================
```

---

## 10. Terminal Screenshots

| Screenshot | Description | File Path |
| :--- | :--- | :--- |
| **Figure 1** | Original application execution with demo inputs | [`screenshots/01_original_application.png`](screenshots/01_original_application.png) |
| **Figure 2** | Initial Hypothesis fuzz test execution showing 7 failures | [`screenshots/02_initial_fuzz_failures.png`](screenshots/02_initial_fuzz_failures.png) |
| **Figure 3** | Fixed application execution with input validation | [`screenshots/03_fixed_application.png`](screenshots/03_fixed_application.png) |
| **Figure 4** | Final Hypothesis execution showing all 11 tests passing | [`screenshots/04_final_fuzz_tests.png`](screenshots/04_final_fuzz_tests.png) |

---

## 11. PDF Submission Document Reference
A comprehensive PDF report has been compiled and included:
- **File**: [`Lab7_Fuzz_Testing_Report.pdf`](Lab7_Fuzz_Testing_Report.pdf)
- Contains complete theoretical background, defect taxonomy, code diffs, all embedded execution screenshots, and concluding evaluation remarks.

---

## 12. Directory Structure

```
SE-LAB/
├── lab7/
│   ├── .gitignore
│   ├── README.md                      # Comprehensive Lab 7 documentation
│   ├── processor.py                   # Hardened application (also available as highway_toll.py)
│   ├── highway_toll.py                # Source-compatible application alias
│   ├── test_processor.py              # Hypothesis fuzz test suite (also as test_highway_toll.py)
│   ├── test_highway_toll.py           # Source-compatible test suite alias
│   ├── Lab7_Fuzz_Testing_Report.pdf   # Complete formal PDF submission document
│   └── screenshots/
│       ├── 01_original_application.png
│       ├── 02_initial_fuzz_failures.png
│       ├── 03_fixed_application.png
│       └── 04_final_fuzz_tests.png
└── [Preserved Lab1, Lab2, Lab3, Lab4, lab5, lab6]
```
