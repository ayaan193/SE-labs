"""Use PROCESSOR_MODULE=processor_original to reproduce original failures."""

import importlib
import math
import os

import pytest
from hypothesis import given, settings, strategies as st

app = importlib.import_module(os.environ.get("PROCESSOR_MODULE", "processor"))

arbitrary_input = st.one_of(
    st.none(), st.text(), st.booleans(), st.integers(), st.floats(),
    st.lists(st.integers(), max_size=5),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=3),
)
weights = st.floats(min_value=0, max_value=1_000_000, allow_nan=False, allow_infinity=False)


@settings(max_examples=300)
@given(arbitrary_input)
def test_parse_order_no_crash(value):
    result = app.parse_order(value)
    if result is not None:
        garment, weight = result
        assert garment in {"Regular", "Delicate", "Bedding"}
        assert math.isfinite(weight) and weight >= 0


@settings(max_examples=300)
@given(arbitrary_input)
def test_weight_average_no_crash(value):
    result = app.weight_average(value)
    assert result is None or (math.isfinite(result) and result >= 0)


@settings(max_examples=300)
@given(arbitrary_input)
def test_payable_charge_no_crash(value):
    result = app.payable_charge(value)
    assert result is None or (math.isfinite(result) and result >= 0)


@given(st.sampled_from(["regular", "delicate", "bedding"]), weights)
def test_parse_order_valid(garment, weight):
    assert app.parse_order(f" {garment.upper()} : {weight} ") == (garment.title(), weight)


@given(st.lists(weights, min_size=1, max_size=30))
def test_weight_average_valid(values):
    result = app.weight_average(",".join(map(str, values)))
    assert result == pytest.approx(sum(values) / len(values))
    assert min(values) <= result + 1e-8
    assert result <= max(values) + 1e-8


@given(weights, weights)
def test_payable_charge_valid(charge, discount):
    assert app.payable_charge(f"{charge}|{discount}") == pytest.approx(
        max(charge * 1.18 - discount, 0)
    )


@pytest.mark.parametrize(
    "function,value",
    [
        ("parse_order", None),
        ("parse_order", ""),
        ("parse_order", "regular:-1"),
        ("parse_order", "regular:nan"),
        ("parse_order", "regular:inf"),
        ("parse_order", "unknown:5"),
        ("weight_average", None),
        ("weight_average", ""),
        ("weight_average", "3,,5"),
        ("weight_average", "-1,5"),
        ("weight_average", "nan,5"),
        ("payable_charge", None),
        ("payable_charge", ""),
        ("payable_charge", "-10|2"),
        ("payable_charge", "300|nan"),
        ("payable_charge", "1e309|0"),
    ],
)
def test_invalid_inputs_are_rejected(function, value):
    assert getattr(app, function)(value) is None


def test_fractional_average_regression():
    assert app.weight_average("3,4") == 3.5
