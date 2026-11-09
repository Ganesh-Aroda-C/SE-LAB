"""Highway Toll Application (Lab 7 - Hardened against Fuzz Testing Defects).

Provides vehicle plate parsing, trip cost calculation, and axle classification
with robust defensive input validation.
"""


def parse_plate(plate):
    """Parse vehicle registration plate into (state, district, number).

    Format: STATE-DISTRICT-SERIES-NUMBER (e.g., 'KA-05-AB-1234')
    Returns: (state, district, number) tuple on success, or None on invalid input.
    """
    if not isinstance(plate, str):
        return None

    cleaned = plate.strip()
    parts = cleaned.split("-")
    if len(parts) != 4:
        return None

    state, district_str, series, number_str = parts

    # State should be 2 uppercase alphabetic characters
    if len(state) != 2 or not state.isalpha():
        return None

    # District must be numeric and non-negative
    if not district_str.isdigit():
        return None
    district = int(district_str)
    if district < 0:
        return None

    # Series should be 1-3 alphanumeric characters
    if not (1 <= len(series) <= 3 and series.isalnum()):
        return None

    # Number must be numeric and positive (1 to 4 digits)
    if not number_str.isdigit():
        return None
    number = int(number_str)
    if number <= 0:
        return None

    return state.upper(), district, number


def trip_cost(text):
    """Calculate trip cost based on 'countxrate' format (e.g., '3x150').

    Returns: Total cost as non-negative integer, or None on invalid input.
    """
    if not isinstance(text, str):
        return None

    cleaned = text.lower().strip()
    parts = cleaned.split("x")
    if len(parts) != 2:
        return None

    count_str, rate_str = parts[0].strip(), parts[1].strip()
    if not count_str.isdigit() or not rate_str.isdigit():
        return None

    try:
        count = int(count_str)
        rate = int(rate_str)
    except (ValueError, OverflowError):
        return None

    if count < 0 or rate < 0:
        return None

    return count * rate


def axle_class(axles):
    """Classify vehicle based on axle count.

    Rules:
    - 2 axles: 'car'
    - 3-4 axles: 'truck'
    - >= 5 axles: 'heavy'
    - Invalid axles (< 2, non-integer, booleans, None): returns None
    """
    if axles is None or isinstance(axles, (bool, list, dict, set, tuple)):
        return None

    try:
        if isinstance(axles, float):
            if not axles.is_integer():
                return None
            n = int(axles)
        elif isinstance(axles, int):
            n = axles
        elif isinstance(axles, str):
            clean = axles.strip()
            # Reject non-integer strings, decimals, and negative signs
            if not clean.lstrip("-").isdigit():
                return None
            n = int(clean)
        else:
            return None
    except (ValueError, TypeError, OverflowError):
        return None

    if n < 2:
        return None
    if n == 2:
        return "car"
    if n <= 4:
        return "truck"
    return "heavy"


def main():
    """Interactive demo demonstrating functions with input validation."""
    print("==== Running parse_plate ====")
    user_input = input("Enter a plate (e.g. KA-05-AB-1234): ")
    result = parse_plate(user_input)
    print("State, District and Number:", result)

    print("\n==== Running trip_cost ====")
    user_input = input("Enter trips x rate (e.g. 3x150): ")
    result = trip_cost(user_input)
    print("Trip Cost:", result)

    print("\n==== Running axle_class ====")
    user_input = input("Enter an axle count (e.g. 3): ")
    result = axle_class(user_input)
    print("Vehicle Class:", result)


if __name__ == "__main__":
    main()
