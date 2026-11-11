"""Lab 7 laundry input processing. Invalid input returns None."""

import math

GARMENTS = {"regular", "delicate", "bedding"}


def _nonnegative_number(text):
    """Parse a finite, nonnegative number; return None on invalid input."""
    try:
        value = float(text)
    except (ValueError, TypeError, OverflowError):
        return None
    return value if math.isfinite(value) and value >= 0 else None


def parse_order(text):
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    garment, raw_weight = text.split(":")
    garment = garment.strip().lower()
    weight = _nonnegative_number(raw_weight)
    if garment not in GARMENTS or weight is None:
        return None
    return garment.title(), weight


def weight_average(weights_csv):
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return None
    values = [_nonnegative_number(part) for part in weights_csv.split(",")]
    if any(value is None for value in values):
        return None
    # Divide first so even a list of very large finite weights can be averaged.
    try:
        average = math.fsum(value / len(values) for value in values)
    except OverflowError:
        return None
    return average if math.isfinite(average) else None


def payable_charge(text):
    if not isinstance(text, str) or text.count("|") != 1:
        return None
    raw_charge, raw_discount = text.split("|")
    charge = _nonnegative_number(raw_charge)
    discount = _nonnegative_number(raw_discount)
    if charge is None or discount is None:
        return None
    total = charge * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0.0)


def main():
    for heading, prompt, function in [
        ("parse_order", "Enter garment:weight in kg (e.g. regular:6): ", parse_order),
        ("weight_average", "Enter garment weights as CSV (e.g. 3,5,8): ", weight_average),
        ("payable_charge", "Enter charge|discount (e.g. 300|40): ", payable_charge),
    ]:
        print(f"==== Running {heading} ====")
        result = function(input(prompt))
        print("Invalid input" if result is None else f"Result: {result}")
        print()


if __name__ == "__main__":
    main()
