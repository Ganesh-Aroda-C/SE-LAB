BASE_TOLL = {2: 100, 3: 150, 4: 250}
EXEMPT = ("ambulance", "fire_engine")


def toll_for(axles, is_peak, has_fastag):
    if axles < 2:
        raise ValueError("invalid axle count")
    if axles in BASE_TOLL:
        base = BASE_TOLL[axles]
    else:
        base = 400
    if is_peak:
        base = base * 1.25
    if has_fastag:
        if axles == 2:
            base = base * 0.9
        else:
            base = base * 0.95
    return round(base, 2)


def toll_charge(vehicle, axles, is_peak, has_fastag):
    if vehicle in EXEMPT:
        return 0
    return toll_for(axles, is_peak, has_fastag)


def pass_advice(trips, axles, pass_price):
    cost = 0
    for is_peak, has_fastag in trips:
        cost += toll_for(axles, is_peak, has_fastag)
    if cost > pass_price:
        return "buy_pass"
    if cost == pass_price:
        return "either"
    return "pay_per_trip"
