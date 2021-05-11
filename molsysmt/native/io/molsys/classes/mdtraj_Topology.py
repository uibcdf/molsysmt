from molsysmt._private_tools.exceptions import *

def from_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = molsysmt_Topology_to_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system




