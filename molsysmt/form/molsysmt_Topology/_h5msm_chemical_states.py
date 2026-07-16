"""Serializing native chemical states in the H5MSM 0.4 layout."""

import h5py
import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native.topology import (
    Bonds_DataFrame,
    Components_DataFrame,
    _ChemicalStateStorage,
)


_ATOM_DTYPES = {
    'formal_charge': 'Int16',
    'is_aromatic': 'boolean',
    'n_unpaired_electrons': 'UInt8',
    'n_implicit_hydrogens': 'UInt8',
    'allows_implicit_hydrogens': 'boolean',
    'stereochemistry': 'string',
}

_BOND_DTYPES = {
    'bond_id': 'string',
    'atom1_index': 'Int64',
    'atom2_index': 'Int64',
    'bond_order': 'UInt8',
    'fractional_bond_order': 'Float64',
    'bond_type': 'string',
    'is_aromatic': 'boolean',
    'is_conjugated': 'boolean',
    'stereochemistry': 'string',
    'stereo_atom1_index': 'Int64',
    'stereo_atom2_index': 'Int64',
    'donor_atom_index': 'Int64',
    'acceptor_atom_index': 'Int64',
    'joins_components': 'boolean',
    'evidence': 'string',
    'provenance_index': 'Int64',
}

_COMPONENT_DTYPES = {
    'component_id': 'string',
    'component_name': 'string',
    'component_type': 'string',
}


def _dataset_values(series, dtype):
    null_mask = series.isna().to_numpy(dtype=bool)
    if dtype == 'string':
        values = series.fillna('').astype(str).to_numpy(dtype=object)
        h5_dtype = h5py.string_dtype()
    elif dtype == 'boolean':
        values = series.fillna(False).to_numpy(dtype=np.uint8)
        h5_dtype = np.uint8
    elif dtype.startswith('Float'):
        values = series.fillna(0.0).to_numpy(dtype=np.float64)
        h5_dtype = np.float64
    else:
        values = series.fillna(0).to_numpy(dtype=np.int64)
        h5_dtype = np.int64
    return values, null_mask, h5_dtype


def _write_nullable_table(group, table, dtypes, dataset_options):
    for name in table.columns:
        if name not in dtypes:
            raise StructuralInconsistencyError(
                reason=f'H5MSM 0.4 has no declared dtype for column {name!r}.',
                caller='molsysmt.form.molsysmt_Topology.to_file_h5msm',
            )
        values, null_mask, h5_dtype = _dataset_values(table[name], dtypes[name])
        group.create_dataset(name, data=values, dtype=h5_dtype, **dataset_options)
        if null_mask.any():
            group.create_dataset(
                f'{name}__is_null', data=null_mask, dtype=np.bool_, **dataset_options
            )


def _read_nullable_table(group, dtypes, index):
    output = pd.DataFrame(index=index)
    for name, dtype in dtypes.items():
        if name not in group:
            continue
        dataset = group[name]
        values = dataset.asstr()[:] if dtype == 'string' else dataset[:]
        series = pd.Series(pd.array(values, dtype=dtype), index=index)
        mask_name = f'{name}__is_null'
        if mask_name in group:
            series.loc[group[mask_name][:].astype(bool)] = pd.NA
        output[name] = series
    unknown = {
        name for name in group
        if not name.endswith('__is_null') and name not in dtypes
    }
    if unknown:
        raise StructuralInconsistencyError(
            reason=f'H5MSM 0.4 contains unknown columns {sorted(unknown)}.',
            caller='molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology',
        )
    return output


def write_chemical_states(topology, topology_group, dataset_options):
    """Writing every native chemical state and compatibility hard links."""

    if 'chemical_states' in topology_group:
        del topology_group['chemical_states']
    states_group = topology_group.create_group('chemical_states')
    states_group.attrs['n_chemical_states'] = len(topology._chemical_states)
    reference_index = topology._reference_chemical_state_index
    states_group.attrs['reference_chemical_state_index'] = (
        -1 if reference_index is None else int(reference_index)
    )

    for state_index, state in enumerate(topology._chemical_states):
        state._ensure_compatibility(topology.n_atoms)
        group = states_group.create_group(str(state_index))
        if state.state_id is not None:
            group.attrs['state_id'] = state.state_id
        group.attrs['connectivity_completeness'] = state.connectivity_completeness
        group.attrs['component_completeness'] = state.component_completeness
        group.attrs['component_evidence'] = state.component_evidence
        group.attrs['provenance_index'] = (
            -1 if state.provenance_index is None else int(state.provenance_index)
        )

        component_indices = state.component_indices
        values = component_indices.fillna(-1).to_numpy(dtype=np.int64)
        group.create_dataset('component_indices', data=values, **dataset_options)

        components = group.create_group('components')
        _write_nullable_table(components, state.components, _COMPONENT_DTYPES, dataset_options)

        atom_attributes = group.create_group('atom_attributes')
        _write_nullable_table(atom_attributes, state.atom_attributes, _ATOM_DTYPES, dataset_options)

        bonds = group.create_group('bonds')
        _write_nullable_table(bonds, state.bonds, _BOND_DTYPES, dataset_options)

    for legacy_name in ('components', 'bonds'):
        if legacy_name in topology_group:
            del topology_group[legacy_name]
    atoms_group = topology_group['atoms']
    if 'component_index' in atoms_group:
        del atoms_group['component_index']

    if reference_index is not None:
        reference_group = states_group[str(reference_index)]
        topology_group['components'] = reference_group['components']
        compatibility_bonds = topology_group.create_group('bonds')
        for name, dataset in reference_group['bonds'].items():
            compatibility_bonds[name] = dataset
        if 'bond_order' in reference_group['bonds']:
            compatibility_bonds['order'] = reference_group['bonds']['bond_order']
        else:
            compatibility_bonds.create_dataset('order', (0,), dtype=h5py.string_dtype())
        if 'bond_type' in reference_group['bonds']:
            compatibility_bonds['type'] = reference_group['bonds']['bond_type']
        else:
            compatibility_bonds.create_dataset('type', (0,), dtype=h5py.string_dtype())
        atoms_group['component_index'] = reference_group['component_indices']
        topology_group.attrs['n_components'] = len(reference_group['components']['component_id'])
        topology_group.attrs['n_bonds'] = len(reference_group['bonds']['atom1_index'])
    else:
        topology_group.attrs['n_components'] = -1
        topology_group.attrs['n_bonds'] = -1


def read_chemical_states(topology_group, n_atoms):
    """Reading all chemical states from an H5MSM 0.4 topology group."""

    if 'chemical_states' not in topology_group:
        raise StructuralInconsistencyError(
            reason='H5MSM 0.4 topology is missing its chemical_states group.',
            caller='molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology',
        )
    states_group = topology_group['chemical_states']
    n_states = int(states_group.attrs.get('n_chemical_states', len(states_group)))
    expected_names = [str(index) for index in range(n_states)]
    if sorted(states_group.keys(), key=int) != expected_names:
        raise StructuralInconsistencyError(
            reason='H5MSM 0.4 chemical-state indices are not contiguous and ordered.',
            caller='molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology',
        )

    output = []
    for state_index in range(n_states):
        group = states_group[str(state_index)]
        component_values = group['component_indices'][:].astype(np.int64)
        component_indices = pd.Series(
            pd.array(
                [pd.NA if value < 0 else value for value in component_values],
                dtype='Int64',
            ),
            index=range(n_atoms),
        )

        component_table = _read_nullable_table(
            group['components'], _COMPONENT_DTYPES, range(len(group['components']['component_id']))
        )
        components = Components_DataFrame(n_components=0)
        for name in _COMPONENT_DTYPES:
            components[name] = component_table[name]

        atom_attributes = _read_nullable_table(
            group['atom_attributes'], _ATOM_DTYPES, range(n_atoms)
        )
        bond_count = len(group['bonds']['atom1_index'])
        bond_table = _read_nullable_table(group['bonds'], _BOND_DTYPES, range(bond_count))
        bonds = Bonds_DataFrame(n_bonds=0)
        for name in bond_table.columns:
            bonds[name] = bond_table[name]

        provenance_index = int(group.attrs.get('provenance_index', -1))
        state = _ChemicalStateStorage(
            n_atoms=n_atoms,
            bonds=bonds,
            components=components,
            component_indices=component_indices,
            state_id=group.attrs.get('state_id'),
            connectivity_completeness=group.attrs['connectivity_completeness'],
            component_completeness=group.attrs['component_completeness'],
            component_evidence=group.attrs['component_evidence'],
            provenance_index=None if provenance_index < 0 else provenance_index,
        )
        state.atom_attributes = atom_attributes
        state._ensure_compatibility(n_atoms)
        output.append(state)

    reference_index = int(states_group.attrs.get('reference_chemical_state_index', -1))
    if reference_index >= n_states:
        raise StructuralInconsistencyError(
            reason='H5MSM 0.4 reference chemical-state index is out of range.',
            caller='molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology',
        )
    return output, None if reference_index < 0 else reference_index
