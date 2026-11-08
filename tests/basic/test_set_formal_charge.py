"""Protect the public formal-charge boundary and its chemical-state owner."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard


def policy_units():
    return tuple(
        str(puw.get_unit(puw.standardize(puw.quantity([1], unit))))
        for unit in ("nm", "ps", "elementary_charge")
    )


@pytest.fixture(params=["standard", "nondefault"])
def charge_policy(request):
    units = (
        ["nm", "ps", "elementary_charge"]
        if request.param == "standard"
        else ["pm", "fs", "coulomb"]
    )
    with puw.context(standard_units=units):
        before = policy_units()
        yield
        assert policy_units() == before


@pytest.fixture
def states(charge_policy):
    result = msm.ChemicalStates(n_atoms=3)
    result.append_state()
    msm.set(result, element="atom", formal_charge=[-1, 0, 1])
    return result


@pytest.mark.parametrize(
    "value",
    [
        1.5,
        -0.5,
        1.0,
        np.float64(2.5),
        float("nan"),
        float("inf"),
        np.bool_(True),
        "not a charge",
        {"count": 1},
        object(),
        True,
        [1.5],
        np.array(1.5),
    ],
)
def test_invalid_nonquantity_charge_has_public_diagnostic_and_no_mutation(
    states, value
):
    before = msm.get(states, element="atom", formal_charge=True)
    with pytest.raises(msm.ArgumentError) as refusal:
        msm.set(states, element="atom", selection=[0], formal_charge=value)
    assert refusal.value.extra["argument"] == "formal_charge"
    assert refusal.value.extra["caller"] == "molsysmt.basic.set.set"
    assert msm.get(states, element="atom", formal_charge=True) == before


@pytest.mark.parametrize("value", [2, np.int64(-2)])
def test_integer_scalar_charge_preserves_other_atoms(states, value):
    msm.set(states, element="atom", selection=[1], formal_charge=value)
    assert msm.get(states, element="atom", formal_charge=True) == [-1, int(value), 1]


def test_nullable_aligned_counts_preserve_selection_order(states):
    msm.set(states, element="atom", selection=[2, 0], formal_charge=[None, -2])
    assert msm.get(states, element="atom", formal_charge=True) == [-2, 0, None]
    msm.set(states, element="atom", selection=[2, 1], formal_charge=(1, pd.NA))
    assert msm.get(states, element="atom", formal_charge=True) == [-2, None, 1]


@pytest.mark.parametrize("unit", ["elementary_charge", "coulomb"])
def test_genuine_quantity_charge_is_converted_to_integer_counts(states, unit):
    value = puw.convert(puw.quantity([-2, 2], "elementary_charge"), to_unit=unit)
    msm.set(states, element="atom", selection=[2, 0], formal_charge=value)
    assert msm.get(states, element="atom", formal_charge=True) == [2, 0, -2]


def test_incompatible_quantity_units_reject_without_mutation(states):
    with pytest.raises(msm.ArgumentError):
        msm.set(
            states,
            element="atom",
            selection=[0],
            formal_charge=puw.quantity([1], "nm"),
        )
    assert msm.get(states, element="atom", formal_charge=True) == [-1, 0, 1]


def test_backend_failure_is_not_relabelled_as_invalid_input(states, monkeypatch):
    value = puw.quantity([1], "elementary_charge")
    original = puw.get_value

    def unavailable(quantity, *args, **kwargs):
        if quantity is value:
            raise RuntimeError("unit backend unavailable")
        return original(quantity, *args, **kwargs)

    monkeypatch.setattr(puw, "get_value", unavailable)
    with pytest.raises(RuntimeError, match="unit backend unavailable"):
        msm.set(states, element="atom", selection=[0], formal_charge=value)
    assert msm.get(states, element="atom", formal_charge=True) == [-1, 0, 1]


def test_invalid_charge_preserves_evaluated_empty_analysis(charge_policy):
    system = MolSys(n_atoms=1)
    system.structures = Structures(coordinates=puw.quantity(np.zeros((2, 1, 3)), "nm"))
    msm.set(system, element="atom", formal_charge=-1)
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=1,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="test.formal_charge",
    )
    system.interactions = {"empty": analysis}
    with pytest.raises(msm.ArgumentError):
        msm.set(system, element="atom", formal_charge=1.5)
    assert system.interactions["empty"] is analysis
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1])
    assert msm.get(system, element="atom", formal_charge=True) == [-1]


def test_query_flag_keeps_its_boolean_contract(states):
    assert msm.get(states, element="atom", formal_charge=True) == [-1, 0, 1]
    with pytest.raises(msm.ArgumentError):
        msm.get(states, element="atom", formal_charge=1)
