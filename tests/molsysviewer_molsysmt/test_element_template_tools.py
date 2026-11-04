"""Receive explicit reference data without molecular binding or preparation."""

import copy
import doctest
import inspect

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

BONDS = {
    "group.get_bonded_atom_pairs": {
        "group_name": "ALA",
        "atom_names": ["N", "CA", "C", "O", "CB"],
    },
    "group.amino_acid.get_bonded_atom_pairs": {
        "group_name": "ALA",
        "atom_names": ["N", "CA", "C", "O", "CB"],
    },
    "group.ion.get_bonded_atom_pairs": {
        "group_name": "SO4",
        "atom_names": ["S", "O1", "O2", "O3", "O4"],
    },
    "group.saccharide.get_bonded_atom_pairs": {
        "group_name": "NAG",
        "atom_names": ["C1", "C2", "C3"],
    },
    "group.small_molecule.get_bonded_atom_pairs": {
        "group_name": "ATP",
        "atom_names": ["PG", "O1G", "O2G"],
    },
    "group.terminal_capping.get_bonded_atom_pairs": {
        "group_name": "ACE",
        "atom_names": ["CH3", "C", "O"],
    },
    "group.water.get_bonded_atom_pairs": {"atom_names": ["O", "H1", "H2"]},
}
DATABASES = {
    "group.amino_acid.get_group_db": "ALA",
    "group.ion.get_group_db": "SO4",
    "group.saccharide.get_group_db": "NAG",
    "group.small_molecule.get_group_db": "ATP",
    "group.terminal_capping.get_group_db": "ACE",
}
ARGS = {
    **BONDS,
    **{path: {"group_name": value} for path, value in DATABASES.items()},
    "group.amino_acid.get_expected_heavy_atoms": {"group_name": "ALA"},
    "group.amino_acid.get_expected_hydrogens": {"group_name": "ALA"},
}
PATHS = tuple(ARGS)


def _path(root, path):
    for name in path.split("."):
        root = getattr(root, name)
    return root


def _equal(actual, expected):
    assert type(actual) is type(expected)
    if isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for name in expected:
            _equal(actual[name], expected[name])
    elif isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            _equal(left, right)
    elif isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
    else:
        assert actual == expected


def _outcome(function, parameters):
    try:
        return "result", function(**copy.deepcopy(parameters))
    except Exception as error:
        return "error", (type(error), str(error))


@pytest.fixture(params=["empty", "loaded"])
def view(request):
    with (
        msv.new_view() if request.param == "empty" else msv.demo["pentalanine"]
    ) as owner:
        yield owner


@pytest.mark.parametrize("path", PATHS)
def test_native_signatures_discovery_help_and_validation(path):
    with msv.new_view() as view:
        native = _path(msm.element, path)
        method = _path(view.addons.molsysmt.element, path)
        parameters = list(inspect.signature(native).parameters.values())
        if "skip_digestion" not in inspect.signature(native).parameters:
            parameters.append(
                inspect.Parameter(
                    "skip_digestion", inspect.Parameter.KEYWORD_ONLY, default=False
                )
            )
        assert list(inspect.signature(method).parameters.values()) == parameters
        assert method.digestion_plan is not None
        help_text = inspect.getdoc(method)
        assert "Works with an open empty view" in help_text
        assert "Reference templates" in help_text
        assert "\nmolecular_system :" not in help_text
        for parameter in parameters:
            assert f"{parameter.name} :" in help_text
        assert path.rsplit(".", 1)[1] in dir(
            _path(view.addons.molsysmt.element, path.rsplit(".", 1)[0])
        )
        assert not hasattr(view.addons.molsysmt, path.rsplit(".", 1)[1])
        with pytest.raises(UnknownArgumentError):
            method(**ARGS[path], molecular_system=None)
        with pytest.raises(ArgumentError):
            method(**ARGS[path], skip_digestion="yes")


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize("skip", [False, True])
def test_explicit_queries_keep_native_results_and_caller_inputs(view, path, skip):
    native = _path(msm.element, path)
    method = _path(view.addons.molsysmt.element, path)
    parameters = copy.deepcopy(ARGS[path])
    before = copy.deepcopy(parameters)
    target = view.molsys
    native_parameters = copy.deepcopy(parameters)
    if "skip_digestion" in inspect.signature(native).parameters:
        native_parameters["skip_digestion"] = skip
    _equal(method(**parameters, skip_digestion=skip), native(**native_parameters))
    _equal(parameters, before)
    assert view.molsys is target


@pytest.mark.parametrize("path", BONDS)
@pytest.mark.parametrize("sorted_pairs", [False, True])
@pytest.mark.parametrize("indices", [None, [1040, 1009, 1030, 1007, 1012]])
def test_bonds_retain_explicit_nonconsecutive_index_mapping_and_order(
    view, path, sorted_pairs, indices
):
    parameters = copy.deepcopy(BONDS[path])
    n_atoms = len(parameters["atom_names"])
    parameters["atom_indices"] = None if indices is None else indices[:n_atoms]
    parameters["sorted"] = sorted_pairs
    method = _path(view.addons.molsysmt.element, path)
    result = method(**parameters)
    _equal(result, _path(msm.element, path)(**parameters))
    labels = list(range(n_atoms)) if indices is None else indices[:n_atoms]
    assert len(result) > 0
    assert all(len(pair) == 2 and set(pair) <= set(labels) for pair in result)
    if sorted_pairs:
        assert result == sorted(result)


@pytest.mark.parametrize("path", BONDS)
@pytest.mark.parametrize("container", [tuple, np.asarray])
def test_native_container_and_error_behavior_is_not_silently_normalized(
    view, path, container
):
    parameters = copy.deepcopy(BONDS[path])
    parameters["atom_names"] = container(parameters["atom_names"])
    _equal(
        _outcome(_path(view.addons.molsysmt.element, path), parameters),
        _outcome(_path(msm.element, path), parameters),
    )


@pytest.mark.parametrize("path", DATABASES)
def test_reference_database_is_independent_and_not_cached_or_assigned(view, path):
    method = _path(view.addons.molsysmt.element, path)
    result = method(DATABASES[path])
    expected = copy.deepcopy(result)
    assert isinstance(result, dict)
    assert len(result) > 0
    result.clear()
    _equal(method(DATABASES[path]), expected)
    _equal(_path(msm.element, path)(DATABASES[path]), expected)


@pytest.mark.parametrize(
    "path", [p for p in PATHS if p != "group.water.get_bonded_atom_pairs"]
)
@pytest.mark.parametrize("name", ["not-a-known-name", "", "ala"])
def test_native_unknown_name_and_case_contracts_remain_visible(view, path, name):
    parameters = copy.deepcopy(ARGS[path])
    parameters["group_name"] = name
    _equal(
        _outcome(_path(view.addons.molsysmt.element, path), parameters),
        _outcome(_path(msm.element, path), parameters),
    )


@pytest.mark.parametrize(
    "name,present",
    [
        ("ALA", None),
        ("ALA", ["N", "CA", "C", "O", "CB"]),
        ("MSE", ["SE"]),
        ("MLY", None),
        ("PTR", None),
    ],
)
def test_expected_heavy_atoms_retain_template_context_and_container(
    view, name, present
):
    method = view.addons.molsysmt.element.group.amino_acid.get_expected_heavy_atoms
    result = method(name, present_atom_names=present)
    _equal(
        result,
        msm.element.group.amino_acid.get_expected_heavy_atoms(
            name, present_atom_names=present
        ),
    )
    assert result is None or isinstance(result, set)
    if name == "MSE":
        assert "SE" in result
    if name == "ALA" and present is not None:
        assert result == set(present)


@pytest.mark.parametrize("name", ["ASP", "GLU", "HIS", "LYS", "CYS", "PRO", "ALA"])
@pytest.mark.parametrize(
    "context",
    [
        dict(pH=2.0),
        dict(pH=7.4),
        dict(pH=12.0),
        dict(pH=2.0, is_n_terminal=True, is_c_terminal=True),
        dict(is_disulfide=True),
    ],
)
def test_expected_hydrogen_context_is_explicit_and_preserved(view, name, context):
    method = view.addons.molsysmt.element.group.amino_acid.get_expected_hydrogens
    parameters = {
        "group_name": name,
        "present_atom_names": ["N", "CA", "C", "O"],
        **context,
    }
    _equal(
        method(**parameters),
        msm.element.group.amino_acid.get_expected_hydrogens(**parameters),
    )


def test_pending_edits_scene_history_and_primary_are_untouched():
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
        for path, parameters in ARGS.items():
            _equal(
                _path(tools.element, path)(**parameters),
                _path(msm.element, path)(**parameters),
            )
        assert view.molsys is target
        assert tools.get_sync_status() == status
        assert view.widget.initial_messages == messages
        assert (view.history._undo, view.history._redo) == history


@pytest.mark.parametrize("path", PATHS)
def test_cached_handles_are_independent_of_replacement_and_reject_closed_view(path):
    with msv.new_view() as other:
        first = msv.new_view()
        method = _path(first.addons.molsysmt.element, path)
        expected = method(**ARGS[path])
        with msv.demo["dialanine"] as source:
            first.load(source.molsys, mode="replace")
        _equal(method(**ARGS[path]), expected)
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            method(**ARGS[path], skip_digestion=True)
        _equal(_path(other.addons.molsysmt.element, path)(**ARGS[path]), expected)
        assert other.molsys is None


def test_inherited_expected_heavy_atom_examples_are_executable():
    with msv.new_view() as view:
        native = msm.element.group.amino_acid.get_expected_heavy_atoms
        doc = inspect.getdoc(
            view.addons.molsysmt.element.group.amino_acid.get_expected_heavy_atoms
        )
        example = doctest.DocTestParser().get_doctest(
            doc, {"get_expected_heavy_atoms": native}, "addon-heavy-atoms", None, 0
        )
        result = doctest.DocTestRunner().run(example)
        assert result.attempted == 5
        assert result.failed == 0
