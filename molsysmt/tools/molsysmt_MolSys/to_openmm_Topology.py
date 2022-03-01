def to_openmm_Topology(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')


    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.tools.molsysmt_MolSys import get_box_from_system as get_box_from_system

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, check_form=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check_form=False)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, box=box, atom_indices=atom_indices, check_form=False)

    return tmp_item

