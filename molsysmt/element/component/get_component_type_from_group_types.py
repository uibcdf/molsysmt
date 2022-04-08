def get_component_type_from_group_types(group_types):

    n_groups = len(group_types)
    first_type = group_types[0]

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type=first_type
    elif (first_type == 'aminoacid') or (first_type == 'terminal_capping'):
        if first_type == 'terminal_capping': n_groups -=1
        if group_types[-1] == 'terminal_capping': n_groups -=1
        if n_groups>=50:
            tmp_type='protein'
        else:
            tmp_type='peptide'
    elif first_type == 'nucleotide':
        if first_name in rna_group_names:
            tmp_type = 'rna'
        elif first_name in dna_group_names:
            tmp_type = 'dna'

    return tmp_type

