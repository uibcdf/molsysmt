"""Receive stable molecule/group queries and state-local component projections."""

import copy
import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys

PATHS = tuple(
    f"{scope}.{name}"
    for scope, names in {
        "component": [
            "get_component_index",
            "get_component_id",
            "get_component_name",
            "get_component_type",
            "get_n_components",
        ],
        "molecule": [
            "get_molecule_index",
            "get_molecule_id",
            "get_molecule_name",
            "get_molecule_type",
            "get_n_molecules",
        ],
        "group": ["get_group_type"],
    }.items()
    for name in names
)
LEGACY = "group.small_molecule.small_molecule_is_amino_acid"
LOCAL = {"molecule.get_n_molecules", LEGACY}


def _method(root, path):
    for part in path.split("."):
        root = getattr(root, part)
    return root


def _equal(actual, expected):
    assert type(actual) is type(expected)
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
    elif isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected)
        for first, second in zip(actual, expected):
            _equal(first, second)
    elif expected is pd.NA:
        assert actual is pd.NA
    else:
        assert actual == expected


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as owner:
        yield owner


@pytest.mark.parametrize("path", (*PATHS, LEGACY))
def test_exact_binding_signatures_help_and_skip_controls(view, path):
    native = _method(msm.element, path)
    method = _method(view.addons.molsysmt.element, path)
    parameters = list(inspect.signature(native).parameters.values())[1:]
    if path in LOCAL:
        parameters.append(
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            )
        )
    assert list(inspect.signature(method).parameters.values()) == parameters
    assert method.digestion_plan is not None
    assert "current" in inspect.getdoc(method)
    assert "\nmolecular_system :" not in inspect.getdoc(method)
    assert "update_view" not in inspect.signature(method).parameters
    assert not hasattr(view.addons.molsysmt, path.split(".")[-1])
    for parameter in parameters:
        assert f"{parameter.name} :" in inspect.getdoc(method)
    args = ("ATP",) if path == LEGACY else ()
    with pytest.raises(UnknownArgumentError):
        method(*args, molecular_system=view.molsys)
    with pytest.raises(ArgumentError):
        method(*args, skip_digestion="yes")


@pytest.mark.parametrize("path", (*PATHS, LEGACY))
@pytest.mark.parametrize("skip", [False, True])
def test_native_defaults_and_skip_forwarding(view, path, skip):
    arguments = {} if path in LOCAL else {"skip_digestion": skip}
    if path == LEGACY:
        arguments["group_name"] = "ATP"
    expected = _method(msm.element, path)(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(
        **{**arguments, "skip_digestion": skip}
    )
    _equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("selection", [[2, 0], [], "atom_index==0"])
def test_numeric_empty_and_native_text_selections(view, path, selection):
    arguments = {"selection": selection}
    if not path.split(".")[-1].startswith("get_n_"):
        arguments["element"] = "atom"
    expected = _method(msm.element, path)(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(**arguments)
    _equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
def test_explicit_mdtraj_syntax_is_not_rewritten(view, path):
    arguments = {"selection": "index 0", "syntax": "MDTraj"}
    if not path.split(".")[-1].startswith("get_n_"):
        arguments["element"] = "atom"
    expected = _method(msm.element, path)(view.molsys, **arguments)
    actual = _method(view.addons.molsysmt.element, path)(**arguments)
    _equal(actual, expected)


@pytest.mark.parametrize("path", PATHS)
def test_projection_flags_leave_stable_and_chemical_tables_unchanged(view, path):
    native = _method(msm.element, path)
    flags = [
        name
        for name in inspect.signature(native).parameters
        if name.startswith("redefine_")
    ]
    stable = {
        name: getattr(view.molsys.topology, name).copy(deep=True)
        for name in ["atoms", "groups", "molecules", "chains", "entities"]
    }
    chemistry = copy.deepcopy(view.molsys.chemical_states)
    scene = view.export_state()
    for active in [*flags, "all"]:
        arguments = {flag: active in {flag, "all"} for flag in flags}
        expected = native(view.molsys, **arguments)
        actual = _method(view.addons.molsysmt.element, path)(**arguments)
        _equal(actual, expected)
        for name, table in stable.items():
            pd.testing.assert_frame_equal(getattr(view.molsys.topology, name), table)
        assert view.molsys.chemical_states._inventory_equals(chemistry)
        assert view.export_state() == scene


@pytest.mark.parametrize("path", PATHS)
def test_invalid_atom_selection_retains_native_rejection(view, path):
    arguments = {"selection": [1000000]}
    if not path.split(".")[-1].startswith("get_n_"):
        arguments["element"] = "atom"
    with pytest.raises(Exception) as error:
        _method(msm.element, path)(view.molsys, **arguments)
    with pytest.raises(type(error.value)):
        _method(view.addons.molsysmt.element, path)(**arguments)


@pytest.mark.parametrize("path", (*PATHS, LEGACY))
def test_empty_owner_closed_owner_and_current_replacement(path):
    args = ("ATP",) if path == LEGACY else ()
    with msv.new_view() as empty:
        method = _method(empty.addons.molsysmt.element, path)
        with pytest.raises(ValueError, match="Load a molecular system"):
            method(*args)
    with pytest.raises(RuntimeError, match="closed view"):
        method(*args, skip_digestion=True)
    with msv.demo["pentalanine"] as first, msv.demo["dialanine"] as second:
        method = _method(first.addons.molsysmt.element, path)
        merged = msm.merge(
            [first.molsys, second.molsys],
            structure_indices=np.array([0], dtype=np.int64),
        )
        first.load(merged, mode="replace")
        _equal(method(*args), _method(msm.element, path)(first.molsys, *args))
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            method(*args)
        _equal(
            _method(second.addons.molsysmt.element, path)(*args),
            _method(msm.element, path)(second.molsys, *args),
        )


def test_queries_do_not_flush_pending_native_edits(view):
    tools = view.addons.molsysmt
    tools.basic.set(
        coordinates=msm.get(view.molsys, coordinates=True), update_view=False
    )
    status = tools.get_sync_status()
    assert status["state"] == "pending"
    messages = copy.deepcopy(view.widget.initial_messages)
    history = (list(view.history._undo), list(view.history._redo))
    for path in (*PATHS, LEGACY):
        args = ("ATP",) if path == LEGACY else ()
        _equal(
            _method(tools.element, path)(*args),
            _method(msm.element, path)(view.molsys, *args),
        )
    assert tools.get_sync_status() == status
    assert view.widget.initial_messages == messages
    assert (view.history._undo, view.history._redo) == history


def test_components_do_not_redefine_stable_molecules(view):
    molsys = msm.copy(view.molsys)
    molsys.chemical_states.remove_bonds("all")
    with msv.new_view(molsys) as current:
        tools = current.addons.molsysmt.element
        n_atoms = current.molsys.topology.n_atoms
        assert tools.molecule.get_n_molecules() == 1
        assert tools.molecule.get_molecule_index() == [0]
        assert tools.component.get_n_components() == n_atoms
        np.testing.assert_array_equal(
            tools.component.get_component_index(element="atom"), np.arange(n_atoms)
        )
        assert current.molsys.topology.n_molecules == 1
        result = tools.component.get_component_index()
        result[0] = 1000000
        assert tools.component.get_component_index()[0] == 0


def test_absent_chemistry_is_not_repaired_by_stable_queries(view):
    # Build a real absent-domain probe; the ordinary setter rejects None.
    partial = MolSys._from_partial_domains(
        topology=view.molsys.topology.copy(),
        structures=view.molsys.structures.copy(),
    )
    with msv.new_view(partial) as current:
        before = current.export_state()
        for path in (*[p for p in PATHS if not p.startswith("component.")], LEGACY):
            args = ("ATP",) if path == LEGACY else ()
            _equal(
                _method(current.addons.molsysmt.element, path)(*args),
                _method(msm.element, path)(current.molsys, *args),
            )
        for path in [p for p in PATHS if p.startswith("component.")]:
            try:
                expected = _method(msm.element, path)(current.molsys)
            except Exception as error:
                with pytest.raises(type(error)):
                    _method(current.addons.molsysmt.element, path)()
            else:
                _equal(_method(current.addons.molsysmt.element, path)(), expected)
        assert current.molsys.chemical_states is None
        assert current.export_state() == before


def test_legacy_amino_acid_helper_remains_a_name_pattern(view):
    molsys = msm.copy(view.molsys)
    msm.set(molsys, element="group", selection=[1], group_name="ATP")
    with msv.new_view(molsys) as current:
        method = current.addons.molsysmt.element.group.small_molecule.small_molecule_is_amino_acid
        before = current.export_state()
        assert method("ATP") is True
        assert method("not-a-catalogued-name") is False
        assert method("ALA") is False
        assert "does not validate chemical connectivity" in inspect.getdoc(method)
        assert current.export_state() == before
