def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pytraj_Topology import to_molsysmt_Topology as pytraj_Topology_to_molsysmt_Topology

    return pytraj_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)
