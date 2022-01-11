def extract(item, atom_indices='all', frame_indices='all', copy_if_all=True):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        tmp_item = item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

