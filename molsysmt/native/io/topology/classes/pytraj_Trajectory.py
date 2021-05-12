from molsysmt._private_tools.exceptions import *

def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def from_pytraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .pytraj_Topology import from_pytraj_Topology as molsysmt_Topology_from_pytraj_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = molsysmt_Topology_from_pytraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

