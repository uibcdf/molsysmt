def to_molsysmt_MolSys(item, atom_indices='all', model_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.native import MolSys
    from molsysmt.tools.file_pdb import to_molsysmt_Topology as file_pdb_to_molsysmt_Topology
    from molsysmt.tools.file_pdb import to_molsysmt_Trajectory as file_pdb_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = file_pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, model_indices=model_indices, check_form=False)
    tmp_item.trajectory = file_pdb_to_molsysmt_Trajectory(item, atom_indices=atom_indices, model_indices=model_indices, check_form=False)

    return tmp_item

