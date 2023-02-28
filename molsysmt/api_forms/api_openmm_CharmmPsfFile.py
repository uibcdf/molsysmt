def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_CharmmPsfFile import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    return openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    return openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)

