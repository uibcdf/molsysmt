"""Compare four-role observations against unmodified ProLIF 2.2.2."""

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw

MANIFEST = Path(__file__).resolve().parents[3] / "devtools/data/halogen_bond_validation_systems.json"
CASES = json.loads(MANIFEST.read_text())["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["smiles"])
@pytest.mark.parametrize("form", ["rdkit", "native", "h5msm"])
def test_original_reference_observations_survive_forms(case, form, tmp_path):
    molecule = Chem.MolFromSmiles(case["smiles"])
    coordinates = np.asarray(case["coordinates_nm"])
    for xyz in coordinates:
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(xyz * 10)
        molecule.AddConformer(conformer, assignId=True)
    source = molecule
    if form != "rdkit":
        source = msm.convert(molecule, to_form="molsysmt.MolSys")
    if form == "h5msm":
        path = str(tmp_path / "reference.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.halogen_bonds.get_halogen_bonds(
        source, pbc=False, heavy_mode="force" if form == "h5msm" else "off")
    expected = {
        (item["structure_index"], tuple(item["donor_halogen"]), tuple(item["acceptor_reference"])):
        (item["distance_nm"], item["donor_angle_radians"], item["acceptor_angle_radians"])
        for item in case["observations"]
    }
    actual = {}
    for row, (frame, relation) in enumerate(zip(result.occurrence_structures, result.occurrence_relations)):
        participants = result.relation(int(relation))["participants"]
        atoms = [int(participant["atom_indices"][0]) for participant in participants]
        key = int(frame), tuple(atoms[:2]), tuple(atoms[2:])
        assert key not in actual
        actual[key] = tuple(result.measurements[name][row] for name in
                            ("distance", "donor_angle", "acceptor_angle"))
    boundary = set(case.get("boundary_structure_indices", []))
    assert {key for key in actual if key[0] not in boundary} == {
        key for key in expected if key[0] not in boundary}
    # An exact nominal cutoff can change membership by roundoff after the
    # angstrom-to-nanometer conversion. Check its geometry and strict rule
    # independently; never broaden the production detector's threshold.
    if boundary and any(key[0] in boundary for key in expected):
        widened = msm.interactions.halogen_bonds.get_halogen_bonds(
            source, pbc=False, structure_indices=sorted(boundary),
            distance_threshold="0.351 nm",
            donor_angle_range=puw.quantity([129.9, 180], "degrees"),
            acceptor_angle_range=puw.quantity([79.9, 140], "degrees"))
        assert widened.n_interactions == 1
        values = tuple(widened.measurements[name][0] for name in
                       ("distance", "donor_angle", "acceptor_angle"))
        key = next(key for key in expected if key[0] in boundary)
        np.testing.assert_allclose(values, expected[key], atol=1e-15, rtol=0)
        accepted = values[0] <= .35 and np.deg2rad(130) <= values[1] <= np.pi
        accepted &= np.deg2rad(80) <= values[2] <= np.deg2rad(140)
        assert (key in actual) == bool(accepted)
    for key in expected.keys() & actual.keys():
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-12, rtol=0)
    assert result.evaluated_structure_indices.tolist() == list(range(len(coordinates)))
