"""Compare public methods against executed original reference cores."""

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm

MANIFEST = (
    Path(__file__).resolve().parents[3]
    / "devtools/data/attributed_interaction_oracles.json"
)
DATA = json.loads(MANIFEST.read_text())


def test_original_oracles_include_positive_and_negative_decisions():
    water = next(case for case in DATA["hbonds"] if case["name"] == "water")
    for method, observations in water["observations"].items():
        assert observations, (
            f"The {method} reference must actually recognize the water sites."
        )
        assert len({row["structure_index"] for row in observations}) < len(
            water["coordinates_nm"]
        )
    for method in ("prolif", "mdtraj_geometry", "molstar_geometry"):
        assert (
            0 < len(DATA["pi_pi"][0][method]) < len(DATA["pi_pi"][0]["coordinates_nm"])
        )


@pytest.mark.parametrize("method", ["prolif", "mdtraj_geometry", "molstar_geometry"])
def test_perpendicular_pi_endpoint_has_the_analytic_float64_geometry(method, tmp_path):
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6)))
    edge = ring[:, [2, 1, 0]] + [0, 0, 0.4]
    case = dict(
        smiles="c1ccccc1.c1ccccc1",
        coordinates_nm=[np.concatenate((ring, edge)).tolist()],
    )
    result = msm.interactions.pi_pi.get_pi_pi_interactions(
        _source(case, "native", tmp_path), method=method, pbc=False
    )
    assert result.n_interactions == 1
    np.testing.assert_allclose(
        result.measurements["plane_angle"], np.pi / 2, atol=1e-12, rtol=0
    )


def _source(case, form, tmp_path):
    params = Chem.SmilesParserParams()
    params.removeHs = not case.get("explicit_hydrogens", False)
    molecule = Chem.MolFromSmiles(case["smiles"], params)
    for xyz in case["coordinates_nm"]:
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        molecule.AddConformer(conformer, assignId=True)
    if form == "rdkit":
        return molecule
    native = msm.convert(molecule, to_form="molsysmt.MolSys")
    if form == "native":
        return native
    path = str(tmp_path / "source.h5msm")
    msm.convert(native, to_form=path)
    return path


def _rows(result):
    rows = []
    for frame, relation in zip(
        result.occurrence_structures, result.occurrence_relations
    ):
        participants = result.relation(int(relation))["participants"]
        rows.append(
            (int(frame), *(tuple(item["atom_indices"]) for item in participants))
        )
    assert len(rows) == len(set(rows)), (
        "Parallel observations must not be silently overwritten by the comparison."
    )
    return set(rows)


@pytest.mark.parametrize("case", DATA["pi_pi"], ids=lambda item: item["name"])
@pytest.mark.parametrize("method", ["prolif", "molstar_geometry", "mdtraj_geometry"])
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_pi_pi_original_cores_across_forms(case, method, form, tmp_path):
    result = msm.interactions.pi_pi.get_pi_pi_interactions(
        _source(case, form, tmp_path),
        method=method,
        pbc=False,
        heavy_mode="force" if form == "h5msm" else "off",
    )
    expected = case[method]
    if method == "molstar_geometry":
        expected = [
            (frame, tuple(case["ring_a"]), tuple(case["ring_b"])) for frame in expected
        ]
    else:
        expected = [
            (row["structure_index"], tuple(row["ring_a"]), tuple(row["ring_b"]))
            for row in expected
        ]
    assert _rows(result) == set(expected)
    assert result.evaluated_structure_indices.tolist() == list(
        range(len(case["coordinates_nm"]))
    )
    assert result.measure_units["intersection_distance"] == "nm"
    assert result.parameters["method_reference"]["software"] in {
        "ProLIF",
        "Mol*",
        "MDTraj",
    }
    if method == "prolif":
        actual = {
            key: index
            for index, key in enumerate(
                [
                    (
                        int(frame),
                        *(
                            tuple(p["atom_indices"])
                            for p in result.relation(int(relation))["participants"]
                        ),
                    )
                    for frame, relation in zip(
                        result.occurrence_structures, result.occurrence_relations
                    )
                ]
            )
        }
        for row in case[method]:
            key = row["structure_index"], tuple(row["ring_a"]), tuple(row["ring_b"])
            np.testing.assert_allclose(
                result.measurements["distance"][actual[key]],
                row["distance_nm"],
                atol=1e-12,
                rtol=0,
            )


@pytest.mark.parametrize("case", DATA["cation_pi"], ids=lambda item: item["name"])
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_cation_pi_original_molstar_geometry_across_forms(case, form, tmp_path):
    result = msm.interactions.cation_pi.get_cation_pi_interactions(
        _source(case, form, tmp_path),
        method="molstar_geometry",
        pbc=False,
        heavy_mode="force" if form == "h5msm" else "off",
    )
    assert _rows(result) == {
        (frame, tuple(case["cation"]), tuple(case["ring"]))
        for frame in case["molstar_geometry"]
    }
    assert (
        result.parameters["plane_method"] == "cross_of_first_three_basis_member_atoms"
    )
    assert result.parameters["exclude_direct_covalent"] is False


@pytest.mark.parametrize("case", DATA["hbonds"], ids=lambda item: item["name"])
@pytest.mark.parametrize(
    "method",
    ["baker_hubbard", "wernet_nilsson", "cpptraj", "prolif", "mdanalysis_geometry"],
)
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_hbond_original_cores_across_forms(case, method, form, tmp_path):
    options = (
        dict(
            donor_hydrogen_pairs=case["explicit_donor_hydrogen_pairs"],
            acceptor_atom_indices=case["explicit_acceptor_atom_indices"],
        )
        if method == "mdanalysis_geometry"
        else {}
    )
    result = msm.interactions.hbonds.get_hbonds(
        _source(case, form, tmp_path),
        method=method,
        pbc=False,
        heavy_mode="force" if form == "h5msm" else "off",
        **options,
    )
    expected = {
        (row["structure_index"], *(tuple([atom]) for atom in row["atoms"]))
        for row in case["observations"][method]
    }
    assert _rows(result) == expected
    assert result.evaluated_structure_indices.tolist() == list(
        range(len(case["coordinates_nm"]))
    )
    assert result.measure_units["dha_angle"] == "radians"
    assert result.software["molsysmt"] == msm.__version__
    assert result.parameters["method_reference"]["software"] in {
        "ProLIF",
        "CPPTRAJ",
        "MDTraj",
        "MDAnalysis",
    }
