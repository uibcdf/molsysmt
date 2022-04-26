def get_component_type_from_group_names(group_names):

    from ..group import get_group_type_from_group_name
    from ..group.nucleotide import rna_names, dna_names

    n_groups = len(group_names)
    first_name = group_names[0]
    first_type = get_group_type_from_group_name(first_name)
    last_name = group_names[-1]
    last_type = get_group_type_from_group_name(last_name)

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type=first_type
    elif (first_type == 'aminoacid') or (first_type == 'terminal capping'):
        if first_type == 'terminal capping': n_groups -=1
        if last_type == 'terminal capping': n_groups -=1
        if n_groups>=50:
            tmp_type='protein'
        else:
            tmp_type='peptide'
    elif first_type == 'nucleotide':
        if first_name in rna_names:
            tmp_type = 'rna'
        elif first_name in dna_names:
            tmp_type = 'dna'

    return tmp_type

