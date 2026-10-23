"""Receiving real MolSysMT reads through the redesigned bound Viewer facade."""

import inspect
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.skipif(
    not isinstance(getattr(msv.MolSysView, "closed", None), property),
    reason="This host predates the redesigned tools lifecycle; backend support is independent.",
)


@pytest.fixture
def view():
    registry = msv.addons
    registered = registry.contains("molsysmt")
    if not registered:
        registry.register_module("molsysviewer_molsysmt.tools")
    view = msv.demo["pentalanine"]
    try:
        yield view
    finally:
        view.close()
        if not registered:
            registry.unregister("molsysmt")


@pytest.mark.parametrize(
    "name",
    (
        "get",
        "select",
        "info",
        "get_attributes",
        "has_attribute",
        "get_label",
        "extract",
    ),
)
def test_signatures_defaults_digestion_and_help_match_native(view, name):
    native = getattr(msm.basic, name)
    bound = getattr(view.addons.molsysmt.basic, name)
    signature = inspect.signature(native)
    expected = signature.replace(parameters=list(signature.parameters.values())[1:])
    assert inspect.signature(bound) == expected
    assert "skip_digestion" in inspect.signature(bound).parameters
    assert getattr(bound, "digestion_plan", None) is not None
    assert "current view.molsys" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    assert getattr(view.addons.molsysmt, name) == bound


def test_nonconsecutive_coordinates_keep_values_units_and_scene(view):
    tools = view.addons.molsysmt
    before = view.export_state()
    target = view.molsys
    args = dict(
        element="atom",
        selection=[0, 2, 4],
        structure_indices=[2, 0, 2],
        coordinates=True,
    )
    expected = msm.basic.get(target, **args)
    actual = tools.basic.get(**args)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(actual, to_unit="nm"),
        msm.pyunitwizard.get_value(expected, to_unit="nm"),
    )
    assert actual.shape == (3, 3, 3)
    assert view.molsys is target
    assert view.export_state() == before
    assert not hasattr(tools.basic, "remove")
    assert not hasattr(tools, "set")


@pytest.mark.parametrize(
    "name, kwargs",
    (
        ("select", {"selection": "atom_type=='N'", "structure_indices": [2, 0]}),
        (
            "info",
            {"element": "group", "selection": [0, 1], "output_type": "dictionary"},
        ),
        ("get_attributes", {"output_type": "dictionary"}),
        ("has_attribute", {"attribute": "coordinates", "structure_indices": [2, 0]}),
        ("get_label", {"selection": [0, 1]}),
    ),
)
def test_native_read_results(view, name, kwargs):
    native = getattr(msm.basic, name)(view.molsys, **kwargs)
    bound = getattr(view.addons.molsysmt.basic, name)(**kwargs)
    assert bound == native


def test_native_errors_and_primary_override(view):
    tools = view.addons.molsysmt
    for name, kwargs in (
        ("get", {"unknown_attribute": True}),
        ("select", {"selection": [1000000]}),
        ("get_label", {"unknown_argument": True}),
    ):
        with pytest.raises(Exception) as native_failure:
            getattr(msm.basic, name)(view.molsys, **kwargs)
        with pytest.raises(type(native_failure.value)):
            getattr(tools.basic, name)(**kwargs)
    with pytest.raises(TypeError, match="bound to view.molsys"):
        tools.basic.get(molecular_system=view.molsys, n_atoms=True)
    with pytest.raises(msm.ArgumentError):
        tools.basic.get(n_atoms=True, skip_digestion="yes")


def test_cached_method_follows_replacement_disable_and_close(view):
    tools = view.addons.molsysmt
    read = tools.basic.get
    original_count = read(n_atoms=True)
    with msv.demo["dialanine"] as other:
        view.load(other.molsys, mode="replace")
    assert read(n_atoms=True) == msm.basic.get(view.molsys, n_atoms=True)
    assert read(n_atoms=True) != original_count
    view.addons.manager.disable("molsysmt")
    assert view.addons.molsysmt is tools
    assert read(n_atoms=True) > 0
    view.close()
    assert view.closed
    with pytest.raises(RuntimeError, match="closed view"):
        read(n_atoms=True, skip_digestion=True)


def test_two_views_and_empty_target(view):
    with msv.MolSysView() as empty:
        empty_tools = empty.addons.molsysmt
        assert empty_tools is not view.addons.molsysmt
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty_tools.basic.get(n_atoms=True)
    assert view.addons.molsysmt.basic.get(n_atoms=True) > 0


def test_real_metadata_discovery_and_lazy_import(tmp_path):
    config = tomllib.loads((ROOT / "pyproject.toml").read_text())
    entries = config["project"]["entry-points"]["molsysviewer.addons"]
    metadata = tmp_path / "molsysmt_tools_source_probe-0.dist-info"
    metadata.mkdir()
    (metadata / "METADATA").write_text(
        "Metadata-Version: 2.1\nName: molsysmt-tools-source-probe\nVersion: 0\n"
    )
    (metadata / "entry_points.txt").write_text(
        "[molsysviewer.addons]\n"
        + "\n".join(f"{name} = {value}" for name, value in entries.items())
        + "\n"
    )
    program = """
import json
import sys
import molsysmt
import molsysviewer_molsysmt
assert 'molsysviewer' not in sys.modules
import molsysviewer as msv
with msv.demo['dialanine'] as view:
    tools = view.addons.molsysmt
    assert tools.basic.get(n_atoms=True) == molsysmt.get(view.molsys, n_atoms=True)
    print(json.dumps({'addon': 'molsysmt', 'n_atoms': tools.basic.get(n_atoms=True)}))
"""
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(tmp_path), str(ROOT), str(Path(msv.__file__).parents[1])]
    )
    result = subprocess.run(
        [sys.executable, "-c", program],
        env=environment,
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout.splitlines()[-1])
    assert payload["addon"] == "molsysmt" and payload["n_atoms"] > 0


@pytest.mark.parametrize("frames", [[2, 0, 2], [2, 0]])
def test_extract_returns_native_subset_without_adopting_it(view, frames):
    target = view.molsys
    before = view.export_state()
    kwargs = dict(
        selection=[0, 2, 4], structure_indices=frames, to_form="molsysmt.MolSys"
    )
    expected = msm.basic.extract(target, **kwargs)
    actual = view.addons.molsysmt.basic.extract(**kwargs)
    assert type(actual) is type(expected)
    assert actual is not target
    assert actual.get_n_atoms() == 3
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(actual.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(expected.structures.coordinates, to_unit="nm"),
    )
    assert actual.structures.n_structures == len(frames)
    assert view.molsys is target and view.export_state() == before
    msm.set(actual, selection=[0], element="atom", atom_name="COPIED")
    assert msm.get(target, selection=[0], element="atom", atom_name=True) != ["COPIED"]


def test_extract_preserves_native_copy_policy_and_rejects_invalid_indices(view):
    target = view.molsys
    result = view.addons.molsysmt.basic.extract(copy_if_all=False)
    assert (result is target) == (
        msm.basic.extract(target, copy_if_all=False) is target
    )
    before = view.export_state()
    with pytest.raises(Exception) as native_failure:
        msm.basic.extract(target, structure_indices=[1000000])
    with pytest.raises(type(native_failure.value)):
        view.addons.molsysmt.extract(structure_indices=[1000000])
    assert view.molsys is target and view.export_state() == before
