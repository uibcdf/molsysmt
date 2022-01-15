
def set_box_to_system(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')
        if not is_molsysmt_Trajectory(to_item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    n_frames_trajectory = item.coordinates.shape[0]
    n_frames_box = value.shape[0]

    if n_frames_trajectory == n_frames_box:
        item.box = value
    else:
        if n_frames_box == 1:
            item.box = np.broadcast_to(value[0]._value, (n_frames_trajectory,3,3)) * value.unit
        else:
            raise ValueError("box and coordinates have different shape")

    pass

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')
        if not is_molsysmt_Trajectory(to_item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    raise NotImplementedError

