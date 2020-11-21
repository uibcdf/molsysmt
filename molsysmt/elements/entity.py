from molsysmt.utils.exceptions import *
import numpy as np

types = ["water", "ion", "cosolute", "protein", "peptide", "rna", "dna", "lipid", "small molecule"]

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

    molecule_index, molecule_type = get(item, target='molecule', molecule_index=True, molecule_type=True)
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
                group_name = get(item, target='atom', indices=m_atoms[0], group_name=True)[0]
                name = group_name
                type = 'lipid'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'small molecule':
                group_name = get(item, target='atom', indices=m_atoms[0], group_name=True)[0]
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

def entity_index_from_atom(item, indices='all'):

    output, _,  _ = _aux(item)

    if indices is not 'all':
        output = output[indices]

    return output

def entity_id_from_entity(item, indices='all'):

    if indices is 'all':
        from molsysmt.multitool import get
        n_entities = get(item, target='system', n_entities=True)
        output = np.full(n_entities, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

def entity_name_from_entity(item, indices='all'):

    entity_index_from_atom, entity_name_from_atom, _ = _aux(item)

    output=[]
    if indices is 'all':
        indices = np.unique(entity_index_from_atom)

    for ii in indices:
        atom_index = np.where(entity_index_from_atom==ii)
        output.append(entity_name_from_atom[atom_index])

    output = np.array(output, dtype=object)

    return output

def entity_type_from_entity(item, indices='all'):

    entity_index_from_atom, _, entity_type_from_atom = _aux(item)

    if indices is 'all':
        indices = np.unique(entity_index_from_atom)

    output=[]
    for ii in indices:
        atom_index = np.where(entity_index_from_atom==ii)[0][0]
        output.append(entity_type_from_atom[atom_index])

    output = np.array(output, dtype=object)

    return output

def n_entities_from_system(item, indices='all'):

    from molsysmt import get

    entity_index_from_atom = get(item, target='atom', indices='all', entity_index=True)
    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
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

def _shortpath_to_build_entities(molecule_index_from_atom, molecule_type_from_atom, group_name_from_atom):

    n_atoms = molecule_index_from_atom.shape[0]
    molecule_indices = np.unique(molecule_index_from_atom)

    index_array = np.full(n_atoms, None, dtype=object)
    id_array = np.full(n_atoms, None, dtype=object)
    name_array = np.full(n_atoms, None, dtype=object)
    type_array = np.full(n_atoms, None, dtype=object)

    entities = {}
    n_entities = 0
    n_peptides = 0
    n_proteins = 0

    for molecule_index in molecule_indices:

        mask = (molecule_index_from_atom==molecule_index)
        molecule_type = molecule_type_from_atom[mask][0]

        if molecule_type == 'water':
            entity_name = 'water'
            entity_type = 'water'
            try:
                entity_index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        elif molecule_type == 'ion':
            entity_name = group_name_from_atom[mask][0]
            entity_type = 'ion'
            try:
                entity_index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        elif molecule_type == 'peptide':
            entity_name = 'Peptide_'+str(n_peptides)
            entity_type = 'peptide'
            n_peptides+=1
            try:
                index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        elif molecule_type == 'protein':
            entity_name = 'Protein_'+str(n_proteins)
            entity_type = 'protein'
            n_proteins+=1
            try:
                entity_index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        elif molecule_type == 'lipid':
            entity_name = group_name_from_atom[mask][0]
            entity_type = 'lipid'
            try:
                entity_index = entities[entity_name]
            except:
                entity_entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        elif molecule_type == 'small molecule':
            entity_name = group_name_from_atom[mask][0]
            entity_type = 'small molecule'
            try:
                entity_index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1
        else:
            entity_name = 'unknown'
            entity_type = 'unknown'
            try:
                entity_index = entities[entity_name]
            except:
                entities[entity_name]=n_entities
                entity_index=n_entities
                n_entities+=1

        index_array[mask]=entity_index
        name_array[mask]=entity_name
        type_array[mask]=entity_type

    return index_array, id_array, name_array, type_array

