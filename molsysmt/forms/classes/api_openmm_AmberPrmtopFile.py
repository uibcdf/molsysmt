from os.path import basename as _basename
from simtk.openmm.app import AmberPrmtopFile as _openmm_AmberPrmtopFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_AmberPrmtopFile : form_name,
    'openmm.AmberPrmtopFile' : form_name
}

info=["",""]
with_topology=True
with_trajectory=False

def to_molsysmt_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)
    return tmp_item

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    return item.topology

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import _select

    tmp_item = to_molsysmt_Topology(item)
    atom_indices = _select(tmp_item, selection)
    return atom_indices

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

