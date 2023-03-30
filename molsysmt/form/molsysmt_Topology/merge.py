from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd

@digest(form='molsysmt.Topology')
def merge(items, atom_indices='all'):

    from molsysmt.native import Topology
    from . import get_n_atoms_from_system, get_n_groups_from_system, \
            get_n_components_from_system, get_n_chains_from_system, \
            get_n_molecules_from_system, get_n_entities_from_system
    from . import extract

    n_items = len(items)

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ValueError(atom_indices)

    output = Topology()

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

    #rebuild molecules and entities

    group_name = merged.atoms_dataframe['group_name'].to_numpy()
    component_type = merged.atoms_dataframe['component_type'].to_numpy()

    molecule_index = merged.atoms_dataframe['molecule_index'].to_numpy()
    molecule_name = merged.atoms_dataframe['molecule_name'].to_numpy()
    molecule_type = merged.atoms_dataframe['molecule_type'].to_numpy()
    entity_index = merged.atoms_dataframe['entity_index'].to_numpy()
    entity_type = merged.atoms_dataframe['entity_type'].to_numpy()
    entity_name = merged.atoms_dataframe['entity_name'].to_numpy()
    entity_id = merged.atoms_dataframe['entity_id'].to_numpy()

    entities= {}
    n_entities = 0
    n_peptides = 0
    n_proteins = 0

    current_molecule_index = -1
    atom_indices_in_molecule = []
    group_names_in_molecule = []


    for ii in range(count_n_atoms):

        if current_molecule_index!=molecule_index[ii]:

            current_molecule_index=molecule_index[ii]
            current_molecule_name=molecule_name[ii]
            current_molecule_type=molecule_type[ii]

            if current_molecule_type=='water':

                try:

                    current_entity_index = entities[current_molecule_name]['entity_index']
                    current_entity_id = entities[current_molecule_name]['entity_id']
                    current_entity_name = entities[current_molecule_name]['entity_name']
                    current_entity_type = entities[current_molecule_name]['entity_type']

                except:

                    current_entity_index = n_entities
                    current_entity_id = n_entities
                    current_entity_name = current_molecule_name
                    current_entity_type = current_molecule_type

                    entities[current_entity_name]={}
                    entities[current_entity_name]['entity_index'] = current_entity_index
                    entities[current_entity_name]['entity_id'] = current_entity_id
                    entities[current_entity_name]['entity_name'] = current_entity_name
                    entities[current_entity_name]['entity_type'] = current_entity_type

                    n_entities +=1

    else:




    return output

