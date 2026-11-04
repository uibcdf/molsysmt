"""Receive export-label projection with explicit maps and no scene adoption."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from tests.build.test_merge_nonpolar_hydrogens import declared_methanol
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard
NAMES = ["H1291", "H0", "H1292", "H1", "H2", "HD"]


def source():
    system = declared_methanol()
    msm.set(system, atom_name=NAMES)
    return system


@pytest.fixture
def view():
    with msv.new_view(source()) as owner:
        owner.regions.add(selection=[0, 2], tag="keep")
        owner.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=6,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.name-projection",
            ),
            name="preserve",
            assume_aligned=True,
        )
        yield owner


def test_expert_signature_help_and_required_export_policy(view):
    method = view.addons.molsysmt.build.project_atom_names
    native = inspect.signature(msm.build.project_atom_names)
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert method.digestion_plan is not None
    assert (
        inspect.signature(method).parameters["target_form"].default
        is inspect.Parameter.empty
    )
    assert "project_atom_names" in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, "project_atom_names")
    text = inspect.getdoc(method)
    assert "Export naming projection" in text
    assert "not a file write" in text
    assert "protected and shared" in text
    assert "not a name-based atom match" in text
    assert "independent native diagnostic" not in text
    for extra in (
        {"molecular_system": view.molsys},
        {"update_view": True},
        {"in_place": True},
    ):
        with pytest.raises(UnknownArgumentError):
            method(target_form="file:pdbqt", **extra)
    with pytest.raises(ArgumentError):
        method(target_form="file:pdbqt", skip_digestion="yes")


@pytest.mark.parametrize("target", ["file:pdbqt", "string:pdbqt_text"])
@pytest.mark.parametrize("selection", ["all", [2, 0, 2], [], "atom_index in [0, 2]"])
@pytest.mark.parametrize("skip", [False, True])
def test_native_names_identity_maps_full_axes_and_source_scene(
    view, target, selection, skip
):
    before = snapshot(view)
    result = view.addons.molsysmt.build.project_atom_names(
        target_form=target, selection=selection, return_report=True, skip_digestion=skip
    )
    expected = msm.build.project_atom_names(
        view.molsys,
        target_form=target,
        selection=selection,
        return_report=True,
        skip_digestion=skip,
    )
    same(result, expected)
    output, report = result["molecular_system"], result["report"]
    assert output is not view.molsys
    assert output.get_n_atoms() == 6 and output.structures.n_structures == 3
    assert report["schema"] == "molsysmt.atom_map@1"
    np.testing.assert_array_equal(report["source_to_output_atom_indices"], np.arange(6))
    np.testing.assert_array_equal(report["output_to_source_atom_indices"], np.arange(6))
    assert report["source_atom_names"].tolist() == NAMES
    assert report["source_atom_ids"].tolist() == ["17", "3", "45", "90", "7", "11"]
    if not isinstance(selection, list) or selection:
        assert output.topology.atoms.atom_name.tolist() == [
            "H3",
            "H0",
            "H4",
            "H1",
            "H2",
            "HD",
        ]
        assert report["renamed_atom_indices"].tolist() == [0, 2]
    else:
        assert output.topology.atoms.atom_name.tolist() == NAMES
        assert report["renamed_atom_indices"].shape == (0,)
    assert report["renamed_atom_indices"].dtype == np.int64
    unchanged(view, before)


@pytest.mark.parametrize("report", [False, True])
def test_public_output_edits_detach_protected_shared_coordinates(view, report):
    before = snapshot(view)
    result = view.addons.molsysmt.build.project_atom_names(
        "file:pdbqt", return_report=report
    )
    output = result["molecular_system"] if report else result
    old_xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")
    output_xyz = puw.get_value(output.structures.coordinates, to_unit="nm")
    assert np.shares_memory(old_xyz, output_xyz)
    msm.set(output, coordinates=puw.quantity(output_xyz.copy() + 4, "nm"))
    msm.set(output, selection=[0], atom_name=["NEW"])
    assert not np.shares_memory(puw.get_value(output.structures.coordinates), old_xyz)
    unchanged(view, before)
    if report:
        assert result["report"]["output_atom_names"][0] == "H3"
        result["report"]["source_to_output_atom_indices"][:] = -1
        unchanged(view, before)


@pytest.mark.parametrize("selection", [None, [-1], [6], [True], [1.2], [[0, 1]]])
def test_native_invalid_selection_errors_are_retained_without_a_write(view, selection):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.project_atom_names(
            view.molsys, target_form="file:pdbqt", selection=selection
        )
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.project_atom_names("file:pdbqt", selection=selection)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize("target", [None, "file:pdb", ["file:pdbqt"], "not_a_form"])
def test_native_target_rejection_does_not_guess_an_export_format(view, target):
    before = snapshot(view)
    with pytest.raises(ArgumentError):
        view.addons.molsysmt.build.project_atom_names(target)
    unchanged(view, before)


def test_pending_reads_preserve_the_pending_scene_and_current_coordinates(view):
    tools = view.addons.molsysmt
    xyz = puw.get_value(view.molsys.structures.coordinates, to_unit="nm").copy() + 3
    tools.basic.set(coordinates=puw.quantity(xyz, "nm"), update_view=False)
    before = snapshot(view)
    result = tools.build.project_atom_names("file:pdbqt", return_report=True)
    np.testing.assert_array_equal(
        puw.get_value(result["molecular_system"].structures.coordinates, to_unit="nm"),
        xyz,
    )
    assert tools.get_sync_status()["state"] == "pending"
    unchanged(view, before)


def test_maps_compose_with_the_existing_explicit_native_map_contract(view):
    before = snapshot(view)
    result = view.addons.molsysmt.build.project_atom_names(
        "file:pdbqt", return_report=True
    )
    actual = view.addons.molsysmt.basic.compose_atom_maps([result["report"]])
    expected = msm.basic.compose_atom_maps([result["report"]])
    same(actual, expected)
    np.testing.assert_array_equal(actual["source_to_output_atom_indices"], np.arange(6))
    unchanged(view, before)


def test_cached_projection_follows_a_different_primary_and_rejects_closed_owner(view):
    method = view.addons.molsysmt.build.project_atom_names
    replacement = source()
    msm.set(replacement, atom_name=["C-long", "O", "H0", "H1", "H2", "HD"])
    view.load(replacement, mode="replace")
    result = method("file:pdbqt")
    assert result.topology.atoms.atom_name[0] == "C0"
    assert view.molsys.topology.atoms.atom_name[0] == "C-long"
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method("file:pdbqt", skip_digestion=True)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.project_atom_names("file:pdbqt")
