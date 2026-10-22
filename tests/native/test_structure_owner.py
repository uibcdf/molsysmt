"""Protect geometry publication, owner isolation and sparse analysis validity."""

import copy
import gc
import pickle
import weakref

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys
from tests.native.test_molsys_interactions import _analysis, _system


@pytest.fixture
def system():
    result = _system()
    result.structures.time = puw.quantity([0.0, 1.0, 2.0], "ps")
    result.structures.box = puw.quantity(np.repeat(np.eye(3)[None], 3, axis=0), "nm")
    result.interactions = {"pairs": _analysis(), "second": _analysis()}
    return result


@pytest.mark.parametrize("field", ["coordinates", "box"])
def test_selected_direct_edits_invalidate_empty_and_populated_structures(system, field):
    previous = system.interactions["pairs"]
    view = previous.query(structure_indices=[2, 0])
    indices = [2, 0, 2]
    if field == "coordinates":
        # Atom 2 has no previous observations, but its movement may create edges.
        system.structures.set_coordinates(
            indices=[2],
            structure_indices=indices,
            value=puw.quantity(np.arange(9.0).reshape(3, 1, 3), "angstrom"),
        )
        np.testing.assert_allclose(
            puw.get_value(
                system.structures.get_coordinates(indices=[2], structure_indices=[2]),
                to_unit="nm",
            ),
            [[[0.6, 0.7, 0.8]]],
        )
    else:
        system.structures.set_box(
            structure_indices=indices,
            value=puw.quantity(
                np.repeat((20 * np.eye(3))[None], 3, axis=0), "angstrom"
            ),
        )
    for analysis in system.interactions.values():
        np.testing.assert_array_equal(analysis.evaluated_structure_indices, [1])
        assert analysis.n_interactions == 0
    np.testing.assert_array_equal(previous.evaluated_structure_indices, [0, 1, 2])
    assert view.n_interactions == 1


@pytest.mark.parametrize("field", ["coordinates", "box"])
@pytest.mark.parametrize("route", ["property", "native", "agnostic"])
def test_full_geometry_assignment_notifies_owner(system, field, route):
    value = puw.quantity(np.ones((3, 3, 3)), "angstrom")
    if route == "property":
        setattr(system.structures, field, value)
    elif route == "native":
        getattr(system.structures, "set_" + field)(value=value)
    else:
        msm.set(system.structures, **{field: value})
    for analysis in system.interactions.values():
        assert analysis.evaluated_structure_indices.size == 0
    np.testing.assert_allclose(
        puw.get_value(getattr(system.structures, field), to_unit="nm"), 0.1
    )


@pytest.mark.parametrize("field", ["coordinates", "box"])
def test_clearing_geometry_preserves_other_series_and_invalidates(system, field):
    setattr(system.structures, field, None)
    assert system.structures.n_structures == 3
    assert getattr(system.structures, field) is None
    assert system.interactions["pairs"].evaluated_structure_indices.size == 0


@pytest.mark.parametrize("field", ["coordinates", "box"])
@pytest.mark.parametrize("failure", ["units", "shape", "index", "resize"])
def test_rejected_edits_preserve_geometry_and_analysis(system, field, failure):
    original = getattr(system.structures, "_" + field)
    analysis = system.interactions["pairs"]
    kwargs = {"structure_indices": [0]}
    value = np.ones((1, 3, 3))
    unit = "nm"
    if failure == "units":
        unit = "ps"
    elif failure == "shape":
        value = np.ones((1, 2, 3))
    elif failure == "index":
        kwargs["structure_indices"] = [3]
    else:
        kwargs["structure_indices"] = "all"
        value = np.ones((2, 3, 3))
    with pytest.raises(Exception):
        getattr(system.structures, "set_" + field)(
            **kwargs, value=puw.quantity(value, unit)
        )
    assert getattr(system.structures, "_" + field) is original
    assert system.interactions["pairs"] is analysis


@pytest.mark.parametrize("field", ["coordinates", "box"])
def test_empty_selections_and_metadata_do_not_invalidate(system, field):
    analysis = system.interactions["pairs"]
    getattr(system.structures, "set_" + field)(
        structure_indices=[], value=puw.quantity(np.empty((0, 3, 3)), "nm")
    )
    system.structures.set_coordinates(
        indices=[], value=puw.quantity(np.empty((3, 0, 3)), "nm")
    )
    system.structures.set_time(value=puw.quantity([3.0, 4.0, 5.0], "ps"))
    assert system.interactions["pairs"] is analysis


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, lambda x: x.copy(deep=False)]
)
def test_domain_copies_detach_and_system_copies_bind_their_own_owner(system, copier):
    isolated = copier(system.structures)
    assert getattr(isolated, "_molsys_owner_ref", None) is None
    isolated.set_coordinates(
        structure_indices=[2], value=puw.quantity(np.ones((1, 3, 3)), "nm")
    )
    duplicate = copier(system)
    assert duplicate.structures._molsys_owner_ref() is duplicate
    duplicate.structures.set_coordinates(
        structure_indices=[2], value=puw.quantity(np.ones((1, 3, 3)), "nm")
    )
    np.testing.assert_array_equal(
        duplicate.interactions["pairs"].evaluated_structure_indices, [0, 1]
    )
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )
    np.testing.assert_array_equal(puw.get_value(system.structures.coordinates), 0.0)


@pytest.mark.parametrize("route", ["pickle", "legacy_pickle", "h5msm"])
def test_restoration_binds_owner_and_preserves_invalidation(system, route, tmp_path):
    if route == "pickle":
        restored = pickle.loads(pickle.dumps(system))
    elif route == "legacy_pickle":
        state = system.__dict__.copy()
        state["structures"] = copy.deepcopy(state.pop("_structures"))
        state["_topology"] = copy.deepcopy(state["_topology"])
        restored = object.__new__(MolSys)
        restored.__setstate__(state)
    else:
        path = str(tmp_path / "owner.h5msm")
        msm.convert(system, to_form=path)
        restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert restored.structures._molsys_owner_ref() is restored
    restored.structures.set_box(
        structure_indices=[2], value=puw.quantity(np.eye(3)[None] * 2, "nm")
    )
    np.testing.assert_array_equal(
        restored.interactions["pairs"].evaluated_structure_indices, [0, 1]
    )
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1, 2]
    )


def test_owner_is_weak_and_standalone_pickle_has_no_owner(system):
    system = system.copy(deep=False)
    structures = system.structures
    restored = pickle.loads(pickle.dumps(structures))
    assert getattr(restored, "_molsys_owner_ref", None) is None
    owner = weakref.ref(system)
    del system
    gc.collect()
    assert owner() is None
    structures.set_box(value=puw.quantity(np.eye(3)[None].repeat(3, axis=0), "nm"))


def test_domain_attachment_owns_a_separate_wrapper_and_detaches_previous(system):
    other = _system()
    previous = other.structures
    other.structures = system.structures
    assert previous._molsys_owner_ref is None
    assert other.structures is not system.structures
    assert np.shares_memory(
        other.structures._coordinates._blocks[0],
        system.structures._coordinates._blocks[0],
    )
    assert other.structures._molsys_owner_ref() is other
    assert system.structures._molsys_owner_ref() is system


def test_selected_edit_never_materializes_full_geometry(system, monkeypatch):
    from molsysmt.native._structure_array import _StructureArray

    def forbidden(*args, **kwargs):
        pytest.fail("Owner notification materialized complete geometry")

    monkeypatch.setattr(_StructureArray, "_dense", forbidden)
    system.structures.set_coordinates(
        indices=[2],
        structure_indices=[2],
        value=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
    )
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1]
    )


@pytest.mark.parametrize("field", ["coordinates", "box"])
def test_invalidation_allocation_failure_keeps_geometry_unpublished(
    system, field, monkeypatch
):
    previous = getattr(system.structures, "_" + field)
    analysis = system.interactions["pairs"]

    def failed(*args, **kwargs):
        raise MemoryError("Cannot allocate invalidation snapshot")

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", failed)
    with pytest.raises(MemoryError, match="invalidation snapshot"):
        getattr(system.structures, "set_" + field)(
            structure_indices=[2], value=puw.quantity(np.ones((1, 3, 3)), "nm")
        )
    assert getattr(system.structures, "_" + field) is previous
    assert system.interactions["pairs"] is analysis
    assert "_pending_interaction_edits" not in vars(system)


@pytest.mark.parametrize("field", ["coordinates", "box"])
def test_property_atom_or_box_axes_are_validated_before_invalidation(system, field):
    analysis = system.interactions["pairs"]
    original = getattr(system.structures, "_" + field)
    with pytest.raises(Exception):
        setattr(system.structures, field, puw.quantity(np.ones((3, 2, 3)), "nm"))
    assert getattr(system.structures, "_" + field) is original
    assert system.interactions["pairs"] is analysis


def test_notification_respects_nondefault_output_units(system):
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        system.structures.set_coordinates(
            indices=[2],
            structure_indices=[2],
            value=puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"),
        )
        selected = system.structures.get(
            element="atom", selection=[2], structure_indices=[2], coordinates=True
        )
        assert puw.has_unit(selected, "angstrom")
        np.testing.assert_allclose(puw.get_value(selected), [[[10.0, 20.0, 30.0]]])
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [0, 1]
    )


def test_public_system_delegation_does_not_repeat_native_invalidation(
    system, monkeypatch
):
    original = msm.Interactions.invalidate_structures
    calls = []

    def counted(self, structure_indices, **kwargs):
        calls.append(self)
        return original(self, structure_indices, **kwargs)

    monkeypatch.setattr(msm.Interactions, "invalidate_structures", counted)
    msm.set(
        system,
        selection=[2],
        structure_indices=[2],
        coordinates=puw.quantity([[[1.0, 2.0, 3.0]]], "nm"),
    )
    assert len(calls) == len(system.interactions)
    assert "_pending_interaction_edits" not in vars(system)


@pytest.mark.parametrize("fail", [False, True])
def test_nested_edits_publish_union_of_scopes_even_after_delegate_failure(system, fail):
    def edit():
        with system._invalidating_interaction_frames([0]):
            system.structures.set_box(
                structure_indices=[2],
                value=puw.quantity(np.eye(3)[None] * 2, "nm"),
            )
            if fail:
                raise RuntimeError("Failure after publishing geometry")

    if fail:
        with pytest.raises(RuntimeError, match="after publishing"):
            edit()
    else:
        edit()
    np.testing.assert_array_equal(
        system.interactions["pairs"].evaluated_structure_indices, [1]
    )
    assert "_pending_interaction_edits" not in vars(system)
