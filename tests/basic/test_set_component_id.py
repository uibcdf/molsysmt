"""Preserving scalar ID semantics through the owning native chemical forms."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys

puw = msm.pyunitwizard


@pytest.fixture(params=["standard", "nondefault"])
def component_policy(request):
    units = (
        ["nm", "ps", "elementary_charge"]
        if request.param == "standard"
        else ["pm", "fs", "coulomb"]
    )
    with puw.context(standard_units=units):

        def policy():
            return tuple(
                str(puw.get_unit(puw.standardize(puw.quantity(1, unit))))
                for unit in ("nm", "ps", "elementary_charge")
            )

        before = policy()
        yield
        assert policy() == before


@pytest.fixture(params=["molsys", "chemical_states", "dictionary"])
def target(request, component_policy):
    molsys = MolSys(n_atoms=3, n_components=2)
    msm.set(molsys, element="atom", component_index=[0, 0, 1])
    msm.set(
        molsys,
        element="component",
        component_id=["101", "W"],
        component_name=["head", "tail"],
        component_type=["small molecule", "water"],
    )
    if request.param == "molsys":
        return molsys
    if request.param == "chemical_states":
        return molsys.chemical_states
    return msm.convert(molsys.chemical_states, to_form="molsysmt.ChemicalStatesDict")


def _labels(target):
    return msm.get(
        target,
        element="component",
        component_id=True,
        component_name=True,
        component_type=True,
    )


@pytest.mark.parametrize("element", ["atom", "component"])
@pytest.mark.parametrize(
    "value", ["001", "custom", "1 nm", "all", 17, np.int64(7), None]
)
def test_scalar_component_ids_use_the_chemical_owner_contract(target, element, value):
    before = _labels(target)
    membership = msm.get(target, element="atom", component_index=True)
    msm.set(target, element=element, component_id=value)
    expected = None if value is None else str(value)
    after = _labels(target)
    assert after[0] == [expected, expected]
    assert after[1:] == before[1:]
    assert msm.get(target, element="atom", component_index=True) == membership


@pytest.mark.parametrize("element,selection", [("component", [1, 0]), ("atom", [2, 0])])
def test_component_id_vectors_follow_selection_order(target, element, selection):
    msm.set(
        target, element=element, selection=selection, component_id=["right", "left"]
    )
    assert _labels(target) == [
        ["left", "right"],
        ["head", "tail"],
        ["small molecule", "water"],
    ]


@pytest.mark.parametrize("value", [True, False, 1.5, np.bool_(True), float("nan")])
def test_invalid_component_ids_reject_without_changing_metadata(target, value):
    before = _labels(target)
    with pytest.raises(msm.ArgumentError) as refusal:
        msm.set(target, element="component", component_id=value)
    assert refusal.value.extra["argument"] == "component_id"
    assert _labels(target) == before


@pytest.mark.parametrize("element", ["atom", "component"])
def test_empty_component_id_assignment_is_a_validated_noop(target, element):
    before = _labels(target)
    msm.set(target, element=element, selection=[], component_id="untouched")
    assert _labels(target) == before
