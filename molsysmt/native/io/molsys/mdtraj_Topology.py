from molsysmt._private_tools.exceptions import *

def from_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = molsysmt_Topology_to_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system




