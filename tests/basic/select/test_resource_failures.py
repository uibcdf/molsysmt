"""Preserve resource and process-control exceptions at the real public boundary."""

import errno
import importlib

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError

EXPRESSIONS = {
    "MolSysMT": "atom_index>=0",
    "MDTraj": "index >= 0",
    "MDAnalysis": "index 0",
}


@pytest.fixture
def one_atom():
    builder = msm.MolSysBuilder()
    builder.add_atom(atom_type="C", atom_name="control")
    builder.set_coordinates(msm.pyunitwizard.quantity([[[0, 0, 0]]], "nm"))
    return builder.build()


def resource_failure(kind):
    failure = (
        MemoryError("synthetic capacity failure")
        if kind == "memory"
        else OSError(errno.ENOMEM, "synthetic capacity failure")
    )
    failure.add_note("Original resource note")
    failure.__cause__ = RuntimeError("original resource cause")
    return failure


def inject_backend(monkeypatch, syntax, failure):
    selector = importlib.import_module("molsysmt.basic.selector")
    calls = []

    def injected(*args):
        calls.append(args)
        raise failure

    monkeypatch.setitem(selector._dict_select, syntax, injected)
    return calls


@pytest.mark.parametrize("kind", ["memory", "enomem"])
def test_original_plain_resource_failure_with_explicit_state(
    one_atom, monkeypatch, kind
):
    failure = (
        MemoryError("synthetic")
        if kind == "memory"
        else OSError(errno.ENOMEM, "synthetic")
    )
    calls = inject_backend(monkeypatch, "MolSysMT", failure)
    with pytest.raises(BaseException) as caught:
        msm.select(one_atom, "atom_index>=0", structure_indices=[0], chemical_state=0)
    assert len(calls) == 1
    assert caught.value is failure
    assert caught.value.__cause__ is None


@pytest.mark.parametrize("syntax", EXPRESSIONS)
@pytest.mark.parametrize("kind", ["memory", "enomem"])
def test_expression_backend_preserves_original_resource_object(
    one_atom, monkeypatch, syntax, kind
):
    failure = resource_failure(kind)
    cause = failure.__cause__
    calls = inject_backend(monkeypatch, syntax, failure)
    with pytest.raises(BaseException) as caught:
        msm.select(
            one_atom,
            EXPRESSIONS[syntax],
            structure_indices=[0],
            syntax=syntax,
            chemical_state=0 if syntax == "MolSysMT" else "reference",
        )
    assert len(calls) == 1
    assert caught.value is failure
    assert caught.value.__cause__ is cause
    assert "Original resource note" in caught.value.__notes__


@pytest.mark.parametrize("syntax", EXPRESSIONS)
@pytest.mark.parametrize("kind", ["interrupt", "exit"])
def test_expression_backend_preserves_process_control(
    one_atom, monkeypatch, syntax, kind
):
    failure = (
        KeyboardInterrupt("synthetic interrupt")
        if kind == "interrupt"
        else SystemExit(19)
    )
    calls = inject_backend(monkeypatch, syntax, failure)
    with pytest.raises(BaseException) as caught:
        msm.select(one_atom, EXPRESSIONS[syntax], syntax=syntax)
    assert len(calls) == 1
    assert caught.value is failure


@pytest.mark.parametrize("syntax", EXPRESSIONS)
@pytest.mark.parametrize("kind", ["value", "syntax", "other_oserror"])
def test_ordinary_parser_failures_keep_catalog_diagnostic_and_cause(
    one_atom, monkeypatch, syntax, kind
):
    failure = {
        "value": ValueError("synthetic invalid expression"),
        "syntax": SyntaxError("synthetic invalid expression"),
        "other_oserror": OSError(errno.ENOENT, "synthetic missing parser input"),
    }[kind]
    calls = inject_backend(monkeypatch, syntax, failure)
    with pytest.raises(msm.ArgumentError) as caught:
        msm.select(one_atom, EXPRESSIONS[syntax], syntax=syntax)
    assert len(calls) == 1
    assert caught.value.__cause__ is failure


@pytest.mark.parametrize("syntax", EXPRESSIONS)
@pytest.mark.parametrize("kind", ["argument", "catalog"])
def test_backend_catalog_errors_are_not_replaced(one_atom, monkeypatch, syntax, kind):
    failure = (
        msm.ArgumentError(
            argument="selection", value="synthetic", caller="molsysmt.select"
        )
        if kind == "argument"
        else StructuralInconsistencyError(reason="synthetic provider evidence failure")
    )
    calls = inject_backend(monkeypatch, syntax, failure)
    with pytest.raises(BaseException) as caught:
        msm.select(one_atom, EXPRESSIONS[syntax], syntax=syntax)
    assert len(calls) == 1
    assert caught.value is failure


@pytest.mark.parametrize("branch", ["inventory", "bond"])
@pytest.mark.parametrize("kind", ["memory", "enomem"])
def test_direct_evaluation_routes_preserve_resource_identity(
    one_atom, monkeypatch, branch, kind
):
    failure = resource_failure(kind)
    calls = []

    def injected(*args):
        calls.append(args)
        raise failure

    if branch == "inventory":
        module = importlib.import_module("molsysmt.basic.selector._group_inventory")
        monkeypatch.setattr(module, "select_inventory", injected)
        element, selection = "group", "group_index>=0"
    else:
        module = importlib.import_module("molsysmt.basic.selector.molsysmt")
        monkeypatch.setattr(module, "selection_uses_bond_attributes", lambda _: True)
        monkeypatch.setattr(module, "select_bonds_standard", injected)
        element, selection = "bond", "bond_order==1"
    with pytest.raises(BaseException) as caught:
        msm.select(one_atom, selection, element=element)
    assert len(calls) == 1
    assert caught.value is failure


@pytest.mark.parametrize("form", ["topology", "chemical_states", "h5msm"])
@pytest.mark.parametrize("kind", ["memory", "enomem"])
def test_resource_identity_does_not_depend_on_native_or_file_form(
    one_atom, monkeypatch, tmp_path, form, kind
):
    if form == "h5msm":
        source = str(tmp_path / "one_atom.h5msm")
        msm.h5msm.write(one_atom, source)
    else:
        source = getattr(one_atom, form)
    failure = resource_failure(kind)
    calls = inject_backend(monkeypatch, "MolSysMT", failure)
    with pytest.raises(BaseException) as caught:
        msm.select(source, "atom_index>=0")
    assert len(calls) == 1
    assert caught.value is failure


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj", "MDAnalysis"])
@pytest.mark.parametrize("kind", ["memory", "enomem"])
def test_actual_evaluator_preserves_resource_identity(
    one_atom, t4_h5msm_molsys, t4_pdb_file, monkeypatch, engine, kind
):
    failure = resource_failure(kind)
    calls = []

    def injected(*args, **kwargs):
        calls.append((args, kwargs))
        raise failure

    if engine == "MolSysMT":
        import pandas as pd

        monkeypatch.setattr(pd.DataFrame, "query", injected)
        source, selection = one_atom, 'atom_name=="control"'
    elif engine == "MDTraj":
        mdtraj = pytest.importorskip("mdtraj")
        monkeypatch.setattr(mdtraj.Topology, "select", injected)
        source, selection = t4_h5msm_molsys, "name CA"
    else:
        mda = pytest.importorskip("MDAnalysis")
        source = mda.Universe(t4_pdb_file)
        monkeypatch.setattr(mda.Universe, "select_atoms", injected)
        selection = "name CA"
    with pytest.raises(BaseException) as caught:
        msm.select(source, selection, syntax=engine)
    assert len(calls) == 1, repr(caught.value)
    assert caught.value is failure
