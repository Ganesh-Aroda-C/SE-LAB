# Lab 6: Code and Branch Coverage Analysis — Highway Toll Application

## Student Details
- **Course**: Software Engineering Lab (SE-LAB)
- **Lab Assignment**: Lab 6 — Code and Branch Coverage Analysis
- **Assigned Repository**: [SETAPESU26/L6_L7_36_highway_toll](https://github.com/SETAPESU26/L6_L7_36_highway_toll)
- **Target Application**: `highway_toll.py`

---

## 1. Lab Objectives
- Understand the fundamental differences between line (code) coverage, branch coverage, and path coverage.
- Use `pytest` and Python's `coverage` tool to measure, evaluate, and enhance test completeness.
- Identify untested statements, conditional decisions, boundary values, and exception paths in legacy application code.
- Design comprehensive test suites that achieve at least 90% (up to 100%) line coverage and branch coverage without artificial inflation.

---

## 2. Highway Toll Application Overview (`highway_toll.py`)
The assigned application calculates toll fees on automated highway tollways based on:
1. **Axle Count**:
   - Valid count must be $\ge 2$; counts $< 2$ raise a `ValueError("invalid axle count")`.
   - 2 axles: Standard base toll = ₹100.
   - 3 axles: Standard base toll = ₹150.
   - 4 axles: Standard base toll = ₹250.
   - 5 or more axles: Default base toll = ₹400.
2. **Peak Hour Surcharges**:
   - `is_peak=True`: Adds a 25% surcharge (`base * 1.25`).
3. **FASTag Electronic Toll Collection Discounts**:
   - `has_fastag=True` on 2-axle vehicles: 10% discount (`base * 0.9`).
   - `has_fastag=True` on $>2$-axle vehicles: 5% discount (`base * 0.95`).
   - Output rounded to 2 decimal places (`round(base, 2)`).
4. **Emergency Vehicle Exemptions**:
   - Vehicles in `EXEMPT = ("ambulance", "fire_engine")` incur ₹0 charge.
5. **Monthly Pass Advisory (`pass_advice`)**:
   - Computes aggregate trip cost against monthly pass price.
   - Returns `"buy_pass"` if cost > pass price, `"either"` if cost == pass price, and `"pay_per_trip"` if cost < pass price.

---

## 3. Difference Between Code Coverage and Branch Coverage

| Metric | Definition | Limitation |
| :--- | :--- | :--- |
| **Line Coverage** | Measures the percentage of executable code statements executed at least once during test execution. | Can report high or 100% coverage while completely ignoring untested boolean branches, edge-case conditions, or unhandled logical states. |
| **Branch Coverage** | Measures whether every decision branch (both TRUE and FALSE outcomes) of each conditional structure (`if`, `else`, loop headers) has been traversed. | Requires testing both affirmative and negative execution paths, revealing subtle logic bugs, boundary weaknesses, and hidden defaults. |

---

## 4. Tools and Installation
- **Python**: 3.11+
- **pytest**: 9.2.0 (Testing framework)
- **coverage**: 7.17.2 (Coverage measurement engine)

### Installation
```bash
pip install coverage pytest
```

---

## 5. Initial Baseline vs. Code Coverage Results

### Baseline (Starter Test `test_highway_toll.py`)
- **Statements**: 28
- **Missed**: 15
- **Line Coverage**: **46%** (Untested: 7, 11, 13, 15-18, 25, 29-36)
- **Branch Coverage**: **39%** (18 branches, 5 partially covered)

### Code Coverage Test Suite (`CodeCoverageTest_highway_toll_application.py`)
- **Total Test Cases**: 17 tests (all passing)
- **Statements**: 28 (Application) + 70 (Test suite) = 98
- **Missed**: 0
- **Line Coverage**: **100%** (Exceeds 90% requirement)

### Execution Command
```bash
coverage run -m pytest CodeCoverageTest_highway_toll_application.py
coverage report -m
```

---

## 6. Code Coverage Terminal Output Screenshot
The terminal screenshot below confirms genuine execution of the test suite and 100% line coverage:

![Code Coverage](screenshots/code_coverage.png)

---

## 7. Test Case Summary (`CodeCoverageTest_highway_toll_application.py`)
1. `test_toll_for_invalid_axle_count_raises_value_error`: Axle counts < 2 (1, 0, -2) raise `ValueError`.
2. `test_toll_for_two_axles_standard_rate`: 2-axle base tariff ₹100.
3. `test_toll_for_three_axles_standard_rate`: 3-axle base tariff ₹150.
4. `test_toll_for_four_axles_standard_rate`: 4-axle base tariff ₹250.
5. `test_toll_for_five_or_more_axles_default_rate`: 5+ axles default tariff ₹400.
6. `test_toll_for_peak_hour_surcharges`: 25% peak hour surcharges across all axle tiers.
7. `test_toll_for_fastag_discount_two_axles`: 10% FASTag discount for 2-axle vehicles.
8. `test_toll_for_fastag_discount_multi_axles`: 5% FASTag discount for $>2$-axle vehicles.
9. `test_toll_for_combined_peak_and_fastag`: Combined peak surcharge + FASTag discount with rounding.
10. `test_toll_charge_exempt_vehicles`: Emergency vehicle exemption (ambulance, fire_engine -> ₹0).
11. `test_toll_charge_non_exempt_standard_vehicles`: Normal vehicles delegating to `toll_for`.
12. `test_toll_charge_non_exempt_invalid_axles_raises`: Non-exempt vehicles propagating `ValueError`.
13. `test_pass_advice_buy_pass`: Trip cost > pass price recommending `"buy_pass"`.
14. `test_pass_advice_either`: Trip cost == pass price recommending `"either"`.
15. `test_pass_advice_pay_per_trip`: Trip cost < pass price recommending `"pay_per_trip"`.
16. `test_pass_advice_empty_trips_list`: Empty trip schedule handling (zero cost).
17. `test_pass_advice_mixed_trips_scenario`: Multi-trip mixed peak and FASTag evaluation.
