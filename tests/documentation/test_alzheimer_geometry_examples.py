"""Check the course's real geometry cells against independent coordinates."""

import base64
import gzip
import hashlib
import io
import json
import socket
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

ROOT = Path(__file__).resolve().parents[2]
LESSON = ROOT / "docs/content/course/Path_Alzheimer/30_Geometrical_Measurements.ipynb"
COORDINATES = ROOT / "docs/_static/data/2beg.pdb.gz"


def _section_code(title):
    cells = json.loads(LESSON.read_text())["cells"]
    for index, cell in enumerate(cells):
        if cell["cell_type"] == "markdown" and title in "".join(cell["source"]):
            return next(
                "".join(c["source"])
                for c in cells[index + 1 :]
                if c["cell_type"] == "code"
            )
    raise AssertionError("Missing course section: " + title)


def _execute(namespace, title):
    exec(compile(_section_code(title), str(LESSON), "exec"), namespace)


def _xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


@pytest.fixture(params=[["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def unit_policy(request):
    with puw.context(standard_units=request.param):
        yield


@pytest.fixture(scope="module")
def measurement_system():
    # The original three broken cells are tested independently of the old
    # live-download setup. This is a coordinate control, not a docking model.
    fibril = msm.convert(
        COORDINATES,
        to_form="molsysmt.MolSys",
        structure_indices=0,
        get_missing_bonds=False,
    )
    peptide = msm.build.build_peptide("KLVFF")
    peptide = msm.structure.center(
        peptide,
        target_coordinates=msm.structure.get_center(fibril)
        + puw.quantity([0, 0, 4], "nm"),
    )
    molsys = msm.merge([fibril, peptide])
    n_target = msm.get(fibril, n_atoms=True)
    return {
        "msm": msm,
        "np": np,
        "puw": puw,
        "molsys": molsys,
        "fibril_atom_indices": np.arange(n_target),
        "peptide_atom_indices": np.arange(n_target, msm.get(molsys, n_atoms=True)),
        "core_atom_indices": np.asarray(msm.select(molsys, selection="chain_index==2")),
    }


def test_center_distance_uses_both_declared_centers(measurement_system, unit_policy):
    namespace = dict(measurement_system)
    _execute(namespace, "## 1. Simple Distances")
    xyz = _xyz(namespace["molsys"])[0]
    expected = np.linalg.norm(
        xyz[namespace["peptide_atom_indices"]].mean(axis=0)
        - xyz[namespace["core_atom_indices"]].mean(axis=0)
    )
    actual = namespace["center_distance"]
    assert actual.shape == (1, 1, 1)
    np.testing.assert_allclose(puw.get_value(actual, to_unit="nm")[0, 0, 0], expected)


def test_minimum_pair_addresses_the_actual_source_atoms(
    measurement_system, unit_policy
):
    namespace = dict(measurement_system)
    _execute(namespace, "## 2. Finding the Closest Contact")
    xyz = _xyz(namespace["molsys"])[0]
    a, b = namespace["peptide_atom_indices"], namespace["fibril_atom_indices"]
    distances = np.linalg.norm(xyz[a, None] - xyz[None, b], axis=-1)
    i, j = np.unravel_index(np.argmin(distances), distances.shape)
    np.testing.assert_array_equal(namespace["closest_atom_pairs"], [[a[i], b[j]]])
    np.testing.assert_allclose(
        puw.get_value(namespace["minimum_distance"], to_unit="nm"), [distances[i, j]]
    )


def test_angle_uses_named_atoms_and_the_middle_vertex(measurement_system, unit_policy):
    namespace = dict(measurement_system)
    _execute(namespace, "## 3. Measuring Orientation")
    triplet = np.asarray(namespace["atom_indices"])
    names = np.asarray(msm.get(namespace["molsys"], element="atom", atom_name=True))
    assert names[triplet].tolist() == ["CA", "CA", "CA"]
    assert triplet[0] in namespace["peptide_atom_indices"]
    assert triplet[1] in namespace["core_atom_indices"]
    assert triplet[2] in namespace["peptide_atom_indices"]
    xyz = _xyz(namespace["molsys"])[0, triplet]
    first, second = xyz[0] - xyz[1], xyz[2] - xyz[1]
    cosine = np.dot(first, second) / (np.linalg.norm(first) * np.linalg.norm(second))
    expected = np.arccos(np.clip(cosine, -1, 1))
    np.testing.assert_allclose(
        puw.get_value(namespace["angle"], to_unit="radians"), [[expected]]
    )


def test_complete_lesson_retains_the_deposit_and_explicit_placement(
    unit_policy, monkeypatch
):
    import matplotlib.pyplot as plt

    def refuse_network(*args, **kwargs):
        pytest.fail("The offline geometry lesson attempted external network access")

    monkeypatch.setattr(socket, "getaddrinfo", refuse_network)
    monkeypatch.setattr(socket.socket, "connect", refuse_network)
    monkeypatch.chdir(LESSON.parent)
    plotted = []
    original_imshow = plt.imshow

    def observe_imshow(values, *args, **kwargs):
        plotted.append(np.asarray(values).copy())
        return original_imshow(values, *args, **kwargs)

    monkeypatch.setattr(plt, "imshow", observe_imshow)
    before = hashlib.sha256(COORDINATES.read_bytes()).hexdigest()
    namespace = {"__name__": "__geometry_lesson__"}
    try:
        for cell in json.loads(LESSON.read_text())["cells"]:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), str(LESSON), "exec"), namespace)
    finally:
        plt.close("all")

    # Read the deposited fixed-width Cartesian fields independently of the
    # MolSysMT parser. PDB positions are in angstrom, not the session unit.
    model = gzip.decompress(COORDINATES.read_bytes()).decode().split("ENDMDL", 1)[0]
    records = [line for line in model.splitlines() if line.startswith("ATOM  ")]
    deposited = (
        np.asarray(
            [
                [float(line[a:b]) for a, b in ((30, 38), (38, 46), (46, 54))]
                for line in records
            ]
        )
        / 10
    )
    np.testing.assert_allclose(_xyz(namespace["fibril"]), deposited[None], atol=1e-12)
    assert msm.get(namespace["fibril"], n_structures=True) == 1
    assert msm.get(namespace["fibril"], n_chains=True) == 5
    assert msm.get(namespace["molsys"], n_structures=True) == 1

    merged = _xyz(namespace["molsys"])[0]
    a, b = namespace["fibril_atom_indices"], namespace["peptide_atom_indices"]
    np.testing.assert_array_equal(np.concatenate((a, b)), np.arange(len(merged)))
    np.testing.assert_allclose(merged[a], deposited, atol=1e-12)
    np.testing.assert_allclose(merged[b], _xyz(namespace["peptide"])[0], atol=1e-12)
    np.testing.assert_allclose(
        merged[b].mean(axis=0) - merged[a].mean(axis=0), [0, 0, 4], atol=1e-12
    )

    core = namespace["core_atom_indices"]
    assert set(
        msm.get(namespace["molsys"], element="atom", selection=core, chain_id=True)
    ) == {"C"}
    assert len(namespace["peptide_ca_indices"]) == 5
    assert len(namespace["core_ca_indices"]) == 26
    first = np.array(
        [merged[atoms].mean(axis=0) for atoms in namespace["peptide_groups"]]
    )
    second = np.array(
        [merged[atoms].mean(axis=0) for atoms in namespace["core_groups"]]
    )
    expected = np.linalg.norm(first[:, None] - second[None], axis=-1)
    np.testing.assert_allclose(
        puw.get_value(namespace["group_distances"], to_unit="nm"), expected[None]
    )
    assert len(plotted) == 1
    np.testing.assert_allclose(plotted[0], expected)
    assert hashlib.sha256(COORDINATES.read_bytes()).hexdigest() == before


def test_coordinate_fixture_matches_its_declared_provenance():
    raw = COORDINATES.read_bytes()
    record = json.loads(COORDINATES.with_name("2beg.provenance.json").read_text())
    assert hashlib.sha256(raw).hexdigest() == record["compressed_sha256"]
    text = gzip.decompress(raw)
    assert hashlib.sha256(text).hexdigest() == record["decompressed_sha256"]
    assert sum(line.startswith(b"MODEL ") for line in text.splitlines()) == 10
    assert b"2BEG" in text[:1000]


def test_saved_group_distance_matrix_has_a_real_figure():
    from PIL import Image

    cells = json.loads(LESSON.read_text())["cells"]
    cell = next(c for c in cells if c.get("id") == "geometry758-group-matrix")
    assert cell.get("execution_count") is not None
    images = [
        output["data"]["image/png"]
        for output in cell["outputs"]
        if "image/png" in output.get("data", {})
    ]
    assert len(images) == 1
    with Image.open(
        io.BytesIO(base64.b64decode("".join(images[0]), validate=True))
    ) as image:
        assert image.format == "PNG" and min(image.size) >= 100
        values = np.asarray(image.convert("RGB"))
        assert values.min() < values.max()
