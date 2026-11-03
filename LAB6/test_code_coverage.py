"""Statement coverage: exercise every executable line of laundry_service."""

import pytest

from laundry_service import (
    dropoff_status,
    extra_weight_charge,
    order_acceptable,
)


def test_unknown_garment_is_rejected():
    with pytest.raises(ValueError, match="^unknown garment type$"):
        extra_weight_charge("leather", 2, "standard", False)


def test_negative_weight_is_rejected():
    with pytest.raises(ValueError, match="^invalid weight$"):
        extra_weight_charge("regular", -1, "standard", False)


def test_weight_inside_allowance_has_no_charge():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_membership_adds_two_kilos_for_delicates():
    assert extra_weight_charge("delicate", 5, "express", True) == 0


def test_standard_extra_weight_charge():
    assert extra_weight_charge("regular", 7, "standard", False) == 60


def test_express_extra_weight_charge():
    assert extra_weight_charge("regular", 7, "express", False) == 100


def test_fractional_extra_weight_charge():
    assert extra_weight_charge("regular", 5.5, "standard", False) == 15


def test_large_standard_order_uses_surcharge():
    # 16 - 5 = 11 extra kg; standard rate becomes 30 + 15.
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_large_express_order_uses_both_surcharges():
    # 16 - 5 = 11 extra kg; express rate becomes 50 + 15 + 10.
    assert extra_weight_charge("regular", 16, "express", False) == 825


def test_bedding_does_not_receive_membership_allowance():
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


@pytest.mark.parametrize(
    "weight, items, delicate, expected",
    [
        (3, 5, True, True),
        (3, 6, True, False),
        (26, 1, False, False),
        (25, 40, False, True),
        (10, 41, False, False),
    ],
)
def test_order_acceptance(weight, items, delicate, expected):
    assert order_acceptable(weight, items, delicate) is expected


@pytest.mark.parametrize(
    "minutes, bedding, express, expected",
    [
        (90, True, False, "accepted"),
        (90, False, True, "accepted"),
        (60, False, False, "accepted"),
        (45, False, False, "late"),
        (39, False, False, "rejected"),
    ],
)
def test_dropoff_outcomes(minutes, bedding, express, expected):
    assert dropoff_status(minutes, bedding, express) == expected
