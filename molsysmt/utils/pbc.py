from molsysmt.lib import box as _libbox

def get_shape_from_angles(angles):

    import numpy as np

    shape = None

    alpha = angles[:,0].mean()
    beta = angles[:,1].mean()
    gamma = angles[:,2].mean()

    alpha = np.round(alpha, 2)
    beta = np.round(beta, 2)
    gamma = np.round(gamma, 2)

    if alpha==90.00 and beta==90.00 and gamma==90.00:
        shape = 'cubic'
    else:
        shape = 'triclinic'

    return shape

def get_shape_from_box(box):

    from molsysmt.lib import box as _libbox

    n_frames = box.shape[0]
    angles = _libbox.angles_box(box._value, n_frames)
    return get_shape_from_angles(angles)

def get_box_lengths(box):

    from numpy import asfortranarray, ascontiguousarray

    length_units = box.unit
    n_frames = box.shape[0]
    tmp_box =  asfortranarray(box._value, dtype='float64')
    lengths = _libbox.length_edges_box(tmp_box, n_frames)
    lengths = ascontiguousarray(lengths, dtype='float64')
    del(tmp_box)

    return lengths.round(6)*length_units

def get_box_angles(box):

    from numpy import asfortranarray, ascontiguousarray
    from simtk.unit import degrees

    n_frames = box.shape[0]
    tmp_box =  asfortranarray(box._value, dtype='float64')
    angles = _libbox.angles_box(tmp_box, n_frames)
    angles = ascontiguousarray(angles, dtype='float64')
    del(tmp_box)

    return angles.round(6)*degrees

def get_box_from_lengths_and_angles(lengths, angles):

    from numpy import asfortranarray, ascontiguousarray

    length_units = lengths.unit
    angle_units = angles.unit
    tmp_lengths =  asfortranarray(lengths._value, dtype='float64')
    tmp_angles =  asfortranarray(angles._value, dtype='float64')
    n_frames = lengths.shape[0]

    box = _libbox.lengths_and_angles_to_box(tmp_lengths, tmp_angles, n_frames)
    box = ascontiguousarray(box, dtype='float64')

    del(tmp_lengths, tmp_angles)

    return box.round(6)*length_units

