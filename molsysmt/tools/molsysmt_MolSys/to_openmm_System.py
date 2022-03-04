def to_openmm_System(item, atom_indices='all', structure_indices='all', check=True):


    if check:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, check=False)

    return tmp_item

