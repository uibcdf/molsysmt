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

def get_elements(item):



    from molsysmt import get
    from molsysmt.elements.group import type_to_component_type as group_type_to_component_type
    from networkx import empty_graph, connected_components
    from numpy import empty

    n_atoms = get(item, target='system', n_atoms=True)
    bonded_atoms = get(item, target='bond', atom_index=True)

    G = empty_graph(n_atoms)
    G.add_edges_from(bonded_atoms)

    index_array = empty(n_atoms, dtype=int)
    id_array = empty(n_atoms, dtype=object)
    type_array = empty(n_atoms, dtype=object)
    name_array = empty(n_atoms, dtype=object)

    component_index = 0

    for atom_indices_of_component in connected_components(G):
        aux_list = list(atom_indices_of_component)
        group_type = get(item, target='atom', indices=[aux_list[0]], group_type=True)[0]
        component_type = group_type_to_component_type(group_type)
        if component_type == 'peptide':
            n_groups = get(item, target='atom', indices=aux_list, n_groups=True)
            component_type = group_type_to_component_type(group_type, n_groups)
        index_array[aux_list] = component_index
        type_array[aux_list] = component_type
        component_index += 1

    return index_array, id_array, name_array, type_array

