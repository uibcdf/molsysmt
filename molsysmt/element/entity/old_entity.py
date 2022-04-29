import numpy as np

def _aux(item):

    from molsysmt import get
    from numpy import empty, full

    entities = {}
    n_entities = 0
    n_atoms = get(item, element='system', n_atoms=True)

    n_peptides = 0
    n_proteins = 0

    index_array = full(n_atoms, None, dtype=object)
    name_array = full(n_atoms, None, dtype=object)
    type_array = full(n_atoms, None, dtype=object)

    molecule_index, molecule_type = get(item, element='molecule', molecule_index=True, molecule_type=True)
    atom_indices_in_molecule = get(item, element='molecule', atom_index=True)


    for m_index, m_type, m_atoms in zip(molecule_index, molecule_type, atom_indices_in_molecule):

        m_atoms = m_atoms.astype(int)

        if m_index is not None:

            if m_type == 'water':
                name = 'water'
                type = 'water'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'ion':
                group_name = get(item, element='atom', indices=m_atoms, group_name=True)[0]
                name = group_name
                type = 'ion'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'peptide':
                name = 'Peptide_'+str(n_peptides)
                type = 'peptide'
                n_peptides+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'protein':
                name = 'Protein_'+str(n_proteins)
                type = 'protein'
                n_proteins+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'lipid':
                group_name = get(item, element='atom', indices=m_atoms[0], group_name=True)[0]
                name = group_name
                type = 'lipid'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'small molecule':
                group_name = get(item, element='atom', indices=m_atoms[0], group_name=True)[0]
                name = group_name
                type = 'small molecule'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            else:
                name = 'unknown'
                type = 'unknown'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1

            index_array[m_atoms]=index
            type_array[m_atoms]=type
            name_array[m_atoms]=name

    del(molecule_index, molecule_type, atom_indices_in_molecule)

    return index_array, name_array, type_array

def entity_index_from_atom(item, indices='all', check=True):

    output, _,  _ = _aux(item)

    if indices is not 'all':
        output = output[indices]

    return output

def entity_id_from_entity(item, indices='all', check=True):

    if indices is 'all':
        from molsysmt.basic.get import get
        n_entities = get(item, element='system', n_entities=True)
        output = np.full(n_entities, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def entity_name_from_entity(item, indices='all', check=True):

    entity_index_from_atom, entity_name_from_atom, _ = _aux(item)

    output=[]
    if indices is 'all':
        indices = np.unique(entity_index_from_atom)

    for ii in indices:
        atom_index = np.where(entity_index_from_atom==ii)[0][0]
        output.append(entity_name_from_atom[atom_index])

    output = np.array(output, dtype=object)

    return output

def entity_type_from_entity(item, indices='all', check=True):

    entity_index_from_atom, _, entity_type_from_atom = _aux(item)

    if indices is 'all':
        indices = np.unique(entity_index_from_atom)

    output=[]
    for ii in indices:
        atom_index = np.where(entity_index_from_atom==ii)[0][0]
        output.append(entity_type_from_atom[atom_index])

    output = np.array(output, dtype=object)

    return output

def n_entities_from_system(item, indices='all', check=True):

    from molsysmt import get

    entity_index_from_atom = get(item, element='atom', indices='all', entity_index=True)
    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
        n_entities = output.shape[0]
    return n_entities


