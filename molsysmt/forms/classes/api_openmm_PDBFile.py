from os.path import basename as _basename
from simtk.openmm.app import PDBFile as _openmm_PDBFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_PDBFile : form_name,
    'openmm.PDBFile' : form_name
}

info=["",""]

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory
    tmp_topology = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import extract as extract_openmm_Topology
    tmp_item=item.getTopology()
    tmp_item=extract_openmm_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Trajectory import to_nglview as mdtraj_Trajectory_to_nglview
    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return _mdtraj_Trajectory_to_nglview(tmp_item)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_unit = item.positions.unit
    tmp_positions = [item.positions[ii]._value for ii in indices]
    result.append(tmp_positions*tmp_unit)

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

