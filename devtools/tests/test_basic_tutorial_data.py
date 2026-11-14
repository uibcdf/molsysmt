"""Run the core query tutorials' actual setup without external data services."""

import ast
import importlib
import json
import socket
import warnings
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("name", ["get", "info", "select", "extract"])
def test_basic_query_tutorial_loads_a_real_system_without_network(name, monkeypatch):
    namespace = _load_tutorial(name, monkeypatch)
    msm = namespace["msm"]
    molsys = namespace["molsys"]
    assert msm.get_form(molsys) == "molsysmt.MolSys"
    assert msm.get(molsys, n_atoms=True) > 0
    coordinates = msm.get(molsys, coordinates=True)
    assert coordinates.shape == (1, msm.get(molsys, n_atoms=True), 3)


def _load_tutorial(name, monkeypatch):
    def refuse_network(*args, **kwargs):
        raise OSError("External network is unavailable in this tutorial test")

    monkeypatch.setattr(socket, "getaddrinfo", refuse_network)
    monkeypatch.setattr(socket.socket, "connect", refuse_network)
    # Refuse the remote boundary before its normal exponential retry delays.
    for form in ("file_bcif_gz", "file_bcif", "file_cif_gz", "file_cif"):
        downloader = importlib.import_module(f"molsysmt.form.{form}.download")
        monkeypatch.setattr(downloader, "download_with_retries", refuse_network)
    path = ROOT / f"docs/content/user/tools/basic/{name}.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    namespace = {"__name__": "__tutorial_setup__"}
    with warnings.catch_warnings():
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                if "molsys" in namespace:
                    break
    assert "molsys" in namespace, "The tutorial did not construct its example system"
    return namespace


def test_selection_example_selects_backbone_names_in_groups_10_to_29(monkeypatch):
    namespace = _load_tutorial("select", monkeypatch)
    path = ROOT / "docs/content/user/tools/basic/select.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
        and "# Atoms named CA, C, O or N in groups with indices 10 to 29."
        in "".join(cell["source"])
    ]
    assert len(cells) == 1
    program = ast.parse(cells[0])
    assert isinstance(program.body[-1], ast.Expr)
    exec(
        compile(ast.Module(body=program.body[:-1], type_ignores=[]), str(path), "exec"),
        namespace,
    )
    selected = eval(
        compile(ast.Expression(program.body[-1].value), str(path), "eval"), namespace
    )
    msm = namespace["msm"]
    molsys = namespace["molsys"]
    names, groups = msm.get(molsys, element="atom", atom_name=True, group_index=True)
    expected = np.flatnonzero(
        np.isin(names, ["CA", "C", "O", "N"]) & np.isin(groups, range(10, 30))
    )
    assert expected.size > 0
    np.testing.assert_array_equal(selected, expected)
