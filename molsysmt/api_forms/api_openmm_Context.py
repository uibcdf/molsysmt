def to_openmm_System(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Context import to_openmm_System as openmm_Context_to_openmm_System

    return openmm_Context_to_openmm_System(item, atom_indices=atom_indices)

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.openmm_Context import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    return openmm_Context_to_molsysmt_Structures(item, atom_indices=atom_indices)

