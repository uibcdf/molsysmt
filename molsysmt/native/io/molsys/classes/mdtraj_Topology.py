def from_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = molsysmt_Topology_to_mdtraj_Topology(item.topology, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item




