"""Receive independent reference-rule H removal without implicit scene editing."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Structures
from tests.build.test_get_residue_chemical_coverage import _system
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard
# Bounded deposited-villin control, independent of the private H selector:
# N-terminal H3 and the third NZ proton on five lysines at pH 12.
REMOVED_LABELS = {("H3", 0)} | {("HZ3", i) for i in (7, 24, 29, 30, 32)}


@pytest.fixture(scope="module")
def source():
    source = msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"],
        to_form="molsysmt.MolSys",
    )
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(
            np.repeat(xyz, 3, axis=0) + np.arange(3)[:, None, None], "nm"
        ),
        box=puw.quantity(np.repeat((np.eye(3) * 6)[None], 3, axis=0), "nm"),
        time=puw.quantity([2, 5, 11], "ps"),
        structure_id=["C", "A", "C"],
    )
    assert source.get_n_atoms() == 596
    return source


@pytest.fixture
def view(source):
    with msv.new_view(source.copy()) as view:
        view.regions.add(selection=[0, 2], tag="keep")
        view.shapes.add_sphere(atom_indices=[1], tag="anchor")
        view.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=596,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.protonation",
            ),
            name="saved",
            assume_aligned=True,
        )
        yield view


def retained_indices(source, pH):
    labels = list(
        zip(source.topology.atoms.atom_name, source.topology.atoms.group_index)
    )
    if pH == 12.0:
        assert set(labels) & REMOVED_LABELS == REMOVED_LABELS
    return [
        i for i, label in enumerate(labels) if pH != 12.0 or label not in REMOVED_LABELS
    ]


def test_signature_help_discovery_and_default(view):
    call = view.addons.molsysmt.build.reconcile_protonation
    native = inspect.signature(msm.build.reconcile_protonation)
    assert inspect.signature(call) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert call.digestion_plan is not None
    assert "reconcile_protonation" in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, "reconcile_protonation")
    text = inspect.getdoc(call)
    assert "in_place=True raises NotImplementedError" in text
    assert "no update_view" in text and "pKa" in text
    for parameter in inspect.signature(call).parameters:
        assert f"{parameter} :" in text
    before = snapshot(view)
    result = call()
    assert result is not view.molsys
    same(result, view.molsys)
    unchanged(view, before)


@pytest.mark.parametrize("pH", [7.4, 12.0])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_reference_removals_all_poses_units_and_independent_ownership(
    view, pH, skip, unit
):
    target = view.molsys
    indices = retained_indices(target, pH)
    expected = msm.build.reconcile_protonation(target.copy(), pH=pH)
    before = snapshot(view)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = dict(puw.configure.get_standard_units())
        result = view.addons.molsysmt.build.reconcile_protonation(
            pH=pH, skip_digestion=skip
        )
        assert dict(puw.configure.get_standard_units()) == policy
    assert result is not target
    assert result.get_n_atoms() == (590 if pH == 12 else 596)
    assert result.structures.n_structures == 3
    assert result.structures.structure_id.tolist() == ["C", "A", "C"]
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(target.structures.coordinates, to_unit="nm")[:, indices],
    )
    for field in ("box", "time"):
        same(getattr(result.structures, field), getattr(target.structures, field))
    pd.testing.assert_frame_equal(
        result.topology.atoms,
        target.topology.atoms.iloc[indices].reset_index(drop=True),
        check_frame_type=False,
        # Native extraction normalizes nullable index dtypes. Strict dtype
        # parity with the native result is checked separately below.
        check_dtype=False,
    )
    same(result, expected)
    unchanged(view, before)
    # Neither result data nor its remapped analysis owns the source arrays.
    msm.set(result, coordinates=result.structures.coordinates + puw.quantity(1, "nm"))
    result.interactions = {}
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_repeated_id_labels_do_not_define_correspondence(view, skip):
    msm.set(view.molsys, element="atom", atom_id=["same"] * 596)
    before = snapshot(view)
    result = view.addons.molsysmt.build.reconcile_protonation(
        pH=12.0, skip_digestion=skip
    )
    assert result.get_n_atoms() == 590
    assert set(result.topology.atoms.atom_id) == {"same"}
    unchanged(view, before)


@pytest.mark.parametrize("pH", [7.4, 12.0])
def test_named_analysis_occurrences_follow_native_subset_without_recalculation(
    view, pH
):
    target = view.molsys
    indices = retained_indices(target, 12.0)
    removed = next(i for i in range(596) if i not in indices)
    records = [
        {
            "structure_index": frame,
            "interaction_type": "contact",
            "participants": [
                {"role": "first", "atom_indices": [atom]},
                {"role": "second", "atom_indices": [indices[-1]]},
            ],
        }
        for frame in range(3)
        for atom in (indices[0], removed)
    ]
    observations = msm.Interactions.from_records(
        records,
        n_atoms=596,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic.stored-observations",
    )
    target.interactions = {**target.interactions, "observations": observations}
    before = snapshot(view)
    expected = msm.remove(
        target,
        selection=[i for i in range(596) if i not in indices] if pH == 12 else None,
    )
    result = view.addons.molsysmt.build.reconcile_protonation(pH=pH)
    analysis = result.interactions["observations"]
    assert len(analysis.occurrence_structures) == (3 if pH == 12 else 6)
    assert analysis.n_atoms == result.get_n_atoms()
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    assert analysis is not target.interactions["observations"]
    assert analysis.method == expected.interactions["observations"].method
    same(analysis.to_dict(), expected.interactions["observations"].to_dict())
    assert len(result.interactions["saved"].occurrence_structures) == 0
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("parameters", [{"engine": "OpenMM"}, {"pH": "invalid"}])
def test_native_errors_remain_native_and_preserve_source(view, skip, parameters):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.reconcile_protonation(
            view.molsys.copy(), **parameters, skip_digestion=skip
        )
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.reconcile_protonation(
            **parameters, skip_digestion=skip
        )
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_in_place_rejected_before_science_and_without_pending_state_changes(view, skip):
    before = snapshot(view)
    with pytest.raises(
        NotImplementedError, match="public native removal correspondence"
    ):
        view.addons.molsysmt.build.reconcile_protonation(
            pH=12.0, in_place=True, skip_digestion=skip
        )
    unchanged(view, before)
    view.addons.molsysmt.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    with pytest.raises(
        NotImplementedError, match="public native removal correspondence"
    ):
        view.addons.molsysmt.build.reconcile_protonation(
            in_place=True, skip_digestion=skip
        )
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [1, None, "yes"])
def test_integration_admission_cannot_bypass_boolean_validation(view, skip, value):
    before = snapshot(view)
    with pytest.raises(ArgumentError):
        view.addons.molsysmt.build.reconcile_protonation(
            in_place=value, skip_digestion=skip
        )
    unchanged(view, before)


def test_no_implicit_preparation_structure_or_scene_controls(view):
    call = view.addons.molsysmt.build.reconcile_protonation
    for key in (
        "molecular_system",
        "selection",
        "structure_indices",
        "update_view",
        "return_report",
    ):
        with pytest.raises(UnknownArgumentError):
            call(**{key: None})


def test_pending_primary_and_cached_method_follow_lifetime(view, source):
    tools = view.addons.molsysmt
    call = tools.build.reconcile_protonation
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    result = call(pH=12.0)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
            :, retained_indices(view.molsys, 12.0)
        ],
    )
    unchanged(view, before)
    tools.sync_view()
    replacement = msm.build.reconcile_protonation(source, pH=12.0)
    view.load(replacement, mode="replace")
    assert call(pH=7.4).get_n_atoms() == 590
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.reconcile_protonation()


def test_unassessed_group_is_retained_without_claiming_protonation_readiness():
    source = _system(
        [("UNL", (["C1", "H99"], ["C", "H"], [("C1", "H99", 1)]))], n_frames=2
    )
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.reconcile_protonation(pH=12.0)
        assert result is not view.molsys and result.get_n_atoms() == 2
        same(result, view.molsys)
        unchanged(view, before)


def test_explicit_amber_histidine_state_keeps_its_sidechain_hydrogen():
    source = msm.build.build_peptide("AHA", engine="MolSysMT")
    source = msm.remove(source, selection='atom_type=="H"')
    middle = int(
        source.topology.groups.index[source.topology.groups.group_name == "HIS"][0]
    )
    source.topology.groups.at[middle, "group_name"] = "HID"
    source.topology.set_group_naming_schemes("amber", group_indices=[middle])
    source = msm.build.add_missing_hydrogens(source, pH=12.0, engine="MolSysMT")
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.reconcile_protonation(pH=12.0)
        atoms = result.topology.atoms
        names = set(atoms.loc[atoms.group_index == middle, "atom_name"])
        assert "HD1" in names and "HE2" not in names
        assert (
            result.topology.group_naming_schemes == source.topology.group_naming_schemes
        )
        unchanged(view, before)
