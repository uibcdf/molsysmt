from molsysmt._private_tools.exceptions import *
from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory

## atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    tmp_coordinates = item.coordinates

    if frame_indices is not 'all':
        tmp_coordinates = tmp_coordinates[frame_indices,:,:]

    if indices is not 'all':
        tmp_coordinates = tmp_coordinates[:,indices,:]

    return tmp_coordinates

def get_n_atoms_from_atom(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if indices is 'all':
        output=item.coordinates.shape[1]
    else:
        output=indices.shape[0]

    return output

def get_frame_from_atom(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    tmp_step = get_step_from_system(item, frame_indices=frame_indices, check_form=False)
    tmp_time = get_time_from_system(item, frame_indices=frame_indices, check_form=False)
    tmp_coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices, check_form=False)
    tmp_box = get_box_from_system(item, frame_indices=frame_indices, check_form=False)

    return tmp_step, tmp_time, tmp_coordinates, tmp_box

def get_n_frames_from_atom(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    return get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=False)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if indices is 'all':
        output=item.coordinates.shape[1]
    else:
        output=indices.shape[0]

    return output

def get_coordinates_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if frame_indices is 'all':
        output=item.coordinates
    else:
        output=item.coordinates[frame_indices,:,:]
    return output

def get_box_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    output=None
    if item.box is not None:
        if frame_indices is 'all':
            output=item.box
        else:
            output=item.box[frame_indices,:,:]
    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    from molsysmt.pbc import box_shape_from_box_vectors
    output = None
    box = get_box_from_system(item, indices=indices, frame_indices=frame_indices, check_form=False)
    if box is not None:
        output = box_shape_from_box_vectors(box)
    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    tmp_box_lengths = item.get_box_lengths()
    if frame_indices is 'all':
        output = tmp_box_lengths
    else:
        output = tmp_box_lengths[frame_indices,:]
    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    tmp_box_angles = item.get_box_angles()
    if frame_indices is 'all':
        output = tmp_box_angles
    else:
        output = tmp_box_angles[frame_indices,:]
    return output

def get_time_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if frame_indices is 'all':
        output = item.time
    else:
        output = item.time[frame_indices]
    return output

def get_step_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if frame_indices is 'all':
        output = item.step
    else:
        output = item.step[frame_indices]
    return output

def get_frame_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    return get_frame_from_atom(item, frame_indices=frame_indices, check_form=False)

def get_n_frames_from_system(item, indices='all', frame_indices='all', check_form=True):

    if check_form:
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    if frame_indices is 'all':
        output=item.coordinates.shape[0]
    else:
        output=frame_indices.shape[0]

    return output

