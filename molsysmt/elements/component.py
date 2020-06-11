def group_name_to_type(group_name, n_groups=1):

    from .groups import name_to_component_type
    return name_to_component_type(group_name, n_groups)

def group_type_to_type(group_type, n_groups=1):

    from .groups import type_to_component_type
    return type_to_component_type(grouptypee, n_groups)

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


