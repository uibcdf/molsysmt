"""Receive native graph publication, true no-ops and scene-only retry."""

import inspect
import sys
from collections import Counter

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError
from molsysviewer.system_edits import SystemEditPendingError, SystemEditSyncError
from molsysviewer.widget import MolSysViewerWidget

import molsysmt as msm
from molsysmt.native import Structures
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard


def source():
    with msv.demo["dialanine"] as demo:
        result = demo.molsys.copy()
    result.chemical_states.remove_bonds("all")
    xyz = puw.get_value(result.structures.coordinates, to_unit="nm")[:1]
    # Replace the one-frame fixture with an explicitly associated three-frame
    # series, rather than carrying its old association array over new axes.
    msm.set(result, structure_chemical_state_index=None)
    result.structures = Structures(
        coordinates=puw.quantity(np.concatenate([xyz, xyz + 1, xyz + 2]), "nm"),
        time=puw.quantity([2, 7, 15], "ps"),
        box=puw.quantity(np.tile(5 * np.eye(3), (3, 1, 1)), "nm"),
        structure_id=[11, 24, 80],
    )
    msm.set(result, structure_chemical_state_index=[0, 0, 0])
    result.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=result.get_n_atoms(),
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="receiving.bond-edit",
        )
    }
    return result


@pytest.fixture
def view():
    with msv.new_view(source()) as view:
        view.regions.add(selection=[6, 8], tag="kept")
        view.shapes.add_sphere(atom_indices=[8], tag="anchor")
        yield view


def unchanged_attempt(view, before):
    # An attempted/no-op operation receives an audit ID, not a new revision.
    before = list(before)
    before[3] = {
        **before[3],
        "operation_id": view.addons.molsysmt.get_sync_status()["operation_id"],
    }
    unchanged(view, before)


def test_native_signature_help_and_discovery(view):
    method = view.addons.molsysmt.build.add_missing_bonds
    native = inspect.signature(msm.build.add_missing_bonds)
    assert inspect.signature(method) == native.replace(
        parameters=list(native.parameters.values())[1:]
        + [
            inspect.Parameter(
                "update_view", inspect.Parameter.KEYWORD_ONLY, default=True
            )
        ]
    )
    assert method.digestion_plan is not None
    assert "add_missing_bonds" in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, "add_missing_bonds")
    doc = inspect.getdoc(method)
    assert "\nmolecular_system :" not in doc
    for parameter in inspect.signature(method).parameters:
        assert f"{parameter} :" in doc
    assert "structure_index=0" in doc and "not the visible frame" in doc
    for extra in ("molecular_system", "chemical_state", "structure_indices", "prepare"):
        with pytest.raises(UnknownArgumentError):
            method(**{extra: None})


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_selected_bond_addition_preserves_native_science_and_ownership(
    view, in_place, skip
):
    before = snapshot(view)
    target = view.molsys
    coordinate_storage = target.structures._coordinates
    reference = target.chemical_states._reference_index
    old_analysis = target.interactions["empty"]
    old_coverage = old_analysis.to_dict()
    expected = msm.build.add_missing_bonds(
        target, selection="group_index==1", in_place=False
    )
    result = view.addons.molsysmt.build.add_missing_bonds(
        selection="group_index==1", in_place=in_place, skip_digestion=skip
    )
    output = target if in_place else result
    same(output, expected)
    assert msm.get(output, bonded_atom_pairs=True) == [
        [6, 7],
        [6, 8],
        [8, 9],
        [8, 10],
        [8, 14],
        [10, 11],
        [10, 12],
        [10, 13],
        [14, 15],
    ]
    assert output.chemical_states._reference_index == reference
    assert output.interactions["empty"].evaluated_structure_indices.tolist() == []
    same(old_analysis.to_dict(), old_coverage)
    for name in ("atoms", "groups", "molecules", "entities", "chains"):
        pd.testing.assert_frame_equal(
            getattr(output.topology, name),
            getattr(before[1].topology, name),
            check_frame_type=False,
        )
    if in_place:
        assert result is None and view.molsys is target
        assert target.structures._coordinates is coordinate_storage
        assert view.regions["kept"].atom_indices == (6, 8)
        assert view.shapes.records()[0]["options"]["atom_indices"] == [8]
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
        assert not view.history.can_undo()
    else:
        assert result is not target
        unchanged(view, before)


@pytest.mark.parametrize("update_view", [False, True])
def test_no_new_bonds_preserves_coverage_history_and_revision(view, update_view):
    tools = view.addons.molsysmt
    tools.build.add_missing_bonds()
    # New evidence after reconstruction must survive another no-op call.
    view.interactions.attach(
        source().interactions["empty"], name="evaluated", assume_aligned=True
    )
    view.regions["kept"].hide()
    before = snapshot(view)
    stored = view.molsys.chemical_states._resolve_chemical_state().bonds
    assert tools.build.add_missing_bonds(update_view=update_view) is None
    assert view.molsys.chemical_states._resolve_chemical_state().bonds is stored
    unchanged_attempt(view, before)


@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize(
    "parameters",
    [
        {"selection": [1000]},
        {"structure_index": 1000},
        {"max_bond_length": "2 ps"},
        {"engine": "not-an-engine"},
    ],
)
def test_native_rejection_preserves_science_scene_and_pending_work(
    view, in_place, parameters
):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[0,0,1] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.add_missing_bonds(view.molsys.copy(), in_place=in_place, **parameters)
    with pytest.raises(type(native.value)) as actual:
        tools.build.add_missing_bonds(in_place=in_place, **parameters)
    assert str(actual.value) == str(native.value)
    unchanged_attempt(view, before)
    tools.sync_view()
    assert tools.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("parameters", [{"update_view": 1}, {"in_place": "yes"}])
def test_integration_flags_validate_even_when_digestion_is_skipped(view, parameters):
    before = snapshot(view)
    with pytest.raises(Exception):
        view.addons.molsysmt.build.add_missing_bonds(skip_digestion=True, **parameters)
    unchanged(view, before)


def test_deferred_bonds_compose_with_removal_and_noop_can_sync_earlier_work(view):
    tools = view.addons.molsysmt
    source_id = view.load_blocks[0]["source_id"]
    region = view.regions["kept"]
    sphere = view.shapes["anchor"]
    tools.build.add_missing_bonds(update_view=False)
    assert tools.get_sync_status()["state"] == "pending"
    with pytest.raises(SystemEditPendingError):
        region.hide(skip_digestion=True)
    tools.basic.remove(selection=[0], in_place=True, update_view=False)
    assert tools.get_sync_status()["pending_operations"] == 2
    expected = msm.get(view.molsys, bonded_atom_pairs=True)
    tools.build.add_missing_bonds()  # no new bond; synchronize retained work
    assert tools.get_sync_status()["state"] == "synchronized"
    assert tools.get_sync_status()["target_revision"] == 2
    assert msm.get(view.molsys, bonded_atom_pairs=True) == expected
    assert view.regions["kept"] is region and region.atom_indices == (5, 7)
    assert view.shapes["anchor"] is sphere
    assert view.shapes.records()[0]["options"]["atom_indices"] == [7]
    assert view.load_blocks[0]["source_id"] == source_id


class InterruptedBondWidget(MolSysViewerWidget):
    interrupted = False

    def send(self, content, buffers=None):
        if self.interrupted and content.get("op") == "add_sphere":
            self.interrupted = False
            raise OSError("bond receiving transport interruption")
        return super().send(content, buffers=buffers)


def test_scene_retry_does_not_repeat_bond_publication():
    with msv.MolSysView(transport=InterruptedBondWidget()) as view:
        view.load(source())
        view.shapes.add_sphere(atom_indices=[8], tag="anchor")
        view._ready = True
        view.widget.interrupted = True
        codes = {
            inspect.unwrap(msm.build.add_missing_bonds).__code__: "write",
            inspect.unwrap(msm.build.get_missing_bonds).__code__: "candidates",
        }
        calls = Counter()

        def observe(frame, event, argument):
            if event == "call" and frame.f_code in codes:
                calls[codes[frame.f_code]] += 1

        previous = sys.getprofile()
        sys.setprofile(observe)
        try:
            with pytest.raises(SystemEditSyncError) as error:
                view.addons.molsysmt.build.add_missing_bonds()
            state = view.molsys.chemical_states._resolve_chemical_state()
            stored = state.bonds
            view.addons.molsysmt.sync_view()
        finally:
            sys.setprofile(previous)
        assert error.value.science_completed and error.value.scientific_result is None
        assert isinstance(error.value.__cause__, OSError)
        assert calls == {"write": 1, "candidates": 1}
        assert state.bonds is stored
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 1
        assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_cached_method_rebinds_and_rejects_closed_or_empty_owner(view):
    method = view.addons.molsysmt.build.add_missing_bonds
    view.load(source(), mode="replace")
    replacement = view.molsys
    method()
    assert view.molsys is replacement and msm.get(replacement, n_bonds=True) > 0
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.add_missing_bonds()


@pytest.mark.parametrize("cutoff", ["2 angstroms", "0.2 nm", "200 pm"])
def test_length_units_and_numeric_selection_retain_literal_pairs(view, cutoff):
    indices = msm.select(view.molsys, selection="group_index==1")
    view.addons.molsysmt.build.add_missing_bonds(
        selection=indices, max_bond_length=cutoff
    )
    assert msm.get(view.molsys, bonded_atom_pairs=True) == [
        [6, 7],
        [6, 8],
        [8, 9],
        [8, 10],
        [8, 14],
        [10, 11],
        [10, 12],
        [10, 13],
        [14, 15],
    ]


def test_other_states_associations_and_both_payload_encoders_keep_identity():
    from molsysviewer.loaders.array_native_molsys import serialize_array_native_molsys
    from molsysviewer.loaders.json_molsys import serialize_json_molsys

    molecular = source()
    molecular.chemical_states.append_state()
    before = molecular.copy()
    with msv.new_view(molecular) as view:
        other = view.molsys.chemical_states._states[1]
        other_bonds = other.bonds
        view.addons.molsysmt.build.add_missing_bonds(selection="group_index==1")
        assert other.bonds is other_bonds
        assert view.molsys.chemical_states._states[1].bonds.equals(
            before.chemical_states._states[1].bonds
        )
        np.testing.assert_array_equal(
            msm.get(view.molsys, structure_chemical_state_index=True), [0, 0, 0]
        )
        expected = msm.get(view.molsys, bonded_atom_pairs=True)
        json_payload = serialize_json_molsys(view.molsys)
        binary_payload = serialize_array_native_molsys(view.molsys)
        for payload in (json_payload, binary_payload.metadata):
            assert (
                list(
                    map(
                        list,
                        zip(payload["bonds"]["indexA"], payload["bonds"]["indexB"]),
                    )
                )
                == expected
            )
