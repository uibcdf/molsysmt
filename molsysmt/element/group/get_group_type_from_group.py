def get_group_type_from_group(item, indices='all'):

    from molsysmt.basic import get
    from .get_group_type_from_group_name import name_to_type
    group_names = get(item, target='group', indices=indices, group_name=True)
    output= np.vectorize(name_to_type)(group_names).astype('object')
    return output

