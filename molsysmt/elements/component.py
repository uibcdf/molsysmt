
def group_names_to_type(group_names):

    from .groups import name_to_type

    group_types = name_to_type(group_names)
    return group_types_to_type(group_types)

def group_types_to_type(group_types):

    if type(group_types) is str:
        if group_types in ['water', 'ion', 'cosolute',  'small molecule']:
            tmp_type = group_types
        elif group_types == 'aminoacid':
            tmp_type = 'peptide'
        elif group_types == 'nucleotide':
            from .group import rna_names, dna_names
            if group_types in rna_names:
                tmp_type = 'rna'
            elif group_types in dna_names:
                tmp_type = 'dna'
    else:
        tmp_type = group_types_to_type(group_types[0])
        if tmp_type == 'aminoacid':
            if len(group_types)>=50:
                tmp_type == 'protein'
            else:
                tmp_type == 'peptide'

    return tmp_type

def is_type(item, indices='all', selection=None, syntaxis='MolSysMT'):

    from molsysmt import select, get

    if selection is not None:
         indices = select(item, taret='component', selection=selection, syntaxis=syntaxis)

    group_types = get(item, target='component', indices=indices, group_type=True)

    return list(map(group_types_to_type,group_types))

