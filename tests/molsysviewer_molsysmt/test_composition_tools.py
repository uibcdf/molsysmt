"""Receive molecular composition, explicit collections and managed prefix edits."""

import copy
import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentLengthError, StructuralInconsistencyError

puw = msm.pyunitwizard
BOUND = ("add", "append_structures")
COLLECTION = ("merge", "concatenate_structures")


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            yield result


def xyz(system):
    return puw.get_value(system.structures.coordinates, to_unit="nm")


def same_system(actual, expected):
    assert actual.get_n_atoms() == expected.get_n_atoms()
    assert actual.structures.n_structures == expected.structures.n_structures
    np.testing.assert_allclose(xyz(actual), xyz(expected), atol=1e-7)
    pd.testing.assert_frame_equal(actual.topology.atoms, expected.topology.atoms)
    pd.testing.assert_frame_equal(
        actual.chemical_states._resolve_chemical_state().bonds,
        expected.chemical_states._resolve_chemical_state().bonds,
    )


@pytest.mark.parametrize("name", BOUND + COLLECTION)
def test_signature_defaults_keyword_controls_digestion_and_aliases(view, name):
    native = inspect.signature(getattr(msm.basic, name))
    method = getattr(view.addons.molsysmt.basic, name)
    parameters = list(native.parameters.values())
    if name in BOUND:
        parameters = parameters[1:] + [
            inspect.Parameter(
                "update_view", inspect.Parameter.KEYWORD_ONLY, default=True
            )
        ]
    assert inspect.signature(method) == native.replace(parameters=parameters)
    assert getattr(view.addons.molsysmt, name) == method
    assert method.digestion_plan is not None
    doc = inspect.getdoc(method)
    assert "View integration" in doc
    if name in BOUND:
        assert "\nto_molecular_system :" not in doc
        assert "Native in_place=True" in doc
    else:
        assert "explicit molecular_systems collection" in doc


@pytest.mark.parametrize("name", COLLECTION)
@pytest.mark.parametrize("container", [list, tuple])
def test_collections_work_before_loading_and_do_not_insert_a_primary(
    view, name, container
):
    source = msm.copy(view.molsys)
    before = xyz(source).copy()
    with msv.new_view() as empty:
        result = getattr(empty.addons.molsysmt.basic, name)(container([source, source]))
        expected = getattr(msm.basic, name)(container([source, source]))
        same_system(result, expected)
        assert result is not source
        assert empty.molsys is None
    assert result.get_n_atoms() == (124 if name == "merge" else 62)
    assert result.structures.n_structures == (3 if name == "merge" else 6)
    np.testing.assert_array_equal(xyz(source), before)


@pytest.mark.parametrize("name", COLLECTION)
@pytest.mark.parametrize("indices", [[[2, 0], [1, 2]], np.array([2, 0])])
def test_collection_per_source_lists_and_common_arrays_preserve_order(
    view, name, indices
):
    sources = [msm.copy(view.molsys), msm.copy(view.molsys)]
    sources[1].structures.coordinates = puw.quantity(xyz(sources[1]) + [1, 0, 0], "nm")
    kwargs = dict(
        structure_indices=indices,
        selections=[[0, 1], [0, 1]],
        to_form="molsysmt.MolSys",
    )
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    result = getattr(view.addons.molsysmt.basic, name)(sources, **kwargs)
    expected = getattr(msm.basic, name)(sources, **kwargs)
    same_system(result, expected)
    assert result.get_n_atoms() == (4 if name == "merge" else 2)
    assert result.structures.n_structures == (2 if name == "merge" else 4)
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


@pytest.mark.parametrize("name", COLLECTION)
def test_collection_lengths_retain_native_rejection_without_scene_effect(view, name):
    state = view.export_state()
    with pytest.raises(ArgumentLengthError):
        getattr(view.addons.molsysmt.basic, name)(
            [view.molsys, view.molsys], selections=[[0]]
        )
    assert view.export_state() == state


@pytest.mark.parametrize("name", BOUND)
@pytest.mark.parametrize("in_place", [False, True])
@pytest.mark.parametrize("update", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_bound_native_semantics_and_deferred_ownership(
    view, name, in_place, update, skip
):
    target = view.molsys
    source = msm.copy(target)
    before = xyz(target).copy()
    region = view.regions.add(atom_indices=[1, 2], tag="preserved")
    expected = msm.copy(target)
    assert getattr(msm.basic, name)(expected, source) is None
    result = getattr(view.addons.molsysmt.basic, name)(
        source, in_place=in_place, update_view=update, skip_digestion=skip
    )
    assert view.molsys is target
    if in_place:
        assert result is None
        same_system(target, expected)
        assert view.addons.molsysmt.get_sync_status()["state"] == (
            "synchronized" if update else "pending"
        )
        view.addons.molsysmt.sync_view()
        assert view.regions["preserved"] is region and region.atom_indices == (1, 2)
        assert view.player.n_structures == expected.structures.n_structures
    else:
        same_system(result, expected)
        assert result is not target
        np.testing.assert_array_equal(xyz(target), before)
        assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"
    np.testing.assert_array_equal(xyz(source), before)


@pytest.mark.parametrize("name", BOUND)
def test_native_repeated_nonconsecutive_source_structures(view, name):
    source = msm.copy(view.molsys)
    kwargs = dict(structure_indices=[2, 0, 2])
    if name == "add":
        kwargs["selection"] = [0, 2, 3]
    expected = getattr(msm.basic, name)(view.molsys, source, in_place=False, **kwargs)
    getattr(view.addons.molsysmt.basic, name)(source, **kwargs)
    same_system(view.molsys, expected)


@pytest.mark.parametrize("name", BOUND)
@pytest.mark.parametrize("deferred", [False, True])
def test_native_strict_rejection_preserves_previous_scientific_and_scene_state(
    view, name, deferred
):
    source = msm.copy(view.molsys)
    source.structures.occupancy = np.ones((3, 62))
    view.molsys.structures.occupancy = None
    tools = view.addons.molsysmt
    if deferred:
        tools.basic.set(
            coordinates=puw.quantity(xyz(view.molsys) + [0.1, 0, 0], "nm"),
            update_view=False,
        )
    status = tools.get_sync_status()
    before = xyz(view.molsys).copy()
    with pytest.raises(StructuralInconsistencyError):
        getattr(tools.basic, name)(source, attribute_policy="strict")
    np.testing.assert_array_equal(xyz(view.molsys), before)
    after = tools.get_sync_status()
    # An attempted operation has its own ID, including atomic native rejection.
    assert {k: v for k, v in after.items() if k != "operation_id"} == {
        k: v for k, v in status.items() if k != "operation_id"
    }


@pytest.mark.parametrize("name", ["add"])
def test_named_target_coverage_remains_native_and_incoming_analyses_reject(view, name):
    source = msm.copy(view.molsys)
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=62,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="receiving.composition",
    )
    view.interactions.attach(analysis, name="retained", assume_aligned=True)
    visual = view.interactions.add("retained", tag="visual", structure_indices=[2])
    getattr(view.addons.molsysmt.basic, name)(source)
    kept = view.molsys.interactions["retained"]
    assert kept.evaluated_structure_indices.tolist() == [0, 2]
    assert view.interactions["visual"] is visual
    assert visual.filter["structure_indices"] == [2]
    if name == "add":
        assert kept.evaluation_universe_indices.tolist() == list(range(62))
        assert kept.atom_source_indices[62:].tolist() == [-1] * 62
    else:
        assert kept.structure_source_indices.tolist() == [0, 1, 2, -1, -1, -1]
    # Use an atom-compatible system for append; native source analyses still
    # need their own explicit merge policy rather than silent attachment.
    incoming = msm.copy(view.molsys)
    status = view.addons.molsysmt.get_sync_status()
    with pytest.raises(ValueError, match="explicit analysis"):
        getattr(view.addons.molsysmt.basic, name)(incoming)
    after = view.addons.molsysmt.get_sync_status()
    assert {k: v for k, v in after.items() if k != "operation_id"} == {
        k: v for k, v in status.items() if k != "operation_id"
    }


def test_append_named_analysis_with_implicit_single_state_keeps_coverage():
    from rdkit import Chem

    from molsysmt.native import Structures

    source = msm.convert(Chem.MolFromSmiles("CCO"))
    source.structures = Structures(
        coordinates=puw.quantity(np.arange(27).reshape(3, 3, 3), "nm")
    )
    incoming = source.copy()
    with msv.new_view(source) as view:
        analysis = msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="receiving.implicit-state",
        )
        view.interactions.attach(analysis, name="saved", assume_aligned=True)
        view.addons.molsysmt.basic.append_structures(incoming)
        result = view.molsys.interactions["saved"]
        assert result.n_structures == 6
        assert result.evaluated_structure_indices.tolist() == [0, 2]
        assert result.structure_source_indices.tolist() == [0, 1, 2, -1, -1, -1]


def test_append_named_analysis_and_explicit_state_links_receive_native_outcome(view):
    from molsysviewer.system_edits import SystemEditPendingError

    incoming = msm.copy(view.molsys)
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=62,
        n_structures=3,
        evaluated_structure_indices=[0, 2],
        method="receiving.explicit-state",
    )
    view.interactions.attach(analysis, name="saved", assume_aligned=True)
    target = view.molsys
    native = msm.copy(target)
    # #520 currently fails after structure publication. Preserve both native
    # outcomes: a future provider repair must keep coverage and correspondence;
    # a partial scientific write must never be mistaken for atomic rejection.
    try:
        msm.append_structures(native, incoming)
    except ValueError as error:
        assert "atom/structure domains" in str(error)
        with pytest.raises(ValueError, match="atom/structure domains"):
            view.addons.molsysmt.basic.append_structures(incoming)
        assert target.structures.n_structures == native.structures.n_structures == 6
        assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
        with pytest.raises(SystemEditPendingError):
            view.export_state()
        view.addons.manager.system_edits.replace(incoming)
        assert view.molsys.structures.n_structures == 3
        assert target.structures.n_structures == 6  # Replacement is not molecular undo.
    else:
        view.addons.molsysmt.basic.append_structures(incoming)
        same_system(target, native)
        assert target.interactions["saved"].evaluated_structure_indices.tolist() == [
            0,
            2,
        ]
        assert target.interactions["saved"].structure_source_indices.tolist() == [
            0,
            1,
            2,
            -1,
            -1,
            -1,
        ]


@pytest.mark.parametrize("name", BOUND)
def test_cached_destination_tracks_replacement_and_closed_view(view, name):
    method = getattr(view.addons.molsysmt.basic, name)
    original = view.molsys
    with msv.demo["dialanine"] as source:
        view.load(source.molsys, mode="replace")
    source = msm.copy(view.molsys)
    result = method(source, in_place=False)
    assert result.get_n_atoms() == (44 if name == "add" else 22)
    assert result.structures.n_structures == (1 if name == "add" else 2)
    assert original.get_n_atoms() == 62 and original.structures.n_structures == 3
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        method(source)


@pytest.mark.parametrize("name", BOUND)
def test_primary_override_and_empty_view_reject_before_mutation(view, name):
    source = msm.copy(view.molsys)
    with pytest.raises(UnknownArgumentError):
        getattr(view.addons.molsysmt.basic, name)(source, to_molecular_system=source)
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt.basic, name)(source)


def test_growth_and_removal_compose_from_last_scene_without_rerunning_science(view):
    tools = view.addons.molsysmt
    source = msm.copy(view.molsys)
    region = view.regions.add(atom_indices=[0, 2], tag="prefix")
    tools.basic.add(source, update_view=False)
    tools.basic.append_structures(
        msm.copy(view.molsys), structure_indices=[2, 0], update_view=False
    )
    tools.basic.remove(
        selection=[1], structure_indices=[0, 3], in_place=True, update_view=False
    )
    assert view.molsys.get_n_atoms() == 123
    assert view.molsys.structures.n_structures == 3
    assert tools.get_sync_status()["pending_operations"] == 3
    tools.sync_view()
    assert view.regions["prefix"] is region and region.atom_indices == (0, 1)
    assert view.player.n_structures == 3
    # The loaded structures were [0, 8, 3] in their original source, not
    # newly invented local-origin indices [0, 1, 2].
    assert view.load_blocks[0]["structure_map"]["runs"] == [[8, 0, 1], [3, 1, 1]]


def test_append_unknown_per_structure_visual_data_rejects_before_native_write(view):
    source = msm.copy(view.molsys)
    view.shapes.add_sphere(
        structure_centers=puw.quantity(np.zeros((3, 3)), "nm"),
        radius="0.1 nm",
        tag="series",
    )
    state = copy.deepcopy(view.export_state())
    with pytest.raises(ValueError, match="per-structure shapes"):
        view.addons.molsysmt.basic.append_structures(source)
    assert view.molsys.structures.n_structures == 3
    assert view.export_state() == state


def test_coordinate_only_and_h5msm_sources_preserve_native_scope(view, tmp_path):
    from molsysmt.native import Structures

    source = Structures(coordinates=puw.quantity(xyz(view.molsys) + [1, 0, 0], "nm"))
    expected = msm.append_structures(
        view.molsys, source, structure_indices=[2, 0], in_place=False
    )
    view.addons.molsysmt.basic.append_structures(source, structure_indices=[2, 0])
    same_system(view.molsys, expected)
    filename = str(tmp_path / "incoming.h5msm")
    msm.h5msm.write(msm.extract(view.molsys, structure_indices=[0]), filename)
    result = view.addons.molsysmt.basic.merge(
        [filename, filename], to_form="molsysmt.MolSys"
    )
    assert result.get_n_atoms() == 124 and result.structures.n_structures == 1


@pytest.mark.parametrize("name", BOUND)
def test_native_coordinate_drop_is_completed_science_and_retry_never_repeats_it(
    view, name
):
    from molsysviewer.system_edits import SystemEditSyncError

    source = msm.copy(view.molsys)
    before = xyz(source).copy()
    source.structures.coordinates = None
    with pytest.raises(SystemEditSyncError) as failure:
        getattr(view.addons.molsysmt.basic, name)(source)
    assert failure.value.science_completed is True
    assert failure.value.scientific_result is None
    tools = view.addons.molsysmt
    assert tools.get_sync_status()["state"] == "sync_failed"
    expected_atoms = 124 if name == "add" else 62
    expected_structures = 3 if name == "add" else 6
    assert view.molsys.get_n_atoms() == expected_atoms
    assert view.molsys.structures.n_structures == expected_structures
    with pytest.raises(ValueError, match="requires structural coordinates"):
        tools.sync_view()
    assert view.molsys.get_n_atoms() == expected_atoms
    assert view.molsys.structures.n_structures == expected_structures
    # The expert explicitly supplies missing scientific data; synchronization
    # subsequently publishes this existing result without performing add again.
    coordinates = np.concatenate([before, before], axis=1 if name == "add" else 0)
    msm.set(view.molsys, coordinates=puw.quantity(coordinates, "nm"))
    tools.sync_view()
    assert tools.get_sync_status()["state"] == "synchronized"
    assert view.player.n_structures == expected_structures


@pytest.mark.parametrize("name", BOUND)
def test_complementary_source_items_are_one_system(view, name):
    source = msm.copy(view.molsys)
    items = [source.topology, source.chemical_states, source.structures]
    expected = getattr(msm.basic, name)(view.molsys, items, in_place=False)
    getattr(view.addons.molsysmt.basic, name)(items)
    same_system(view.molsys, expected)


def test_explicit_mechanics_collection_keeps_native_form_units_and_report_policy():
    from molsysmt._private.smonitor import StructuralAttributeDropWarning
    from molsysmt.native import MolecularMechanics

    left = MolecularMechanics(
        atom_ff_type=np.array(["C", "N"]), partial_charge=np.array([0.25, -0.5])
    )
    right = MolecularMechanics(
        atom_ff_type=np.array(["OA"]), partial_charge=np.array([-0.75])
    )
    left.partial_charge_assignment = {"producer": "independent", "atom_indices": [0, 1]}
    with msv.new_view() as empty, puw.context(standard_units=["angstrom", "coulomb"]):
        with pytest.warns(StructuralAttributeDropWarning):
            result = empty.addons.molsysmt.basic.merge(
                [left, right], selections=[[1, 0], [0]]
            )
        assert isinstance(result, MolecularMechanics)
        np.testing.assert_allclose(
            result.partial_charge.astype(float), [-0.5, 0.25, -0.75]
        )
        assert result.atom_ff_type.tolist() == ["N", "C", "OA"]
        assert result.partial_charge_assignment is None
        assert left.partial_charge_assignment["producer"] == "independent"
        assert empty.molsys is None


def test_file_output_defaults_retain_native_not_implemented_rejection(view, tmp_path):
    from molsysmt._private.smonitor import NotImplementedMethodError

    filename = str(tmp_path / "source.h5msm")
    msm.h5msm.write(view.molsys, filename)
    with pytest.raises(NotImplementedMethodError):
        view.addons.molsysmt.basic.merge([filename, filename])
