def extract(item, atom_indices='all', frame_indices='all', copy_if_all=True, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

