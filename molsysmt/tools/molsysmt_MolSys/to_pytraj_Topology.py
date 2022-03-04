def to_pytraj_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_as_molsysmt_Topology
    from molsysmt.tools.molsysmt_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item = molsysmt_Topology_to_pytraj_Topology(tmp_item, check=False)

    return tmp_item

