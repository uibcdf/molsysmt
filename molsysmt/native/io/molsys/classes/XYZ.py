def to_XYZ (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt import get

    tmp_item = get(item, target='atom', selection=atom_indices, frame_indices=frame_indices,
                coordinates=True)

    return tmp_item

