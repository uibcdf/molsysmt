"""Reject unavailable bioassembly editing without an internal dispatch error."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import NotWithThisFormError
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard


def operation(unit="nm", scale=1):
    return {
        "chain_indices": [0],
        "rotations": np.repeat(np.eye(3)[None], 2, axis=0),
        "translations": puw.quantity(np.array([[0, 0, 0], [3, 0, 0]]) * scale, unit),
    }


@pytest.mark.parametrize("domain", ["structures", "molsys"])
@pytest.mark.parametrize("element", [None, "system"])
@pytest.mark.parametrize("scope", ["all", [1]])
@pytest.mark.parametrize("replacement", ["none", "empty", "named"])
def test_unavailable_bioassembly_set_is_typed_and_preserves_the_source(
    domain, element, scope, replacement
):
    structures = Structures(
        coordinates=puw.quantity(np.arange(12).reshape(2, 2, 3), "nm"),
        time=puw.quantity([2, 5], "ps"),
        bioassembly={"original": operation()},
    )
    target = (
        structures
        if domain == "structures"
        else MolSys._from_partial_domains(structures=structures)
    )
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=2,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="synthetic.bioassembly-availability",
    )
    if domain == "molsys":
        target.interactions = {"keep": analysis}
    original_xyz = structures._coordinates
    original_metadata = structures.bioassembly
    value = (
        None
        if replacement == "none"
        else {}
        if replacement == "empty"
        else {"new": operation("pm", 1000)}
    )
    with pytest.raises(NotWithThisFormError):
        msm.set(target, element=element, structure_indices=scope, bioassembly=value)
    assert structures.bioassembly is original_metadata
    assert structures._coordinates is original_xyz and structures.n_structures == 2
    np.testing.assert_array_equal(puw.get_value(structures.time, to_unit="ps"), [2, 5])
    if domain == "molsys":
        assert target.interactions["keep"] is analysis
        np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1])


@pytest.mark.parametrize("unit,scale", [("nm", 1), ("pm", 1000)])
def test_constructor_and_getter_keep_named_operation_units(unit, scale):
    declared = {"two-copies": operation(unit, scale)}
    saved = deepcopy(declared)
    structures = Structures(bioassembly=declared)
    result = msm.get(structures, bioassembly=True)
    assert list(result) == ["two-copies"]
    np.testing.assert_array_equal(result["two-copies"]["chain_indices"], [0])
    np.testing.assert_array_equal(
        result["two-copies"]["rotations"], saved["two-copies"]["rotations"]
    )
    np.testing.assert_allclose(
        puw.get_value(result["two-copies"]["translations"], to_unit="nm"),
        [[0, 0, 0], [3, 0, 0]],
        rtol=0,
        atol=1e-14,
    )
