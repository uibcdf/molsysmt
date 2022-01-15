def to_molsysmt_TrajectoryDict(item, atom_indices='all', frame_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    from molsysmt.tools.molsysmt_Trajectory import get_frame_from_atom

    step, time, coordinates, box = get_frame_from_atom(item, indices=atom_indices, frame_indices=frame_indices, check_form=False)

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

