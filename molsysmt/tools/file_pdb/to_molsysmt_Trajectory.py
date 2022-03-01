def to_molsysmt_Trajectory(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check_form=check_form)

    from molsysmt.native import Trajectory
    tmp_item = Trajectory(filepath=item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

