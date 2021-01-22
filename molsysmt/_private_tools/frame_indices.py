import numpy as np

def complementary_frame_indices(item, frame_indices):

    from molsysmt import get

    n_frames = get(item, target='system', n_frames=True)

    mask = np.ones(n_frames,dtype=bool)
    mask[frame_indices]=False
    return list(np.where(mask)[0])

def digest_frame_indices(frame_indices):

    if type(frame_indices)==str:
        if frame_indices in ['all', 'All', 'ALL']:
            frame_indices = 'all'
        else:
            raise ValueError()
    elif type(frame_indices) in [int, np.int64, np.int]:
        frame_indices = np.array([frame_indices], dtype='int64')
    elif hasattr(frame_indices, '__iter__'):
        frame_indices = np.array(frame_indices, dtype='int64')

    return frame_indices

