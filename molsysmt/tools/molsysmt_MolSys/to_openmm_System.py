def to_openmm_System(item, atom_indices='all', frame_indices='all', check_form=True):


    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices,
                                                  frame_indices=frame_indices, check_form=False)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, check_form=False)

    return tmp_item

