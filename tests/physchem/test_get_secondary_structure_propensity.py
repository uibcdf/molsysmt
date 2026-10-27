"""Testing primary-reference lookup, form parity and strict group selection."""

import hashlib
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, UnknownGroupInTableError
from molsysmt.native import MolSys, Structures

RECEIPT = json.loads(
    (
        Path(__file__).parents[2]
        / "devtools/data/secondary_structure_propensity_review_20261026.json"
    ).read_text()
)["levitt_primary"]
NAMES = RECEIPT["amino_acid_order"]
REFERENCES = {
    "alpha_helix": RECEIPT["independent_visual_transcription"]["alpha_helix_levitt"],
    "beta_sheet": RECEIPT["independent_visual_transcription"]["beta_sheet_levitt"],
    "reverse_turn": RECEIPT["independent_visual_transcription"]["beta_turn_levitt"],
}


def named_groups(names):
    builder = msm.MolSysBuilder()
    for name in names:
        index = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([index], group_name=name)
    return builder.build()


@pytest.fixture(
    params=["molsysmt.MolSys", "molsysmt.Topology", "molsysmt.MolSysDict", "file"]
)
def reference_system(request, tmp_path):
    molsys = named_groups(NAMES)
    if request.param == "file":
        return msm.convert(molsys, to_form=str(tmp_path / "groups.h5msm"))
    return msm.convert(molsys, to_form=request.param)


@pytest.mark.parametrize("conformation", REFERENCES)
@pytest.mark.parametrize("selection", ["all", [19, 0, 19], [], 0])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_primary_values_forms_selections_and_unit_policy(
    reference_system, conformation, selection, length_unit
):
    reference = np.array(REFERENCES[conformation])
    expected = (
        reference
        if selection == "all"
        else reference[np.atleast_1d(selection).astype(int)]
    )
    with msm.pyunitwizard.context(standard_units=[length_unit, "ps", "radians"]):
        result = msm.physchem.get_secondary_structure_propensity(
            reference_system, conformation, selection=selection
        )
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64
    assert result.shape == (len(expected),)
    assert not msm.pyunitwizard.is_quantity(result)
    np.testing.assert_allclose(result, expected, rtol=0, atol=1e-14)


@pytest.mark.parametrize(
    "syntax,selection",
    [("MolSysMT", "group_index in [0, 14]"), ("MDTraj", "resid 0 14")],
)
def test_native_and_external_selection(reference_system, syntax, selection):
    if syntax == "MDTraj":
        pytest.importorskip("mdtraj")
    result = msm.physchem.get_secondary_structure_propensity(
        reference_system, "alpha_helix", syntax=syntax, selection=selection
    )
    np.testing.assert_array_equal(result, [1.29, 0.56])


@pytest.mark.parametrize("name", ["MSE", "SEP", "HID", "ACE", "NME", "DUM", "X", "LIG"])
def test_unsupported_groups_fail_without_parent_or_zero_mapping(name):
    with pytest.raises(UnknownGroupInTableError):
        msm.physchem.get_secondary_structure_propensity(
            named_groups([name]), "alpha_helix"
        )


@pytest.mark.parametrize("element", ["atom", "system", "chain", "molecule"])
def test_unsupported_population_precedes_selection(element):
    with pytest.raises(ArgumentChoiceError, match="element"):
        msm.physchem.get_secondary_structure_propensity(
            named_groups(["ALA"]),
            "alpha_helix",
            element=element,
            selection="invalid !!!!!",
        )


@pytest.mark.parametrize(
    "argument, value",
    [
        ("conformation", None),
        ("conformation", 3),
        ("conformation", []),
        ("conformation", "coil"),
        ("conformation", "helix"),
        ("definition", None),
        ("definition", 3),
        ("definition", "levitt"),
        ("definition", "chou_1978"),
    ],
)
def test_public_argument_validation(argument, value):
    kwargs = {"conformation": "alpha_helix", argument: value}
    with pytest.raises(msm.ArgumentError, match=argument):
        msm.physchem.get_secondary_structure_propensity(named_groups(["ALA"]), **kwargs)


@pytest.mark.parametrize("missing", [None, np.nan])
def test_missing_names_fail(missing):
    molsys = named_groups(["ALA"])
    molsys.topology.groups["group_name"] = [missing]
    with pytest.raises(msm.ArgumentError, match="names for every selected group"):
        msm.physchem.get_secondary_structure_propensity(molsys, "alpha_helix")


def test_coordinates_only_cannot_supply_group_identity():
    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    with pytest.raises(msm.ArgumentError, match="names for every selected group"):
        msm.physchem.get_secondary_structure_propensity(source, "alpha_helix")


def test_detached_results_and_source_integrity(reference_system):
    is_file = isinstance(reference_system, str)
    if is_file:
        before = hashlib.sha256(Path(reference_system).read_bytes()).digest()
    elif isinstance(reference_system, MolSys):
        atoms = reference_system.topology.atoms.copy(deep=True)
        groups = reference_system.topology.groups.copy(deep=True)
    result = msm.physchem.get_secondary_structure_propensity(
        reference_system, "alpha_helix"
    )
    result[:] = 0
    np.testing.assert_array_equal(
        msm.physchem.get_secondary_structure_propensity(
            reference_system, "alpha_helix"
        ),
        REFERENCES["alpha_helix"],
    )
    if is_file:
        assert hashlib.sha256(Path(reference_system).read_bytes()).digest() == before
    elif isinstance(reference_system, MolSys):
        pd.testing.assert_frame_equal(reference_system.topology.atoms, atoms)
        pd.testing.assert_frame_equal(reference_system.topology.groups, groups)


def test_ratios_are_not_clipped_or_class_probabilities():
    values = [
        msm.physchem.get_secondary_structure_propensity(
            named_groups(["ALA"]), category
        )[0]
        for category in REFERENCES
    ]
    np.testing.assert_array_equal(values, [1.29, 0.90, 0.77])
    assert sum(values) != 1


def test_optional_attribution_absence_and_failure_preserve_science(monkeypatch):
    from molsysmt import _ackredit

    molsys = named_groups(["ALA"])
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    baseline = msm.physchem.get_secondary_structure_propensity(molsys, "alpha_helix")

    def broken():
        raise RuntimeError("controlled provider failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = msm.physchem.get_secondary_structure_propensity(molsys, "alpha_helix")
    np.testing.assert_array_equal(result, baseline)


def test_real_attribution_reuses_enclosing_session_and_credits_empty_lookup():
    ackredit = pytest.importorskip("ackredit")
    molsys = named_groups(["ALA"])
    with ackredit.session("propensity references"):
        with ackredit.scope("consumer.describe_groups"):
            for category in REFERENCES:
                msm.physchem.get_secondary_structure_propensity(molsys, category)
            msm.physchem.get_secondary_structure_propensity(
                molsys, "alpha_helix", selection=[]
            )
        assert "levitt_1978" in ackredit.get_used_items()
        assert (
            "molsysmt.physchem.get_secondary_structure_propensity"
            in ackredit.current_session().usage_tree["consumer.describe_groups"][
                "children"
            ]
        )
    with ackredit.session("invalid lookup"):
        with pytest.raises(UnknownGroupInTableError):
            msm.physchem.get_secondary_structure_propensity(
                named_groups(["DUM"]), "alpha_helix"
            )
        assert not ackredit.get_used_items()
