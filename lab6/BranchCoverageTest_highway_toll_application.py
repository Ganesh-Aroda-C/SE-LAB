"""Branch Coverage Test Suite for Highway Toll Application.

Course: Software Engineering Lab (SE-LAB)
Lab: Lab 6 - Code and Branch Coverage Analysis
Target Module: highway_toll.py

This test suite explicitly exercises both TRUE and FALSE outcomes for every
conditional statement and decision branch in the highway toll module.
"""

import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ============================================================================
# Branch 1: if axles < 2 (Line 6)
# ============================================================================

def test_branch_axles_less_than_two_true():
    """Branch Decision: axles < 2 -> TRUE (Raises ValueError)."""
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, is_peak=False, has_fastag=False)

    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(0, is_peak=True, has_fastag=True)

    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(-5, is_peak=False, has_fastag=False)


def test_branch_axles_less_than_two_false():
    """Branch Decision: axles < 2 -> FALSE (Proceeds to base calculation)."""
    # Boundary value: exactly 2 axles
    assert toll_for(2, is_peak=False, has_fastag=False) == 100


# ============================================================================
# Branch 2: if axles in BASE_TOLL (Line 8)
# ============================================================================

def test_branch_axles_in_base_toll_true():
    """Branch Decision: axles in BASE_TOLL -> TRUE (Lookup standard tariff)."""
    # 2 axles -> 100
    assert toll_for(2, is_peak=False, has_fastag=False) == 100
    # 3 axles -> 150
    assert toll_for(3, is_peak=False, has_fastag=False) == 150
    # 4 axles -> 250
    assert toll_for(4, is_peak=False, has_fastag=False) == 250


def test_branch_axles_in_base_toll_false():
    """Branch Decision: axles in BASE_TOLL -> FALSE (Fallback base = 400)."""
    # 5 axles -> default base 400
    assert toll_for(5, is_peak=False, has_fastag=False) == 400
    # 7 axles -> default base 400
    assert toll_for(7, is_peak=False, has_fastag=False) == 400


# ============================================================================
# Branch 3: if is_peak (Line 12)
# ============================================================================

def test_branch_is_peak_true():
    """Branch Decision: is_peak -> TRUE (Base multiplied by 1.25)."""
    # 2 axles peak: 100 * 1.25 = 125.0
    assert toll_for(2, is_peak=True, has_fastag=False) == 125.0
    # 5 axles peak: 400 * 1.25 = 500.0
    assert toll_for(5, is_peak=True, has_fastag=False) == 500.0


def test_branch_is_peak_false():
    """Branch Decision: is_peak -> FALSE (Base unmodified)."""
    # 2 axles non-peak: 100
    assert toll_for(2, is_peak=False, has_fastag=False) == 100
    # 5 axles non-peak: 400
    assert toll_for(5, is_peak=False, has_fastag=False) == 400


# ============================================================================
# Branch 4: if has_fastag (Line 14)
# ============================================================================

def test_branch_has_fastag_true():
    """Branch Decision: has_fastag -> TRUE (Discount evaluation branch)."""
    # Exercised via FASTag active
    assert toll_for(2, is_peak=False, has_fastag=True) == 90.0


def test_branch_has_fastag_false():
    """Branch Decision: has_fastag -> FALSE (No discount applied)."""
    # Exercised via FASTag inactive
    assert toll_for(2, is_peak=False, has_fastag=False) == 100
    assert toll_for(3, is_peak=False, has_fastag=False) == 150


# ============================================================================
# Branch 5: if axles == 2 (Nested inside has_fastag, Line 15)
# ============================================================================

def test_branch_fastag_axles_equals_two_true():
    """Branch Decision: has_fastag AND axles == 2 -> TRUE (10% discount)."""
    # 100 * 0.9 = 90.0
    assert toll_for(2, is_peak=False, has_fastag=True) == 90.0
    # Peak + FASTag 2-axle: 100 * 1.25 * 0.9 = 112.5
    assert toll_for(2, is_peak=True, has_fastag=True) == 112.5


def test_branch_fastag_axles_equals_two_false():
    """Branch Decision: has_fastag AND axles == 2 -> FALSE (5% discount)."""
    # 3 axles: 150 * 0.95 = 142.5
    assert toll_for(3, is_peak=False, has_fastag=True) == 142.5
    # 4 axles: 250 * 0.95 = 237.5
    assert toll_for(4, is_peak=False, has_fastag=True) == 237.5
    # 5 axles (fallback base): 400 * 0.95 = 380.0
    assert toll_for(5, is_peak=False, has_fastag=True) == 380.0
    # Peak + FASTag multi-axle: 150 * 1.25 * 0.95 = 178.12
    assert toll_for(3, is_peak=True, has_fastag=True) == 178.12


# ============================================================================
# Branch 6: if vehicle in EXEMPT (Line 23)
# ============================================================================

def test_branch_vehicle_in_exempt_true():
    """Branch Decision: vehicle in EXEMPT -> TRUE (Returns 0)."""
    # Test 'ambulance'
    assert toll_charge("ambulance", 2, is_peak=False, has_fastag=False) == 0
    assert toll_charge("ambulance", 5, is_peak=True, has_fastag=True) == 0

    # Test 'fire_engine'
    assert toll_charge("fire_engine", 3, is_peak=True, has_fastag=False) == 0
    assert toll_charge("fire_engine", 4, is_peak=False, has_fastag=True) == 0


def test_branch_vehicle_not_in_exempt_false():
    """Branch Decision: vehicle in EXEMPT -> FALSE (Calls toll_for)."""
    # Test standard vehicle categories
    assert toll_charge("car", 2, is_peak=False, has_fastag=False) == 100
    assert toll_charge("bus", 3, is_peak=True, has_fastag=False) == 187.5
    assert toll_charge("truck", 4, is_peak=False, has_fastag=True) == 237.5
    assert toll_charge("van", 2, is_peak=True, has_fastag=True) == 112.5

    # Invalid axles on non-exempt vehicle propagates exception
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_charge("motorcycle", 1, is_peak=False, has_fastag=False)


# ============================================================================
# Branch 7: for is_peak, has_fastag in trips (Line 30)
# ============================================================================

def test_branch_trips_loop_entered():
    """Branch Decision: trips has items -> TRUE (Executes loop accumulation)."""
    trips = [(False, False), (True, False)]
    # Cost = 100 + 125 = 225
    assert pass_advice(trips, axles=2, pass_price=200) == "buy_pass"


def test_branch_trips_loop_bypassed():
    """Branch Decision: trips is empty -> FALSE (Loop body skipped, cost = 0)."""
    # Cost = 0 < 50 -> pay_per_trip
    assert pass_advice([], axles=2, pass_price=50) == "pay_per_trip"
    # Cost = 0 == 0 -> either
    assert pass_advice([], axles=2, pass_price=0) == "either"


# ============================================================================
# Branch 8: if cost > pass_price (Line 32)
# ============================================================================

def test_branch_cost_greater_than_pass_price_true():
    """Branch Decision: cost > pass_price -> TRUE (Returns 'buy_pass')."""
    # 2 trips of 100 = 200 > 150
    trips = [(False, False), (False, False)]
    assert pass_advice(trips, axles=2, pass_price=150) == "buy_pass"


def test_branch_cost_greater_than_pass_price_false():
    """Branch Decision: cost > pass_price -> FALSE (Proceeds to cost == pass_price)."""
    # 1 trip of 100 <= 100
    trips = [(False, False)]
    assert pass_advice(trips, axles=2, pass_price=100) != "buy_pass"


# ============================================================================
# Branch 9: if cost == pass_price (Line 34)
# ============================================================================

def test_branch_cost_equals_pass_price_true():
    """Branch Decision: cost == pass_price -> TRUE (Returns 'either')."""
    # 1 trip of 100 == pass_price 100
    trips = [(False, False)]
    assert pass_advice(trips, axles=2, pass_price=100) == "either"


def test_branch_cost_equals_pass_price_false():
    """Branch Decision: cost == pass_price -> FALSE (Returns 'pay_per_trip')."""
    # 1 trip of 100 < pass_price 150 -> returns 'pay_per_trip'
    trips = [(False, False)]
    assert pass_advice(trips, axles=2, pass_price=150) == "pay_per_trip"
