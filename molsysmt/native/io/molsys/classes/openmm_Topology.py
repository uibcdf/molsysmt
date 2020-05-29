def to_openmm_Topology (item, trajectory_item=None ,atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    tmp_item = molsysmt_Topology_to_openmm_Topology(item.topology, atom_indices=atom_indices)

    return tmp_item

