def to_aminoacids3_seq (item, atom_indices='all', frame_indices='all'):

    from molsysmt import get
    from numpy import unique

    group_names = get(item, target='group', selection=atom_indices, group_name=True)
    tmp_item = ''.join([ii.title() for ii in group_names])
    return 'aminoacids3:'+tmp_item

