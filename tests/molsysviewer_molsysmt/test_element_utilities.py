"""Receive explicit element utilities without borrowing a molecular system."""

import copy
import doctest
import inspect
import subprocess
import sys

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, UnknownAtomNameWarning

PATHS = (
    "is_element",
    "is_composed_of",
    "atom.is_atom_type",
    "atom.normalize_atom_types",
    "atom.get_atom_type_from_atom_name",
    "atom.get_atom_type_from_atom_ff_type",
    "group.is_group_type",
    "group.get_group_type_from_group_name",
)
LOCAL_SKIP = {
    "is_element",
    "is_composed_of",
    "atom.get_atom_type_from_atom_name",
    "group.is_group_type",
}
ARGS = {
    "is_element": ("atom",),
    "is_composed_of": ("group", "atom"),
    "atom.is_atom_type": ("Ca",),
    "atom.normalize_atom_types": ("D",),
    "atom.get_atom_type_from_atom_name": ("CA",),
    "atom.get_atom_type_from_atom_ff_type": ("HD",),
    "group.is_group_type": ("amino acid",),
    "group.get_group_type_from_group_name": ("ALA",),
}


def _path(namespace, path):
    for part in path.split("."):
        namespace = getattr(namespace, part)
    return namespace


def _outcome(function, *args, **kwargs):
    try:
        return "result", function(*args, **kwargs)
    except Exception as error:
        return "error", type(error)


@pytest.fixture(params=["empty", "loaded"])
def view(request):
    owner = msv.new_view() if request.param == "empty" else msv.demo["pentalanine"]
    with owner:
        yield owner


@pytest.mark.parametrize("path", PATHS)
def test_exact_names_signatures_help_and_validation(path):
    with msv.new_view() as view:
        assert "element" in dir(view.addons.molsysmt)
        tools = view.addons.molsysmt.element
        assert set(dir(tools)) == {
            "is_element",
            "is_composed_of",
            "atom",
            "group",
            "chain",
            "entity",
            "component",
            "molecule",
        }
        assert set(dir(tools.atom)) == {
            p.split(".")[1] for p in PATHS if p.startswith("atom.")
        }
        assert set(dir(tools.group)) == {
            "get_bonded_atom_pairs",
            "is_group_type",
            "get_group_type_from_group_name",
            "get_group_type",
            "small_molecule",
            "amino_acid",
            "ion",
            "lipid",
            "nucleotide",
            "saccharide",
            "terminal_capping",
            "water",
        }
        method, native = _path(tools, path), _path(msm.element, path)
        expected = inspect.signature(native)
        if path in LOCAL_SKIP:
            expected = expected.replace(
                parameters=[
                    *expected.parameters.values(),
                    inspect.Parameter(
                        "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
                    ),
                ]
            )
        assert inspect.signature(method) == expected
        assert method.digestion_plan is not None
        assert "open empty view" in inspect.getdoc(method)
        for parameter in expected.parameters:
            assert f"{parameter} :" in inspect.getdoc(method)
        assert "molecular_system" not in expected.parameters
        assert "update_view" not in expected.parameters
        if path == "is_composed_of":
            assert (
                view.addons.molsysmt.is_composed_of.__func__
                is view.addons.molsysmt.basic.is_composed_of.__func__
            )
            assert method.__func__ is not view.addons.molsysmt.is_composed_of.__func__
        else:
            assert not hasattr(view.addons.molsysmt, path.split(".")[-1])
        with pytest.raises(UnknownArgumentError):
            method(*ARGS[path], molecular_system=None)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "value,expected",
    [
        ("atom", True),
        ("groups", True),
        ("system", True),
        ("residues", True),
        ("Atom", False),
        ("unrecognized", False),
    ],
)
def test_element_names_keep_native_case_and_alias_semantics(
    view, skip, value, expected
):
    result = view.addons.molsysmt.element.is_element(value, skip_digestion=skip)
    assert result is expected
    assert result is msm.element.is_element(value)


@pytest.mark.parametrize(
    "first,second,expected",
    [
        ("system", "atoms", True),
        ("group", "atom", True),
        ("atom", "group", False),
        ("chain", "entity", True),
        ("chain", "chain", False),
    ],
)
def test_declared_composition_is_an_explicit_label_relation(
    view, first, second, expected
):
    assert view.addons.molsysmt.element.is_composed_of(first, second) is expected
    assert msm.element.is_composed_of(first, second) is expected


@pytest.mark.parametrize("skip", [False, True])
def test_atom_utilities_preserve_symbols_isotopes_shapes_and_inputs(view, skip):
    tools = view.addons.molsysmt.element.atom
    values = np.array(["Ca", "CA", "H", "D", "T", "Du", "Og"])
    saved = values.copy()
    result = tools.is_atom_type(values, skip)
    assert result.dtype == np.dtype(bool) and result.shape == (7,)
    np.testing.assert_array_equal(
        result, [True, False, True, False, False, False, True]
    )
    np.testing.assert_array_equal(result, msm.element.atom.is_atom_type(values, skip))
    np.testing.assert_array_equal(values, saved)
    result[0] = False
    assert tools.is_atom_type("Ca", skip) is True
    assert tools.is_atom_type([], skip).shape == (0,)
    symbols, isotopes = ["C", "D", "T", "Ca"], [13, None, 3, pd.NA]
    actual = tools.normalize_atom_types(symbols, isotopes, skip)
    assert actual == (["C", "H", "H", "Ca"], [13, 2, 3, None])
    assert actual == msm.element.atom.normalize_atom_types(symbols, isotopes, skip)
    assert (
        symbols == ["C", "D", "T", "Ca"]
        and isotopes[1] is None
        and isotopes[3] is pd.NA
    )
    actual[0][0] = "O"
    assert tools.normalize_atom_types(symbols, isotopes, skip)[0][0] == "C"
    assert tools.normalize_atom_types([], skip_digestion=skip) == ([], [])
    assert tools.normalize_atom_types("D", skip_digestion=skip) == ("H", 2)
    assert tools.get_atom_type_from_atom_name("CA", skip_digestion=skip) == "C"
    labels = ["A", "NA", "HD", "Cl"]
    assert tools.get_atom_type_from_atom_ff_type(labels, "autodock4", skip) == [
        "C",
        "N",
        "H",
        "Cl",
    ]
    assert labels == ["A", "NA", "HD", "Cl"]
    assert tools.get_atom_type_from_atom_ff_type([], skip_digestion=skip) == []


@pytest.mark.parametrize(
    "group_name,expected",
    [
        ("ALA", "amino acid"),
        ("HOH", "water"),
        ("ACE", "terminal capping"),
        (None, "unknown"),
        ("not-a-group", "unknown"),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_group_classification_calls_the_public_export(view, group_name, expected, skip):
    tools = view.addons.molsysmt.element.group
    assert tools.get_group_type_from_group_name(group_name, skip) == expected
    assert tools.get_group_type_from_group_name(
        group_name, skip
    ) == msm.element.group.get_group_type_from_group_name(group_name, skip)
    assert tools.is_group_type("amino acid", skip_digestion=skip) is True
    assert tools.is_group_type("amino_acid", skip_digestion=skip) is False


@pytest.mark.parametrize(
    "path,args,kwargs",
    [
        ("is_element", ([],), {}),
        ("is_composed_of", ([], "atom"), {}),
        ("group.is_group_type", ([],), {}),
        ("atom.is_atom_type", (12,), {}),
        ("atom.is_atom_type", ([["C"]],), {}),
        ("atom.normalize_atom_types", (["C", "H"],), {"isotope": [13]}),
        ("atom.normalize_atom_types", ("D",), {"isotope": 3}),
        ("atom.normalize_atom_types", ("C",), {"isotope": 0}),
        ("atom.get_atom_type_from_atom_ff_type", ("C",), {"typing_scheme": "unknown"}),
        ("atom.get_atom_type_from_atom_ff_type", ("CG0",), {}),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_native_rejections_are_not_translated_or_repaired(
    view, path, args, kwargs, skip
):
    extra = {**kwargs, "skip_digestion": skip}
    native_extra = kwargs if path in LOCAL_SKIP else extra
    assert _outcome(
        _path(view.addons.molsysmt.element, path), *args, **extra
    ) == _outcome(_path(msm.element, path), *args, **native_extra)


def test_unknown_atom_name_keeps_native_warning_and_marker(view):
    with pytest.warns(UnknownAtomNameWarning):
        assert (
            view.addons.molsysmt.element.atom.get_atom_type_from_atom_name("ZZ_unknown")
            == "UNK"
        )
    with pytest.warns(UnknownAtomNameWarning):
        assert msm.element.atom.get_atom_type_from_atom_name("ZZ_unknown") == "UNK"


@pytest.mark.parametrize("path", sorted(LOCAL_SKIP))
def test_addon_only_skip_control_remains_boolean(path):
    with msv.new_view() as view:
        with pytest.raises(ArgumentError) as error:
            _path(view.addons.molsysmt.element, path)(*ARGS[path], skip_digestion="yes")
        assert "skip_digestion" in str(error.value)


def test_explicit_utilities_do_not_flush_managed_edits_or_change_the_scene():
    with msv.demo["pentalanine"] as view:
        tools = view.addons.molsysmt
        tools.basic.set(
            coordinates=msm.get(view.molsys, coordinates=True), update_view=False
        )
        status = tools.get_sync_status()
        assert status["state"] == "pending"
        target = view.molsys
        coordinates = msm.pyunitwizard.get_value(
            msm.get(target, coordinates=True)
        ).copy()
        messages = copy.deepcopy(view.widget.initial_messages)
        history = (list(view.history._undo), list(view.history._redo))
        for path in PATHS:
            _path(tools.element, path)(*ARGS[path])
        assert tools.get_sync_status() == status
        assert view.molsys is target
        assert view.widget.initial_messages == messages
        assert (view.history._undo, view.history._redo) == history
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(msm.get(target, coordinates=True)), coordinates
        )


@pytest.mark.parametrize("path", PATHS)
def test_cached_methods_replacement_close_and_other_view_lifetime(path):
    with msv.new_view() as other:
        first = msv.new_view()
        method = _path(first.addons.molsysmt.element, path)
        expected = method(*ARGS[path])
        with msv.demo["dialanine"] as source:
            first.load(source.molsys, mode="replace")
        assert method(*ARGS[path]) == expected
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            method(*ARGS[path], skip_digestion=True)
        assert _path(other.addons.molsysmt.element, path)(*ARGS[path]) == expected
        assert other.molsys is None


@pytest.mark.parametrize("path", PATHS)
def test_inherited_native_examples_execute(path):
    with msv.new_view() as view:
        method = _path(view.addons.molsysmt.element, path)
        example = doctest.DocTestParser().get_doctest(
            inspect.getdoc(method), {}, path, None, 0
        )
        outcome = doctest.DocTestRunner().run(example)
        assert outcome.failed == 0
        if path in {
            "atom.is_atom_type",
            "atom.normalize_atom_types",
            "atom.get_atom_type_from_atom_ff_type",
        }:
            assert outcome.attempted > 0


@pytest.mark.parametrize(
    "first_module",
    ["molsysmt.element.atom", "molsysviewer", "molsysviewer_molsysmt.tools"],
)
def test_fresh_import_orders_preserve_native_exports_and_discovery(first_module):
    program = f"""
import importlib
importlib.import_module({first_module!r})
import molsysmt as msm
assert msm.element.atom.normalize_atom_types('D') == ('H', 2)
assert msm.element.group.get_group_type_from_group_name('ALA') == 'amino acid'
import molsysviewer as msv
with msv.new_view() as view:
    tools = view.addons.molsysmt.element
    assert tools.atom.normalize_atom_types('D') == ('H', 2)
    assert tools.group.get_group_type_from_group_name('ALA') == 'amino acid'
    assert tools.is_composed_of('group', 'atom') is True
    assert view.molsys is None
assert msm.element.atom.normalize_atom_types('D') == ('H', 2)
print('explicit-element-import-order-ok')
"""
    result = subprocess.run(
        [sys.executable, "-c", program],
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "explicit-element-import-order-ok" in result.stdout
