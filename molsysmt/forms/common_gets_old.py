# from openmm_topology

## Atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_atoms = get_n_atoms_from_system(item)
        output = _arange(n_atoms, dtype=int)
    else:
        output = indices

    return output

#def get_atom_id_from_atom(item, indices='all', frame_indices='all'):


#def get_atom_name_from_atom(item, indices='all', frame_indices='all'):


#def get_atom_type_from_atom(item, indices='all', frame_indices='all'):


#def get_group_index_from_atom (item, indices='all', frame_indices='all'):


def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_ids = get_group_id_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_ids))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_names = get_group_name_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_names))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices=indices)
    group_indices = np.unique(group_index_from_atom)
    group_types = get_group_type_from_group(item, indices=group_indices)
    aux_dict = dict(zip(group_indices, group_types))
    output = np.vectorize(aux_dict.__getitem__)(group_index_from_atom)
    del(aux_dict)
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_elements

    output, _, _, _ = get_elements(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_ids = get_component_id_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_ids))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_names = get_component_name_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_names))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    component_index_from_atom = get_component_index_from_atom(item, indices=indices)
    component_indices = np.unique(component_index_from_atom)
    component_types = get_component_type_from_component(item, indices=component_indices)
    aux_dict = dict(zip(component_indices, component_types))
    output = np.vectorize(aux_dict.__getitem__)(component_index_from_atom)
    del(aux_dict)
    return output

#def get_chain_index_from_atom (item, indices='all', frame_indices='all'):


def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_ids = get_chain_id_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_ids))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_names = get_chain_name_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_names))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    chain_index_from_atom = get_chain_index_from_atom(item, indices=indices)
    chain_indices = np.unique(chain_index_from_atom)
    chain_types = get_chain_type_from_chain(item, indices=chain_indices)
    aux_dict = dict(zip(chain_indices, chain_types))
    output = np.vectorize(aux_dict.__getitem__)(chain_index_from_atom)
    del(aux_dict)
    return output

#def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_ids = get_molecule_id_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_ids))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_names = get_molecule_name_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_names))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    molecule_index_from_atom = get_molecule_index_from_atom(item, indices=indices)
    molecule_indices = np.unique(molecule_index_from_atom)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    aux_dict = dict(zip(molecule_indices, molecule_types))
    output = np.vectorize(aux_dict.__getitem__)(molecule_index_from_atom)
    del(aux_dict)
    return output

#def get_entity_index_from_atom (item, indices='all', frame_indices='all'):


def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_ids = get_entity_id_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(molecule_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_names = get_entity_name_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_names))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_types = get_entity_type_from_entity(item, indices=entity_indices)
    aux_dict = dict(zip(entity_indices, entity_types))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_atoms_from_system(item)
    else:
        return indices.shape[0]

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    output = get_group_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    output = get_component_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_atom (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

#def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_bond_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):
#
#    output=[]
#
#    if indices is 'all':
#
#        for bond in item.bonds():
#            output.append([bond.atom1.index, bond.atom2.index])
#
#    else:
#
#        set_indices = set(indices)
#
#        for bond in item.bonds():
#            if bond.atom1.index in set_indices:
#                if bond.atom2.index in set_indices:
#                    output.append([bond.atom1.index, bond.atom2.index])
#
#    output = _array(output, dtype=int)
#
#    return(output)
#
#def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_mass_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError
#
#def get_charge_from_atom(item, indices='all', frame_indices='all'):
#
#    raise NotImplementedError

def get_form_from_atom(item, indices='all', frame_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    group_index_from_atom = get_group_index_from_atom(item, indices='all')

    if indices is 'all':
        n_groups = get_n_groups_from_system(item)
        indices = np.arange(n_groups)

    output = []
    for group_index in indices:
        atom_indices = np.where(group_index_from_atom==group_index)
        output.append(atom_indices)

    output = np.array(output)

    return output

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_ids = get_atom_id_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_ids))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_names = get_atom_names_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_names))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group(item, indices=indices)
    atom_indices = np.unique(atom_index_from_atom)
    atom_types = get_atom_types_from_atom(item, indices=atom_indices)
    aux_dict = dict(zip(atom_indices, atom_types))
    output = np.vectorize(aux_dict.__getitem__)(atom_index_from_group)
    del(aux_dict)
    return output

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        output = _arange(n_indices, dtype=int)
    else:
        output = indices

    return output

#def get_group_id_from_group(item, indices='all', frame_indices='all'):


#def get_group_name_from_group(item, indices='all', frame_indices='all'):


#def get_group_type_from_group(item, indices='all', frame_indices='all'):


def get_component_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_index_from_atom = get_component_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_name_from_atom = get_component_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_id_from_atom = get_component_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    component_type_from_atom = get_component_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(component_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].chain.index for ii in indices]
    output = _array(output)
    del(group)
    return output

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].chain.id for ii in indices]
    output = _array(output)
    del(group)
    return output

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [None for ii in indices]
    del(group)
    return output

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [None for ii in indices]
    del(group)
    return output

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_index_from_atom = get_molecule_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    atom_index_from_group = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_group:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    output = get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    output = get_component_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_group (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_group(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_id = get_atom_id_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_id[mask])

    output = _array(output)

    return output

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_name = get_atom_name_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_name[mask])

    output = _array(output)

    return output

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    atom_type = get_atom_type_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(atom_type[mask])

    output = _array(output)

    return output

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_components_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    component_indices = get_component_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (component_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_component(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_component (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_components_from_system(item))
     else:
         output = indices
     return output

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_id_from_atom = get_component_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_name_from_atom = get_component_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    component_type_from_atom = get_component_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(component_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_index_from_atom = get_chain_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_id_from_atom = get_chain_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_name_from_atom = get_chain_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    chain_type_from_atom = get_chain_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(chain_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_index_from_atom = get_molecule_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    atom_index_from_component = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_component:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    output = get_group_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    output = get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_component (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_component(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_id_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_name_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_atom_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_atom_type_from_atom(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_id_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_name_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_type_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_molecules_from_system(item)
        indices = range(n_indices)

    chain_index = get_chain_index_from_atom(item, indices='all')
    molecule_indices = get_molecule_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (molecule_indices==ii)
        output.append(_unique(chain_index[mask]))

    output = _array(output)

    return output

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_molecules_from_system(item))
     else:
         output = indices
     return output

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_id_from_atom = get_molecule_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_name_from_atom = get_molecule_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    molecule_type_from_atom = get_molecule_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(molecule_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    atom_index_from_molecule = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_molecule:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    output = get_group_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    output = get_component_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_molecule (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.index for atom in atoms]))
    del(chain)
    output = _array(output)
    return output

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.id for atom in atoms], dtype=int))
    del(chain)
    output = _array(output)
    return output

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.name for atom in atoms], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        atoms = list(chain[ii].atoms())
        output.append(_array([atom.element.symbol for atom in atoms], dtype=object))
    del(chain)
    output = _array(output)
    return output


def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.index for residue in residues]))
    del(chain)
    output = _array(output)
    return output

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.id for residue in residues], dtype=int))
    del(chain)
    output = _array(output)
    return output

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([residue.name for residue in residues], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type

    chain=list(item.chains())

    output = []
    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)
    for ii in indices:
        residues = list(chain[ii].residues())
        output.append(_array([name_to_type(residue.name) for residue in residues], dtype=object))
    del(chain)
    output = _array(output)
    return output

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    chain_indices = get_chain_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (chain_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_id_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_name_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_component_type_from_component(item)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        output = _arange(n_indices, dtype=int)
    else:
        output = indices
    return output

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = _array(output)
    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _array(output)
    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _array(output)
    return output

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    molecule_index = get_molecule_index_from_atom(item, indices='all')
    chain_indices = get_chain_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (chain_indices==ii)
        output.append(_unique(molecule_index[mask]))

    output = _array(output)

    return output

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_id_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_name_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_chain(item, indices=indices, frame_indices=frame_indices)
    aux_output = get_molecule_type_from_molecule(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(aux_output[aux_indices])
    output = _array(output)
    return output

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_index_from_atom = get_entity_index_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_index_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    atom_index_from_chain = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_chain:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    output = get_group_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    output = get_component_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_chain (item, indices=indices, frame_indices=frame_indices)
    output = _unique(output)
    return output.shape[0]

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_indices = get_atom_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_indices[mask])

    output = _array(output)

    return output

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_ids = get_atom_id_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_ids[mask])

    output = _array(output)

    return output

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_names = get_atom_name_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_names[mask])

    output = _array(output)

    return output

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    atom_types = get_atom_type_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(atom_types[mask])

    output = _array(output)

    return output

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    group_index = get_group_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(group_index[mask]))

    output = _array(output)

    return output

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_id_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_name_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_group_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_group_type_from_group(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    component_index = get_component_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(component_index[mask]))

    output = _array(output)

    return output

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_id_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_name_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_component_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_component_type_from_component(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    chain_index = get_chain_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(chain_index[mask]))

    output = _array(output)

    return output

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_id_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_name_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_chain_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_chain_type_from_chain(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_entities_from_system(item)
        indices = range(n_indices)

    molecule_index = get_molecule_index_from_atom(item, indices='all')
    entity_indices = get_entity_index_from_atom(item, indices='all')

    output=[]

    for ii in indices:
        mask = (entity_indices==ii)
        output.append(_unique(molecule_index[mask]))

    output = _array(output)

    return output

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_id_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output


def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_name_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    output=[]
    tmp_indices = get_molecule_index_from_entity(item, indices=indices, frame_indices=frame_indices)
    for aux_indices in tmp_indices:
        output.append(get_molecule_type_from_molecule(item, indices=aux_indices, frame_indices=frame_indices))
    output = _array(output)
    return output

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

     if indices is 'all':
         output = _arange(get_n_entities_from_system(item))
     else:
         output = indices
     return output

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_id_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_name_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    output = []
    for atom_indices in atom_index_from_entity:
        output.append(entity_type_from_atom[atom_indices[0]])

    output = _array(output)
    return output

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    output = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    output = get_group_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    output = get_component_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    output = get_molecule_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    output = get_chain_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    output = [ii.shape[0] for ii in output]
    return output

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    output = get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    return output.shape[0]

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.getNumAtoms()

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.getNumResidues()

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return get_n_components_from_atom(item, indices='all')

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.getNumChains()

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return get_n_molecules_from_atom(item, indices='all')

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return get_n_entities_from_atom(item, indices='all')

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.getNumBonds()

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='aminoacid').sum()

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    group_types = get_group_type_from_group(item, indices='all')
    return (group_types=='nucleotide').sum()

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='ion').sum()

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='water').sum()

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='cosolute').sum()

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='small_molecule').sum()

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='peptide').sum()

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='protein').sum()

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='dna').sum()

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    molecule_types = get_molecule_type_from_molecule(item, indices='all')
    return (molecule_types=='rna').sum()

def get_mass_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_charge_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    if box is not None:
        box_unit = box.unit
        box = _array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if frame_indices is 'all':
            output=box
        else:
            output=box[frame_indices,:,:]

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    tmp_out = None

    if indices is 'all':

        n_bonds = get_n_bonds_from_system(item)
        tmp_out = _arange(n_bonds, dtype=int)

    else:
        tmp_out = indices

    return tmp_out

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=_array(output)
    del(bond)
    return output

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    if indices is 'all':

        return get_n_bonds_from_system(item)

    else:

        return len(indices)

