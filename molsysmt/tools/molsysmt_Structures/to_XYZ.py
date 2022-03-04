def to_XYZ(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.molsysmt_Structures import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_Structures(item):
            raise WrongFormError('molsysmt.Trajectory')

    from molsysmt.tools.molsysmt_Structures import get_coordinates_from_atom
    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

