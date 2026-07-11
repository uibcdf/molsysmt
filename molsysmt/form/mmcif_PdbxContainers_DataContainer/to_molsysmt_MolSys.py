from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.smonitor import (
    warn,
    CrossChainCovalentBondsWarning,
    MolecularSystemMismatchWarning,
)
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd

# https://github.com/rcsb/mmtf/blob/master/spec.md

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.element.group import get_bonded_atom_pairs
    from molsysmt.element.group import get_group_type_from_group_name
    from molsysmt.build import get_missing_bonds
    from molsysmt.configure import min_length_protein

    if isinstance(item, str):
        from .to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
        item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)

    # Atom site 

    with_insertions = False

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('atom_site').getAttributeList())}

    n_atoms = len(item.getObj('atom_site').data)

    atom_name = np.empty(n_atoms, dtype=object)
    atom_id = np.empty(n_atoms, dtype=int)
    atom_type = np.empty(n_atoms, dtype=object)

    group_index_from_atom = np.empty(n_atoms, dtype=int)
    chain_index_from_atom = np.empty(n_atoms, dtype=int)
    entity_index_from_atom = np.empty(n_atoms, dtype=int)

    atom_num_model = np.empty(n_atoms, dtype=int)

    coordinates = np.empty([1,n_atoms,3],dtype=float)
    occupancy = np.empty(n_atoms,dtype=float)
    alternate_location = np.empty(n_atoms,dtype=object)
    b_factor = np.empty([1,n_atoms],dtype=float)

    group_index_to_atom_indices = {}

    group_name = []
    group_id = []

    chain_name = []
    chain_id = []

    entity_id = []

    former_group_id = None
    group_index = -1

    former_chain_id = None
    chain_id_to_chain_index = {}
    chain_index = -1

    entity_id_to_entity_index = {}
    entity_index = -1

    chain_index_to_group_indices = {}
    chain_index_to_entity_index = []

    for atom_index, atom_record in enumerate(item.getObj('atom_site').data):

        atom_id[atom_index] = atom_record[index_att['id']]
        atom_type[atom_index] = atom_record[index_att['type_symbol']].upper()
        atom_name[atom_index] = atom_record[index_att['auth_atom_id']]

        coordinates[0,atom_index,0] = atom_record[index_att['Cartn_x']]
        coordinates[0,atom_index,1] = atom_record[index_att['Cartn_y']]
        coordinates[0,atom_index,2] = atom_record[index_att['Cartn_z']]

        occupancy[atom_index] = atom_record[index_att['occupancy']]
        alternate_location[atom_index] = atom_record[index_att['label_alt_id']]
        b_factor[0,atom_index] = atom_record[index_att['B_iso_or_equiv']]

        atom_num_model[atom_index] = atom_record[index_att['pdbx_PDB_model_num']]

        aux_group_id = atom_record[index_att['auth_seq_id']]
        aux_group_name = atom_record[index_att['auth_comp_id']]
        aux_chain_id = atom_record[index_att['label_asym_id']]
        aux_chain_name = atom_record[index_att['auth_asym_id']]
        aux_entity_id = atom_record[index_att['label_entity_id']]

        if atom_record[index_att['pdbx_PDB_ins_code']] not in ['?','.']:
            aux_group_id = str(aux_group_id)+atom_record[index_att['pdbx_PDB_ins_code']]
            with_insertions = True

        if aux_entity_id not in entity_id_to_entity_index:

            entity_index+=1
            entity_id.append(aux_entity_id)
            entity_id_to_entity_index[aux_entity_id]=entity_index

        else:

            entity_index = entity_id_to_entity_index[aux_entity_id]

        if aux_chain_id not in chain_id_to_chain_index:

            chain_index+=1
            chain_name.append(aux_chain_name)
            chain_id.append(aux_chain_id)
            chain_id_to_chain_index[aux_chain_id]=chain_index
            chain_index_to_entity_index.append(entity_index)
            chain_index_to_group_indices[chain_index]=[]

        else:

            chain_index = chain_id_to_chain_index[aux_chain_id]

        if former_group_id!=aux_group_id or former_chain_id!=aux_chain_id:

            group_index+=1
            group_name.append(aux_group_name)
            group_id.append(aux_group_id)
            chain_index_to_group_indices[chain_index].append(group_index)
            group_index_to_atom_indices[group_index]=[]
            former_group_id=aux_group_id
            former_chain_id=aux_chain_id

        group_index_from_atom[atom_index] = group_index
        chain_index_from_atom[atom_index] = chain_index
        entity_index_from_atom[atom_index] = entity_index
        group_index_to_atom_indices[group_index].append(atom_index)

    group_name = np.array(group_name, dtype='object')
    if with_insertions:
        group_id= np.array(group_id, dtype='object')
    else:
        group_id= np.array(group_id, dtype=int)
    chain_name = np.array(chain_name, dtype='object')
    chain_id = np.array(chain_id, dtype='object')
    entity_id = np.array(entity_id, dtype=int)

    # entities

    ## entity_poly

    aux_entity_polymer_type = {}

    if item.exists('entity_poly'):

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity_poly').getAttributeList())}

        for record in item.getObj('entity_poly').data:

            entity_id_value = record[index_att['entity_id']]
            entity_index = entity_id_to_entity_index[entity_id_value]

            aux_dict = {}
            aux_dict['poly_type']=record[index_att['type']]
            aux_dict['amino_acids_1']=record[index_att['pdbx_seq_one_letter_code']]
            aux_dict['chain_name']=record[index_att['pdbx_strand_id']].split(',')
            aux_dict['seq']=[]
            aux_entity_polymer_type[entity_index]=aux_dict

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity_poly_seq').getAttributeList())}

        for record in item.getObj('entity_poly_seq').data:

            entity_id_value = record[index_att['entity_id']]
            entity_index = entity_id_to_entity_index[entity_id_value]

            aux_entity_polymer_type[entity_index]['seq'].append([record[index_att['num']], record[index_att['mon_id']]])

    ## entity_non_poly and entity_branched

    aux_entity_non_polymer_type = {}
    aux_entity_branched_type = {}
    aux_chem_comp_dict = {}

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('chem_comp').getAttributeList())}

    for record in item.getObj('chem_comp').data:
        comp_id = record[index_att['id']]
        aux_chem_comp_dict[comp_id] = record[index_att['type']]

    ### entity_non_poly

    if item.exists('pdbx_entity_nonpoly'):

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('pdbx_entity_nonpoly').getAttributeList())}

        for record in item.getObj('pdbx_entity_nonpoly').data:

            entity_id_value = record[index_att['entity_id']]
            entity_index = entity_id_to_entity_index[entity_id_value]

            aux_dict = {}
            comp_id = record[index_att['comp_id']]
            aux_dict['comp_id'] = comp_id
            aux_dict['comp_type'] = aux_chem_comp_dict[comp_id]
            aux_entity_non_polymer_type[entity_index]=aux_dict

    ### entity_branched

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity').getAttributeList())}

    for entity_index, record in enumerate(item.getObj('entity').data):

        if record[index_att['type']]=='branched':

            aux_dict = {}
            num_of_molecules = record[index_att['pdbx_number_of_molecules']]
            aux_group_indices = chain_index_to_group_indices[entity_index]
            num_of_groups = len(aux_group_indices)
            num_of_groups_per_molecule = num_of_groups//num_of_molecules
            aux_dict['group_indices_per_molecule'] = [aux_group_indices[ii:ii+num_of_groups_per_molecule] for ii
                                                      in range(0, num_of_groups, num_of_groups_per_molecule)]
            aux_dict['seq'] = list(group_name[chain_index_to_group_indices[entity_index]])
            aux_dict['comp_types'] = [aux_chem_comp_dict[ii] for ii in aux_dict['seq']]
            aux_entity_branched_type[entity_index]=aux_dict

    del aux_chem_comp_dict

    ## entities

    entity_name = []
    entity_type = []

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity').getAttributeList())}

    for entity_index, record in enumerate(item.getObj('entity').data):

        aux_entity_name = record[index_att['pdbx_description']]

        match record[index_att['type']]:
            case 'polymer':
                match aux_entity_polymer_type[entity_index]['poly_type']:
                    case 'polypeptide(L)':
                        if len(aux_entity_polymer_type[entity_index]['seq'])>=min_length_protein:
                            aux_entity_type='protein'
                        else:
                            aux_entity_type='peptide'
                    case 'polysaccharide':
                        aux_entity_type='polysaccharide'
                    case 'polydeoxyribonucleotide':
                        aux_entity_type='DNA'
                    case 'polyribonucleotide':
                        aux_entity_type='RNA'
                    case _:
                        aux_entity_type='unknown'
            case 'non-polymer':
                match aux_entity_non_polymer_type[entity_index]['comp_type']:
                    case 'D-saccharide, beta linking':
                        aux_entity_type='polysaccharide'
                    case 'L-saccharide, beta linking':
                        aux_entity_type='polysaccharide'
                    case 'D-saccharide, alpha linking':
                        aux_entity_type='polysaccharide'
                    case 'L-saccharide, alpha linking':
                        aux_entity_type='polysaccharide'
                    #case 'D-peptide linking':
                    #    aux_entity_type='peptide'
                    #case 'L-peptide linking':
                    #    aux_entity_type='peptide'
                    case 'D-amino acid':
                        aux_entity_type='amino acid'
                    case 'L-amino acid':
                        aux_entity_type='amino acid'
                    case 'nucleotide':
                        aux_entity_type='nucleotide'
                    case 'nucleoside':
                        aux_entity_type='nucleotide'
                    case 'water':
                        aux_entity_type='water'
                    case 'solvent':
                        aux_entity_type='water'
                    case 'ion':
                        aux_entity_type='ion'
                    case 'ion, metal':
                        aux_entity_type='ion'
                    case 'small molecule':
                        aux_entity_type='small molecule'
                    case 'organic compound':
                        aux_entity_type='small molecule'
                    case _:
                        aux_entity_type=get_group_type_from_group_name(aux_entity_non_polymer_type[entity_index]['comp_id'])
            case 'branched':
                if all([ii in ['D-saccharide, beta linking', 'D-saccharide, alpha linking',
                               'L-saccharide, beta linking', 'L-saccharide, alpha linking']
                        for ii in aux_entity_branched_type[entity_index]['comp_types']]):
                    n_saccharides = len(aux_entity_branched_type[entity_index]['seq'])
                    if n_saccharides == 1:
                        aux_entity_type='monosaccharide'
                    elif n_saccharides == 2:
                        aux_entity_type='disaccharide'
                    elif 3<=n_saccharides<=10:
                        aux_entity_type='oligosaccharide'
                    else:
                        aux_entity_type='polysaccharide'
                else:
                    aux_entity_type='unknown'
            case 'water':
                aux_entity_type='water'
            case _:
                aux_entity_type='unknown'

        entity_name.append(aux_entity_name)
        entity_type.append(aux_entity_type)

    entity_name = np.array(entity_name, dtype='object')
    entity_type = np.array(entity_type, dtype='object')

    # molecules

    molecule_index_from_group = np.empty(len(group_name), dtype=int)
    molecule_type = []
    molecule_name = []
    entity_index_from_molecule = []

    molecule_index = -1

    for chain_index, group_indices in chain_index_to_group_indices.items():

        aux_entity_index = chain_index_to_entity_index[chain_index]
        aux_entity_type = entity_type[aux_entity_index]
        aux_entity_name = entity_name[aux_entity_index]

        if aux_entity_type in ['protein', 'peptide', 'disaccharide',
                               'oligosaccharide', 'polysaccharide', 'DNA', 'RNA']:
            molecule_index+=1
            for group_index in group_indices:
                molecule_index_from_group[group_index] = molecule_index
            molecule_type.append(aux_entity_type)
            molecule_name.append(aux_entity_name)
            entity_index_from_molecule.append(aux_entity_index)
        else:
            for group_index in group_indices:
                molecule_index+=1
                molecule_index_from_group[group_index] = molecule_index
                molecule_type.append(aux_entity_type)
                molecule_name.append(aux_entity_name)
                entity_index_from_molecule.append(aux_entity_index)

    molecule_type = np.array(molecule_type, dtype='object')
    molecule_name = np.array(molecule_name, dtype='object')
    entity_index_from_molecule = np.array(entity_index_from_molecule, dtype=int)

    # bonds

    atom_pairs_bonded = []

    ## bonds intra-group

    atoms_without_bonds=[]

    if item.exists('chem_comp_bond'):

        bonds_intra_group = {}

        for record in item.getObj('chem_comp_bond'):
            try:
                bonds_intra_group[record[0]].append([record[1], record[2]])
            except Exception:
                bonds_intra_group[record[0]]=[[record[1], record[2]]]

        for aux_group_index, aux_atom_indices in group_index_to_atom_indices.items():

            aux_atom_names = atom_name[aux_atom_indices]
            aux_group_name = group_name[aux_group_index]

            if aux_group_name in bonds_intra_group:

                if aux_group_name not in ['DOD']:
                    for ii,jj in enumerate(aux_atom_names):
                        if jj.startswith('D'):
                            aux_atom_names[ii]='H'+jj[1:]

                dict_aux = {ii:jj for ii,jj in zip(aux_atom_names, aux_atom_indices)}
                dict_mask = {ii:False for ii in aux_atom_names}

                aux_atom_pairs_bonded = []

                for at1, at2 in bonds_intra_group[aux_group_name]:
                    try:
                        aux_atom_pairs_bonded.append(sorted([dict_aux[at1],dict_aux[at2]]))
                        dict_mask[at1]=True
                        dict_mask[at2]=True
                    except Exception:
                        pass

                remains = [ii for ii,jj in dict_mask.items() if not jj]

                if len(remains):
                    if set(remains)==set(['H1','H3']):
                        for at1, at2 in [['N', 'H1'], ['N', 'H3']]:
                            aux_atom_pairs_bonded.append(sorted([dict_aux[at1],dict_aux[at2]]))
                        atom_pairs_bonded += aux_atom_pairs_bonded
                    elif len(aux_atom_indices)==1:
                        atom_pairs_bonded += []
                    else:
                        aux_atom_pairs_bonded = get_bonded_atom_pairs(aux_group_name, aux_atom_names, aux_atom_indices,
                                                                     sorted=False)
                        if aux_atom_pairs_bonded is None:
                            atoms_without_bonds += aux_atom_indices
                        else:
                            atom_pairs_bonded += aux_atom_pairs_bonded
                else:
                    atom_pairs_bonded += aux_atom_pairs_bonded

    else:

        for aux_group_index, aux_atom_indices in group_index_to_atom_indices.items():

            aux_atom_names = atom_name[aux_atom_indices].tolist()
            aux_group_name = group_name[aux_group_index]
            aux_atom_pairs_bonded = get_bonded_atom_pairs(aux_group_name, aux_atom_names, aux_atom_indices)
            if aux_atom_pairs_bonded is None:
                atoms_without_bonds += aux_atom_indices
            else:
                atom_pairs_bonded += aux_atom_pairs_bonded

    ## bonds extra-group

    ### peptidic bonds

    pair_groups_peptidic_bonds=[]

    for chain_index, group_indices in chain_index_to_group_indices.items():
        aux_entity_index = chain_index_to_entity_index[chain_index]
        aux_entity_type = entity_type[aux_entity_index]
        aux_entity_name = entity_name[aux_entity_index]
        if aux_entity_type in ['protein', 'peptide']:
            if aux_entity_polymer_type[aux_entity_index]['poly_type']=='polypeptide(L)':
                former_group_id = -10
                former_group_index = -10
                for aux_group_index in chain_index_to_group_indices[chain_index]:
                    aux_group_id = group_id[aux_group_index]
                    if not with_insertions:
                        if former_group_id+1 == aux_group_id:
                            pair_groups_peptidic_bonds.append([former_group_index, aux_group_index])
                    else:
                        if isinstance(former_group_id, int) and isinstance(aux_group_id, int):
                            if former_group_id+1 == aux_group_id:
                                pair_groups_peptidic_bonds.append([former_group_index, aux_group_index])
                        elif isinstance(former_group_id, int) and isinstance(aux_group_id, str):
                            if str(former_group_id)+'A' == aux_group_id:
                                pair_groups_peptidic_bonds.append([former_group_index, aux_group_index])
                        elif isinstance(former_group_id, str) and isinstance(aux_group_id, str):
                            if former_group_id[:-1]==aux_group_id[:-1] and \
                               ord(aux_group_id[-1])-ord(former_group_id[-1])==1:
                                pair_groups_peptidic_bonds.append([former_group_index, aux_group_index])
                        elif isinstance(former_group_id, str) and isinstance(aux_group_id, int):
                            if int(former_group_id[:-1])+1==aux_group_id:
                                pair_groups_peptidic_bonds.append([former_group_index, aux_group_index])
                    former_group_id=aux_group_id
                    former_group_index=aux_group_index

    for group_index_1, group_index_2 in pair_groups_peptidic_bonds:

        atom_indices_1 = group_index_to_atom_indices[group_index_1]
        C_index = np.argwhere(atom_name[atom_indices_1]=='C')
        atom_indices_2 = group_index_to_atom_indices[group_index_2]
        N_index = np.argwhere(atom_name[atom_indices_2]=='N')
        if len(C_index) and len(N_index):
            atom_pairs_bonded.append([atom_indices_1[C_index[0,0]], atom_indices_2[N_index[0,0]]])

    ### bonds in struct_conn

    atom_pairs_bonded_by_struct_conn = []

    if item.exists('struct_conn'):

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('struct_conn').getAttributeList())}

        for record in item.getObj('struct_conn').data:

            if record[index_att['conn_type_id']]=='covale':

                chain_id_1 = record[index_att['ptnr1_label_asym_id']]
                group_id_1 = record[index_att['ptnr1_auth_seq_id']]
                atom_name_1 = record[index_att['ptnr1_label_atom_id']]
                chain_id_2 = record[index_att['ptnr2_label_asym_id']]
                group_id_2 = record[index_att['ptnr2_auth_seq_id']]
                atom_name_2 = record[index_att['ptnr2_label_atom_id']]

                chain_index_1 = chain_id_to_chain_index[chain_id_1]
                group_indices_1 = chain_index_to_group_indices[chain_index_1]
                group_index_1 = [ii for ii in group_indices_1 if group_id[ii]==group_id_1]
                group_index_1 = group_index_1[0]
                atom_indices_1 = group_index_to_atom_indices[group_index_1]
                atom_index_1 = [ii for ii in atom_indices_1 if atom_name[ii]==atom_name_1]
                atom_index_1 = atom_index_1[0]

                chain_index_2 = chain_id_to_chain_index[chain_id_2]
                group_indices_2 = chain_index_to_group_indices[chain_index_2]
                group_index_2 = [ii for ii in group_indices_2 if group_id[ii]==group_id_2]
                group_index_2 = group_index_2[0]
                atom_indices_2 = group_index_to_atom_indices[group_index_2]
                atom_index_2 = [ii for ii in atom_indices_2 if atom_name[ii]==atom_name_2]
                atom_index_2 = atom_index_2[0]

                if [atom_index_1, atom_index_2] not in atom_pairs_bonded and \
                   [atom_index_2, atom_index_1] not in atom_pairs_bonded:

                    atom_pairs_bonded_by_struct_conn.append(sorted([atom_index_1, atom_index_2]))

    atom_pairs_bonded += atom_pairs_bonded_by_struct_conn

    ### bonds

    atom_pairs_bonded = np.array(sorted(atom_pairs_bonded))
    bond_atom1_index = atom_pairs_bonded[:,0]
    bond_atom2_index = atom_pairs_bonded[:,1]
    del(atom_pairs_bonded)

    # alternate locations

    alt_atom_indices = np.where(alternate_location!='.')[0]
    aux_alternate_location = None

    if len(alt_atom_indices):

        alt_atom_names = atom_name[alt_atom_indices]
        alt_group_indices = group_index_from_atom[alt_atom_indices]
        alt_chain_indices = chain_index_from_atom[alt_atom_indices]
        alt_group_ids = group_id[alt_group_indices]
        alt_chain_ids = chain_id[alt_chain_indices]

        aux_dict = {}
        for aux_atom_index, aux_atom_name, aux_group_id, aux_chain_id in zip(alt_atom_indices, alt_atom_names,
                                                                             alt_group_ids, alt_chain_ids):
            aux_key = tuple([aux_atom_name, aux_group_id, aux_chain_id])
            if aux_key in aux_dict:
                aux_dict[aux_key].append(aux_atom_index)
            else:
                aux_dict[aux_key]=[aux_atom_index]
        atoms_to_be_removed_with_alt_loc=[]
        chosen_with_alt_loc = []
        to_be_fixed_in_bonds = {}
        for same_atoms in aux_dict.values():
            alt_occupancy = occupancy[same_atoms]
            alt_loc = alternate_location[same_atoms]
            if np.allclose(alt_occupancy, alt_occupancy[0]):
                if len(alt_loc)>1:
                    chosen = same_atoms[np.where(alt_loc=='A')[0][0]]
                else:
                    chosen = same_atoms[0]
            else:
                chosen = same_atoms[np.argmax(alt_occupancy)]
            chosen_with_alt_loc.append(chosen)
            atoms_to_be_removed_with_alt_loc += [ii for ii in same_atoms if ii !=chosen]
            to_be_fixed_in_bonds[max(same_atoms)]=chosen

        atom_indices_to_be_kept = np.setdiff1d(np.arange(n_atoms), atoms_to_be_removed_with_alt_loc)
        dict_old_to_new_atom_indices = {jj: ii for ii, jj in enumerate(atom_indices_to_be_kept)}

        if len(atoms_without_bonds):
            atoms_without_bonds = np.setdiff1d(atoms_without_bonds, atoms_to_be_removed_with_alt_loc)
            atoms_without_bonds = [dict_old_to_new_atom_indices[ii] for ii in atoms_without_bonds]

        aux_alternate_location = [{}]
        for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
            atom_index = dict_old_to_new_atom_indices[chosen]
            aux_coordinates = puw.quantity(coordinates[0,same_atoms,:], unit='angstroms', standardized=True)
            aux_b_factor = puw.quantity(b_factor[0,same_atoms], unit='angstroms**2', standardized=True)
            aux_dict={
                    'location_id':alternate_location[same_atoms],
                    'occupancy':occupancy[same_atoms],
                    'b_factor':aux_b_factor,
                    'atom_id':atom_id[same_atoms],
                    'coordinates':aux_coordinates
                    }
            aux_alternate_location[0][atom_index]=aux_dict

        atom_name = atom_name[atom_indices_to_be_kept]
        atom_id = atom_id[atom_indices_to_be_kept]
        atom_type = atom_type[atom_indices_to_be_kept]
        group_index_from_atom = group_index_from_atom[atom_indices_to_be_kept]
        chain_index_from_atom = chain_index_from_atom[atom_indices_to_be_kept]

        for old_atom, new_atom in to_be_fixed_in_bonds.items():
            bond_atom1_index[bond_atom1_index==old_atom]=new_atom
            bond_atom2_index[bond_atom2_index==old_atom]=new_atom

        mask1 = np.isin(bond_atom1_index, atom_indices_to_be_kept)
        mask2 = np.isin(bond_atom2_index, atom_indices_to_be_kept)
        mask = mask1*mask2

        vaux_dict = np.vectorize(dict_old_to_new_atom_indices.__getitem__)
        bond_atom1_index = bond_atom1_index[mask]
        bond_atom1_index = vaux_dict(bond_atom1_index)
        bond_atom2_index = bond_atom2_index[mask]
        bond_atom2_index = vaux_dict(bond_atom2_index)
        
        coordinates = coordinates[:,atom_indices_to_be_kept,:]
        b_factor = b_factor[:,atom_indices_to_be_kept]

        if len(atom_pairs_bonded_by_struct_conn):
            aux_list = []
            for ii,jj in atom_pairs_bonded_by_struct_conn:
                aux_list.append([dict_old_to_new_atom_indices[ii], dict_old_to_new_atom_indices[jj]])
            atom_pairs_bonded_by_struct_conn = aux_list

    # coordinates, box, bioassembly, b-factor

    coordinates = puw.quantity(coordinates, 'angstroms')
    coordinates = puw.standardize(coordinates)

    check_if_cell = True
    if item.exists('exptl'):
        if 'NMR' in item.getObj('exptl').getValue('method'):
            check_if_cell = False

    if item.exists('cell') and check_if_cell:

        from molsysmt.pbc import get_box_from_lengths_and_angles

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('cell').getAttributeList())}

        cell_data = item.getObj('cell').data[0]

        cell_lengths = np.empty([1,3], dtype='float64')
        cell_angles = np.empty([1,3], dtype='float64')

        cell_lengths[0,0]= cell_data[index_att['length_a']]
        cell_lengths[0,1]= cell_data[index_att['length_b']]
        cell_lengths[0,2]= cell_data[index_att['length_c']]

        cell_angles[0,0]= cell_data[index_att['angle_alpha']]
        cell_angles[0,1]= cell_data[index_att['angle_beta']]
        cell_angles[0,2]= cell_data[index_att['angle_gamma']]

        cell_lengths = puw.quantity(cell_lengths, 'angstroms')
        cell_angles = puw.quantity(cell_angles, 'degrees')

        box = get_box_from_lengths_and_angles(cell_lengths, cell_angles, skip_digestion=True)
        box = puw.standardize(box)

    else:

        box = None


    bioassembly = {}

    if item.exists('pdbx_struct_oper_list') and item.exists('pdbx_struct_assembly_gen'):

        operators = {}

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('pdbx_struct_oper_list').getAttributeList())}
        for record in item.getObj('pdbx_struct_oper_list'):
            matrix = np.zeros([3,3], dtype=float)
            vector = np.zeros([3], dtype=float)
            matrix[0,0] = record[index_att['matrix[1][1]']]
            matrix[0,1] = record[index_att['matrix[1][2]']]
            matrix[0,2] = record[index_att['matrix[1][3]']]
            matrix[1,0] = record[index_att['matrix[2][1]']]
            matrix[1,1] = record[index_att['matrix[2][2]']]
            matrix[1,2] = record[index_att['matrix[2][3]']]
            matrix[2,0] = record[index_att['matrix[3][1]']]
            matrix[2,1] = record[index_att['matrix[3][2]']]
            matrix[2,2] = record[index_att['matrix[3][3]']]
            vector[0] = record[index_att['vector[1]']]
            vector[1] = record[index_att['vector[2]']]
            vector[2] = record[index_att['vector[3]']]
            vector = puw.quantity(vector, unit='angstroms', standardized=True)
            operators[str(record[index_att['id']])]={'matrix':matrix, 'vector':vector}

        index_att = {jj:ii for ii,jj in enumerate(item.getObj('pdbx_struct_assembly_gen').getAttributeList())}
        old_chain_id_to_chain_index = {jj:ii for ii,jj in enumerate(chain_id)}
        for record in item.getObj('pdbx_struct_assembly_gen'):
            aux = {'chain_indices': [], 'rotations': [], 'translations': []}
            old_chain_ids = record[index_att['asym_id_list']].split(',')
            aux['chain_indices']=[old_chain_id_to_chain_index[ii] for ii in old_chain_ids]
            operation_expression = record[index_att['oper_expression']]
            if isinstance(operation_expression, int):
                operation_expression = str(operation_expression)
            oper = []
            oper2 = []
            parenCount = operation_expression.count("(")
            if parenCount == 0 :
                if ',' in operation_expression:
                    oper.extend(operation_expression.split(','))
                else:
                    oper.append(operation_expression)
            if parenCount == 1 :
                oper.extend(_parse_operation_expression(operation_expression))
            if parenCount == 2 :
                temp = operation_expression.find(")")
                oper.extend(_parse_operation_expression(operation_expression[0:temp+1]))
                oper2.extend(_parse_operation_expression(operation_expression[temp+1:]))
            if len(oper2)==0:
                for ii in oper:
                    aux['rotations'].append(operators[str(ii)]['matrix'])
                    aux['translations'].append(operators[str(ii)]['vector'])
            else:
                for ii in oper:
                    for jj in oper2:
                        aux_trans, aux_rot = _compose_operation(operators[str(ii)]['vector'], operators[str(ii)]['matrix'],
                                                                operators[str(jj)]['vector'], operators[str(jj)]['matrix'])
                        aux['rotations'].append(aux_rot)
                        aux['translations'].append(aux_trans)

            bioassembly[str(record[index_att['assembly_id']])]=aux

    b_factor = puw.quantity(np.array(b_factor), unit='angstroms**2', standardized=True)

    n_atoms = atom_name.shape[0]
    n_groups = group_name.shape[0]
    n_molecules = molecule_name.shape[0]
    n_entities = entity_name.shape[0]
    n_chains = chain_name.shape[0]

    tmp_item = MolSys(n_atoms=n_atoms, n_groups=n_groups, n_molecules=n_molecules, n_chains=n_chains,
                      n_entities=n_entities)

    tmp_item.topology.atoms["atom_name"] = atom_name
    tmp_item.topology.atoms["atom_id"] = atom_id
    tmp_item.topology.atoms["atom_type"] = atom_type
    tmp_item.topology.atoms["group_index"] = group_index_from_atom
    tmp_item.topology.atoms["chain_index"] = chain_index_from_atom

    tmp_item.topology.groups["group_name"] = group_name
    tmp_item.topology.groups["group_id"] = group_id
    tmp_item.topology.groups["molecule_index"] = molecule_index_from_group

    tmp_item.topology.molecules["molecule_name"] = molecule_name
    tmp_item.topology.molecules["molecule_id"] = np.arange(n_molecules, dtype=int)
    tmp_item.topology.molecules["molecule_type"] = molecule_type
    tmp_item.topology.molecules["entity_index"] = entity_index_from_molecule

    tmp_item.topology.chains["chain_name"] = chain_name
    tmp_item.topology.chains["chain_id"] = chain_id

    tmp_item.topology.entities["entity_name"] = entity_name
    tmp_item.topology.entities["entity_id"] = entity_id
    tmp_item.topology.entities["entity_type"] = entity_type

    tmp_item.structures.append(coordinates=coordinates, box=box, alternate_location=aux_alternate_location,
                              b_factor=b_factor, skip_digestion=True)

    tmp_item.structures.bioassembly=bioassembly

    # Rebuild groups

    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)

    # Build bonds

    if len(atoms_without_bonds):
         
        missing_bonds = get_missing_bonds(tmp_item, selection=atoms_without_bonds, skip_digestion=False)

        if len(missing_bonds):
            missing_bonds = np.array(missing_bonds)
            bond_atom1_index = np.concatenate([bond_atom1_index, missing_bonds[:,0]])
            bond_atom2_index = np.concatenate([bond_atom2_index, missing_bonds[:,1]])

    n_bonds = bond_atom1_index.shape[0]

    tmp_item.topology.bonds._reset(n_bonds=n_bonds)
    tmp_item.topology.bonds["atom1_index"] = bond_atom1_index
    tmp_item.topology.bonds["atom2_index"] = bond_atom2_index
    tmp_item.topology.bonds._remove_empty_columns()
    tmp_item.topology.bonds._sort_bonds()

    # Rebuild components

    tmp_item.topology.rebuild_components(redefine_indices=True, redefine_ids=True,
                                         redefine_names=True, redefine_types=True)

    # Rebuild chains

    tmp_item.topology.rebuild_chains(redefine_indices=False, redefine_ids=False,
                                     redefine_types=True, redefine_names=False)

    # Models

    models = np.unique(atom_num_model)
    n_models = models.shape[0]

    if n_models>1:

        item_per_model = []
        for model_index in models:
            aux_atom_indices = np.where(atom_num_model==model_index)[0].tolist()
            item_per_model.append(tmp_item.extract(atom_indices=aux_atom_indices, skip_digestion=True))

        comparison=[]
        for ii in range(1, n_models):
            aux = item_per_model[0].topology.compare(item_per_model[ii].topology,
                                                     atom_id=False, atom_name=True, atom_type=True,
                                                     group_index=True, group_id=True, group_name=True,
                                                     component_index=True, component_name=True,
                                                     molecule_index=True, molecule_name=True,
                                                     skip_digestion=True)
            comparison.append(aux)

        if all(comparison): 

            for ii in range(1, n_models):
                item_per_model[0].structures.append_structures(item_per_model[ii].structures)


            tmp_item = item_per_model[0]


        else:

            warn(MolecularSystemMismatchWarning(caller="molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys", n_models=n_models))

            tmp_item = item_per_model

            return tmp_item

    del(atom_num_model)

    # Clean up

    del(atom_name, atom_id, atom_type, group_index_from_atom, chain_index_from_atom)
    del(group_name, group_id)
    del(molecule_name, molecule_type, entity_index)
    del(chain_name, chain_id)
    del(entity_name, entity_id, entity_type)
    del(bond_atom1_index, bond_atom2_index)

    # Warnings on struct conn new covalent bonds
    if len(atom_pairs_bonded_by_struct_conn):
        warn(CrossChainCovalentBondsWarning(tmp_item, atom_pairs_bonded_by_struct_conn, caller="molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys"))

    # Extract

    tmp_item.topology._components_dirty = False
    tmp_item.topology._molecules_dirty = False
    tmp_item.topology._entities_dirty = False

    tmp_item = tmp_item.extract(atom_indices=atom_indices, structure_indices=structure_indices,
                                copy_if_all=False, skip_digestion=True)

    return tmp_item

def _parse_operation_expression(expression) :
    operations = []
    stops = [ "," , "-" , ")" ]

    currentOp = ""
    i = 1
	
    # Iterate over the operation expression
    while i in range(1, len(expression) - 1):
        pos = i

        # Read an operation
        while expression[pos] not in stops and pos < len(expression) - 1 : 
            pos += 1    
        currentOp = expression[i : pos]

        # Handle single operations
        if expression[pos] != "-" :
            operations.append(currentOp)
            i = pos

        # Handle ranges
        if expression[pos] == "-" :
            pos += 1
            i = pos
			
            # Read in the range's end value
            while expression[pos] not in stops :
                pos += 1
            end = int(expression[i : pos])
			
            # Add all the operations in [currentOp, end]
            for val in range((int(currentOp)), end + 1) :
                operations.append(str(val))
            i = pos
        i += 1
    return operations

def _compose_operation(trans1, rot1, trans2, rot2) :

    trans1_value, trans1_unit = puw.get_value_and_unit(trans1)
    trans2_value, trans2_unit = puw.get_value_and_unit(trans2)

    op1 = np.zeros([4,4], dtype=float)
    op1[3,3] = 1.0
    op1[:3,:3] = rot1
    op1[:3,3] = trans1_value

    op2 = np.zeros([4,4], dtype=float)
    op2[3,3] = 1.0
    op2[:3,:3] = rot2
    op2[:3,3] = trans2_value

    composed = np.dot(op1,op2)

    output_trans = puw.quantity(composed[:3,3], trans1_unit)
    output_rot = composed[:3,:3]

    return output_trans, output_rot
