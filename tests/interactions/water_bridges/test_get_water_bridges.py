"""Protect same-frame single-water path identities, atom scope and periodic legs."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MemoryBudgetExceededError


def _system(kind='donor', n_frames=3):
    smiles = {'donor': 'O.C=O.C=O', 'acceptor': 'O.N.N', 'mixed': 'O.N.C=O'}[kind]
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    molsys = msm.convert(molecule, to_form='molsysmt.MolSys')
    xyz = np.zeros((molecule.GetNumAtoms(), 3))
    xyz[:, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
    water_h = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(0).GetNeighbors())
    xyz[0] = [0, 0, 0]
    xyz[water_h] = [[.1, 0, 0], [0, .1, 0]]
    endpoints = []
    for position, fragment in enumerate(Chem.GetMolFrags(molecule)[1:]):
        nitrogen = [i for i in fragment if molecule.GetAtomWithIdx(i).GetSymbol() == 'N']
        axis = np.eye(3)[position]
        if nitrogen:
            donor = nitrogen[0]
            hydrogen = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(donor).GetNeighbors())[0]
            xyz[donor], xyz[hydrogen] = -.3 * axis, -.2 * axis
            endpoints.append([donor, hydrogen, 0])
        else:
            acceptor = next(i for i in fragment if molecule.GetAtomWithIdx(i).GetSymbol() == 'O')
            xyz[acceptor] = .3 * axis
            endpoints.append([0, water_h[position], acceptor])
    coordinates = np.repeat(xyz[None], n_frames, axis=0)
    if n_frames == 3:
        external = [i for i in endpoints[1] if i not in [0, *water_h]]
        coordinates[1, external] += [2, 2, 2]
    molsys.structures.append(coordinates=puw.quantity(coordinates, 'nm'))
    return molsys, np.array(endpoints, dtype=np.int64).ravel(), water_h


@pytest.mark.parametrize('kind', ['donor', 'acceptor', 'mixed'])
@pytest.mark.parametrize('method,profile', [
    ('baker_hubbard', None), ('wernet_nilsson', None),
    ('donor_acceptor_distance_angle', 'smarts_donor_acceptor'),
])
def test_analytic_two_leg_truth_for_all_water_directions(kind, method, profile):
    source, atoms, _ = _system(kind)
    result = msm.interactions.water_bridges.get_water_bridges(source, pbc=False, hbond_method=method, hbond_profile=profile)
    assert result.n_interactions == 2 and not source.interactions
    np.testing.assert_array_equal(result.participant_atoms, atoms)
    assert result.occurrence_structures.tolist() == [0, 2]
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    for branch in (1, 2):
        np.testing.assert_allclose(result.measurements[f'leg_{branch}_donor_acceptor_distance'], .3)
        np.testing.assert_allclose(result.measurements[f'leg_{branch}_hydrogen_acceptor_distance'], .2)
        np.testing.assert_allclose(result.measurements[f'leg_{branch}_dha_angle'], np.pi)
    assert result.parameters['hbond_parameters']['method'] == method
    assert result.parameters['mediator_order'] == 1


@pytest.mark.parametrize('mode', ['internal', 'incident', 'between'])
def test_all_participant_scopes_nonconsecutive_frames_and_queries(mode):
    source, atoms, _ = _system()
    actual = np.unique(atoms)
    kwargs = dict(selection=actual, selection_mode=mode)
    if mode == 'between':
        kwargs.update(selection=[0], selection_2=np.setdiff1d(actual, [0]))
    elif mode == 'incident':
        kwargs.update(selection=[2])
    result = msm.interactions.water_bridges.get_water_bridges(source, structure_indices=[2, 0, 2], pbc=False, **kwargs)
    assert result.n_interactions == 2 and result.evaluated_structure_indices.tolist() == [0, 2]
    assert result.query(atom_indices=[0], mode='incident').n_interactions == 2
    assert result.query(atom_indices=[0], mode='internal').n_interactions == 0
    assert result.query(atom_indices=[0], mode='cross').n_interactions == 2
    assert result.query(atom_indices=actual, mode='internal').n_interactions == 2
    endpoints_only = msm.interactions.water_bridges.get_water_bridges(source, selection=[2, 4], pbc=False)
    assert endpoints_only.n_interactions == 0  # Internal never implicitly adds mediator atoms.


@pytest.mark.parametrize('box', [np.eye(3), np.array([[1, .1, 0], [0, 1, .1], [0, 0, 1.]])])
@pytest.mark.parametrize('kind', ['donor', 'acceptor', 'mixed'])
def test_periodic_images_preserve_both_actual_branch_geometries(box, kind):
    source, atoms, _ = _system(kind, n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    shifts = np.zeros((msm.get(source, n_atoms=True), 3), dtype=int)
    shifts[np.unique(atoms)] = [[i % 3 - 1, i % 2, 0] for i in range(len(np.unique(atoms)))]
    # Only imaged participating atoms have scientifically controlled coordinates.
    xyz[0] += shifts @ box
    source.structures.coordinates = puw.quantity(xyz * 10, 'angstrom')
    source.structures.box = puw.quantity(box[None] * 10, 'angstrom')
    with puw.context(standard_units=['angstrom', 'degrees', 'ps', 'e']):
        result = msm.interactions.water_bridges.get_water_bridges(source, distance_threshold='2.5 angstrom', angle_threshold='120 degrees')
    assert result.n_interactions == 1
    observed = xyz[0, result.participant_atoms] + result.image_vectors @ box
    for branch in (1, 2):
        d, h, a = observed[(branch - 1) * 3:branch * 3]
        np.testing.assert_allclose(np.linalg.norm(d - a), result.measurements[f'leg_{branch}_donor_acceptor_distance'][0])
        np.testing.assert_allclose(np.linalg.norm(h - a), result.measurements[f'leg_{branch}_hydrogen_acceptor_distance'][0])
    for atom in np.unique(atoms):
        images = result.image_vectors[result.participant_atoms == atom]
        assert np.all(images == images[0])
    assert np.all(result.image_vectors[0] == 0)


@pytest.mark.parametrize('form', ['native', 'rdkit', 'composite', 'h5msm'])
def test_form_parity_named_h5_roundtrip_reorder_and_removal(form, tmp_path):
    source, atoms, _ = _system()
    reference = msm.interactions.water_bridges.get_water_bridges(source, pbc=False)
    source.interactions = {'solvent-paths': reference}
    path = str(tmp_path / 'paths.h5msm')
    msm.convert(source, to_form=path)
    if form == 'rdkit':
        source = msm.convert(source, to_form='rdkit.Mol')
    elif form == 'composite':
        source = [source.topology, source.structures]
    elif form == 'h5msm':
        source = path
    result = msm.interactions.water_bridges.get_water_bridges(source, pbc=False)
    np.testing.assert_array_equal(result.participant_atoms, atoms)
    loaded = msm.convert(path, to_form='molsysmt.MolSys')
    restored = loaded.interactions['solvent-paths']
    assert restored.parameters == reference.parameters and restored.software == reference.software
    np.testing.assert_array_equal(restored.to_dict()['occurrence_indices'], reference.to_dict()['occurrence_indices'])
    typed = msm.interactions.water_bridges.get_water_bridges(source, pbc=False, output_type='molsysmt.InteractionsDict')
    assert msm.convert(typed, to_form='molsysmt.Interactions').parameters == reference.parameters
    assert msm.extract(loaded, selection=np.unique(atoms)[::-1], structure_indices=[2, 1, 0]).interactions['solvent-paths'].n_interactions == 2
    assert msm.extract(loaded, selection=np.setdiff1d(np.arange(msm.get(loaded, n_atoms=True)), [0])).interactions['solvent-paths'].n_interactions == 0


def test_legs_from_different_frames_are_not_a_bridge_and_empty_shapes():
    source, atoms, _ = _system(n_frames=2)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    xyz[0, atoms[-1]] += 2
    xyz[1, atoms[2]] += 2
    source.structures.coordinates = puw.quantity(xyz, 'nm')
    result = msm.interactions.water_bridges.get_water_bridges(source, pbc=False)
    assert result.n_interactions == 0 and result.evaluated_structure_indices.tolist() == [0, 1]
    assert result.query().to_dict()['occurrence_indices'].shape == (0,)
    assert set(result.measure_units.values()) == {'nm', 'radians'}
    no_frames = msm.interactions.water_bridges.get_water_bridges(source, structure_indices=[], pbc=False)
    assert no_frames.evaluated_structure_indices.shape == (0,)


@pytest.mark.parametrize('options', [
    {'method': 'prolif'}, {'profile': 'multiwater'}, {'hbond_method': 'invented'},
    {'hbond_profile': 'explicit_sites', 'hbond_method': 'donor_acceptor_distance_angle'},
    {'distance_threshold': .25}, {'distance_threshold': '1 ps'}, {'distance_threshold': '-1 nm'},
    {'angle_threshold': '1 nm'}, {'angle_threshold': '-1 degrees'},
    {'structure_indices': [3]}, {'selection_mode': 'between'}, {'selection_2': [2]},
    {'selection_mode': 'between', 'selection': [0], 'selection_2': [0]},
])
def test_invalid_parameters_fail(options):
    with pytest.raises(msm.ArgumentError):
        msm.interactions.water_bridges.get_water_bridges(_system()[0], pbc=False, **options)


def test_streaming_legs_from_h5_without_full_coordinate_loading(monkeypatch, tmp_path):
    source, _, _ = _system(n_frames=50)
    path = str(tmp_path / 'water.h5msm')
    msm.convert(source, to_form=path)
    monkeypatch.setattr(msm.configure, 'chunk_size', 7)
    monkeypatch.setattr(msm.configure, 'max_ram_usage', 2_000_000)
    from molsysmt.form import _h5msm05_modular
    monkeypatch.setattr(_h5msm05_modular, 'read_molsys_file', lambda *a, **k: pytest.fail('Full file load'))
    for item in (source, path):
        result = msm.interactions.water_bridges.get_water_bridges(item, pbc=False, heavy_mode='force')
        assert result.n_interactions == 50 and result.execution_records[0]["details"]['execution_chunks'] == 8
    selected = msm.interactions.water_bridges.get_water_bridges(path, pbc=False, heavy_mode='force', structure_indices=[49, 0, 25, 49])
    assert selected.occurrence_structures.tolist() == [0, 25, 49]
    monkeypatch.setattr(msm.configure, 'max_ram_usage', 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.interactions.water_bridges.get_water_bridges(source, pbc=False)


def test_ackredit_and_saved_leg_attribution_preserve_real_producer():
    ackredit = pytest.importorskip('ackredit')
    with ackredit.session('water-producer'):
        result = msm.interactions.water_bridges.get_water_bridges(_system()[0], pbc=False)
        credited = ackredit.get_used_items()
        assert 'doi:10.1186/s13321-021-00548-6' in credited
        assert any(item['roles'] == ['scientific_criterion'] for item in result.parameters['attribution']['items'])
    with ackredit.session('water-reader'):
        typed = msm.convert(result, to_form='molsysmt.InteractionsDict')
        assert msm.convert(typed, to_form='molsysmt.Interactions').parameters == result.parameters
        assert ackredit.get_used_items() == {}


def test_bifurcated_water_hydrogen_is_a_shared_atom_not_a_lost_role():
    source, atoms, _ = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    xyz[0, atoms[-1]] = [.32, .01, 0]
    source.structures.coordinates = puw.quantity(xyz, 'nm')
    result = msm.interactions.water_bridges.get_water_bridges(source, pbc=False)
    assert result.n_interactions == 1
    assert result.participant_atoms[1] == result.participant_atoms[4]
    assert result.participant_atoms[0] == result.participant_atoms[3] == 0
    assert result.query(atom_indices=[result.participant_atoms[1]], mode='incident').n_interactions == 1


def test_two_legs_to_the_same_external_heavy_atom_do_not_form_a_path():
    source, atoms, _ = _system('acceptor', n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    xyz[0, atoms[3:5]] += 2
    molecule = msm.convert(source, to_form='rdkit.Mol')
    extra_h = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(int(atoms[0])).GetNeighbors())[1]
    xyz[0, extra_h] = [-.2, .01, 0]
    source.structures.coordinates = puw.quantity(xyz, 'nm')
    legs = msm.interactions.hbonds.get_hbonds(source, selection=[0], selection_mode='incident', pbc=False)
    assert legs.n_interactions == 2
    assert msm.interactions.water_bridges.get_water_bridges(source, pbc=False).n_interactions == 0


def test_dense_path_fanout_fails_its_sparse_budget(monkeypatch):
    molecule = Chem.AddHs(Chem.MolFromSmiles('O.' + '.'.join(['C=O'] * 40)))
    source = msm.convert(molecule, to_form='molsysmt.MolSys')
    xyz = np.zeros((1, molecule.GetNumAtoms(), 3))
    xyz[0, :, 2] = np.arange(molecule.GetNumAtoms()) * 3 + 3
    water_h = sorted(a.GetIdx() for a in molecule.GetAtomWithIdx(0).GetNeighbors())
    xyz[0, 0], xyz[0, water_h] = [0, 0, 0], [[.1, 0, 0], [0, .1, 0]]
    for atom in molecule.GetAtoms():
        if atom.GetSymbol() == 'O' and atom.GetIdx() != 0:
            xyz[0, atom.GetIdx()] = [.3, 0, 0]
    source.structures.append(coordinates=puw.quantity(xyz, 'nm'))
    monkeypatch.setattr(msm.configure, 'max_ram_usage', 1_000_000)
    with pytest.raises(MemoryBudgetExceededError, match='sparse-result'):
        msm.interactions.water_bridges.get_water_bridges(source, pbc=False)
