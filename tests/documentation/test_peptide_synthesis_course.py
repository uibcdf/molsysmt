"""Exercise the peptide lesson's real cells with independent inventory/torsion checks."""

import json
import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

ROOT = Path(__file__).resolve().parents[2]
LESSON = ROOT / "docs/content/course/Path_Alzheimer/24_Peptide_Synthesis.ipynb"


def section_code(prefix):
    cells = json.loads(LESSON.read_text())["cells"]
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "markdown" and prefix in "".join(cell["source"]):
            return next(
                "".join(c["source"]) for c in cells[i + 1 :] if c["cell_type"] == "code"
            )
    raise AssertionError("Missing course section " + prefix)


def xyz(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")


def torsions(molsys, quartets):
    result = []
    coordinates = xyz(molsys)[0]
    for a, b, c, d in coordinates[np.asarray(quartets)]:
        axis = c - b
        axis /= np.linalg.norm(axis)
        first, last = a - b, d - c
        first -= (first @ axis) * axis
        last -= (last @ axis) * axis
        result.append(np.arctan2(np.cross(axis, first) @ last, first @ last))
    return np.asarray(result)


@pytest.fixture(params=[["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def unit_policy(request):
    with puw.context(standard_units=request.param):
        yield


def test_actual_capping_cell_constructs_explicit_cap_groups(unit_policy):
    namespace = {"msm": msm, "np": np, "puw": puw}
    exec(compile(section_code("## 2."), str(LESSON), "exec"), namespace)
    capped = namespace["capped_peptide"]
    names = msm.get(capped, element="group", group_name=True)
    assert names == ["ACE", "LYS", "LEU", "VAL", "PHE", "PHE", "NME"]
    assert msm.get(capped, n_atoms=True) == 109
    assert np.isfinite(xyz(capped)).all()
    graph = msm.chemical_states.get_bondgraph(capped)
    assert graph.number_of_nodes() == 109
    assert graph.number_of_edges() >= 108
    # Each cap is covalently connected to its neighboring amino-acid group.
    groups = np.asarray(msm.get(capped, element="atom", group_index=True))
    edges = {tuple(sorted((int(groups[a]), int(groups[b])))) for a, b in graph.edges}
    assert (0, 1) in edges and (5, 6) in edges


def test_actual_helical_cell_reaches_torsions_without_editing_its_source(unit_policy):
    capped = msm.build.build_peptide("AceLysLeuValPhePheNme")
    before = xyz(capped).copy()
    namespace = {"msm": msm, "np": np, "puw": puw, "capped_peptide": capped}
    exec(compile(section_code("## 3."), str(LESSON), "exec"), namespace)
    helix = namespace["helical_peptide"]
    assert helix is not capped
    np.testing.assert_array_equal(xyz(capped), before)
    assert msm.get(helix, element="group", group_name=True) == msm.get(
        capped, element="group", group_name=True
    )
    for key, target in [("phi", -60), ("psi", -45), ("omega", 180)]:
        quartets = msm.chemical_states.get_dihedral_quartets(helix, **{key: True})
        assert len(quartets) == 5
        delta = torsions(helix, quartets) - np.deg2rad(target)
        np.testing.assert_allclose(
            np.arctan2(np.sin(delta), np.cos(delta)), 0, atol=1e-7
        )
    cells = {c.get("id"): c for c in json.loads(LESSON.read_text())["cells"]}
    exec(
        compile("".join(cells["peptide759-angles"]["source"]), str(LESSON), "exec"),
        namespace,
    )
    graph = msm.chemical_states.get_bondgraph(capped)
    pairs = np.asarray(list(graph.edges), dtype=np.int64)
    after = xyz(helix)
    np.testing.assert_allclose(
        np.linalg.norm(after[:, pairs[:, 0]] - after[:, pairs[:, 1]], axis=-1),
        np.linalg.norm(before[:, pairs[:, 0]] - before[:, pairs[:, 1]], axis=-1),
        atol=1e-11,
    )


def test_committed_scene_contains_the_actual_lesson_model(unit_policy):
    namespace = {}
    cells = {c.get("id"): c for c in json.loads(LESSON.read_text())["cells"]}
    for key in ("imports", "uncapped", "capped", "helical", "angles"):
        exec(
            compile("".join(cells["peptide759-" + key]["source"]), str(LESSON), "exec"),
            namespace,
        )
    scene = ROOT / "docs/_static/views/course_alzheimer_peptide_helix.html"
    text = scene.read_text()
    messages = json.loads(
        re.search(
            r'<script id="molsysviewer-messages"[^>]*>(.*?)</script>', text, re.S
        ).group(1)
    )
    loads = [m["payload"] for m in messages if m["op"] == "load_molsys_payload"]
    assert len(loads) == 1
    payload = loads[0]
    molsys = namespace["helical_peptide"]
    assert len(payload["structures"]) == 1
    # The MolSysViewer molecular payload declares Cartesian coordinates in angstroms.
    expected = puw.get_value(molsys.structures.coordinates, to_unit="angstroms")
    actual = np.asarray([s["coordinates"] for s in payload["structures"]])
    assert actual.shape == (1, 109, 3)
    # Reconstructing successive rotations under a different unit policy can
    # round a near-trans omega differently; allow < 5e-8 nm, not a scale change.
    np.testing.assert_allclose(actual, expected, rtol=0, atol=5e-7)
    assert payload["atoms"]["atom_name"] == msm.get(
        molsys, element="atom", atom_name=True
    )
    np.testing.assert_array_equal(
        payload["atoms"]["residue_index"],
        msm.get(molsys, element="atom", group_index=True),
    )
    assert any(m["op"] == "set_whole_representation" for m in messages)
    ui = json.loads(
        re.search(
            r'<script id="molsysviewer-ui"[^>]*>(.*?)</script>', text, re.S
        ).group(1)
    )
    assert ui["background_mode"] == "transparent"
