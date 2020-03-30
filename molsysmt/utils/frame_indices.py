
def digest(item, frame_indices):

    from numpy import arange, array
    from molsysmt.multitool import get

    if frame_indices is 'all':
        n_frames = get(item, target='system', n_frames=True)
        frame_indices = arange(n_frames, dtype='int64')
    elif type(frame_indices)==int:
        frame_indices = array([frame_indices], dtype='int64')
    elif type(frame_indices) in [tuple, list]:
        frame_indices = array(frame_indices, dtype='int64')

    return frame_indices

