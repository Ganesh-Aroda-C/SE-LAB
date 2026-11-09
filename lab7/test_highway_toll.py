"""Hypothesis Fuzz Testing Suite for Highway Toll Application.

Course: Software Engineering Lab (SE-LAB)
Lab: Lab 7 - Fuzz Testing for Input Validation Bugs
Target Module: processor.py (or highway_toll.py)
"""

import pytest
from hypothesis import given, strategies as st, settings, Verbosity
try:
    from processor import parse_plate, trip_cost, axle_class
except ImportError:
    from highway_toll import parse_plate, trip_cost, axle_class


# Define a broad strategy for arbitrary unexpected data types
any_unexpected_type = st.one_of(
    st.text(),
    st.integers(),
    st.floats(),
    st.booleans(),
    st.lists(st.integers()),
    st.dictionaries(st.text(), st.text()),
    st.none(),
)


# ============================================================================
# 1. Primary Handout Crash Detection Tests (Fuzzing with Text and None)
# ============================================================================

@given(st.text() | st.none())
def test_parse_plate_no_crash(s):
    """Property: parse_plate must handle arbitrary text or None without crashing.
    
    Expected behavior: Function should either return a valid 3-tuple (state, district, number)
    or return None / raise a controlled ValueError for invalid input, never crash with
    AttributeError, IndexError, or unhandled unpacking errors.
    """
    try:
        result = parse_plate(s)
        if result is not None:
            state, district, number = result
            assert isinstance(state, str)
            assert isinstance(district, int)
            assert isinstance(number, int)
    except ValueError:
        # Controlled validation error is acceptable
        pass
    except Exception as e:
        assert False, f"parse_plate crashed with unhandled exception: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_trip_cost_no_crash(s):
    """Property: trip_cost must handle arbitrary text or None without crashing.
    
    Expected behavior: Function should compute valid non-negative cost or return None /
    raise controlled ValueError, never crash with AttributeError or ValueError from unpack.
    """
    try:
        result = trip_cost(s)
        if result is not None:
            assert isinstance(result, int)
            assert result >= 0
    except ValueError:
        # Controlled validation error is acceptable
        pass
    except Exception as e:
        assert False, f"trip_cost crashed with unhandled exception: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_axle_class_no_crash(s):
    """Property: axle_class must handle arbitrary text or None without crashing.
    
    Expected behavior: Function should classify valid vehicle or return None / raise
    controlled ValueError, never crash with TypeError or unhandled int() parse failures.
    """
    try:
        result = axle_class(s)
        if result is not None:
            assert result in ("car", "truck", "heavy")
    except ValueError:
        # Controlled validation error is acceptable
        pass
    except Exception as e:
        assert False, f"axle_class crashed with unhandled exception: {type(e).__name__}: {e}"


# ============================================================================
# 2. Diverse Data Type Fuzzing (Integers, Floats, Lists, Dicts, Booleans)
# ============================================================================

@given(any_unexpected_type)
def test_parse_plate_diverse_types(val):
    """Verify parse_plate handles arbitrary Python types gracefully."""
    try:
        result = parse_plate(val)
        if result is not None:
            assert isinstance(result, tuple) and len(result) == 3
    except ValueError:
        pass
    except Exception as e:
        assert False, f"parse_plate failed on {type(val).__name__} with: {type(e).__name__}: {e}"


@given(any_unexpected_type)
def test_trip_cost_diverse_types(val):
    """Verify trip_cost handles arbitrary Python types gracefully."""
    try:
        result = trip_cost(val)
        if result is not None:
            assert isinstance(result, int) and result >= 0
    except ValueError:
        pass
    except Exception as e:
        assert False, f"trip_cost failed on {type(val).__name__} with: {type(e).__name__}: {e}"


@given(any_unexpected_type)
def test_axle_class_diverse_types(val):
    """Verify axle_class handles arbitrary Python types gracefully."""
    try:
        result = axle_class(val)
        if result is not None:
            assert result in ("car", "truck", "heavy")
    except ValueError:
        pass
    except Exception as e:
        assert False, f"axle_class failed on {type(val).__name__} with: {type(e).__name__}: {e}"


# ============================================================================
# 3. Boundary Values and Logical Invariant Fuzzing
# ============================================================================

@given(st.integers(min_value=-1000, max_value=1))
def test_axle_class_invalid_boundaries(axles):
    """Vehicles cannot have fewer than 2 axles; invalid axles must not classify as valid truck."""
    try:
        result = axle_class(axles)
        # Original buggy code returned 'truck' for negative/zero/one axles!
        assert result is None or result not in ("car", "truck", "heavy"), (
            f"Bug: axle_class({axles}) returned '{result}' for invalid axle count!"
        )
    except ValueError:
        # Controlled validation rejection is expected
        pass


@given(st.integers(min_value=-1000, max_value=-1), st.integers(min_value=-1000, max_value=-1))
def test_trip_cost_negative_inputs(count, rate):
    """Negative trips or rates must not produce negative costs."""
    text = f"{count}x{rate}"
    try:
        result = trip_cost(text)
        assert result is None or result >= 0, f"Bug: trip_cost({text}) produced negative: {result}"
    except ValueError:
        pass


# ============================================================================
# 4. Valid Input Property Preservation Fuzzing
# ============================================================================

@given(
    st.sampled_from(["KA", "MH", "DL", "TN", "KL"]),
    st.integers(min_value=1, max_value=99),
    st.sampled_from(["A", "AB", "CD", "ZZ"]),
    st.integers(min_value=1, max_value=9999),
)
def test_parse_plate_valid_format_preservation(state, district, series, number):
    """Verify that correctly formatted license plates are parsed accurately."""
    plate = f"{state}-{district:02d}-{series}-{number}"
    res = parse_plate(plate)
    assert res == (state.upper(), district, number)


@given(st.integers(min_value=1, max_value=1000), st.integers(min_value=1, max_value=1000))
def test_trip_cost_valid_multiplication(count, rate):
    """Verify that valid integer trip expressions compute exact multiplication."""
    text = f"{count}x{rate}"
    assert trip_cost(text) == count * rate


@given(st.integers(min_value=2, max_value=50))
def test_axle_class_valid_ranges(axles):
    """Verify vehicle classification rules for valid axle counts."""
    cls = axle_class(axles)
    if axles == 2:
        assert cls == "car"
    elif axles in (3, 4):
        assert cls == "truck"
    else:
        assert cls == "heavy"
