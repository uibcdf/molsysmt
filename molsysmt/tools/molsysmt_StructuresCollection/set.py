
def set_box_to_system(item, indices='all', structure_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory.is_molsysmt_Trajectory import _checking_form
        _checking_form(item, check_form=check_form)

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

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory.is_molsysmt_Trajectory import _checking_form
        _checking_form(item, check_form=check_form)

    raise NotImplementedError

