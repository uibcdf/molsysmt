from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.composition import Composition as _molmodmt_Composition

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Composition : form_name,
    'molmodmt.Composition': form_name
}

def to_networkx_Graph(item, atom_indices='all', frame_indices='all'):

    from .api_networkx_Graph import extract_subsystem as extract_networkx_Graph
    from networkx import empty_graph

    G = empty_graph(item.n_atoms)

    for bond in item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    tmp_item = extract_networkx_Graph(G, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molmodmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    return item.copy()

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolModMT(item, selection):

    from molmodmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item.dataframe, selection)
    return atom_indices

###### Get

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.index'].to_list()
    else:
        output_list = item.dataframe['atom.index'][indices].to_list()

    return output_list

def get_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.id'].to_list()
    else:
        output_list = item.dataframe['atom.id'][indices].to_list()

    return output_list

def get_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.name'].to_list()
    else:
        output_list = item.dataframe['atom.name'][indices].to_list()

    return output_list

def get_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['atom.type'].to_list()
    else:
        output_list = item.dataframe['atom.type'][indices].to_list()

    return output_list

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.index'].to_list()
    else:
        output_list = item.dataframe['group.index'][indices].to_list()

    return output_list

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.id'].to_list()
    else:
        output_list = item.dataframe['group.id'][indices].to_list()

    return output_list

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.name'].to_list()
    else:
        output_list = item.dataframe['group.name'][indices].to_list()

    return output_list

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['group.type'].to_list()
    else:
        output_list = item.dataframe['group.type'][indices].to_list()

    return output_list

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.index'].to_list()
    else:
        output_list = item.dataframe['component.index'][indices].to_list()

    return output_list

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.id'].to_list()
    else:
        output_list = item.dataframe['component.id'][indices].to_list()

    return output_list

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.name'].to_list()
    else:
        output_list = item.dataframe['component.name'][indices].to_list()

    return output_list

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['component.type'].to_list()
    else:
        output_list = item.dataframe['component.type'][indices].to_list()

    return output_list

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.index'].to_list()
    else:
        output_list = item.dataframe['chain.index'][indices].to_list()

    return output_list

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.id'].to_list()
    else:
        output_list = item.dataframe['chain.id'][indices].to_list()

    return output_list

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.name'].to_list()
    else:
        output_list = item.dataframe['chain.name'][indices].to_list()

    return output_list

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.type'].to_list()
    else:
        output_list = item.dataframe['chain.type'][indices].to_list()

    return output_list

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.index'].to_list()
    else:
        output_list = item.dataframe['molecule.index'][indices].to_list()

    return output_list

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.id'].to_list()
    else:
        output_list = item.dataframe['molecule.id'][indices].to_list()

    return output_list

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.name'].to_list()
    else:
        output_list = item.dataframe['molecule.name'][indices].to_list()

    return output_list

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.type'].to_list()
    else:
        output_list = item.dataframe['molecule.type'][indices].to_list()

    return output_list

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.index'].to_list()
    else:
        output_list = item.dataframe['molecule.index'][indices].to_list()

    return output_list

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.id'].to_list()
    else:
        output_list = item.dataframe['molecule.id'][indices].to_list()

    return output_list

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.name'].to_list()
    else:
        output_list = item.dataframe['molecule.name'][indices].to_list()

    return output_list

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.type'].to_list()
    else:
        output_list = item.dataframe['molecule.type'][indices].to_list()

    return output_list










def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.name'].to_list()
    else:
        output_list = item.dataframe['chain.name'][indices].to_list()

    return output_list

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.index'].to_list()
    else:
        output_list = item.dataframe['chain.index'][indices].to_list()

    return output_list

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['chain.id'].to_list()
    else:
        output_list = item.dataframe['chain.id'][indices].to_list()

    return output_list

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from numpy import unique

    df=item.dataframe

    if indices is 'all':
        output_list = df.loc[df['molecule.type'] == 'water']['group.index'].to_list()
    else:
        output_list = df.loc[df['molecule.type'][indices] == 'water']['group.index'].to_list()

    output_list = unique(output_list)

    return output_list.shape[0]

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from numpy import unique

    df=item.dataframe

    if indices is 'all':
        output_list = df.loc[df['molecule.type'] == 'ion']['group.index'].to_list()
    else:
        output_list = df.loc[df['molecule.type'][indices] == 'ion']['group.index'].to_list()

    output_list = unique(output_list)

    return output_list.shape[0]

def get_bonded_atoms_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_bonded_atoms_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #tmp_indices = [trajectory_indices[ii] for ii in indices]
    #bonded_atoms_composition = _get(item.composition, indices=tmp_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #bonded_atoms = {}
    #for ii_composition, ii_bonded_composition in bonded_atoms_composition.items():
    #    bonded_atoms[traduction[ii_composition]]=[traduction[jj] for jj in ii_bonded_composition]

    #return bonded_atoms

def get_molecules_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecule_type_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        output_list = item.dataframe['molecule.type'].to_list()
    else:
        output_list = item.dataframe['molecule.type'][indices].to_list()

    return output_list

## group

## chain

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.n_groups

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return item.n_components

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.n_chains

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return item.n_molecules

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return item.n_entities

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    return item.n_ions

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    return item.n_waters

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    return item.n_cosolutes

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    return item.n_small_molecules

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    return item.n_peptides

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    return item.n_proteins

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    return item.n_dnas

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    return item.n_rnas

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return item.n_molecules

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.n_bonds

def get_form_from_system(item, indices='all', frame_indices='all'):

    return item.form_name

def get_masses_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_bonded_atoms_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #bonded_atoms_composition = _get(item.composition, indices=trajectory_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #bonded_atoms = {}
    #for ii_composition, ii_bonded_composition in bonded_atoms_composition.items():
    #    bonded_atoms[traduction[ii_composition]]=[traduction[jj] for jj in ii_bonded_composition]

    #return bonded_atoms

def get_bonds_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_graph_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_molecules_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molmodmt_Composition import get_molecules_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #molecules_composition = _get(item.composition, indices=trajectory_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #molecules = []
    #for tmp_molecule in molecules_composition:
    #    molecules.append([traduction[ii] for ii in tmp_molecule])

    #return molecules

