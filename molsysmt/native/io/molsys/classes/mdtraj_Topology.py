def from_mdtraj_Topology(item, atom_indices='all', frame_indices='all', topology_item=None,
                         trajectory_item=None, coordinates_item=None, box_item=None):

    raise NotImplementedError

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all', topology_item=None,
                       trajectory_item=None, coordinates_item=None, box_item=None):

    from molsysmt.native.io.topology.classes import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = molsysmt_Topology_to_mdtraj_Topology(item.topology, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item




