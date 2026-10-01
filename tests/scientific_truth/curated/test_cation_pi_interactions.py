"""Compare attributed observations with unmodified ProLIF 2.2.2 truth."""

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw

MANIFEST = Path(__file__).resolve().parents[3] / 'devtools/data/cation_pi_validation_systems.json'
CASES = json.loads(MANIFEST.read_text())['cases']


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['name'])
@pytest.mark.parametrize('form', ['rdkit', 'native', 'h5msm'])
def test_prolif_original_observations_survive_forms(case, form, tmp_path):
    if 'bundled_protein' in case:
        from devtools.scripts.ionic_validation_systems import prepare_system
        _, reference, coordinates, molecule = prepare_system(case['bundled_protein'])
        assert reference['sha256'] == case['sha256']
    else:
        molecule = Chem.MolFromSmiles(case['smiles'])
        coordinates = np.asarray(case['coordinates_nm'])
    molecule.RemoveAllConformers()
    for xyz in coordinates:
        conformer = Chem.Conformer(molecule.GetNumAtoms())
        conformer.SetPositions(xyz * 10)
        molecule.AddConformer(conformer, assignId=True)
    source = molecule
    if form != 'rdkit':
        source = msm.convert(molecule, to_form='molsysmt.MolSys')
    if form == 'h5msm':
        path = str(tmp_path / 'truth.h5msm')
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.cation_pi.get_cation_pi_interactions(
        source, distance_threshold=puw.quantity(case['distance_nm'], 'nm'),
        angle_threshold=puw.quantity(case['angle_degrees'], 'degrees'), pbc=False,
        heavy_mode='force' if form == 'h5msm' else 'off')
    expected = {(item['structure_index'], tuple(item['cation']), tuple(item['ring'])):
                (item['distance_nm'], min(item['normal_angle_radians'], np.pi - item['normal_angle_radians']), item['normal_angle_radians']) for item in case['observations']}
    actual = {}
    for row, (frame, relation_index) in enumerate(zip(result.occurrence_structures, result.occurrence_relations)):
        participants = result.relation(int(relation_index))['participants']
        key = int(frame), tuple(participants[0]['atom_indices']), tuple(participants[1]['atom_indices'])
        assert key not in actual
        actual[key] = (result.measurements['distance'][row], result.measurements['normal_angle'][row], result.measurements['oriented_normal_angle'][row])
    assert actual.keys() == expected.keys()
    for key in expected:
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-12, rtol=0)
    assert result.evaluated_structure_indices.tolist() == list(range(len(coordinates)))
    assert result.parameters['method_reference']['version'] == '2.2.2'
