
def digest(item, frame_indices):

    from numpy import arange
    from molmodmt import get

    if frame_indices == 'all':
        n_frames = get(item, n_frames=True)
        frame_indices = arange(n_frames)
    elif type(frame_indices)==int:
        frame_indices = [frame_indices]

    return frame_indices

