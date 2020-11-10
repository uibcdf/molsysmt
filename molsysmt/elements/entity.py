from molsysmt.utils.exceptions import *
import numpy as np

types = ["water", "ion", "cosolute", "protein", "peptide", "rna", "dna", "lipid"]

def _aux(item):

    from molsysmt import get
    from numpy import empty, full

    entities = {}
    n_entities = 0
    n_atoms = get(item, target='system', n_atoms=True)

    n_peptides = 0
    n_proteins = 0

    index_array = full(n_atoms, None, dtype=object)
    name_array = full(n_atoms, None, dtype=object)
    type_array = full(n_atoms, None, dtype=object)

    molecule_index, molecule_type = get(item, target='molecule', index=True, type=True)
    atom_indices_in_molecule = get(item, target='molecule', atom_index=True)

    for m_index, m_type, m_atoms in zip(molecule_index, molecule_type, atom_indices_in_molecule):

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
                group_name = get(item, target='atom', indices=m_atoms, group_name=True)[0]
                name = group_name
                type = 'ion'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'peptide':
                name = 'Peptide'+str(n_peptides)
                type = 'peptide'
                n_peptides+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'protein':
                name = 'Protein'+str(n_proteins)
                type = 'protein'
                n_proteins+=1
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'lipid':
                group_name = get(item, target='group', indices=m_atoms, name=True)[0]
                name = group_name
                type = 'lipid'
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

def get_entity_index_from_atom(item, indices='all'):

    output, _, _ = _aux(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_entity_id_from_atom(item, indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices=indices)
    entity_indices = np.unique(entity_index_from_atom)
    entity_ids = get_entity_id_from_entity(item, indices=component_entity)
    aux_dict = dict(zip(entity_indices, entity_ids))
    output = np.vectorize(aux_dict.__getitem__)(entity_index_from_atom)
    del(aux_dict)
    return output

def get_entity_name_from_atom(item, indices='all'):

    _, output, _ = _aux(item)

    if indices is not 'all':
        output = output[indices]

    return output


def get_entity_type_from_atom(item, indices='all'):

    _, _, output = _aux(item)

    if indices is not 'all':
        output = output[indices]

    return output

def get_atom_index_from_entity(item, indices='all'):

    entity_index_from_atom = get_entity_index_from_atom(item, indices='all')
    indices_aux = get_entity_index_from_entity(item, indices='all')

    output = []
    for ii in indices_aux:
        tmp_indices = np.where(aaa==ii)[0]
        output.append(tmp_indices)

    output = np.array(output, dtype=object)

    return output

def get_entity_index_from_entity(item, indices='all'):

    if indices is 'all':
        entity_index_from_atom = get_entity_index_from_atom(item, indices='all')
        entity_indices = np.unique(entity_index_from_atom)
        n_entities = entity_indices.shape[0]
        output = np.arange(n_entities)
    else:
        output = np.array(indices)

    return output

def get_entity_index_from_entity(item, indices='all'):

    if indices is 'all':
        n_entities = get_n_entities_from_system(item)
        output = np.arange(n_entities)
    else:
        output = np.array(indices)

    return output

def get_n_entities_from_system(item, indices='all'):

    output = get_entity_index_from_atom(item, indices='all')
    if output[0] is None:
        n_entities = 0
    else:
        output = np.unique(output)
        n_entities = output.shape[0]
    return n_entities

def type_from_MMTFDecoder_entity (mmtf_entity):

    if mmtf_entity['type']=='water':
        return 'water'
    elif mmtf_entity['type']=='polymer':
        return _get_type_from_sequence(mmtf_entity['sequence'])
    else:
        return None

    pass

def _get_type_from_sequence(sequence):

    from .molecule import _get_type_from_sequence as molecule_type_from_sequence

    molecule_type = molecule_type_from_sequence(sequence)

    if molecule_type == 'protein':
        return 'protein'
    elif molecule_type == 'dna':
        return 'dna'
    elif molecule_type == 'rna':
        return 'rna'
    elif molecule_type == 'peptide':
        return 'peptide'
    else:
        return None

def get_elements(item):

    index_array, name_array, type_array = _aux(item)
    id_array = get_entity_id_from_atom(item, indices='all')

    return index_array, id_array, name_array, type_array

