"""Receive real capability reports without a primary system or scene effects."""

import copy
import importlib
import inspect
import json
import os
import subprocess
import sys
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

NAMES = ("forms", "conversions", "dependencies", "syntaxes")
OPTIONS = {
    "forms": {"form_type": "file"},
    "conversions": {
        "from_form": ["molsysmt.MolSys", "molsysmt.MolSys"],
        "to_form": ["molsysmt.Topology", "unknown:destination"],
    },
    "dependencies": {},
    "syntaxes": {},
}
ROOT = Path(__file__).resolve().parents[2]


def native(name):
    # The public syntax compatibility module intentionally has a broad Python
    # signature; the report it delegates to owns the explicit call contract.
    if name == "syntaxes":
        return importlib.import_module("molsysmt.supported.supported").syntaxes
    return getattr(msm.supported, name)


@pytest.fixture(params=["empty", "loaded"])
def view(request):
    owner = msv.new_view() if request.param == "empty" else msv.demo["pentalanine"]
    try:
        yield owner
    finally:
        owner.close()


@pytest.mark.parametrize("name", NAMES)
def test_discovery_signature_validation_and_help(name):
    with msv.new_view() as view:
        facade = view.addons.molsysmt
        assert "supported" in dir(facade)
        assert set(dir(facade.supported)) == set(NAMES)
        method = getattr(facade.supported, name)
        assert inspect.signature(method) == inspect.signature(native(name))
        assert method.digestion_plan is not None
        assert "open empty view" in inspect.getdoc(method)
        assert "molecular_system" not in inspect.signature(method).parameters
        assert "update_view" not in inspect.signature(method).parameters
        assert not hasattr(facade, name)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("output_type", ["styler", "dataframe", "dictionary"])
@pytest.mark.parametrize("skip", [False, True])
def test_reports_match_native_without_reading_or_updating_system(
    view, name, output_type, skip
):
    facade = view.addons.molsysmt
    method = getattr(facade.supported, name)
    options = copy.deepcopy(OPTIONS[name])
    original_options = copy.deepcopy(options)
    target, state, status = view.molsys, view.export_state(), facade.get_sync_status()
    messages = copy.deepcopy(view.widget.initial_messages)
    expected = native(name)(**options, output_type="dataframe", skip_digestion=skip)
    result = method(**options, output_type=output_type, skip_digestion=skip)
    if output_type == "styler":
        assert type(result) is type(native(name)(**options))
        actual = result.data
    elif output_type == "dictionary":
        assert set(result) == {"index", "columns", "data"}
        actual = pd.DataFrame(**result)
    else:
        actual = result
    pd.testing.assert_frame_equal(actual, expected)
    assert options == original_options
    assert view.molsys is target and view.export_state() == state
    assert facade.get_sync_status() == status
    assert view.widget.initial_messages == messages


@pytest.mark.parametrize("name", NAMES)
def test_default_output_and_independent_results(name):
    with msv.new_view() as view:
        method = getattr(view.addons.molsysmt.supported, name)
        default = method(**OPTIONS[name])
        pd.testing.assert_frame_equal(default.data, native(name)(**OPTIONS[name]).data)
        first = method(**OPTIONS[name], output_type="dictionary")
        first["data"][0][0] = "edited metadata"
        assert "edited metadata" not in str(
            method(**OPTIONS[name], output_type="dictionary")
        )
        assert "edited metadata" not in str(
            native(name)(**OPTIONS[name], output_type="dictionary")
        )


def test_form_lists_nested_metadata_filters_and_conversion_axes():
    with msv.new_view() as view:
        tools = view.addons.molsysmt.supported
        for category in (None, "all", "file", "class", "string"):
            assert tools.forms(category, output_type="list") == msm.supported.forms(
                category, output_type="list"
            )
        table = tools.forms(output_type="dataframe")
        index = next(
            index for index, info in table["Info"].items() if isinstance(info, list)
        )
        expected = copy.deepcopy(table.at[index, "Info"])
        table.at[index, "Info"].append("edited nested info")
        assert tools.forms(output_type="dataframe").at[index, "Info"] == expected
        for orientation in ("from", "to"):
            source = ["molsysmt.MolSys", "molsysmt.MolSys"]
            target = ["molsysmt.Topology", "unknown:destination"]
            result = tools.conversions(
                source, target, as_rows=orientation, output_type="dataframe"
            )
            expected = pd.DataFrame(
                [[True, False]], index=["molsysmt.MolSys"], columns=target
            )
            if orientation == "to":
                expected = expected.T
            pd.testing.assert_frame_equal(result, expected)
            empty = tools.conversions(
                [], target, as_rows=orientation, output_type="dataframe"
            )
            assert empty.shape == ((0, 2) if orientation == "from" else (2, 0))
            assert (
                empty.columns if orientation == "from" else empty.index
            ).tolist() == target
            assert source == ["molsysmt.MolSys", "molsysmt.MolSys"]
        filtered = tools.conversions(
            from_form_type="file", to_viewer="NGLView", output_type="dataframe"
        )
        assert filtered.columns.tolist() == ["nglview.NGLWidget"]
        assert set(filtered.index) == set(tools.forms("file", output_type="list"))
        self_route = tools.conversions(
            "molsysmt.MolSys", "molsysmt.MolSys", output_type="dataframe"
        )
        assert bool(self_route.iloc[0, 0]) is False


@pytest.mark.parametrize("name", NAMES)
def test_invalid_outputs_controls_and_unbound_arguments_preserve_scene(view, name):
    method = getattr(view.addons.molsysmt.supported, name)
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(ArgumentError, match="output_type"):
        method(output_type="not-supported")
    for option in (
        {"molecular_system": view.molsys},
        {"selection": "all"},
        {"update_view": False},
    ):
        with pytest.raises(UnknownArgumentError):
            method(**option)
    for invalid in (1, "True", None):
        with pytest.raises(ArgumentError):
            method(skip_digestion=invalid)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


def test_metadata_reports_preserve_pending_edits_and_returned_data_survives_close():
    with msv.demo["pentalanine"] as view:
        facade = view.addons.molsysmt
        coordinates = msm.get(view.molsys, coordinates=True)
        facade.basic.set(coordinates=coordinates, update_view=False)
        status = facade.get_sync_status()
        assert status["state"] == "pending"
        scene, target = copy.deepcopy(view.widget.initial_messages), view.molsys
        before = msm.pyunitwizard.get_value(coordinates, to_unit="nm").copy()
        for name in NAMES:
            result = getattr(facade.supported, name)(
                **OPTIONS[name], output_type="dictionary"
            )
            assert result["columns"]
        assert facade.get_sync_status() == status
        assert view.widget.initial_messages == scene
        assert view.molsys is target
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(msm.get(target, coordinates=True), to_unit="nm"),
            before,
        )
        retained = facade.supported.forms
        record = retained(output_type="dictionary")
        expected = copy.deepcopy(record)
    assert record == expected
    with pytest.raises(RuntimeError, match="closed view"):
        retained(output_type="dictionary")


@pytest.mark.parametrize("name", NAMES)
def test_two_views_closed_handles_and_replacement(name):
    first, second = msv.new_view(), msv.new_view()
    try:
        old = getattr(first.addons.molsysmt.supported, name)
        other = getattr(second.addons.molsysmt.supported, name)
        result = old(**OPTIONS[name], output_type="dictionary")
        with msv.demo["dialanine"] as source:
            first.load(source.molsys, mode="replace")
        assert old(**OPTIONS[name], output_type="dictionary") == result
        first.close()
        with pytest.raises(RuntimeError, match="closed view"):
            old(**OPTIONS[name], output_type="dictionary")
        assert other(**OPTIONS[name], output_type="dictionary") == result
        assert second.molsys is None
    finally:
        first.close()
        second.close()


@pytest.mark.parametrize("compatibility_first", [False, True])
@pytest.mark.parametrize("table_first", [False, True])
def test_cold_discovery_syntax_import_order_and_native_alias_semantics(
    tmp_path, compatibility_first, table_first
):
    program = f"""
import importlib
import json
if {table_first!r}:
    from molsysmt._private.argdigest.normalization.attribute_synonyms import TABLES
else:
    from molsysmt.attribute import get_argument_aliases
import molsysmt as msm
def alias_error():
    try:
        msm.get(None, atom_names=True, atom_name=False)
    except Exception as error:
        return type(error).__name__
    raise AssertionError('duplicate names were accepted')
before = alias_error()
if {compatibility_first!r}:
    importlib.import_module('molsysmt.supported.syntaxes')
import molsysviewer as msv
with msv.new_view() as view:
    tools = view.addons.molsysmt.supported
    if not {compatibility_first!r}:
        importlib.import_module('molsysmt.supported.syntaxes')
    assert 'molsysmt.MolSys' in tools.forms(output_type='list')
    assert tools.dependencies(output_type='dictionary')['columns']
    assert tools.conversions(['molsysmt.MolSys'], ['molsysmt.Topology'], output_type='dictionary')['data'] == [[True]]
    table = tools.syntaxes(output_type='dataframe').set_index('Syntax')
    assert bool(table.loc['MolSysMT', 'Selection input']) is True
    assert bool(table.loc['MolSysMT', 'Translation output']) is False
    assert bool(table.loc['NGLView', 'Selection input']) is False
    assert bool(table.loc['NGLView', 'Translation output']) is True
    assert view.molsys is None
assert alias_error() == before
print(json.dumps({{'native_alias_error': before, 'metadata': 'passed'}}))
"""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(ROOT), str(Path(msv.__file__).parents[1])]
    )
    result = subprocess.run(
        [sys.executable, "-c", program],
        cwd=tmp_path,
        env=environment,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    record = json.loads(result.stdout.splitlines()[-1])
    assert record["metadata"] == "passed"
    assert record["native_alias_error"] in {
        "ArgumentConsistencyError",
        "UnknownArgumentError",
    }
