from os.path import basename as _basename
from simtk.openmm import System as _openmm_System

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_System : form_name,
    'openmm.System' : form_name,
}

##### Get

## Atom

def get_n_atoms_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_atoms_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_name_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_name_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_atom_type_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_atom_type_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_residues_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residues_from_atom as _get
    _get(item.topology, indices=indices)

def get_residue_name_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residue_from_atom as _get
    _get(item.topology, indices=indices)

def get_residue_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_residue_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_index_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_atom as _get
    _get(item.topology, indices=indices)

def get_chain_id_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_aminoacids_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_aminoacids_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_nucleotides_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_nucleotides_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_waters_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_waters_from_atom as _get
    _get(item.topology, indices=indices)

def get_n_ions_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_ions_from_atom as _get
    _get(item.topology, indices=indices)

def get_mass_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_mass as _get
    return _get(item, indices=indices)

def get_net_mass_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_net_mass as _get
    return _get(item, indices=indices)

def get_charge_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_charge as _get
    return _get(item, indices=indices)
def get_net_charge_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_atom (item, indices=None, frame_indices=None):

    from molmodmt import get_degrees_of_freedom_charge as _get
    return _get(item, indices=indices)

def get_molecule_type_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_atom as _get
    return _get(item, indices=indices)

def get_coordinates_from_atom (item, indices=None, frame_indices=None):

    from .api_openmm_Positions import get_coordinates_from_atom as _get
    return _get(item, indices=indices)

## residue

def get_n_residues_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_residues_from_residue as _get
    return _get(item, indices=indices)

def get_residue_name_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_name_from_residue as _get
    return _get(item, indices=indices)

def get_residue_index_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_index_from_residue as _get
    return _get(item, indices=indices)

def get_residue_id_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_residue_id_from_residue as _get
    return _get(item, indices=indices)

def get_chain_index_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_residue as _get
    return _get(item, indices=indices)

def get_chain_id_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_residue as _get
    return _get(item, indices=indices)

def get_molecule_type_from_residue (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_residue as _get
    return _get(item, indices=indices)

## chain

def get_chain_index_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_index_from_chain as _get
    return _get(item, indices=indices)

def get_chain_id_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_chain_id_from_chain as _get
    return _get(item, indices=indices)

def get_molecule_type_from_chain (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_molecule_type_from_chain as _get
    return _get(item, indices=indices)

## system

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from .api_openmm_Topology import get_n_atoms_from_system as _get
    return _get(item, indices=indices)

def get_charge_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_charge as _get
    return _get(item, indices=indices)

def get_net_charge_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_net_charge as _get
    return _get(item, indices=indices)

def get_n_degrees_of_freedom_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get_degrees_of_freedom as _get
    return _get(item, indices=indices)

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

