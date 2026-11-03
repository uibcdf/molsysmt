"""Receive attribute metadata without a primary system or hidden scene effects."""

import copy
import doctest
import importlib
import inspect
import os
import subprocess
import sys
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

NAMES = (
    "get_argument_aliases",
    "is_attribute",
    "is_chemical_state_attribute",
    "is_structural_attribute",
    "is_topological_attribute",
    "is_mechanical_attribute",
    "bonds_are_required_to_get_attribute",
)
PREDICATES = NAMES[2:6]
CASES = {
    "atom_index": (False, True, True, False),
    "coordinates": (False, True, False, False),
    "bond_order": (True, False, True, False),
    "formal_charge": (True, False, True, False),
    "forcefield": (False, False, False, True),
}
ROOT = Path(__file__).resolve().parents[2]


def _arguments(name):
    return () if name == "get_argument_aliases" else ("atom_index",)


def _outcome(function, *args, **kwargs):
    try:
        return "result", function(*args, **kwargs)
    except Exception as error:
        return "error", type(error)


@pytest.fixture(params=["empty", "loaded"])
def view(request):
    owner = msv.new_view() if request.param == "empty" else msv.demo["pentalanine"]
    try:
        yield owner
    finally:
        owner.close()


@pytest.mark.parametrize("name", NAMES)
def test_explicit_discovery_signatures_digestion_and_help(name):
    with msv.new_view() as view:
        facade = view.addons.molsysmt
        assert "attribute" in dir(facade)
        assert set(dir(facade.attribute)) == set(NAMES)
        method = getattr(facade.attribute, name)
        expected = inspect.signature(getattr(msm.attribute, name))
        if name in {"is_attribute", "get_argument_aliases"}:
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
        assert "molecular_system" not in expected.parameters
        assert "update_view" not in expected.parameters
        assert not hasattr(facade, name)


@pytest.mark.parametrize("attribute,expected", CASES.items())
@pytest.mark.parametrize("skip", [False, True])
def test_literal_classifications_overlap_and_native_parity(
    view, attribute, expected, skip
):
    tools = view.addons.molsysmt.attribute
    target, state, status = (
        view.molsys,
        view.export_state(),
        view.addons.molsysmt.get_sync_status(),
    )
    messages = copy.deepcopy(view.widget.initial_messages)
    assert tools.is_attribute(attribute, skip_digestion=skip) is True
    for name, literal in zip(PREDICATES, expected, strict=True):
        result = getattr(tools, name)(attribute, skip)
        assert result is literal
        assert result is getattr(msm.attribute, name)(attribute, skip)
    assert view.molsys is target
    assert view.export_state() == state
    assert view.widget.initial_messages == messages
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize(
    "value", ["not_an_attribute", "atom_names", None, 0, ["atom_name"]]
)
@pytest.mark.parametrize("skip", [False, True])
def test_membership_preserves_raw_names_values_and_native_errors(view, value, skip):
    actual = _outcome(
        view.addons.molsysmt.attribute.is_attribute, value, skip_digestion=skip
    )
    assert actual == _outcome(msm.attribute.is_attribute, value)
    if isinstance(value, str):
        assert actual == ("result", False)


@pytest.mark.parametrize("name", [*PREDICATES, "bonds_are_required_to_get_attribute"])
@pytest.mark.parametrize(
    "value", ["not_an_attribute", "atom_indices", None, ["atom_index"]]
)
@pytest.mark.parametrize("skip", [False, True])
def test_native_validated_and_bypassed_inputs_are_not_reinterpreted(name, value, skip):
    with msv.new_view() as view:
        assert _outcome(
            getattr(view.addons.molsysmt.attribute, name), value, skip_digestion=skip
        ) == _outcome(getattr(msm.attribute, name), value, skip_digestion=skip)


@pytest.mark.parametrize(
    "attribute", ["molecule_index", "molecule_id", "entity_index", "n_molecules"]
)
def test_stored_topology_queries_and_source_axis_requirements(view, attribute):
    tools = view.addons.molsysmt.attribute
    for source in (None, "atom", "group", "molecule", "chain", "entity", "system"):
        assert tools.bonds_are_required_to_get_attribute(attribute, source) is False
    for source in ("bond", "component"):
        assert tools.bonds_are_required_to_get_attribute(attribute, source) is True
    assert tools.bonds_are_required_to_get_attribute("bond_order") is True
    # The literal no-bond contract is useful on an actual stable domain too.
    with msv.demo["pentalanine"] as source:
        topology = source.molsys.topology
        values = msm.get(topology, element="atom", **{attribute: True})
        assert values is not None
        assert not hasattr(topology, "chemical_states")


def test_alias_contract_has_native_nested_independent_ownership(view):
    tools = view.addons.molsysmt.attribute
    expected = msm.attribute.get_argument_aliases()
    first = tools.get_argument_aliases()
    assert first == expected
    assert first["schema_version"] == 1
    assert first["attribute_synonyms"]["atom_names"] == "atom_name"
    assert first["element_attribute_aliases"]["group"]["name"] == "group_name"
    first["attribute_synonyms"]["invented"] = "atom_name"
    first["element_attribute_aliases"]["group"]["name"] = "atom_name"
    assert tools.get_argument_aliases() == expected
    assert tools.get_argument_aliases(skip_digestion=True) == expected
    assert msm.attribute.get_argument_aliases() == expected
    assert tools.is_attribute("atom_names") is False
    assert tools.is_attribute("invented") is False


@pytest.mark.parametrize("name", NAMES)
def test_invalid_integration_controls_and_unbound_keywords_preserve_scene(view, name):
    function = getattr(view.addons.molsysmt.attribute, name)
    args = _arguments(name)
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    for bad in (1, "True", None):
        with pytest.raises(ArgumentError):
            function(*args, skip_digestion=bad)
    for option in (
        {"molecular_system": view.molsys},
        {"selection": "all"},
        {"update_view": False},
    ):
        with pytest.raises(UnknownArgumentError):
            function(*args, **option)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


def test_metadata_does_not_flush_pending_edits_or_alter_primary_scene_and_history():
    with msv.demo["pentalanine"] as view:
        facade = view.addons.molsysmt
        facade.basic.set(
            coordinates=msm.get(view.molsys, coordinates=True), update_view=False
        )
        status = facade.get_sync_status()
        assert status["state"] == "pending"
        scene = copy.deepcopy(view.widget.initial_messages)
        history = (list(view.history._undo), list(view.history._redo))
        target = view.molsys
        coordinates = msm.pyunitwizard.get_value(
            msm.get(target, coordinates=True), to_unit="nm"
        ).copy()
        for name in NAMES:
            getattr(facade.attribute, name)(*_arguments(name))
        assert facade.get_sync_status() == status
        assert view.widget.initial_messages == scene
        assert (view.history._undo, view.history._redo) == history
        assert view.molsys is target
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(msm.get(target, coordinates=True), to_unit="nm"),
            coordinates,
        )


@pytest.mark.parametrize("name", NAMES)
def test_replacement_two_views_closed_handles_and_detached_results(name):
    first, other = msv.new_view(), msv.new_view()
    try:
        retained = getattr(first.addons.molsysmt.attribute, name)
        expected = retained(*_arguments(name))
        with msv.demo["dialanine"] as source:
            first.load(source.molsys, mode="replace")
        assert retained(*_arguments(name)) == expected
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            retained(*_arguments(name))
        assert (
            getattr(other.addons.molsysmt.attribute, name)(*_arguments(name))
            == expected
        )
        assert other.molsys is None
        if name == "get_argument_aliases":
            assert expected["schema_version"] == 1
    finally:
        first.close()
        other.close()


@pytest.mark.parametrize(
    "first_module",
    [
        "molsysmt._private.argdigest.normalization.attribute_synonyms",
        "molsysmt._private.argdigest.normalization.get_element_names",
        "molsysmt._private.argdigest.domain.attribute",
        "molsysmt.attribute",
        "molsysmt.attribute.get_argument_aliases",
        "molsysviewer_molsysmt._attribute",
    ],
)
def test_cold_import_orders_preserve_alias_collision_and_metadata(first_module):
    program = f"""
import importlib
importlib.import_module({first_module!r})
import molsysmt as msm
from argdigest import ArgumentConsistencyError, UnknownArgumentError
def check_native():
    try:
        msm.get(None, atom_names=True, atom_name=False)
    except ArgumentConsistencyError:
        pass
    else:
        raise AssertionError('alias collision was not rejected')
    try:
        msm.get(None, definitely_unknown=True)
    except UnknownArgumentError:
        pass
    else:
        raise AssertionError('unknown native keyword was accepted')
check_native()
import molsysviewer as msv
from pathlib import Path
assert Path(msv.__file__).resolve() == Path({str(Path(msv.__file__))!r}).resolve()
with msv.new_view() as view:
    tools = view.addons.molsysmt.attribute
    assert tools.get_argument_aliases() == msm.attribute.get_argument_aliases()
    assert tools.is_attribute('atom_name') is True
    assert tools.is_attribute('atom_names') is False
    assert tools.is_topological_attribute('bond_order') is True
    assert tools.is_chemical_state_attribute('bond_order') is True
    assert tools.is_structural_attribute('atom_index') is True
    assert tools.is_mechanical_attribute('forcefield') is True
    assert tools.bonds_are_required_to_get_attribute('molecule_index', 'atom') is False
    check_native()
check_native()
"""
    env = dict(
        os.environ,
        PYTHONPATH=os.pathsep.join([str(ROOT), str(Path(msv.__file__).parents[1])]),
    )
    result = subprocess.run(
        [sys.executable, "-c", program],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_real_public_method_help_examples():
    module = importlib.import_module("molsysviewer_molsysmt._attribute")
    result = doctest.testmod(module, raise_on_error=True)
    assert result.failed == 0 and result.attempted == 6
