"""H5MSM 0.4 chemical-state persistence and 0.3 migration tests."""

from pathlib import Path

import h5py
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FormatError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


def _rich_topology():
    topology = Topology(n_atoms=4)
    topology.atoms['atom_id'] = ['7', '7', '9', '10']
    topology.atoms['atom_name'] = ['C1', 'N1', 'O1', 'H1']
    topology.atoms['isotope'] = pd.array([13, pd.NA, 18, pd.NA], dtype='UInt16')
    topology._set_component_indices([0, 0, 0, 0])
    topology.components.loc[0] = ['cmp', 'ligand', 'small molecule']
    state = topology._reference_chemical_state
    state.state_id = 'neutral'
    state.connectivity_completeness = 'complete'
    state.component_completeness = 'complete'
    state.component_evidence = 'explicit'
    state.provenance_index = 3
    msm.set(
        topology,
        element='atom',
        formal_charge=[0, 1, -1, None],
        atom_is_aromatic=[True, True, False, None],
        n_unpaired_electrons=[0, 0, 1, None],
        n_implicit_hydrogens=[0, 0, 0, None],
        allows_implicit_hydrogens=[False, False, True, None],
        atom_stereochemistry=['R', 'unspecified', None, None],
    )
    topology._append_chemical_state_bonds(
        [[0, 1], [1, 2]],
        bond_id=['b', None],
        bond_order=[1, None],
        fractional_bond_order=[None, 1.5],
        bond_type=['covalent', 'dative'],
        is_aromatic=[True, False],
        is_conjugated=[True, None],
        stereochemistry=['E', None],
        stereo_atom1_index=[2, None],
        stereo_atom2_index=[3, None],
        donor_atom_index=[None, 1],
        acceptor_atom_index=[None, 2],
        joins_components=[True, False],
        evidence=['explicit', 'inferred'],
        provenance_index=[3, None],
    )
    return topology


def test_v04_roundtrip_preserves_full_reference_state(tmp_path):
    topology = _rich_topology()
    filename = tmp_path / 'rich.h5msm'

    msm.convert(topology, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.Topology')

    with h5py.File(filename, 'r') as file:
        assert file.attrs['version'] == '0.4'
        assert file['topology/components'].id == file['topology/chemical_states/0/components'].id
        assert file['topology/bonds/atom1_index'].id == file['topology/chemical_states/0/bonds/atom1_index'].id
        assert file['topology/bonds/order'].id == file['topology/chemical_states/0/bonds/bond_order'].id
        assert file['topology/atoms/component_index'].id == file['topology/chemical_states/0/component_indices'].id

    state = observed._reference_chemical_state
    assert state.state_id == 'neutral'
    assert state.connectivity_completeness == 'complete'
    assert state.component_completeness == 'complete'
    assert state.component_evidence == 'explicit'
    assert state.provenance_index == 3
    assert state.atom_attributes.equals(topology._reference_chemical_state.atom_attributes)
    assert state.component_indices.equals(topology._get_component_indices())
    assert state.components.astype('string').equals(topology.components.astype('string'))
    assert state.bonds.equals(topology.bonds)
    assert observed.atoms['atom_id'].tolist() == ['7', '7', '9', '10']
    assert observed.atoms['isotope'].equals(topology.atoms['isotope'])
    assert msm.get(filename, element='atom', isotope=True)[0] == 13
    assert msm.get(filename, element='atom', formal_charge=True)[:3] == [0, 1, -1]
    assert msm.get(filename, element='atom', atom_is_aromatic=True)[:3] == [True, True, False]
    assert msm.has_attribute(filename, 'atom_stereochemistry')


def test_v04_roundtrip_preserves_multiple_states_without_reference(tmp_path):
    topology = _rich_topology()
    second_index = topology._append_chemical_state(state_id='radical')
    topology._set_chemical_state_atom_attribute(
        'formal_charge', [1, 0, -1, 0], state_index=second_index
    )
    topology._set_component_indices([0, 0, 1, 1], state_index=second_index)
    second = topology._resolve_chemical_state(second_index)
    second.components = topology.components.copy()
    second.components.loc[1] = ['solvent', 'water', 'water']
    topology._append_chemical_state_bonds(
        [[0, 2]], bond_order=[2], bond_type=['covalent'],
        joins_components=[True], state_index=second_index,
    )
    topology._set_reference_chemical_state_index(None)
    filename = tmp_path / 'multi.h5msm'

    msm.convert(topology, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert msm.get(filename, element='system', n_chemical_states=True) == 2
    assert msm.get(filename, element='system', chemical_state_id=True) == [
        'neutral', 'radical'
    ]
    assert len(observed._chemical_states) == 2
    assert observed._reference_chemical_state_index is None
    assert observed._chemical_states[0].state_id == 'neutral'
    assert observed._chemical_states[1].state_id == 'radical'
    assert observed._chemical_states[1].component_indices.tolist() == [0, 0, 1, 1]
    assert observed._chemical_states[1].bonds['bond_order'].tolist() == [2]
    metadata = msm.get(
        observed,
        element='system',
        output_type='dictionary',
        chemical_state_index=True,
        chemical_state_id=True,
        n_chemical_states=True,
        reference_chemical_state_index=True,
        connectivity_completeness=True,
        component_completeness=True,
        component_evidence=True,
    )
    assert metadata == {
        'chemical_state_index': [0, 1],
        'chemical_state_id': ['neutral', 'radical'],
        'n_chemical_states': 2,
        'reference_chemical_state_index': None,
        'connectivity_completeness': ['complete', 'partial'],
        'component_completeness': ['complete', 'unavailable'],
        'component_evidence': ['explicit', 'unknown'],
    }
    with pytest.raises(StructuralInconsistencyError, match='ambiguous'):
        msm.get(observed, element='atom', formal_charge=True)


def test_v04_selected_write_remaps_every_state(tmp_path):
    topology = _rich_topology()
    second_index = topology._append_chemical_state(state_id='second')
    topology._set_component_indices([0, 0, 0, 0], state_index=second_index)
    topology._resolve_chemical_state(second_index).components = topology.components.copy()
    topology._append_chemical_state_bonds(
        [[1, 2], [2, 3]], bond_order=[1, 1], state_index=second_index
    )
    filename = tmp_path / 'selected.h5msm'

    msm.convert(
        topology, to_form='file:h5msm', selection=[1, 2, 3], output_filename=filename
    )
    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert observed.n_atoms == 3
    assert observed._chemical_states[0].bonds['atom1_index'].tolist() == [0]
    assert observed._chemical_states[0].bonds['atom2_index'].tolist() == [1]
    assert observed._chemical_states[1].bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1], [1, 2]]


def test_v03_bundled_file_migrates_to_one_reference_state():
    filename = Path(__file__).parent / 'data' / 'alanine_dipeptide_v03.h5msm'

    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert msm.get(filename, element='system', n_chemical_states=True) == 1
    assert msm.get(filename, element='system', component_evidence=True) == ['unknown']
    assert len(observed._chemical_states) == 1
    assert observed._reference_chemical_state_index == 0
    assert observed._reference_chemical_state.connectivity_completeness == 'complete'
    assert observed._reference_chemical_state.component_evidence == 'unknown'


def test_v03_numeric_ids_are_normalized_to_strings(tmp_path):
    source = Path(__file__).parent / 'data' / 'alanine_dipeptide_v03.h5msm'
    filename = tmp_path / 'numeric-ids.h5msm'
    filename.write_bytes(source.read_bytes())
    with h5py.File(filename, 'r+') as file:
        del file['topology/atoms/atom_id']
        file['topology/atoms'].create_dataset('atom_id', data=np.arange(22))

    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert observed.atoms['atom_id'].tolist() == [str(index) for index in range(22)]


def test_unknown_h5msm_version_is_rejected(tmp_path):
    filename = tmp_path / 'future.h5msm'
    with h5py.File(filename, 'w') as file:
        file.attrs['type'] = 'h5msm'
        file.attrs['version'] = '99.0'

    with pytest.raises(FormatError, match='Unsupported H5MSM version'):
        msm.convert(filename, to_form='molsysmt.Topology')


def test_v04_preserves_materialized_all_null_column(tmp_path):
    topology = Topology(n_atoms=2)
    topology._reference_chemical_state.atom_attributes['formal_charge'] = pd.Series(
        pd.array([pd.NA, pd.NA], dtype='Int16')
    )
    filename = tmp_path / 'nullable.h5msm'

    msm.convert(topology, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert 'formal_charge' in observed._reference_chemical_state.atom_attributes
    assert observed._reference_chemical_state.atom_attributes['formal_charge'].isna().all()


def test_v04_roundtrip_preserves_zero_state_as_unavailable(tmp_path):
    topology = Topology(n_atoms=2)
    topology._clear_chemical_states()
    filename = tmp_path / 'zero-state.h5msm'

    msm.convert(topology, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.Topology')

    assert msm.get(filename, element='system', n_chemical_states=True) == 0
    assert observed._chemical_states == []
    assert observed._reference_chemical_state_index is None
    with pytest.raises(StructuralInconsistencyError, match='no chemical state'):
        msm.get(observed, element='atom', formal_charge=True)


def test_v04_molsys_persists_implicit_single_state_association(tmp_path):
    molsys = MolSys()
    molsys.topology = _rich_topology()
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 4, 3)), 'nm')
    )
    filename = tmp_path / 'molsys.h5msm'

    msm.convert(molsys, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.MolSys')

    with h5py.File(filename, 'r') as file:
        assert file['structures/chemical_state_index'][:].tolist() == [0, 0]
    assert msm.get(observed, structure_chemical_state_index=True) == [0, 0]
    assert not hasattr(observed.structures, '_chemical_state_indices')


def test_v04_molsys_roundtrip_preserves_nullable_structure_state_mapping(tmp_path):
    molsys = MolSys()
    molsys.topology = _rich_topology()
    molsys.topology._append_chemical_state(state_id='product')
    molsys.topology._set_reference_chemical_state_index(None)
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((3, 4, 3)), 'nm')
    )
    molsys._set_structure_chemical_state_indices([0, 1, pd.NA])
    filename = tmp_path / 'mapped-multistate.h5msm'

    msm.convert(molsys, to_form='file:h5msm', output_filename=filename)
    observed = msm.convert(filename, to_form='molsysmt.MolSys')
    observed_subset = msm.convert(
        filename,
        to_form='molsysmt.MolSys',
        structure_indices=[1, 2],
    )

    with h5py.File(filename, 'r') as file:
        assert file['structures/chemical_state_index'][:].tolist() == [0, 1, -1]
    assert msm.get(filename, structure_chemical_state_index=True) == [0, 1, None]
    assert msm.get(observed, structure_chemical_state_index=True) == [0, 1, pd.NA]
    assert msm.get(observed_subset, structure_chemical_state_index=True) == [1, pd.NA]
    assert not hasattr(observed.structures, '_chemical_state_indices')
