from os.path import basename as _basename
from simtk.openmm.app import GromacsGroFile as _openmm_GromacsGroFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_GromacsGroFile : form_name,
    'openmm.GromacsGroFile' : form_name
}

info=["",""]
with_topology=True
with_trajectory=True

def to_molsysmt_DataFrame(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_molsysmt_DataFrame as openmm_Topology_to_molsysmt_DataFrame
    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_DataFrame(item, atom_indices=atom_indices)
    return tmp_item

def to_openmm_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    return item.topology

def to_mdtraj_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_nglview(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select

    tmp_item = to_molsysmt_DataFrame(item)
    atom_indices = dataframe_select(tmp_item, selection)
    return atom_indices

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

