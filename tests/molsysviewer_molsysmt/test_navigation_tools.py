"""Receive independent visualization and exact historical callable aliases."""

import inspect
from importlib import import_module

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import NotImplementedMethodError
from tests.molsysviewer_molsysmt.test_build_assignment_tools import snapshot, unchanged
from tests.molsysviewer_molsysmt.test_hbond_site_tools import same
from tests.molsysviewer_molsysmt.test_interaction_detector_tools import hbond_system

puw = msm.pyunitwizard
HISTORICAL = (
    "get_donor_atoms",
    "get_acceptor_atoms",
    "get_buch_hbonds",
    "get_luzard_chandler_hbonds",
)


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as view:
        view.regions.add(selection=[0, 2], tag="parent-only")
        view.shapes.add_sphere(atom_indices=[1], tag="parent-anchor")
        yield view


def test_view_signature_help_native_root_alias_and_digestion(view):
    call = view.addons.molsysmt.basic.view
    native = inspect.signature(msm.basic.view)
    assert inspect.signature(call) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert call.digestion_plan is not None
    assert view.addons.molsysmt.view == call
    assert "view" in dir(view.addons.molsysmt.basic)
    assert "current view.molsys" in inspect.getdoc(call)
    assert "not a clone" in inspect.getdoc(call)
    for name in inspect.signature(call).parameters:
        assert f"{name} :" in inspect.getdoc(call)
    for key in ("molecular_system", "update_view", "in_place"):
        with pytest.raises(UnknownArgumentError):
            call(**{key: None})


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "syntax,selection",
    [
        ("MolSysMT", [0, 2, 4]),
        ("MolSysMT", "atom_index in [0,2,4]"),
        ("MDTraj", "index 0 2 4"),
    ],
)
def test_view_keeps_requested_atoms_repeated_structure_order_and_parent(
    view, skip, syntax, selection
):
    view.player.go_to_structure(7)
    before = snapshot(view)
    structures = [8, 3, 8]
    expected = puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
        structures
    ][:, [0, 2, 4]]
    with view.addons.molsysmt.basic.view(
        selection=selection,
        structure_indices=structures,
        syntax=syntax,
        skip_digestion=skip,
    ) as result:
        assert isinstance(result, msv.MolSysView)
        assert result is not view and result.molsys is not view.molsys
        assert result.molsys.get_n_atoms() == 3
        np.testing.assert_array_equal(
            puw.get_value(result.molsys.structures.coordinates, to_unit="nm"), expected
        )
        assert not result.regions and result.shapes.count() == 0
        assert len(result.history._undo) == 0
        msm.set(result.molsys, coordinates=puw.quantity(np.zeros_like(expected), "nm"))
        unchanged(view, before)
    unchanged(view, before)


def test_view_uses_pending_primary_without_sync_and_has_independent_lifetime(view):
    tools = view.addons.molsysmt
    call = tools.basic.view
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    child = call(selection=[0, 2], structure_indices=[2, 0])
    try:
        np.testing.assert_array_equal(
            puw.get_value(child.molsys.structures.coordinates, to_unit="nm"),
            puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[[2, 0]][
                :, [0, 2]
            ],
        )
        unchanged(view, before)
        view.close()
        assert not child.closed
        with pytest.raises(RuntimeError, match="closed view"):
            call()
    finally:
        child.close()


def test_cached_view_rebinds_to_replacement_and_empty_native_input(view):
    call = view.addons.molsysmt.basic.view
    replacement = msm.extract(view.molsys, selection=[0, 2], structure_indices=[1])
    view.load(replacement, mode="replace")
    before = snapshot(view)
    with call() as child:
        assert (
            child.molsys.get_n_atoms() == 2
            and child.molsys.structures.n_structures == 1
        )
    unchanged(view, before)
    with msv.new_view() as empty:
        before = snapshot(empty)
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.basic.view()
        unchanged(empty, before)


@pytest.mark.parametrize(
    "parameters",
    [{"selection": [-1]}, {"structure_indices": [10000]}, {"viewer": "unavailable"}],
)
@pytest.mark.parametrize("skip", [False, True])
def test_view_native_rejections_preserve_source(view, parameters, skip):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.basic.view(view.molsys, **parameters, skip_digestion=skip)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.basic.view(**parameters, skip_digestion=skip)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize("name", HISTORICAL)
def test_legacy_namespace_is_exact_canonical_bound_alias(view, name):
    tools = view.addons.molsysmt
    alias = getattr(tools.hbonds, name)
    canonical = getattr(tools.interactions.hbonds, name)
    assert alias == canonical and alias.__self__ is canonical.__self__
    assert alias.__func__ is canonical.__func__
    assert inspect.signature(alias) == inspect.signature(canonical)
    assert alias.digestion_plan is canonical.digestion_plan
    assert getattr(msm.hbonds, name) is getattr(msm.interactions.hbonds, name)
    assert set(dir(tools.hbonds)) == set(HISTORICAL)
    for unavailable in (
        "get_hbonds",
        "get_hbond_sites",
        "get_hbond_site_directions",
        "unreviewed",
    ):
        assert not hasattr(tools.hbonds, unavailable)


@pytest.mark.parametrize("name", HISTORICAL)
@pytest.mark.parametrize("skip", [False, True])
def test_legacy_calls_keep_scientific_parameters_and_native_result(name, skip):
    with msv.new_view(hbond_system()) as view:
        args = (
            {}
            if name in HISTORICAL[:2]
            else dict(
                structure_indices=[2, 0, 2],
                pbc=False,
                output_type="molsysmt.Interactions",
            )
        )
        before = snapshot(view)
        native_args = dict(args)
        if "skip_digestion" in inspect.signature(getattr(msm.hbonds, name)).parameters:
            native_args["skip_digestion"] = skip
        expected = getattr(msm.hbonds, name)(view.molsys, **native_args)
        actual = getattr(view.addons.molsysmt.hbonds, name)(**args, skip_digestion=skip)
        if isinstance(actual, msm.Interactions):
            same(actual.to_dict(), expected.to_dict())
        else:
            same(actual, expected)
        unchanged(view, before)


def test_cached_legacy_alias_rebinds_after_replacement_and_respects_pending_and_closed(
    view,
):
    call = view.addons.molsysmt.hbonds.get_acceptor_atoms
    view.load(hbond_system(), mode="replace")
    view.addons.molsysmt.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    same(call(), msm.hbonds.get_acceptor_atoms(view.molsys))
    unchanged(view, before)
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.hbonds.get_acceptor_atoms()


@pytest.mark.parametrize("name", ["run_NVT_equilibration", "run_NPT_equilibration"])
def test_native_dynamics_stubs_are_not_offered_as_available_tools(view, name):
    with pytest.raises(NotImplementedMethodError):
        getattr(import_module("molsysmt.molecular_dynamics"), name)(None)
    assert not hasattr(view.addons.molsysmt, "molecular_dynamics")
    assert "molecular_dynamics" not in dir(view.addons.molsysmt)
