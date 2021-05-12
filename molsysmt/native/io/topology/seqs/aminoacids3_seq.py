def to_aminoacids3_seq (item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt import get
    from numpy import unique

    group_names = get(item, target='group', selection=atom_indices, group_name=True)
    tmp_item = ''.join([ii.title() for ii in group_names])
    tmp_item = 'aminoacids3:'+tmp_item
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

