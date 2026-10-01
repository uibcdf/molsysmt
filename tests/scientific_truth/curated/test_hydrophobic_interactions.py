"""Compare hydrophobic atoms and unordered observations with original ProLIF."""

import json
from pathlib import Path

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm

MANIFEST = Path(__file__).resolve().parents[3] / 'devtools/data/hydrophobic_validation_systems.json'
CASES = json.loads(MANIFEST.read_text())['cases']


@pytest.mark.parametrize('case', CASES, ids=lambda case: case['smiles'] + ('-indexed-H' if case['add_hydrogens'] else ''))
@pytest.mark.parametrize('form', ['rdkit', 'native', 'h5msm'])
def test_original_sites_and_observations_survive_forms(case, form, tmp_path):
    source = Chem.MolFromSmiles(case['smiles'])
    if case['add_hydrogens']:
        source = Chem.AddHs(source)
    for xyz in case['coordinates_nm']:
        conformer = Chem.Conformer(source.GetNumAtoms())
        conformer.SetPositions(np.asarray(xyz) * 10)
        source.AddConformer(conformer, assignId=True)
    if form != 'rdkit':
        source = msm.convert(source, to_form='molsysmt.MolSys')
    if form == 'h5msm':
        path = str(tmp_path / 'reference.h5msm')
        msm.convert(source, to_form=path)
        source = path
    sites = msm.physchem.get_hydrophobic_sites(source)
    assert sites['hydrophobic_atom_indices'].tolist() == case['hydrophobic_atom_indices']
    result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, pbc=False, heavy_mode='force' if form == 'h5msm' else 'off')
    expected = {(item['structure_index'], tuple(item['atoms'])): item['distance_nm']
                for item in case['observations']}
    actual = {}
    for row, (frame, relation) in enumerate(zip(result.occurrence_structures, result.occurrence_relations)):
        participants = result.relation(int(relation))['participants']
        key = int(frame), tuple(int(p['atom_indices'][0]) for p in participants)
        assert key not in actual
        actual[key] = result.measurements['distance'][row]
    assert actual.keys() == expected.keys()
    for key in expected:
        np.testing.assert_allclose(actual[key], expected[key], atol=1e-12, rtol=0)
    assert result.evaluated_structure_indices.tolist() == list(range(len(case['coordinates_nm'])))
    # A reversed disjoint atom partition must select the same canonical subset.
    midpoint = result.n_atoms // 2
    between = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, selection=list(range(midpoint, result.n_atoms)), selection_2=list(range(midpoint)),
        selection_mode='between', pbc=False)
    expected_cross = {key for key in expected if key[1][0] < midpoint <= key[1][1]}
    actual_cross = {(int(frame), tuple(int(p['atom_indices'][0]) for p in between.relation(int(relation))['participants']))
                    for frame, relation in zip(between.occurrence_structures, between.occurrence_relations)}
    assert actual_cross == expected_cross
