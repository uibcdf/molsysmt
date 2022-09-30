from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_entity_all_from_atom(molecular_system):

    from molsysmt import get
    from numpy import empty, full

    entities = {}
    n_entities = 0
    n_atoms = get(molecular_system, element='system', n_atoms=True)

    n_peptides = 0
    n_proteins = 0

    index_array = np.full(n_atoms, None, dtype=object)
    name_array = np.full(n_atoms, None, dtype=object)
    type_array = np.full(n_atoms, None, dtype=object)

    molecule_index, molecule_type = get(molecular_system, element='molecule', molecule_index=True, molecule_type=True)
    atom_indices_in_molecule = get(molecular_system, element='molecule', atom_index=True)


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
                group_name = get(molecular_system, element='atom', indices=m_atoms, group_name=True)[0]
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
                group_name = get(molecular_system, element='atom', indices=m_atoms[0], group_name=True)[0]
                name = group_name
                type = 'lipid'
                try:
                    index = entities[name]
                except:
                    entities[name]=n_entities
                    index=n_entities
                    n_entities+=1
            elif m_type == 'small molecule':
                group_name = get(molecular_system, element='atom', indices=m_atoms[0], group_name=True)[0]
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


