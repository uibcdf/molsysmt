
def set_box_to_system(item, indices='all', structure_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item, check_form=check_form)

    n_structures_trajectory = item.coordinates.shape[0]
    n_structures_box = value.shape[0]

    if n_structures_trajectory == n_structures_box:
        item.box = value
    else:
        if n_structures_box == 1:
            item.box = np.broadcast_to(value[0]._value, (n_structures_trajectory,3,3)) * value.unit
        else:
            raise ValueError("box and coordinates have different shape")

    pass

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item, check_form=check_form)

    raise NotImplementedError

