
def group_name_to_type(group_name):

    if type(groups_type) is str:
        if group_name in ['water', 'ion', 'cosolute',  'small molecule']:
            return group_name
        elif group_name == 'aminoacid':
            return 'peptide'
        elif group_name == 'nucleotide':
            from .group import rna_names, dna_names
            if group_name in rna_names:
                return 'rna'
            elif group_name in dna_names:
                return 'dna'
    else:
        tmp_type = group_name_to_type(group_name[0])
        if tmp_type == 'peptide':
            if len(group_name)>=50:
                tmp_type == 'protein'

def is_type(item, indices='all', selection=None, syntaxis='MolSysMT'):

    from molsysmt import select, get

    if selection is not None:
         indices = select(item, taret='component', selection=selection, syntaxis=syntaxis)

    group_names = get(item, target='component', indices=indices, group_name=True)

    return list(map(name_to_type,group_names))


    pass

