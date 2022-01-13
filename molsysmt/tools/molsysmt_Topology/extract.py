def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all'):
        tmp_item = item.copy()
    elif atom_indices is not 'all':
        tmp_item = item.extract(atom_indices=atom_indices)

    return tmp_item

