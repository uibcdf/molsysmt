def from_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = openmm_Topology_to_molsysmt_Topology(item.topology, atom_indices=atom_indices)

    return tmp_item

