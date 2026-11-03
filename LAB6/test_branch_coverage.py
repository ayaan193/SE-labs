"""Branch coverage: independently exercise decisions and their boundaries."""

import pytest

from laundry_service import (
    dropoff_status,
    extra_weight_charge,
    order_acceptable,
)


@pytest.mark.parametrize("garment", ["silk", "", None])
def test_unknown_garment_branch(garment):
    with pytest.raises(ValueError, match="^unknown garment type$"):
        extra_weight_charge(garment, 0, "standard", False)


@pytest.mark.parametrize("weight", [-0.01, -1, -100])
def test_negative_weight_branch(weight):
    with pytest.raises(ValueError, match="^invalid weight$"):
        extra_weight_charge("regular", weight, "standard", False)


def test_garment_validation_precedes_weight_validation():
    with pytest.raises(ValueError, match="^unknown garment type$"):
        extra_weight_charge("silk", -1, "standard", False)


@pytest.mark.parametrize(
    "garment, member, expected",
    [
        ("regular", False, 90),
        ("regular", True, 30),
        ("delicate", False, 150),
        ("delicate", True, 90),
        ("bedding", False, 0),
        ("bedding", True, 0),
    ],
)
def test_membership_condition_combinations(garment, member, expected):
    # Covers both short-circuit outcomes and the bedding membership exception.
    assert extra_weight_charge(garment, 8, "standard", member) == expected


@pytest.mark.parametrize(
    "garment, member, allowance",
    [
        ("regular", False, 5),
        ("regular", True, 7),
        ("delicate", False, 3),
        ("delicate", True, 5),
        ("bedding", False, 8),
        ("bedding", True, 8),
    ],
)
@pytest.mark.parametrize("extra, expected", [(-0.5, 0), (0, 0), (0.5, 15)])
def test_included_weight_boundary(garment, member, allowance, extra, expected):
    assert extra_weight_charge(
        garment, allowance + extra, "standard", member
    ) == expected


@pytest.mark.parametrize(
    "weight, speed, expected",
    [
        (0, "standard", 0),
        (5.5, "standard", 15),
        (5.5, "express", 25),
        (15, "standard", 300),
        (15, "express", 500),
        (15.5, "standard", 472.5),
        (15.5, "express", 787.5),
    ],
)
def test_rate_and_ten_extra_kilo_boundary(weight, speed, expected):
    # Exactly ten extra kg has no surcharge; above ten applies it to all extra kg.
    assert extra_weight_charge("regular", weight, speed, False) == pytest.approx(
        expected
    )


@pytest.mark.parametrize(
    "weight, items, expected",
    [(1, 4, True), (1, 5, True), (1, 6, False), (100, 5, True)],
)
def test_delicate_item_limit_and_weight_bypass(weight, items, expected):
    # Current specification checks only item count for delicate orders.
    assert order_acceptable(weight, items, True) is expected


@pytest.mark.parametrize(
    "weight, items, expected",
    [
        (24.99, 39, True),
        (24.99, 40, True),
        (24.99, 41, False),
        (25, 39, True),
        (25, 40, True),
        (25, 41, False),
        (25.01, 39, False),
        (25.01, 40, False),
        (25.01, 41, False),
    ],
)
def test_regular_weight_and_item_boundaries(weight, items, expected):
    assert order_acceptable(weight, items, False) is expected


@pytest.mark.parametrize(
    "bedding, express, cutoff",
    [(False, False, 60), (False, True, 90), (True, False, 90), (True, True, 120)],
)
@pytest.mark.parametrize(
    "offset, expected",
    [(1, "accepted"), (0, "accepted"), (-1, "late"), (-20, "late"), (-21, "rejected")],
)
def test_all_dropoff_decisions_and_cutoff_boundaries(
    bedding, express, cutoff, offset, expected
):
    assert dropoff_status(cutoff + offset, bedding, express) == expected
