"""Protect directed metal roles, chemical evidence and sparse geometric candidates."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MemoryBudgetExceededError


def _system(n_frames=3):
    molsys = msm.convert(Chem.MolFromSmiles('[Zn+2].O.N'), to_form='molsysmt.MolSys')
    xyz = np.repeat(np.array([[[0, 0, 0], [.2, 0, 0], [0, .27, 0]]]), n_frames, axis=0)
    if n_frames == 3:
        xyz[1, 1:] += 2
    molsys.structures.append(coordinates=puw.quantity(xyz, 'nm'))
    return molsys


@pytest.mark.parametrize('mode,first,second,count', [
    ('internal', [0, 1], None, 2), ('internal', [1], None, 0),
    ('incident', [0], None, 4), ('incident', [1], None, 2),
    ('between', [1, 2], [0], 4), ('between', [0], [1], 2),
])
def test_directed_roles_sparse_queries_and_empty_frames(mode, first, second, count):
    source = _system()
    result = msm.interactions.metal_coordination.get_metal_coordination(
        source, selection=first, selection_2=second, selection_mode=mode,
        structure_indices=[2, 0, 2, 1], pbc=False)
    assert result.n_interactions == count
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.query(structure_indices=[1]).n_interactions == 0
    assert not source.interactions
    if count:
        assert result.participant_roles == ('metal', 'ligand') * (count // 2)
        assert result.query(atom_indices=[0], mode='incident').n_interactions == count
        assert result.query(atom_indices=[0], mode='internal').n_interactions == 0
        assert result.relation_types == ('metal_coordination_candidate',) * (count // 2)


@pytest.mark.parametrize('form', ['native', 'rdkit', 'composite', 'h5msm'])
def test_form_parity_and_named_typed_persistence(form, tmp_path):
    source = _system()
    reference = msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False)
    source.interactions = {'metal-sites': reference}
    path = str(tmp_path / 'metal.h5msm')
    msm.convert(source, to_form=path)
    if form == 'rdkit':
        source = msm.convert(source, to_form='rdkit.Mol')
    elif form == 'composite':
        source = [source.topology, source.structures]
    elif form == 'h5msm':
        source = path
    result = msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False)
    np.testing.assert_array_equal(result.participant_atoms, reference.participant_atoms)
    np.testing.assert_allclose(result.measurements['distance'], reference.measurements['distance'])
    loaded = msm.convert(path, to_form='molsysmt.MolSys')
    assert loaded.interactions['metal-sites'].parameters == reference.parameters
    assert loaded.interactions['metal-sites'].software == reference.software
    subset = msm.extract(loaded, selection=[2, 0], structure_indices=[2, 1, 0])
    assert subset.interactions['metal-sites'].n_interactions == 2
    assert msm.extract(loaded, selection=[1, 2]).interactions['metal-sites'].n_interactions == 0
    typed = msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False, output_type='molsysmt.InteractionsDict')
    assert msm.convert(typed, to_form='molsysmt.Interactions').n_interactions == 4


@pytest.mark.parametrize('box', [np.eye(3), np.array([[1, .1, 0], [0, 1, .1], [0, 0, 1.]])])
def test_periodic_images_and_nondefault_units(box):
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    xyz[0, 1] += np.array([1, -1, 0]) @ box
    source.structures.coordinates = puw.quantity(xyz * 10, 'angstrom')
    source.structures.box = puw.quantity(box[None] * 10, 'angstrom')
    with puw.context(standard_units=['angstrom', 'degrees', 'ps', 'e']):
        result = msm.interactions.metal_coordination.get_metal_coordination(source, distance_threshold='2.8 angstrom')
    pairs = result.participant_atoms.reshape(-1, 2)
    observed = xyz[0, pairs] + result.image_vectors.reshape(-1, 2, 3) @ box
    np.testing.assert_allclose(np.linalg.norm(observed[:, 1] - observed[:, 0], axis=1), result.measurements['distance'])
    np.testing.assert_allclose(result.measurements['distance'], [.2, .27])
    assert result.measure_units == {'distance': 'nm'}
    reverse = msm.interactions.metal_coordination.get_metal_coordination(source, selection=[1, 2], selection_2=[0], selection_mode='between')
    np.testing.assert_array_equal(result.image_vectors, reverse.image_vectors)


@pytest.mark.parametrize('options', [
    {'method': 'prolif'}, {'profile': 'all_metals'}, {'distance_threshold': .28},
    {'distance_threshold': '1 ps'}, {'distance_threshold': '-1 nm'},
    {'distance_threshold': puw.quantity([.2, .3], 'nm')}, {'structure_indices': [3]},
    {'selection_mode': 'between'}, {'selection_2': [1]},
    {'selection_mode': 'between', 'selection': [0], 'selection_2': [0]},
])
def test_invalid_parameters_fail(options):
    with pytest.raises(msm.ArgumentError):
        msm.interactions.metal_coordination.get_metal_coordination(_system(), pbc=False, **options)


def test_inclusive_cutoff_empty_evaluation_and_geometry_errors():
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    xyz[0, 1] = [.28, 0, 0]
    source.structures.coordinates = puw.quantity(xyz, 'nm')
    assert msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False).n_interactions == 2
    assert msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False, distance_threshold='.279 nm').n_interactions == 1
    empty = msm.interactions.metal_coordination.get_metal_coordination(source, selection=[], pbc=False)
    assert empty.evaluated_structure_indices.tolist() == [0] and empty.n_interactions == 0
    assert empty.query().to_dict()['occurrence_indices'].dtype == np.int64
    xyz = xyz.copy()
    xyz[0, 0, 0] = np.nan
    source.structures.coordinates = puw.quantity(xyz, 'nm')
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False)
    source = _system(n_frames=1)
    source.structures.box = puw.quantity(np.zeros((1, 3, 3)), 'nm')
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.interactions.metal_coordination.get_metal_coordination(source)


def test_streamed_h5_projection_and_budget(monkeypatch, tmp_path):
    source = _system(n_frames=50)
    path = str(tmp_path / 'source.h5msm')
    msm.convert(source, to_form=path)
    monkeypatch.setattr(msm.configure, 'chunk_size', 7)
    monkeypatch.setattr(msm.configure, 'max_ram_usage', 2_000_000)
    from molsysmt.form import _h5msm05_modular
    monkeypatch.setattr(_h5msm05_modular, 'read_molsys_file', lambda *a, **k: pytest.fail('Full file load'))
    for item in (source, path):
        result = msm.interactions.metal_coordination.get_metal_coordination(item, pbc=False, heavy_mode='force')
        assert result.n_interactions == 100 and result.execution_records[0]["details"]['execution_chunks'] == 8
    monkeypatch.setattr(msm.configure, 'max_ram_usage', 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.interactions.metal_coordination.get_metal_coordination(source, pbc=False)
