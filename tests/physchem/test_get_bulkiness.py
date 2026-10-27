"""Reference-table parity and typed selection contracts for Zimmerman bulkiness."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, UnknownGroupInTableError

# Independent reference: AAindex1 ZIMJ680102 and official ProtScale, reviewed
# 2026-10-26. This checks table parity, not the original geometric derivation.
NAMES = "ALA ARG ASN ASP CYS GLN GLU GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL".split()
REFERENCE = np.array(
    [
        11.50,
        14.28,
        12.82,
        11.68,
        13.46,
        14.45,
        13.57,
        3.40,
        13.69,
        21.40,
        21.40,
        15.71,
        16.25,
        19.80,
        17.43,
        9.47,
        15.77,
        21.67,
        18.03,
        21.57,
    ]
)


def named_groups(names):
    builder = msm.MolSysBuilder()
    groups = []
    for index, name in enumerate(names):
        atom = builder.add_atom(atom_name="CA", atom_type="C", atom_id=str(index))
        groups.append(builder.add_group([atom], group_name=name, group_id=str(index)))
    builder.add_chain(groups, chain_id="A")
    return builder.build()


@pytest.fixture(
    params=["molsysmt.MolSys", "molsysmt.Topology", "molsysmt.MolSysDict", "file"]
)
def reference_system(request, tmp_path):
    molsys = named_groups(NAMES)
    if request.param == "file":
        return msm.convert(molsys, to_form=str(tmp_path / "groups.h5msm"))
    return msm.convert(molsys, to_form=request.param)


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("selection", ["all", [19, 0, 19], []])
def test_bulkiness_curation_and_configured_area_units(
    reference_system, length_unit, selection
):
    expected = REFERENCE if selection == "all" else REFERENCE[selection]
    with msm.pyunitwizard.context(standard_units=[length_unit, "ps", "radians"]):
        result = msm.physchem.get_bulkiness(reference_system, selection=selection)
        assert msm.pyunitwizard.is_quantity(result)
        assert result.shape == (len(expected),)
        assert (
            msm.pyunitwizard.get_unit(result) == msm.pyunitwizard.unit(length_unit) ** 2
        )
        values = msm.pyunitwizard.get_value(result, to_unit="angstrom**2")
        assert values.dtype.kind == "f"
        np.testing.assert_allclose(values, expected, rtol=0, atol=1e-12)
        np.testing.assert_allclose(
            msm.pyunitwizard.get_value(result, to_unit="nm**2"),
            expected / 100,
            rtol=0,
            atol=1e-12,
        )


@pytest.mark.parametrize(
    "syntax,selection", [("MolSysMT", "group_index in [0, 7]"), ("MDTraj", "resid 0 7")]
)
def test_bulkiness_external_and_native_selection(reference_system, syntax, selection):
    if syntax == "MDTraj":
        pytest.importorskip("mdtraj")
    result = msm.physchem.get_bulkiness(
        reference_system, selection=selection, syntax=syntax
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"), [11.5, 3.4]
    )


@pytest.mark.parametrize("name", ["MSE", "SEP", "HID", "ACE", "NME", "DUM", "X", "LIG"])
def test_bulkiness_rejects_unsupported_names_without_zero_or_parent_mapping(name):
    molsys = named_groups([name])
    with pytest.raises(UnknownGroupInTableError):
        msm.physchem.get_bulkiness(molsys)


@pytest.mark.parametrize("element", ["atom", "system", "chain", "molecule"])
def test_bulkiness_rejects_element_before_evaluating_selection(element):
    with pytest.raises(ArgumentChoiceError, match="element"):
        msm.physchem.get_bulkiness(
            named_groups(["ALA"]), element=element, selection="invalid !!!!!"
        )


@pytest.mark.parametrize("definition", ["other", None, 3])
def test_bulkiness_digests_definition(definition):
    with pytest.raises(msm.ArgumentError, match="definition"):
        msm.physchem.get_bulkiness(named_groups(["ALA"]), definition=definition)


def test_bulkiness_no_coordinates_no_mutation_and_detached_values():
    molsys = named_groups(["ALA", "GLY"])
    before_atoms = molsys.topology.atoms.copy(deep=True)
    before_groups = molsys.topology.groups.copy(deep=True)
    result = msm.physchem.get_bulkiness(molsys)
    pd.testing.assert_frame_equal(molsys.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(molsys.topology.groups, before_groups)
    result[0] *= 2
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            msm.physchem.get_bulkiness(molsys), to_unit="angstrom**2"
        ),
        [11.5, 3.4],
    )


def test_bulkiness_strict_lookup_does_not_change_legacy_dummy_policy():
    from molsysmt.physchem.groups._lookup import group_table_value

    assert group_table_value({}, "DUM") == 0.0
    with pytest.raises(UnknownGroupInTableError):
        group_table_value({}, "DUM", allow_placeholders=False)


def test_bulkiness_requires_group_names_in_coordinates_only_input():
    from molsysmt.native import Structures

    source = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    with pytest.raises(msm.ArgumentError, match="names for every selected group"):
        msm.physchem.get_bulkiness(source)


@pytest.mark.parametrize("missing_name", [None, np.nan])
def test_bulkiness_rejects_unassigned_group_names(missing_name):
    molsys = named_groups(["ALA"])
    molsys.topology.groups["group_name"] = [missing_name]
    with pytest.raises(msm.ArgumentError, match="names for every selected group"):
        msm.physchem.get_bulkiness(molsys)


def test_bulkiness_optional_attribution_absence_and_failure(monkeypatch):
    from molsysmt import _ackredit

    molsys = named_groups(["ALA"])
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    baseline = msm.physchem.get_bulkiness(molsys)

    def broken():
        raise RuntimeError("controlled provider failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = msm.physchem.get_bulkiness(molsys)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
        msm.pyunitwizard.get_value(baseline, to_unit="angstrom**2"),
    )


def test_bulkiness_real_attribution_reuses_session_and_credits_empty_calls():
    ackredit = pytest.importorskip("ackredit")
    molsys = named_groups(["ALA"])
    with ackredit.session("bulkiness references"):
        with ackredit.scope("consumer.describe_groups"):
            msm.physchem.get_bulkiness(molsys)
            msm.physchem.get_bulkiness(molsys, selection=[])
        assert {"zimmerman_1968", "proust_2019"} <= set(ackredit.get_used_items())
        assert (
            "molsysmt.physchem.get_bulkiness"
            in ackredit.current_session().usage_tree["consumer.describe_groups"][
                "children"
            ]
        )
    with ackredit.session("unsupported group"):
        with pytest.raises(UnknownGroupInTableError):
            msm.physchem.get_bulkiness(named_groups(["DUM"]))
        assert not ackredit.get_used_items()


def test_bulkiness_single_group_index_retains_the_group_axis():
    result = msm.physchem.get_bulkiness(named_groups(["ALA"]), selection=0)
    assert result.shape == (1,)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="nm**2"), [0.115]
    )
