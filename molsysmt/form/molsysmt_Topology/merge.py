from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.Topology')
def merge(items, atom_indices='all', keep_ids=True, skip_digestion=False):

    from molsysmt.native import Topology
    from . import extract

    n_items = len(items)

    output = Topology()


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
    groups_dataframes = []
    components_dataframes = []
    molecules_dataframes = []
    chains_dataframes = []
    bonds_dataframes = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):

        if is_all(aux_atom_indices):
            tmp_item = aux_item
        else:
            tmp_item = extract(aux_item, atom_indices=aux_atom_indices)

        n_atoms.append(tmp_item.atoms.shape[0])
        n_groups.append(tmp_item.groups.shape[0])
        n_components.append(tmp_item.components.shape[0])
        n_chains.append(tmp_item.chains.shape[0])
        n_molecules.append(tmp_item.molecules.shape[0])
        n_bonds.append(tmp_item.bonds.shape[0])
        atoms_dataframes.append(tmp_item.atoms)
        groups_dataframes.append(tmp_item.groups)
        components_dataframes.append(tmp_item.components)
        molecules_dataframes.append(tmp_item.molecules)
        chains_dataframes.append(tmp_item.chains)
        bonds_dataframes.append(tmp_item.bonds)

    output.atoms = pd.concat(atoms_dataframes, ignore_index=True, copy=False)
    output.groups = pd.concat(groups_dataframes, ignore_index=True, copy=False)
    output.components = pd.concat(components_dataframes, ignore_index=True, copy=False)
    output.molecules = pd.concat(molecules_dataframes, ignore_index=True, copy=False)
    output.chains = pd.concat(chains_dataframes, ignore_index=True, copy=False)
    output.bonds = pd.concat(bonds_dataframes, ignore_index=True, copy=False)

    count_n_atoms=n_atoms[0]
    count_n_groups=n_groups[0]
    count_n_components=n_components[0]
    count_n_chains=n_chains[0]
    count_n_molecules=n_molecules[0]
    count_n_bonds=n_bonds[0]

    for aux_n_atoms, aux_n_groups, aux_n_components, aux_n_chains, aux_n_molecules, aux_n_bonds, in zip(n_atoms[1:], n_groups[1:],
            n_components[1:], n_chains[1:], n_molecules[1:], n_bonds[1:]):

        next_count_n_atoms = count_n_atoms + aux_n_atoms
        next_count_n_groups = count_n_groups + aux_n_groups
        next_count_n_components = count_n_components + aux_n_components
        next_count_n_chains = count_n_chains + aux_n_chains
        next_count_n_molecules = count_n_molecules + aux_n_molecules
        next_count_n_bonds = count_n_bonds + aux_n_bonds

        output.atoms.iloc[count_n_atoms:next_count_n_atoms,3] += count_n_groups
        output.atoms.iloc[count_n_atoms:next_count_n_atoms,4] += count_n_chains
        output.groups.iloc[count_n_groups:next_count_n_groups,3] += count_n_components
        output.components.iloc[count_n_components:next_count_n_components,3] += count_n_molecules
        output.bonds.iloc[count_n_bonds:next_count_n_bonds,0] += count_n_atoms
        output.bonds.iloc[count_n_bonds:next_count_n_bonds,1] += count_n_atoms

        count_n_atoms = next_count_n_atoms
        count_n_groups = next_count_n_groups
        count_n_components = next_count_n_components
        count_n_chains = next_count_n_chains
        count_n_molecules = next_count_n_molecules
        count_n_bonds = next_count_n_bonds

    if not keep_ids:
        output.rebuild_atoms(redefine_ids=True, redefine_types=False)
        output.rebuild_groups(redefine_ids=True, redefine_types=False)
        output.rebuild_components(redefine_indices=False, redefine_ids=True, redefine_types=False,
                                  redefine_names=False)
        output.rebuild_molecules(redefine_indices=False, redefine_ids=True, redefine_types=False,
                                  redefine_names=False)
        output.rebuild_chains(redefine_ids=True, redefine_types=True)
    else:
        output.rebuild_chains(redefine_ids=False, redefine_types=True)

    output.rebuild_entities()

    return output

