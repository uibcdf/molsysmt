import numpy as np
from .rna import group_name as rna_group_names
from .dna import group_name as dna_group_names

types = ['water', 'ion', 'cosolute', 'small molecule', 'lipid', 'peptide', 'protein', 'rna', 'dna']

def component_index_from_atom(item, indices='all'):

    from molsysmt.basic import get
    from molsysmt.lib import bonds as _libbonds

    n_atoms, n_bonds = get(item, target='system', n_atoms=True, n_bonds=True)

    if n_bonds==0:
        output = np.full(n_atoms, None, dtype=object)

    else:

        atoms_indices = get(item, target='bond', indices='all', atom_index=True)

        output = _libbonds.component_indices(atoms_indices, n_atoms, n_bonds)
        output = np.ascontiguousarray(output, dtype=int)

    if indices is not 'all':
        output = output[indices]

    return output

def component_id_from_component(item, indices='all'):

    if indices is 'all':
        from molsysmt.basic import get
        n_components = get(item, target='system', n_components=True)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def component_name_from_component(item, indices='all'):

    if indices is 'all':
        from molsysmt.basic import get
        n_components = get(item, target='system', n_components=True)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def component_type_from_component(item, indices='all'):

    from molsysmt.basic import get

    group_types_from_component = get(item, target='component', indices=indices, group_type=True)

    output = []

    for group_types in group_types_from_component:
        component_type = _type_from_group_type(group_types)
        output.append(component_type)

    output = np.array(output, dtype=object)

    return output

def n_components_from_system(item, indices='all'):

    from molsysmt import get

    component_index_from_atom = get(item, target='atom', indices='all', component_index=True)
    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = np.unique(component_index_from_atom)
        n_components = output.shape[0]
    return n_components

def _type_from_group_type(group_types):

    n_groups = len(group_types)
    first_type = group_types[0]

    if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
        tmp_type = first_type
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


def _shortpath_to_build_components(n_atoms, n_bonds, atom_index_from_bond, group_index_from_atom, group_type_from_atom):

    from molsysmt.lib import bonds as _libbonds

    if n_bonds==0:

        index_array = np.full(n_atoms, None, dtype=object)
        id_array = np.full(n_atoms, None, dtype=object)
        name_array = np.full(n_atoms, None, dtype=object)
        type_array = np.full(n_atoms, None, dtype=object)

    else:

        index_array = _libbonds.component_indices(atom_index_from_bond, n_atoms, n_bonds)
        index_array = np.ascontiguousarray(index_array, dtype=int)

        component_indices = np.unique(index_array)
        n_components = component_indices.shape[0]

        id_array = np.full(n_atoms, None, dtype=object)
        name_array = np.full(n_atoms, None, dtype=object)
        type_array = np.full(n_atoms, None, dtype=object)

        for ii in component_indices:
            mask = (index_array==ii)
            first_type = group_type_from_atom[mask][0]
            if first_type in ['water', 'ion', 'cosolute', 'small molecule', 'lipid']:
                tmp_type=first_type
            elif first_type == 'aminoacid':
                n_groups = np.unique(group_index_from_atom[mask]).shape[0]
                if n_groups>=50:
                    tmp_type='protein'
                else:
                    tmp_type='peptide'
            elif first_type == 'nucleotide':
                if first_name in rna_group_names:
                    tmp_type = 'rna'
                elif first_name in dna_group_names:
                    tmp_type = 'dna'
            type_array[mask]=tmp_type

    return index_array, id_array, name_array, type_array

