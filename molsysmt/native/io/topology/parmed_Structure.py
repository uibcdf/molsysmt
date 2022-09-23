def from_parmed_Structure(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_items.api_parmed_Structure import to_openmm_Topology as parmed_Structure_to_openmm_Topology
    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = parmed_Structure_to_openmm_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

