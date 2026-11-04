"""Receive explicit name classifiers without molecular binding or hidden normalization."""

import copy
import doctest
import inspect
import subprocess
import sys

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

PATHS = (
    "component.is_component_type",
    "molecule.is_molecule_type",
    "group.amino_acid.get_1_letter_code_from_name",
    "group.amino_acid.get_standard_name",
    "group.amino_acid.is_amino_acid",
    "group.ion.is_ion",
    "group.lipid.is_lipid",
    "group.nucleotide.is_nucleotide",
    "group.saccharide.is_saccharide",
    "group.small_molecule.is_small_molecule",
    "group.terminal_capping.is_c_terminal_capping",
    "group.terminal_capping.is_n_terminal_capping",
    "group.terminal_capping.is_terminal_capping",
    "group.water.is_water",
)
ARGS = dict(
    zip(
        PATHS,
        [
            "peptide",
            "waters",
            "MSE",
            "MSE",
            "ALA",
            "NA",
            "POPC",
            "DA",
            "NAG",
            "ATP",
            "ACE",
            "NME",
            "ACE",
            "HOH",
        ],
    )
)


def _path(root, path):
    for name in path.split("."):
        root = getattr(root, name)
    return root


def _outcome(function, value, **parameters):
    try:
        result = function(value, **parameters)
        return "result", type(result), result
    except Exception as error:
        return "error", type(error), str(error)


@pytest.fixture(params=["empty", "loaded"])
def view(request):
    with (
        msv.new_view() if request.param == "empty" else msv.demo["pentalanine"]
    ) as owner:
        yield owner


@pytest.mark.parametrize("path", PATHS)
def test_exact_signatures_discovery_help_and_keyword_only_control(path):
    with msv.new_view() as view:
        native = _path(msm.element, path)
        method = _path(view.addons.molsysmt.element, path)
        expected = [
            *inspect.signature(native).parameters.values(),
            inspect.Parameter(
                "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
            ),
        ]
        assert list(inspect.signature(method).parameters.values()) == expected
        assert method.digestion_plan is not None
        assert "Works with an open empty view" in inspect.getdoc(method)
        assert "not forwarded" in inspect.getdoc(method)
        if path.endswith("get_1_letter_code_from_name"):
            assert "MolSysMT#545" in inspect.getdoc(method)
        if path.endswith(("is_n_terminal_capping", "is_c_terminal_capping")):
            assert "MolSysMT#547" in inspect.getdoc(method)
        assert "\nmolecular_system :" not in inspect.getdoc(method)
        for parameter in expected:
            assert f"{parameter.name} :" in inspect.getdoc(method)
        assert path.split(".")[-1] in dir(
            _path(view.addons.molsysmt.element, path.rsplit(".", 1)[0])
        )
        assert not hasattr(view.addons.molsysmt, path.split(".")[-1])
        with pytest.raises(UnknownArgumentError):
            method(ARGS[path], molecular_system=None)
        with pytest.raises(ArgumentError):
            method(ARGS[path], skip_digestion="yes")


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("skip", [False, True])
def test_native_scalar_behavior_and_unmodified_explicit_inputs(view, path, skip):
    native = _path(msm.element, path)
    method = _path(view.addons.molsysmt.element, path)
    target = view.molsys
    for value in [
        ARGS[path],
        np.str_(ARGS[path]),
        "",
        "not-a-known-name",
        ARGS[path].lower(),
        None,
        [],
        {},
    ]:
        assert _outcome(method, value, skip_digestion=skip) == _outcome(native, value)
    assert view.molsys is target


@pytest.mark.parametrize("path", PATHS)
def test_sampled_native_catalogues_and_canonical_aliases(view, path):
    native = _path(msm.element, path)
    method = _path(view.addons.molsysmt.element, path)
    if path.startswith("component."):
        values = msm.element.component._component_types
    elif path.startswith("molecule."):
        values = msm.element.molecule._molecule_types
    elif path.startswith("group.amino_acid."):
        from molsysmt.element.group.amino_acid.group_types import name_to_type

        values = list(name_to_type)
    elif path == "group.lipid.is_lipid":
        from molsysmt.element.group.lipid.lipid_names import lipid_names

        values = list(lipid_names)
    elif path == "group.nucleotide.is_nucleotide":
        from molsysmt.element.group.nucleotide.nucleotide_names import nucleotide_names

        values = list(nucleotide_names)
    elif path == "group.water.is_water":
        from molsysmt.element.group.water.water_names import water_names

        values = list(water_names)
    else:
        namespace = _path(msm.element, path.rsplit(".", 1)[0])
        values = list(namespace.group_names)
    samples = (
        values if path.startswith("group.amino_acid.") else [*values[:25], *values[-5:]]
    )
    for value in samples:
        assert _outcome(method, value) == _outcome(native, value)


@pytest.mark.parametrize(
    "name,expected",
    [
        ("ALA", "A"),
        ("ARG", "R"),
        ("MSE", "M"),
        ("SEP", "S"),
        ("SEC", "U"),
        ("PYL", "O"),
        ("ASX", "B"),
        ("GLX", "Z"),
        ("UNK", "X"),
    ],
)
def test_literal_supported_one_letter_codes(view, name, expected):
    assert (
        view.addons.molsysmt.element.group.amino_acid.get_1_letter_code_from_name(name)
        == expected
    )


@pytest.mark.parametrize(
    "name,expected",
    [
        ("MSE", "MET"),
        ("SEP", "SER"),
        ("ALA", None),
        ("HOH", None),
        ("not-a-known-name", None),
    ],
)
def test_standard_name_lookup_keeps_native_none_convention(view, name, expected):
    assert (
        view.addons.molsysmt.element.group.amino_acid.get_standard_name(name)
        == expected
    )


@pytest.mark.parametrize("path", [p for p in PATHS if ".get_" not in p])
def test_catalogue_predicates_are_not_queries_of_the_loaded_system(view, path):
    method = _path(view.addons.molsysmt.element, path)
    assert method("not-a-known-name") is False
    assert type(method(ARGS[path])) is bool
    if path == "group.small_molecule.is_small_molecule":
        assert method("ATP") is True
        if view.molsys is not None:
            assert (
                view.addons.molsysmt.element.group.small_molecule.small_molecule_is_amino_acid(
                    "ATP"
                )
                is False
            )


def test_pending_molecular_edits_and_scene_history_remain_untouched():
    with msv.demo["pentalanine"] as view:
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
            assert _outcome(_path(tools.element, path), ARGS[path]) == _outcome(
                _path(msm.element, path), ARGS[path]
            )
        assert tools.get_sync_status() == status
        assert view.widget.initial_messages == messages
        assert view.molsys is target
        assert (view.history._undo, view.history._redo) == history


@pytest.mark.parametrize("path", PATHS)
def test_cached_utility_handles_ignore_replacement_but_reject_closed_owner(path):
    with msv.new_view() as other:
        first = msv.new_view()
        method = _path(first.addons.molsysmt.element, path)
        before = _outcome(method, ARGS[path])
        with msv.demo["dialanine"] as source:
            first.load(source.molsys, mode="replace")
        assert _outcome(method, ARGS[path]) == before
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            method(ARGS[path], skip_digestion=True)
        assert (
            _outcome(_path(other.addons.molsysmt.element, path), ARGS[path]) == before
        )
        assert other.molsys is None


def test_xle_gap_is_preserved_from_native_instead_of_repaired_in_the_facade(view):
    # MolSysMT#545 owns this source's missing XLE route. Accept its future fix.
    assert _outcome(
        view.addons.molsysmt.element.group.amino_acid.get_1_letter_code_from_name, "XLE"
    ) == _outcome(msm.element.group.amino_acid.get_1_letter_code_from_name, "XLE")


@pytest.mark.parametrize(
    "first_module",
    [
        "molsysmt.element.group.amino_acid",
        "molsysviewer",
        "molsysviewer_molsysmt.tools",
    ],
)
def test_cold_import_orders_keep_explicit_lookup_and_lifetime(first_module):
    program = f"""
import importlib
importlib.import_module({first_module!r})
import molsysviewer as msv
with msv.new_view() as view:
    element=view.addons.molsysmt.element
    assert element.group.water.is_water('HOH') is True
    assert element.group.amino_acid.get_standard_name('MSE') == 'MET'
    assert element.group.amino_acid.get_1_letter_code_from_name('SEC') == 'U'
    assert element.molecule.is_molecule_type('waters') is True
    assert view.molsys is None
print('label-import-order-ok')
"""
    result = subprocess.run(
        [sys.executable, "-c", program], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "label-import-order-ok" in result.stdout


def test_inherited_standard_name_examples_remain_executable():
    with msv.new_view() as view:
        native = msm.element.group.amino_acid.get_standard_name
        example = doctest.DocTestParser().get_doctest(
            inspect.getdoc(
                view.addons.molsysmt.element.group.amino_acid.get_standard_name
            ),
            {"get_standard_name": native},
            "addon-standard-name",
            None,
            0,
        )
        result = doctest.DocTestRunner().run(example)
        assert result.attempted == 4
        assert result.failed == 0
