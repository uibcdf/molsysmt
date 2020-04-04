from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.composition import Composition as molsysmt_Composition
from molsysmt.native.io import composition as io_composition

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    molsysmt_Composition : form_name,
    'molsysmt.Composition': form_name
}

info=["",""]

def to_networkx_Graph(item, atom_indices='all', frame_indices='all'):

    from .api_networkx_Graph import extract_subsystem as extract_networkx_Graph
    from networkx import empty_graph

    G = empty_graph(item.n_atoms)

    for bond in item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    tmp_item = extract_networkx_Graph(G, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

from molsysmt.native.io.composition.classes.molsysmt_DataFrame import to_molsysmt_DataFrame
from molsysmt.native.io.composition.seqs.aminoacids1 import to_aminoacids1_seq

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def duplicate(item):

    return item.duplicate()

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_molsysmt(item, selection):

    from molsysmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item.dataframe, selection)
    return atom_indices

###### Get

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_aminoacids_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_nucleotides_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_waters_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_ions_from_atom as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molsysmt_Composition import get_bonded_atoms_from_atom as _get
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

    from .api_molsysmt_DataFrame import get_n_atoms_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_aminoacids_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_nucleotides_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_ions_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_waters_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_cosolutes_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_small_molecules_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_peptides_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_proteins_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_dnas_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_DataFrame import get_n_rnas_from_system as _get
    return _get(item.dataframe, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.n_bonds

def get_form_from_system(item, indices='all', frame_indices='all'):

    return item.form_name

def get_masses_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

    #from .api_molsysmt_Composition import get_bonded_atoms_from_atom as _get
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

    #from .api_molsysmt_Composition import get_molecules_from_atom as _get
    #trajectory_indices = item.trajectory.file.atom_indices
    #molecules_composition = _get(item.composition, indices=trajectory_indices, frame_indices=frame_indices)
    #traduction = { trajectory_indices[ii] : ii for ii in range(len(trajectory_indices)) }
    #molecules = []
    #for tmp_molecule in molecules_composition:
    #    molecules.append([traduction[ii] for ii in tmp_molecule])

    #return molecules

