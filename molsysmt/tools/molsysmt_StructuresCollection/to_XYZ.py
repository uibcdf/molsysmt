def to_XYZ(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_Trajectory(item):
            raise WrongFormError('molsysmt.Trajectory')

    from molsysmt.tools.molsysmt_Trajectory import get_coordinates_from_atom
    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check_form=False)

    return tmp_item

