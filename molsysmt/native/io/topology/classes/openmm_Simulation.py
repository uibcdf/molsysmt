def from_openmm_Simulation(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

