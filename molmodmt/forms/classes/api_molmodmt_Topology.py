from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.topology import Topology as _molmodmt_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Topology : form_name,
    'molmodmt.Topology': form_name
}


def to_mdtraj_Topology (item, atom_indices=None, frame_indices=None):

    from molmodmt import extract

    tmp_item = item
    tmp_item = extract(item, selection=atom_indices)
    return tmp_item

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    from .api_mdtraj_Topology import duplicate as duplicate_mdtraj_Topology
    return duplicate_mdtraj_Topology(item)

###### Get

## atom

def get_index_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_index_from_atom as _get
    return _get(item, indices=indices)

def get_id_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_id_from_atom as _get
    return _get(item, indices=indices)

def get_name_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_name_from_atom as _get
    return _get(item, indices=indices)

def get_element_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_element_from_atom as _get
    return _get(item, indices=indices)

def get_residue_index_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_residue_index_from_atom as _get
    return _get(item, indices=indices)

def get_residue_name_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_residue_name_from_atom as _get
    return _get(item, indices=indices)

def get_residue_id_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_residue_id_from_atom as _get
    return _get(item, indices=indices)

def get_chain_index_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_chain_index_from_atom as _get
    return _get(item, indices=indices)

def get_chain_name_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_chain_name_from_atom as _get
    return _get(item, indices=indices)

def get_chain_id_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_chain_id_from_atom as _get
    return _get(item, indices=indices)

def get_n_aminoacids_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_aminoacids_from_atom as _get
    return _get(item, indices=indices)

def get_n_nucleotides_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_nucleotides_from_atom as _get
    return _get(item, indices=indices)

def get_n_waters_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_waters_from_atom as _get
    return _get(item, indices=indices)

def get_n_ions_from_atom (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_ions_from_atom as _get
    return _get(item, indices=indices)

def get_bonded_atoms_from_atom(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_bonded_atoms_from_atom as _get
    return _get(item, indices=indices)

def get_molecules_from_atom(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_molecules_from_atom as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)


## residue

## chain

## system

def get_n_atoms_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_n_residues_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_residues_from_system as _get
    return _get(item, indices=indices)

def get_n_chains_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_chains_from_system as _get
    return _get(item, indices=indices)

def get_n_aminoacids_from_system (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_aminoacids_from_system as _get
    return _get(item, indices=indices)

def get_n_nucleotides_from_system (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_nucleotides_from_system as _get
    return _get(item, indices=indices)

def get_n_waters_from_system (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_waters_from_system as _get
    return _get(item, indices=indices)

def get_n_ions_from_system (item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_ions_from_system as _get
    return _get(item, indices=indices)

def get_n_molecules_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_molecules_from_system as _get
    return _get(item, indices=indices)

def get_n_bonds_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_n_bonds_from_system as _get
    return _get(item, indices=indices)

def get_n_frames_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Trayectory import get_n_frames_from_system as _get
    return _get(item, indices=indices)

def get_masses_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_masses_from_system as _get
    return _get(item, indices=indices)

def get_bonded_atoms_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_bonded_atoms_from_system as _get
    return _get(item, indices=indices)

def get_bonds_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_bonds_from_system as _get
    return _get(item, indices=indices)

def get_graph_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_graph_from_system as _get
    return _get(item, indices=indices)

def get_molecules_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_molecules_from_system as _get
    return _get(item, indices=indices)

def get_box_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Trajectory import get_box_from_system as _get
    return _get(item, indices=indices)

def get_cell_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Trajectory import get_cell_from_system as _get
    return _get(item, indices=indices)

def get_n_frames_from_system(item, indices=None, frame_indices=None):

    return 0

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

