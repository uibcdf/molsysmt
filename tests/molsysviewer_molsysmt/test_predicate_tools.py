"""Receiving native composition predicates and comparisons with explicit references."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.predicates",
            )
            result.interactions.attach(analysis, name="received", assume_aligned=True)
            result.regions.add(selection=[0, 1, 2], tag="retained")
            yield result


@pytest.mark.parametrize("name", ["contains", "is_composed_of", "compare"])
def test_native_signature_aliases_and_documentation(view, name):
    native = inspect.signature(getattr(msm.basic, name))
    expected = native.replace(parameters=list(native.parameters.values())[1:])
    bound = getattr(view.addons.molsysmt.basic, name)
    assert inspect.signature(bound) == expected
    assert bound.digestion_plan is not None
    assert getattr(view.addons.molsysmt, name) == bound
    assert "current view.molsys" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    if name == "compare":
        assert "molecular_system_2" in expected.parameters
        assert "\nmolecular_system_2 :" in inspect.getdoc(bound)
        assert "raises NotImplementedError before edits" in inspect.getdoc(bound)


@pytest.mark.parametrize("name", ["contains", "is_composed_of"])
@pytest.mark.parametrize(
    "arguments",
    [{}, {"selection": []}, {"waters": False}, {"n_atoms": 3, "selection": [0, 1, 2]}],
)
def test_native_predicates_preserve_selectors_aliases_and_no_condition_branch(
    view, name, arguments
):
    native = getattr(msm.basic, name)(view.molsys, **arguments)
    before = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    analysis = view.molsys.interactions["received"]
    actual = getattr(view.addons.molsysmt, name)(**arguments)
    assert type(actual) is type(native)
    assert actual == native
    assert view.export_state() == before
    assert view.addons.molsysmt.get_sync_status() == status
    assert view.molsys.interactions["received"] is analysis


def test_native_minimum_contains_and_exact_composition_are_distinct(view):
    count = msm.get(view.molsys, n_atoms=True)
    tools = view.addons.molsysmt
    assert tools.contains(n_atoms=count - 1) is True
    assert tools.is_composed_of(n_atoms=count - 1) is False
    assert tools.is_composed_of(n_atoms=count) is True


@pytest.mark.parametrize(
    "options",
    [
        {},
        {"output_type": "dictionary", "atom_name": True, "n_atoms": True},
        {
            "attribute_type": "structural",
            "output_type": "dictionary",
            "include_none": True,
        },
        {"attributes_type": "topological", "atom_name": False},
    ],
)
def test_compare_keeps_native_defaults_results_and_attribute_aliases(view, options):
    reference = msm.copy(view.molsys)
    expected = msm.compare(view.molsys, reference, **options)
    state = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    actual = view.addons.molsysmt.compare(reference, **options)
    assert type(actual) is type(expected)
    assert actual == expected
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


def test_separate_atom_and_structure_scopes_are_preserved(view):
    reference = msm.copy(view.molsys)
    values = msm.get(
        reference,
        element="atom",
        selection=[2],
        structure_indices=[1],
        coordinates=True,
    )
    msm.set(
        reference,
        selection=[2],
        structure_indices=[1],
        coordinates=values + puw.quantity(0.2, "nm"),
    )
    options = dict(
        selection=[2],
        selection_2=[2],
        coordinates=True,
        structure_indices=[2, 0, 2],
        structure_indices_2=[2, 0, 2],
    )
    assert view.addons.molsysmt.compare(reference, **options) == msm.compare(
        view.molsys, reference, **options
    )
    assert view.addons.molsysmt.compare(reference, **options) is True
    options.update(
        structure_indices=[1], structure_indices_2=[1], output_type="dictionary"
    )
    actual = view.addons.molsysmt.compare(reference, **options)
    assert actual == msm.compare(view.molsys, reference, **options)
    assert actual["coordinates"] is False


def test_shape_difference_is_ordinary_inequality_and_reference_is_not_bound(view):
    with msv.demo["dialanine"] as other:
        assert view.addons.molsysmt.compare(other.molsys, n_atoms=True) is False
        assert other.addons.molsysmt.compare(view.molsys, n_atoms=True) is False
        assert view.addons.molsysmt.compare(
            other.molsys, atom_name=True
        ) == msm.compare(view.molsys, other.molsys, atom_name=True)


@pytest.mark.parametrize("trusted", [False, True])
def test_forced_topology_rebuild_rejects_before_mutating_either_input(view, trusted):
    reference = msm.copy(view.molsys)
    original = view.molsys
    original.chemical_states._resolve_chemical_state().components.loc[
        :, "component_name"
    ] = "PRIMARY MARKER"
    reference.chemical_states._resolve_chemical_state().components.loc[
        :, "component_name"
    ] = "REFERENCE MARKER"
    before = [
        (
            item,
            item.chemical_states._resolve_chemical_state().components,
            item.chemical_states._resolve_chemical_state().components.copy(deep=True),
            item.interactions["received"],
        )
        for item in (original, reference)
    ]
    status = view.addons.molsysmt.get_sync_status()
    with pytest.raises(NotImplementedError, match="rebuilds topology in both systems"):
        view.addons.molsysmt.compare(
            reference, redefine_indices=True, skip_digestion=trusted
        )
    assert view.molsys is original
    for item, components, snapshot, analysis in before:
        assert item.chemical_states._resolve_chemical_state().components is components
        assert components.equals(snapshot)
        assert item.interactions["received"] is analysis
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize(
    "name, arguments",
    [
        ("contains", {"n_atomz": True}),
        ("is_composed_of", {"n_atomz": 3}),
        ("compare", {"n_atomz": True}),
        ("compare", {"rule": "in"}),
        ("compare", {"redefine_indices": "yes"}),
        ("compare", {"structure_indices_2": [10000], "coordinates": True}),
    ],
)
def test_native_errors_are_not_replaced_by_fallback_results(view, name, arguments):
    extra = (view.molsys,) if name == "compare" else ()
    with pytest.raises(Exception) as native:
        getattr(msm.basic, name)(view.molsys, *extra, **arguments)
    before = view.addons.molsysmt.get_sync_status()
    with pytest.raises(type(native.value)):
        getattr(view.addons.molsysmt, name)(*extra, **arguments)
    assert view.addons.molsysmt.get_sync_status() == before


def test_primary_override_is_rejected(view):
    tools = view.addons.molsysmt
    for name, extra in [
        ("contains", ()),
        ("is_composed_of", ()),
        ("compare", (view.molsys,)),
    ]:
        with pytest.raises(TypeError, match="bound to view.molsys"):
            getattr(tools, name)(*extra, molecular_system=view.molsys)


def test_pending_data_is_queried_without_synchronizing_or_recalculating(view):
    tools = view.addons.molsysmt
    coordinates = msm.get(
        view.molsys, element="atom", structure_indices=[0], coordinates=True
    )
    tools.set(
        structure_indices=[0],
        coordinates=coordinates + puw.quantity(0.1, "nm"),
        update_view=False,
    )
    reference = msm.copy(view.molsys)
    before = tools.get_sync_status()
    analysis = view.molsys.interactions["received"]
    assert tools.contains(n_atoms=1) == msm.contains(view.molsys, n_atoms=1)
    assert tools.is_composed_of(n_atoms=view.molsys.get_n_atoms()) is True
    assert tools.compare(reference, coordinates=True) is True
    assert tools.get_sync_status() == before
    assert before["state"] == "pending"
    assert view.molsys.interactions["received"] is analysis
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [1, 2])


def test_cached_tools_follow_load_and_close_without_changing_reference(view):
    tools = view.addons.molsysmt
    reference = msm.copy(view.molsys)
    predicate = tools.contains
    composition = tools.is_composed_of
    compare = tools.compare
    count = reference.get_n_atoms()
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    assert predicate(n_atoms=count) is False
    assert composition(n_atoms=view.molsys.get_n_atoms()) is True
    assert compare(reference, n_atoms=True) is False
    assert reference.get_n_atoms() == count
    view.addons.manager.disable("molsysmt")
    assert predicate(n_atoms=1) is True
    view.close()
    for method, extra in [(predicate, ()), (composition, ()), (compare, (reference,))]:
        with pytest.raises(RuntimeError, match="closed view"):
            method(*extra, skip_digestion=True)


@pytest.mark.parametrize("name", ["contains", "is_composed_of", "compare"])
def test_empty_view_rejects_bound_queries(view, name):
    with msv.MolSysView() as empty:
        extra = (view.molsys,) if name == "compare" else ()
        with pytest.raises(ValueError, match="Load a molecular system"):
            getattr(empty.addons.molsysmt, name)(*extra)


def test_explicit_alias_and_canonical_default_still_collide(view):
    options = dict(attribute_type=None, attributes_type="topological")
    with pytest.raises(Exception) as native:
        msm.compare(view.molsys, view.molsys, **options)
    before = view.addons.molsysmt.get_sync_status()
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.compare(view.molsys, **options)
    assert view.addons.molsysmt.get_sync_status() == before
