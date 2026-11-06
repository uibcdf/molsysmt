"""Receive current-system chain/entity queries without assigning projections."""

import copy
import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

PATHS = (
    "chain.get_chain_index",
    "chain.get_chain_id",
    "chain.get_chain_name",
    "chain.get_chain_type",
    "entity.get_entity_index",
    "entity.get_entity_id",
    "entity.get_entity_name",
    "entity.get_entity_type",
    "entity.get_n_entities",
)
LOCAL_SKIP = "entity.get_n_entities"


def _method(root, path):
    for part in path.split("."):
        root = getattr(root, part)
    return root


def _assert_equal(actual, expected):
    assert type(actual) is type(expected)
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        for first, second in zip(actual, expected):
            _assert_equal(first, second)
    elif expected is pd.NA:
        assert actual is pd.NA
    else:
        assert actual == expected


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as owner:
        yield owner


@pytest.mark.parametrize("path", PATHS)
def test_bound_signatures_help_discovery_and_validation(view, path):
    native = _method(msm.element, path)
    method = _method(view.addons.molsysmt.element, path)
    parameters = list(inspect.signature(native).parameters.values())[1:]
    if path == LOCAL_SKIP:
        parameters.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    assert list(inspect.signature(method).parameters.values()) == parameters
    assert method.digestion_plan is not None
    assert "current view.molsys" in inspect.getdoc(method)
    assert "serialized molecular reader" in inspect.getdoc(method)
    assert "\nmolecular_system :" not in inspect.getdoc(method)
    assert "update_view" not in inspect.signature(method).parameters
    assert not hasattr(view.addons.molsysmt, path.split(".")[-1])
    for parameter in parameters:
        assert f"{parameter.name} :" in inspect.getdoc(method)
    with pytest.raises(UnknownArgumentError):
        method(molecular_system=view.molsys)
    with pytest.raises(ArgumentError):
        method(skip_digestion="yes")


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("skip", [False, True])
def test_native_defaults_and_declared_skip_flags_remain_intact(view, path, skip):
    native = _method(msm.element, path)
    arguments = {} if path == LOCAL_SKIP else {"skip_digestion": skip}
    expected = native(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(skip_digestion=skip)
    _assert_equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("selection", [[2, 0], [], "atom_index==0"])
def test_explicit_selections_use_the_current_primary(view, path, selection):
    arguments = {"selection": selection}
    if path != LOCAL_SKIP:
        arguments["element"] = "atom"
    expected = _method(msm.element, path)(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(**arguments)
    _assert_equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
def test_mdtraj_syntax_is_forwarded_without_reinterpretation(view, path):
    arguments = {"selection": "index 0", "syntax": "MDTraj"}
    if path != LOCAL_SKIP:
        arguments["element"] = "atom"
    expected = _method(msm.element, path)(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(**arguments)
    _assert_equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
def test_native_projection_options_do_not_assign_or_change_scene(view, path):
    native = _method(msm.element, path)
    flags = [
        name
        for name in inspect.signature(native).parameters
        if name.startswith("redefine_")
    ]
    tables = {
        name: getattr(view.molsys.topology, name).copy(deep=True)
        for name in ["atoms", "groups", "molecules", "chains", "entities"]
    }
    scene = view.export_state()
    for active in [*flags, "all"]:
        arguments = {flag: active in {flag, "all"} for flag in flags}
        expected = native(view.molsys, **arguments)
        actual = _method(view.addons.molsysmt.element, path)(**arguments)
        _assert_equal(actual, expected)
        for name, before in tables.items():
            pd.testing.assert_frame_equal(getattr(view.molsys.topology, name), before)
        assert view.export_state() == scene


@pytest.mark.parametrize("path", PATHS)
def test_invalid_selection_retains_native_error(view, path):
    arguments = {"selection": [1000000]}
    if path != LOCAL_SKIP:
        arguments["element"] = "atom"
    with pytest.raises(Exception) as native:
        _method(msm.element, path)(view.molsys, **arguments)
    with pytest.raises(type(native.value)):
        _method(view.addons.molsysmt.element, path)(**arguments)


@pytest.mark.parametrize("path", PATHS)
def test_empty_closed_and_replaced_owners_are_distinct(path):
    with msv.new_view() as empty:
        method = _method(empty.addons.molsysmt.element, path)
        with pytest.raises(ValueError, match="Load a molecular system"):
            method()
    with pytest.raises(RuntimeError, match="closed view"):
        method(skip_digestion=True)
    with msv.demo["pentalanine"] as first, msv.demo["dialanine"] as second:
        method = _method(first.addons.molsysmt.element, path)
        first.load(second.molsys, mode="replace")
        _assert_equal(method(), _method(msm.element, path)(first.molsys))
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            method()
        _assert_equal(
            _method(second.addons.molsysmt.element, path)(),
            _method(msm.element, path)(second.molsys),
        )


def test_pending_edits_are_read_without_synchronization_or_history_effect(view):
    tools = view.addons.molsysmt
    tools.basic.set(
        coordinates=msm.get(view.molsys, coordinates=True), update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    messages = copy.deepcopy(view.widget.initial_messages)
    history = (list(view.history._undo), list(view.history._redo))
    target = view.molsys
    for path in PATHS:
        _assert_equal(
            _method(tools.element, path)(), _method(msm.element, path)(target)
        )
    assert tools.get_sync_status() == status
    assert view.molsys is target
    assert view.widget.initial_messages == messages
    assert (view.history._undo, view.history._redo) == history


def test_literal_single_chain_and_entity_results_are_independent(view):
    tools = view.addons.molsysmt.element
    n_atoms = view.molsys.topology.n_atoms
    indices = tools.chain.get_chain_index()
    assert indices == [0] * n_atoms
    assert tools.chain.get_chain_index(element="chain") == [0]
    assert tools.entity.get_entity_index() == [0]
    assert tools.entity.get_n_entities() == 1
    assert tools.entity.get_entity_index(element="atom") == [0] * n_atoms
    indices[0] = 1000
    assert tools.chain.get_chain_index()[0] == 0


def test_multiple_declared_chains_and_entities_keep_native_membership():
    with msv.demo["pentalanine"] as first, msv.demo["dialanine"] as second:
        merged = msm.merge(
            [first.molsys, second.molsys],
            structure_indices=np.array([0], dtype=np.int64),
        )
        with msv.new_view(merged) as view:
            tools = view.addons.molsysmt.element
            assert tools.chain.get_chain_index(element="chain") == [0, 1]
            assert tools.entity.get_entity_index() == [0, 1]
            assert tools.entity.get_n_entities() == 2
            for path in PATHS:
                _assert_equal(
                    _method(tools, path)(), _method(msm.element, path)(view.molsys)
                )
