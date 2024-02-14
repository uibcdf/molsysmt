from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.TopologyOld')
def merge(items, atom_indices='all', skip_digestion=False):

    from molsysmt.native import TopologyOld
    from . import get_n_atoms_from_system, get_n_groups_from_system, \
            get_n_components_from_system, get_n_chains_from_system, \
            get_n_molecules_from_system, get_n_entities_from_system, \
            get_n_bonds_from_system
    from . import extract

    n_items = len(items)

    output = TopologyOld()


    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    n_atoms = []
    n_groups = []
    n_components = []
    n_chains = []
    n_molecules = []
    n_bonds = []
    atoms_dataframes = []
    bonds_dataframes = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):

        if is_all(aux_atom_indices):
            tmp_item = aux_item
        else:
            tmp_item = extract(aux_item, atom_indices=aux_atom_indices)

        n_atoms.append(get_n_atoms_from_system(tmp_item))
        n_groups.append(get_n_groups_from_system(tmp_item))
        n_components.append(get_n_components_from_system(tmp_item))
        n_chains.append(get_n_chains_from_system(tmp_item))
        n_molecules.append(get_n_molecules_from_system(tmp_item))
        n_bonds.append(get_n_bonds_from_system(tmp_item))
        atoms_dataframes.append(tmp_item.atoms_dataframe)
        bonds_dataframes.append(tmp_item.bonds_dataframe)

    output.atoms_dataframe = pd.concat(atoms_dataframes, ignore_index=True, copy=False)
    output.bonds_dataframe = pd.concat(bonds_dataframes, ignore_index=True, copy=False)

    count_n_atoms=n_atoms[0]
    count_n_groups=n_groups[0]
    count_n_components=n_components[0]
    count_n_chains=n_chains[0]
    count_n_molecules=n_molecules[0]
    count_n_bonds=n_bonds[0]

    atom_index = output.atoms_dataframe['atom_index'].to_numpy(copy=False)
    group_index = output.atoms_dataframe['group_index'].to_numpy(copy=False)
    component_index = output.atoms_dataframe['component_index'].to_numpy(copy=False)
    chain_index = output.atoms_dataframe['chain_index'].to_numpy(copy=False)
    molecule_index = output.atoms_dataframe['molecule_index'].to_numpy(copy=False)
    atom1_index = output.bonds_dataframe['atom1_index'].to_numpy(copy=False)
    atom2_index = output.bonds_dataframe['atom2_index'].to_numpy(copy=False)

    for aux_n_atoms, aux_n_groups, aux_n_components, aux_n_chains, aux_n_molecules, aux_n_bonds, in zip(n_atoms[1:], n_groups[1:],
            n_components[1:], n_chains[1:], n_molecules[1:], n_bonds[1:]):

        next_count_n_atoms = count_n_atoms + aux_n_atoms
        next_count_n_groups = count_n_groups + aux_n_groups
        next_count_n_components = count_n_components + aux_n_components
        next_count_n_chains = count_n_chains + aux_n_chains
        next_count_n_molecules = count_n_molecules + aux_n_molecules
        next_count_n_bonds = count_n_bonds + aux_n_bonds

        if count_n_atoms:
            atom_index[count_n_atoms:next_count_n_atoms] += count_n_atoms
        if count_n_groups:
            group_index[count_n_atoms:next_count_n_atoms] += count_n_groups
        if count_n_components:
            component_index[count_n_atoms:next_count_n_atoms] += count_n_components
        if count_n_chains:
            chain_index[count_n_atoms:next_count_n_atoms] += count_n_chains
        if count_n_molecules:
            molecule_index[count_n_atoms:next_count_n_atoms] += count_n_molecules
        if count_n_bonds:
            atom1_index[count_n_bonds:next_count_n_bonds] += count_n_atoms
            atom2_index[count_n_bonds:next_count_n_bonds] += count_n_atoms

        count_n_atoms = next_count_n_atoms
        count_n_groups = next_count_n_groups
        count_n_components = next_count_n_components
        count_n_chains = next_count_n_chains
        count_n_molecules = next_count_n_molecules
        count_n_bonds = next_count_n_bonds

    if not np.shares_memory(atom_index, output.atoms_dataframe['atom_index']):
        output.atoms_dataframe['atom_index'] = atom_index

    if not np.shares_memory(group_index, output.atoms_dataframe['group_index']):
        output.atoms_dataframe['group_index'] = group_index

    if not np.shares_memory(component_index, output.atoms_dataframe['component_index']):
        output.atoms_dataframe['component_index'] = component_index

    if not np.shares_memory(chain_index, output.atoms_dataframe['chain_index']):
        output.atoms_dataframe['chain_index'] = chain_index

    if not np.shares_memory(molecule_index, output.atoms_dataframe['molecule_index']):
        output.atoms_dataframe['molecule_index'] = molecule_index

    if not np.shares_memory(atom1_index, output.bonds_dataframe['atom1_index']):
        output.bonds_dataframe['atom1_index'] = atom1_index

    if not np.shares_memory(atom2_index, output.bonds_dataframe['atom2_index']):
        output.bonds_dataframe['atom2_index'] = atom2_index

    output._build_entities()

    return output

