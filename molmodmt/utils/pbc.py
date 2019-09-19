
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

    from molmodmt.lib import box as _libbox

    n_frames = box.shape[0]
    angles = _libbox.angles_box(box._value, n_frames)
    return get_shape_from_angles(angles)


