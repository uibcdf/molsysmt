def to_molsysmt_TrajectoryDict(item, atom_indices='all', structure_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Structures import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_Structures(item):
            raise WrongFormError('molsysmt.Trajectory')

    from molsysmt.tools.molsysmt_Structures import get_frame_from_atom

    step, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check_form=False)

    tmp_item = {}

    if step is not None:
        tmp_item['step']=step

    if time is not None:
        tmp_item['time']=time

    if coordinates is not None:
        tmp_item['coordinates']=coordinates

    if box is not None:
        tmp_item['box']=box

    return tmp_item

