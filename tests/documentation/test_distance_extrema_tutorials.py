"""Check the actual tutorial reports against source coordinates and memberships."""

import base64
import contextlib
import io
import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]
TUTORIALS = ROOT / "docs/content/user/tools/structure"


@pytest.fixture(params=[["nm", "ps"], ["pm", "fs"]])
def unit_policy(request):
    with msm.pyunitwizard.context(standard_units=request.param):
        yield


@pytest.fixture(scope="module")
def examples():
    return {
        "molsys": msm.convert(
            msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
            structure_indices=[0, 1, 2],
        ),
        "tctim": msm.convert(msm.systems["TcTIM"]["1tcd.h5msm"]),
    }


def _run_example(namespace, name, needle, *, next_code=False):
    path = TUTORIALS / (name + ".ipynb")
    notebook = json.loads(path.read_text())
    code = [
        "".join(cell["source"])
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    ]
    matches = [i for i, cell in enumerate(code) if needle in cell]
    assert len(matches) == 1, "The actual tutorial example must be unambiguous"
    index = matches[0]
    cells = code[index : index + (2 if next_code else 1)]
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        for cell in cells:
            exec(compile(cell, str(path), "exec"), namespace)
    return output.getvalue()


def _namespace(examples):
    return {"msm": msm, "np": np, **examples}


def _coordinates(molsys):
    return msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


@pytest.mark.parametrize("kind", ["minimum", "maximum"])
def test_atom_extrema_example_reports_source_atom_indices(examples, kind, unit_policy):
    namespace = _namespace(examples)
    text = _run_example(
        namespace,
        "get_" + kind + "_distances",
        "pairs, min_distances =" if kind == "minimum" else "pairs_sets, max_d_sets =",
        next_code=kind == "minimum",
    )
    match = re.search(r"(?:between atom |atoms )(\d+) and (\d+)", text)
    assert match is not None, text
    first, second = map(int, match.groups())
    atoms_a = msm.select(examples["molsys"], selection="group_index==0")
    atoms_b = msm.select(examples["molsys"], selection="group_index==4")
    assert first in atoms_a and second in atoms_b, (
        f"Reported atoms {first}, {second} must belong to the original endpoint selections"
    )
    coordinates = _coordinates(examples["molsys"])
    distances = np.linalg.norm(
        coordinates[:, atoms_a, None] - coordinates[:, None, atoms_b], axis=-1
    )
    expected = getattr(np, "min" if kind == "minimum" else "max")(
        distances, axis=(1, 2)
    )
    actual = namespace["min_distances" if kind == "minimum" else "max_d_sets"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(actual, to_unit="nm"), expected
    )
    np.testing.assert_allclose(
        np.linalg.norm(coordinates[0, first] - coordinates[0, second]), expected[0]
    )


def test_per_atom_minimum_example_reports_source_target_index(examples, unit_policy):
    namespace = _namespace(examples)
    text = _run_example(namespace, "get_minimum_distances", "pairs_ind, min_d_ind =")
    match = re.search(r"target atom index (\d+)", text)
    assert match is not None, text
    reported = int(match.group(1))
    atoms_a = msm.select(
        examples["molsys"], selection='group_index==0 and atom_type!="H"'
    )
    atoms_b = msm.select(
        examples["molsys"], selection='group_index==4 and atom_type!="H"'
    )
    coordinates = _coordinates(examples["molsys"])
    distances = np.linalg.norm(
        coordinates[:, atoms_a, None] - coordinates[:, None, atoms_b], axis=-1
    )
    assert reported == atoms_b[np.argmin(distances[0, 0])]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(namespace["min_d_ind"], to_unit="nm"),
        distances.min(axis=2),
    )


def test_interchain_minimum_example_reports_source_atom_indices(examples, unit_policy):
    namespace = _namespace(examples)
    text = _run_example(
        namespace, "get_minimum_distances", "pairs_chains, min_dist_chains ="
    )
    match = re.search(r"atom (\d+) \(chain 0\) and atom (\d+) \(chain 1\)", text)
    assert match is not None, text
    first, second = map(int, match.groups())
    chain_indices = np.asarray(
        msm.get(namespace["tctim"], element="atom", chain_index=True)
    )
    assert (chain_indices[first], chain_indices[second]) == (0, 1)
    coordinates = _coordinates(namespace["tctim"])
    np.testing.assert_allclose(
        np.linalg.norm(coordinates[0, first] - coordinates[0, second]),
        msm.pyunitwizard.get_value(namespace["min_dist_chains"], to_unit="nm")[0],
    )


def test_centroid_minimum_example_reports_source_group_indices(examples, unit_policy):
    namespace = _namespace(examples)
    text = _run_example(namespace, "get_minimum_distances", "pairs_cent, min_d_cent =")
    match = re.search(r"between (?:residue|group) (\d+) and (\d+)", text)
    assert match is not None, text
    first, second = map(int, match.groups())
    molsys = examples["tctim"]
    atom_groups, atom_chains = msm.get(
        molsys, element="atom", group_index=True, chain_index=True
    )
    atom_groups, atom_chains = np.asarray(atom_groups), np.asarray(atom_chains)
    assert first in atom_groups[atom_chains == 0]
    assert second in atom_groups[atom_chains == 1]
    coordinates = _coordinates(molsys)[0]
    first_center = coordinates[atom_groups == first].mean(axis=0)
    second_center = coordinates[atom_groups == second].mean(axis=0)
    np.testing.assert_allclose(
        np.linalg.norm(first_center - second_center),
        msm.pyunitwizard.get_value(namespace["min_d_cent"], to_unit="nm")[0],
    )


@pytest.mark.parametrize(
    "name",
    [
        "get_distances",
        "get_vectors",
        "center",
        "get_contacts",
        "get_neighbors",
        "get_minimum_distances",
        "get_maximum_distances",
    ],
)
def test_geometry_tutorial_preserves_each_executed_plot(name):
    from PIL import Image

    notebook = json.loads((TUTORIALS / (name + ".ipynb")).read_text())
    cells = [
        cell
        for cell in notebook["cells"]
        if cell["cell_type"] == "code" and "plt.show()" in "".join(cell["source"])
    ]
    assert cells
    for cell in cells:
        assert cell.get("execution_count") is not None
        images = [
            output["data"]["image/png"]
            for output in cell.get("outputs", [])
            if "image/png" in output.get("data", {})
        ]
        assert images, f"{name}: an executed plotting cell must retain its figure"
        for encoded in images:
            raw = base64.b64decode("".join(encoded), validate=True)
            with Image.open(io.BytesIO(raw)) as image:
                assert image.format == "PNG" and min(image.size) >= 100
                pixels = np.asarray(image.convert("RGB"))
                assert pixels.min() < pixels.max(), "The saved plot must not be blank"
