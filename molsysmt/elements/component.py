import numpy as np

types = ['water', 'ion', 'cosolute', 'small molecule', 'lipid', 'peptide', 'protein', 'rna', 'dna']

def get_component_index_from_atom(item, indices='all'):

    from molsysmt.multitool import get
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

def get_component_id_from_atom(item, indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_name_from_atom(item, indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_type_from_atom(item, indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_atom_index_from_component(item, indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices='all')
    indices_aux = get_component_index_from_component(item, indices='all')

    output = []
    for ii in indices_aux:
        tmp_indices = np.where(aaa==ii)[0]
        output.append(tmp_indices)

    output = np.array(output, dtype=object)

    return output

def get_component_index_from_component(item, indices='all'):

    if indices is 'all':
        component_index_from_atom = get_component_index_from_atom(item, indices='all')
        component_indices = np.unique(component_index_from_atom)
        n_components = component_indices.shape[0]
        output = np.arange(n_components)
    else:
        output = np.array(indices)

    return output

def get_component_id_from_component(item, indices='all'):

    if indices is 'all':
        n_components = get_n_components_from_system(item)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def get_component_name_from_component(item, indices='all'):

    if indices is 'all':
        n_components = get_n_components_from_system(item)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def get_component_type_from_component(item, indices='all'):

    atom_indices_from_component = get_atom_index_from_component(item, indices=indices)

    output = []

    for atom_indices in atom_indices_from_component:
        component_type = _get_type_from_atoms(item, atom_indices)
        output.append(component_type)

    output = np.array(output, dtype=object)

    return output

def _get_type_from_atoms(item, indices):

    from molsysmt import get
    group_indices = get(item, target='atom', indices=indices, group_index=True)
    group_indices = np.unique(group_indices)
    return _get_type_from_groups(item, group_indices)

def _get_type_from_groups(item, indices):

    from molsysmt import get
    group_names = get(item, target='group', indices=indices, name=True)
    return _get_type_from_group_names(group_names)

def _get_type_from_group_name(group_name, n_groups=1):

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

