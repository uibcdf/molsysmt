
def digest(item, frame_indices):

    from numpy import arange, array
    from molmodmt import get

    if frame_indices == 'all':
        n_frames = get(item, n_frames=True)
        frame_indices = arange(n_frames, dtype='int64')
    elif type(frame_indices)==int:
        frame_indices = array([frame_indices], dtype='int64')

    return frame_indices

