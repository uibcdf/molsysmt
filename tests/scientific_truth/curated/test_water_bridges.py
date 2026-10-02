"""Compare sparse paths with independent joins of original ProLIF HBDonor legs."""

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm

CASES = json.loads(
    (
        Path(__file__).resolve().parents[3]
        / "devtools/data/water_bridge_validation_systems.json"
    ).read_text()
)["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["smiles"])
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_original_reference_legs_and_independent_single_water_paths(
    case, form, tmp_path
):
    source = Chem.AddHs(Chem.MolFromSmiles(case["smiles"]))
    for xyz in case["coordinates_nm"]:
        conformer = Chem.Conformer(source.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        source.AddConformer(conformer, assignId=True)
    if form != "rdkit":
        source = msm.convert(source, to_form="molsysmt.MolSys")
    if form == "h5msm":
        path = str(tmp_path / "source.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.water_bridges.get_water_bridges(
        source,
        pbc=False,
        hbond_method="donor_acceptor_distance_angle",
        hbond_profile="smarts_donor_acceptor",
    )
    expected = {
        (o["structure_index"], tuple(o["atoms"])): o for o in case["observations"]
    }
    actual = {}
    for row, (frame, relation) in enumerate(
        zip(result.occurrence_structures, result.occurrence_relations)
    ):
        key = (
            int(frame),
            tuple(
                int(p["atom_indices"][0])
                for p in result.relation(int(relation))["participants"]
            ),
        )
        assert key not in actual
        actual[key] = row
    assert actual.keys() == expected.keys()
    for key, row in actual.items():
        for branch in (1, 2):
            np.testing.assert_allclose(
                result.measurements[f"leg_{branch}_donor_acceptor_distance"][row],
                expected[key]["da_nm"][branch - 1],
                atol=1e-12,
            )
            np.testing.assert_allclose(
                result.measurements[f"leg_{branch}_dha_angle"][row],
                expected[key]["dha_radians"][branch - 1],
                atol=1e-12,
            )
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]


TWO_WATER_CASES = json.loads(
    (
        Path(__file__).resolve().parents[3]
        / "devtools/data/two_water_bridge_validation_systems.json"
    ).read_text()
)["cases"]


@pytest.mark.parametrize("case", TWO_WATER_CASES, ids=lambda case: case["name"])
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_original_reference_legs_and_independent_two_water_paths(case, form, tmp_path):
    source = Chem.AddHs(Chem.MolFromSmiles(case["smiles"]))
    for xyz in case["coordinates_nm"]:
        conformer = Chem.Conformer(source.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        source.AddConformer(conformer, assignId=True)
    if form != "rdkit":
        source = msm.convert(source, to_form="molsysmt.MolSys")
    if form == "h5msm":
        path = str(tmp_path / "source.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.water_bridges.get_water_bridges(
        source,
        order=2,
        pbc=False,
        hbond_method="donor_acceptor_distance_angle",
        hbond_profile="smarts_donor_acceptor",
    )
    expected = {
        (o["structure_index"], tuple(o["atoms"])): o for o in case["observations"]
    }
    actual = {}
    for row, (frame, relation) in enumerate(
        zip(result.occurrence_structures, result.occurrence_relations)
    ):
        key = (
            int(frame),
            tuple(
                int(p["atom_indices"][0])
                for p in result.relation(int(relation))["participants"]
            ),
        )
        assert key not in actual
        actual[key] = row
    assert actual.keys() == expected.keys()
    for key, row in actual.items():
        for branch in range(1, 4):
            np.testing.assert_allclose(
                result.measurements[f"leg_{branch}_donor_acceptor_distance"][row],
                expected[key]["da_nm"][branch - 1],
                atol=1e-12,
            )
            np.testing.assert_allclose(
                result.measurements[f"leg_{branch}_dha_angle"][row],
                expected[key]["dha_radians"][branch - 1],
                atol=1e-12,
            )
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
