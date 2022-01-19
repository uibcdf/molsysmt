def extract(item, atom_indices='all', frame_indices='all', copy_if_all=True, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory.is_molsysmt_Trajectory import _checking_form
        _checking_form(item, check_form=check_form)

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

