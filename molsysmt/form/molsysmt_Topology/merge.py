from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
import pandas as pd

@digest(form='molsysmt.Topology')
def merge(items, atom_indices='all'):

    from molsysmt.native import Topology
    from . import get_n_atoms_from_system, get_n_groups_from_system, \
            get_n_components_from_system, get_n_chains_from_system, \
            get_n_molecules_from_system, get_n_entities_from_system
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
    n_entities = []
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
        n_entities.append(get_n_entities_from_system(tmp_item))
        atoms_dataframes.append(tmp_item.atoms_dataframe)
        bonds_dataframes.append(tmp_item.bonds_dataframe)

    output.atoms_dataframe = pd.concat(atoms_dataframes, ignore_index=True, copy=False)
    output.bonds_dataframe = pd.concat(bonds_dataframes, ignore_index=True, copy=False)

    count_n_atoms=n_atoms[0]
    count_n_groups=n_groups[0]
    count_n_components=n_components[0]
    count_n_chains=n_chains[0]
    count_n_molecules=n_molecules[0]
    count_n_entities=n_entities[0]

    for aux_n_atoms, aux_n_groups, aux_n_components, aux_n_chains, aux_n_molecules, aux_n_entities in zip(n_atoms[1:], n_groups[1:],
            n_components[1:], n_chains[1:], n_molecules[1:], n_entities[1:]):

        next_count_n_atoms = count_n_atoms + aux_n_atoms
        next_count_n_groups = count_n_groups + aux_n_groups
        next_count_n_components = count_n_components + aux_n_components
        next_count_n_chains = count_n_chains + aux_n_chains
        next_count_n_molecules = count_n_molecules + aux_n_molecules
        next_count_n_entities = count_n_entities + aux_n_entities

        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'atom_index'] += count_n_atoms
        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'group_index'] += count_n_groups
        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'component_index'] += count_n_components
        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'chain_index'] += count_n_chains
        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'molecule_index'] += count_n_molecules
        output.atoms_dataframe.loc[count_n_atoms:next_count_n_atoms, 'entity_index'] += count_n_entities
        output.bonds_dataframe.loc[count_n_atoms:next_count_n_atoms, 'atom1_index'] += count_n_atoms
        output.bonds_dataframe.loc[count_n_atoms:next_count_n_atoms, 'atom2_index'] += count_n_atoms

        count_n_atoms = next_count_n_atoms
        count_n_groups = next_count_n_groups
        count_n_components = next_count_n_components
        count_n_chains = next_count_n_chains
        count_n_molecules = next_count_n_molecules
        count_n_entities = next_count_n_entities

    output._build_entities()

    return output

