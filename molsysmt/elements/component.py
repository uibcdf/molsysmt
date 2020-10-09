types = ['water', 'ion', 'cosolute', 'small molecule', 'lipid', 'peptide', 'protein', 'rna', 'dna']

def type_from_atoms(item, indices):

    from molsysmt import get
    group_indices = get(item, target='atom', indices=indices, group_index=True)
    group_indices = np.unique(group_indices)
    return type_from_groups(item, group_indices)

def type_from_groups(item, indices):

    from molsysmt import get
    group_names = get(item, target='group', indices=indices, name=True)
    return type_from_group_names(group_names)

def type_from_group_name(group_name, n_groups=1):

    from .groups import name_to_type as group_name_to_group_type
    from .groups import dna_names as dna_group_names
    from .groups import rna_names as rna_group_names

    tmp_type = None

    group_types = [group_name_to_group_type(ii) for ii in group_names]

    n_groups = len(group_types)
    first_type = group_types[0]
    first_name = group_names[0]

    if not (np.array(group_types) == first_type):
        raise ValueError("Groups have different type")

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type = group_type
    elif first_type == 'aminoacid':
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

def get_elements(item):

    from molsysmt import get
    from molsysmt.elements.group import type_to_component_type as group_type_to_component_type
    from networkx import empty_graph, connected_components
    from numpy import empty, full

    n_atoms = get(item, target='system', n_atoms=True)
    bonded_atoms = get(item, target='bond', atom_index=True)

    if bonded_atoms is None or len(bonded_atoms)==0:

        index_array = full(n_atoms, None, dtype=object)
        id_array = full(n_atoms, None, dtype=object)
        type_array = full(n_atoms, None, dtype=object)
        name_array = full(n_atoms, None, dtype=object)

    else:

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

