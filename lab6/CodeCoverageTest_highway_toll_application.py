"""Code Coverage Test Suite for Highway Toll Application.

Course: Software Engineering Lab (SE-LAB)
Lab: Lab 6 - Code and Branch Coverage Analysis
Target Module: highway_toll.py
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice, BASE_TOLL, EXEMPT


# ============================================================================
# 1. Tests for toll_for() - Core Toll Calculation by Axles, Peak, and FASTag
# ============================================================================

def test_toll_for_invalid_axle_count_raises_value_error():
    """Verify that axle count less than 2 raises a ValueError."""
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)

    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(0, True, True)

    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(-2, False, False)


def test_toll_for_two_axles_standard_rate():
    """Verify standard rate calculation for 2-axle vehicles."""
    assert toll_for(2, is_peak=False, has_fastag=False) == 100
    assert BASE_TOLL[2] == 100


def test_toll_for_three_axles_standard_rate():
    """Verify standard rate calculation for 3-axle vehicles."""
    assert toll_for(3, is_peak=False, has_fastag=False) == 150
    assert BASE_TOLL[3] == 150


def test_toll_for_four_axles_standard_rate():
    """Verify standard rate calculation for 4-axle vehicles."""
    assert toll_for(4, is_peak=False, has_fastag=False) == 250
    assert BASE_TOLL[4] == 250


def test_toll_for_five_or_more_axles_default_rate():
    """Verify default rate calculation for vehicles with 5+ axles."""
    assert toll_for(5, is_peak=False, has_fastag=False) == 400
    assert toll_for(6, is_peak=False, has_fastag=False) == 400
    assert toll_for(10, is_peak=False, has_fastag=False) == 400


def test_toll_for_peak_hour_surcharges():
    """Verify 25% surcharge during peak hours across axle categories."""
    # 2 axles: 100 * 1.25 = 125.0
    assert toll_for(2, is_peak=True, has_fastag=False) == 125.0
    # 3 axles: 150 * 1.25 = 187.5
    assert toll_for(3, is_peak=True, has_fastag=False) == 187.5
    # 4 axles: 250 * 1.25 = 312.5
    assert toll_for(4, is_peak=True, has_fastag=False) == 312.5
    # 5 axles: 400 * 1.25 = 500.0
    assert toll_for(5, is_peak=True, has_fastag=False) == 500.0


def test_toll_for_fastag_discount_two_axles():
    """Verify 10% FASTag discount specifically for 2-axle vehicles."""
    # 2 axles with FASTag: 100 * 0.9 = 90.0
    assert toll_for(2, is_peak=False, has_fastag=True) == 90.0


def test_toll_for_fastag_discount_multi_axles():
    """Verify 5% FASTag discount for vehicles with more than 2 axles."""
    # 3 axles with FASTag: 150 * 0.95 = 142.5
    assert toll_for(3, is_peak=False, has_fastag=True) == 142.5
    # 4 axles with FASTag: 250 * 0.95 = 237.5
    assert toll_for(4, is_peak=False, has_fastag=True) == 237.5
    # 5 axles with FASTag: 400 * 0.95 = 380.0
    assert toll_for(5, is_peak=False, has_fastag=True) == 380.0


def test_toll_for_combined_peak_and_fastag():
    """Verify cumulative calculation with peak surcharge and FASTag discount."""
    # 2 axles: 100 * 1.25 * 0.9 = 112.5
    assert toll_for(2, is_peak=True, has_fastag=True) == 112.5
    # 3 axles: 150 * 1.25 * 0.95 = 178.125 -> rounded to 178.12
    assert toll_for(3, is_peak=True, has_fastag=True) == 178.12
    # 4 axles: 250 * 1.25 * 0.95 = 296.875 -> rounded to 296.88
    assert toll_for(4, is_peak=True, has_fastag=True) == 296.88
    # 5 axles: 400 * 1.25 * 0.95 = 475.0
    assert toll_for(5, is_peak=True, has_fastag=True) == 475.0


# ============================================================================
# 2. Tests for toll_charge() - Vehicle Type Exemptions & Delegation
# ============================================================================

def test_toll_charge_exempt_vehicles():
    """Verify that exempt emergency vehicles incur zero toll charges."""
    assert "ambulance" in EXEMPT
    assert "fire_engine" in EXEMPT

    assert toll_charge("ambulance", 2, is_peak=False, has_fastag=False) == 0
    assert toll_charge("ambulance", 4, is_peak=True, has_fastag=True) == 0
    assert toll_charge("fire_engine", 3, is_peak=True, has_fastag=False) == 0
    assert toll_charge("fire_engine", 6, is_peak=False, has_fastag=True) == 0


def test_toll_charge_non_exempt_standard_vehicles():
    """Verify that regular non-exempt vehicles delegate to toll_for()."""
    assert toll_charge("car", 2, is_peak=False, has_fastag=False) == 100
    assert toll_charge("car", 2, is_peak=True, has_fastag=True) == 112.5
    assert toll_charge("bus", 3, is_peak=False, has_fastag=True) == 142.5
    assert toll_charge("truck", 4, is_peak=True, has_fastag=False) == 312.5
    assert toll_charge("trailer", 5, is_peak=False, has_fastag=False) == 400


def test_toll_charge_non_exempt_invalid_axles_raises():
    """Verify that non-exempt vehicle with invalid axles raises ValueError."""
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_charge("motorcycle", 1, is_peak=False, has_fastag=False)


# ============================================================================
# 3. Tests for pass_advice() - Monthly Pass Feasibility Evaluation
# ============================================================================

def test_pass_advice_buy_pass():
    """Verify 'buy_pass' advice when aggregate trip cost exceeds pass price."""
    # 2 trips for 2-axle off-peak: 100 + 100 = 200 > pass price 150
    trips = [(False, False), (False, False)]
    assert pass_advice(trips, axles=2, pass_price=150) == "buy_pass"


def test_pass_advice_either():
    """Verify 'either' advice when aggregate trip cost equals pass price."""
    # 1 trip for 2-axle off-peak: 100 == pass price 100
    trips = [(False, False)]
    assert pass_advice(trips, axles=2, pass_price=100) == "either"


def test_pass_advice_pay_per_trip():
    """Verify 'pay_per_trip' advice when aggregate trip cost is below pass price."""
    # 1 trip for 2-axle off-peak: 100 < pass price 180
    trips = [(False, False)]
    assert pass_advice(trips, axles=2, pass_price=180) == "pay_per_trip"


def test_pass_advice_empty_trips_list():
    """Verify pass advice when no trips are scheduled (zero cost)."""
    # 0 trips = cost 0 < pass price 100 -> pay_per_trip
    assert pass_advice([], axles=2, pass_price=100) == "pay_per_trip"
    # 0 trips = cost 0 == pass price 0 -> either
    assert pass_advice([], axles=2, pass_price=0) == "either"


def test_pass_advice_mixed_trips_scenario():
    """Verify pass advice with multiple mixed peak and FASTag trips."""
    trips = [
        (True, True),    # 178.12
        (False, True),   # 142.50
        (True, False),   # 187.50
    ]
    # Total cost = 178.12 + 142.50 + 187.50 = 508.12
    assert pass_advice(trips, axles=3, pass_price=500) == "buy_pass"
    assert pass_advice(trips, axles=3, pass_price=600) == "pay_per_trip"
