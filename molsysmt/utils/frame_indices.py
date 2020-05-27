
def complementary_frame_indices(item, frame_indices):

    from numpy import ones
    from numpy import where
    from molsysmt import get

    n_frames = get(item, target='system', n_frames=True)

    mask = ones(n_frames,dtype=bool)
    mask[frame_indices]=False
    return list(where(mask)[0])

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

