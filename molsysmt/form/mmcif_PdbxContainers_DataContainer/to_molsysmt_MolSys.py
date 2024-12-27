from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd

# https://github.com/rcsb/mmtf/blob/master/spec.md

@digest(form='mmcif.PdbxContainers.DataContainer')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from molsysmt.element.group import get_bonded_atom_pairs
    from molsysmt.build import get_missing_bonds

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('atom_site').getAttributeList())}

    n_atoms = len(item.getObj('atom_site').data)

    atom_name_array = np.empty(n_atoms, dtype=object)
    atom_id_array = np.empty(n_atoms, dtype=int)
    atom_type_array = np.empty(n_atoms, dtype=object)
    atom_group_index_array = np.empty(n_atoms, dtype=int)
    atom_chain_index_array = np.empty(n_atoms, dtype=int)
    atom_num_model_array = np.empty(n_atoms, dtype=int)

    coordinates_array = np.empty([1,n_atoms,3],dtype=float)
    occupancy_array = np.empty(n_atoms,dtype=float)
    alternate_location_array = np.empty(n_atoms,dtype=object)
    b_factor_array = np.empty(n_atoms,dtype=float)

    atom_pairs_bonded = []

    group_name_array = []
    group_id_array = []
    group_entity_id_array = []
    group_chain_id_array = []

    chain_name_array = []
    chain_id_array = []

    chain_id_to_group_indices = {}
    group_index_to_atom_indices = {}

    former_group_id = None
    group_index = -1
    former_chain_id = None
    chain_index = -1

    for atom_index, atom_record in enumerate(item.getObj('atom_site').data):

        atom_id_array[atom_index] = atom_record[index_att['id']]
        atom_type_array[atom_index] = atom_record[index_att['type_symbol']].upper()
        atom_name_array[atom_index] = atom_record[index_att['auth_atom_id']]

        coordinates_array[0,atom_index,0] = atom_record[index_att['Cartn_x']]
        coordinates_array[0,atom_index,1] = atom_record[index_att['Cartn_y']]
        coordinates_array[0,atom_index,2] = atom_record[index_att['Cartn_z']]

        occupancy_array[atom_index] = atom_record[index_att['occupancy']]
        alternate_location_array[atom_index] = atom_record[index_att['label_alt_id']]
        b_factor_array[atom_index] = atom_record[index_att['B_iso_or_equiv']]

        atom_num_model_array[atom_index] = atom_record[index_att['pdbx_PDB_model_num']]

        group_id = atom_record[index_att['auth_seq_id']]
        group_name = atom_record[index_att['auth_comp_id']]
        chain_id = atom_record[index_att['label_asym_id']]
        chain_name = atom_record[index_att['auth_asym_id']]
        entity_id = atom_record[index_att['label_entity_id']]

        if former_chain_id!=chain_id:
            chain_index+=1
            chain_name_array.append(chain_name)
            chain_id_array.append(chain_id)
            chain_id_to_group_indices[chain_id]=[]
            former_chain_id=chain_id

        if former_group_id!=group_id:
            group_index+=1
            group_name_array.append(group_name)
            group_id_array.append(group_id)
            group_entity_id_array.append(entity_id)
            group_chain_id_array.append(chain_id)
            chain_id_to_group_indices[chain_id].append(group_index)
            group_index_to_atom_indices[group_index]=[]
            former_group_id=group_id

        atom_group_index_array[atom_index] = group_index
        atom_chain_index_array[atom_index] = chain_index
        group_index_to_atom_indices[group_index].append(atom_index)

    group_name_array = np.array(group_name_array, dtype='object')
    group_id_array = np.array(group_id_array, dtype=int)
    chain_name_array = np.array(chain_name_array, dtype='object')
    chain_id_array = np.array(chain_id_array, dtype='object')

    # bonds intra-group

    atoms_without_bonds=[]

    if item.exists('chem_comp_bond'):

        bonds_intra_group = {}

        for record in item.getObj('chem_comp_bond'):
            try:
                bonds_intra_group[record[0]].append([record[1], record[2]])
            except:
                bonds_intra_group[record[0]]=[[record[1], record[2]]]

        for group_index, aux_atom_indices in group_index_to_atom_indices.items():

            atom_names = atom_name_array[aux_atom_indices]
            group_name = group_name_array[group_index]

            if group_name in bonds_intra_group:

                dict_aux = {ii:jj for ii,jj in zip(atom_names,aux_atom_indices)}
                dict_mask = {ii:False for ii in atom_names}

                aux_atom_pairs_bonded = []

                for at1, at2 in bonds_intra_group[group_name]:
                    try:
                        aux_atom_pairs_bonded.append(sorted([dict_aux[at1],dict_aux[at2]]))
                        dict_mask[at1]=True
                        dict_mask[at2]=True
                    except:
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
                        aux_atom_pairs_bonded = get_bonded_atom_pairs(group_name, atom_names, aux_atom_indices)
                        if aux_atom_pairs_bonded is None:
                            atoms_without_bonds += aux_atom_indices
                        else:
                            atom_pairs_bonded += aux_atom_pairs_bonded
                else:
                    atom_pairs_bonded += aux_atom_pairs_bonded

    else:

        aux_series = pd.Series(atom_group_index_array)
        group_index_to_atom_indices = {key: list(group.index) for key, group in aux_series.groupby(aux_series)}

        for group_index, aux_atom_indices in group_index_to_atom_indices.items():

            atom_names = atom_name_array[aux_atom_indices].tolist()
            group_name = group_name_array[group_index]
            aux_atom_pairs_bonded = get_bonded_atom_pairs(group_name, atom_names, aux_atom_indices)
            if aux_atom_pairs_bonded is None:
                atoms_without_bonds += aux_atom_indices
            else:
                atom_pairs_bonded += aux_atom_pairs_bonded

    # entities

    entity_id_array = []
    entity_name_array = []
    entity_type_array = []

    entity_dict = {}

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity').getAttributeList())}

    for entity_index, record in enumerate(item.getObj('entity').data):

        entity_id = record[index_att['id']]
        entity_name = record[index_att['pdbx_description']]
        entity_type = record[index_att['type']]

        entity_id_array.append(entity_id)
        entity_name_array.append(entity_name)
        entity_type_array.append(entity_type)

        aux_dict = {}
        aux_dict['entity_index'] = entity_index
        aux_dict['entity_id'] = entity_id
        aux_dict['entity_name'] = entity_name
        aux_dict['entity_type'] = entity_type
        entity_dict[entity_id]=aux_dict

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity_poly').getAttributeList())}

    for record in item.getObj('entity_poly').data:

        entity_id = record[index_att['entity_id']]

        aux_dict = {}
        entity_dict[entity_id]['poly_type']=record[index_att['type']]
        entity_dict[entity_id]['amino_acids_1']=record[index_att['pdbx_seq_one_letter_code']]
        entity_dict[entity_id]['chain_id']=record[index_att['pdbx_strand_id']].split(',')
        entity_dict[entity_id]['seq']=[]

    index_att = {jj:ii for ii,jj in enumerate(item.getObj('entity_poly_seq').getAttributeList())}

    for record in item.getObj('entity_poly_seq').data:

        entity_dict[record[index_att['entity_id']]]['seq'].append([record[index_att['num']],record[index_att['mon_id']]])

    entity_id_array = np.array(entity_id_array, dtype=int)
    entity_name_array = np.array(entity_name_array, dtype=object)
    entity_type_array = np.array(entity_type_array, dtype=object)
    
    # bonds extra-group
    pair_groups_peptidic_bonds=[]
    for entity_id, aux_dict in entity_dict.items():
        if aux_dict['entity_type']=='polymer':
            if aux_dict['poly_type']=='polypeptide(L)':
                for chain_id in aux_dict['chain_id']:
                    former_group_id = -10
                    former_group_index = -10
                    for group_index in chain_id_to_group_indices[chain_id]:
                        group_id = group_id_array[group_index]
                        if former_group_id+1 == group_id:
                            pair_groups_peptidic_bonds.append([former_group_index, group_index])
                        former_group_id=group_id
                        former_group_index=group_index

    for group_index_1, group_index_2 in pair_groups_peptidic_bonds:

        atom_indices_1 = group_index_to_atom_indices[group_index_1]
        C_index = np.argwhere(atom_name_array[atom_indices_1]=='C')
        atom_indices_2 = group_index_to_atom_indices[group_index_2]
        N_index = np.argwhere(atom_name_array[atom_indices_2]=='N')
        if len(C_index) and len(N_index):
            atom_pairs_bonded.append([atom_indices_1[C_index[0,0]], atom_indices_2[N_index[0,0]]])

    atom_pairs_bonded = np.array(sorted(atom_pairs_bonded))
    bond_atom1_index_array = atom_pairs_bonded[:,0]
    bond_atom2_index_array = atom_pairs_bonded[:,1]
    del(atom_pairs_bonded)

    # alternate locations

    alt_atom_indices = np.where(alternate_location_array!='.')[0]
    alternate_location = None

    if len(alt_atom_indices):

        alt_atom_names = atom_name_array[alt_atom_indices]
        alt_group_indices = atom_group_index_array[alt_atom_indices]
        alt_chain_indices = atom_chain_index_array[alt_atom_indices]
        alt_group_ids = group_id_array[alt_group_indices]
        alt_chain_ids = chain_id_array[alt_chain_indices]

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
            alt_occupancy = occupancy_array[same_atoms]
            alt_loc = alternate_location_array[same_atoms]
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

        alternate_location = [{}]
        for chosen, same_atoms in zip(chosen_with_alt_loc, aux_dict.values()):
            atom_index = dict_old_to_new_atom_indices[chosen]
            aux_coordinates = puw.quantity(coordinates_array[0,same_atoms,:], unit='angstroms', standardized=True)
            aux_b_factor = puw.quantity(b_factor_array[same_atoms], unit='angstroms**2', standardized=True)
            aux_dict={
                    'location_id':alternate_location_array[same_atoms],
                    'occupancy':occupancy_array[same_atoms],
                    'b_factor':aux_b_factor,
                    'atom_id':atom_id_array[same_atoms],
                    'coordinates':aux_coordinates
                    }
            alternate_location[0][atom_index]=aux_dict

        atom_name_array = atom_name_array[atom_indices_to_be_kept]
        atom_id_array = atom_id_array[atom_indices_to_be_kept]
        atom_type_array = atom_type_array[atom_indices_to_be_kept]
        atom_group_index_array = atom_group_index_array[atom_indices_to_be_kept]
        atom_chain_index_array = atom_chain_index_array[atom_indices_to_be_kept]

        for old_atom, new_atom in to_be_fixed_in_bonds.items():
            bond_atom1_index_array[bond_atom1_index_array==old_atom]=new_atom
            bond_atom2_index_array[bond_atom2_index_array==old_atom]=new_atom

        mask1 = np.isin(bond_atom1_index_array, atom_indices_to_be_kept)
        mask2 = np.isin(bond_atom2_index_array, atom_indices_to_be_kept)
        mask = mask1*mask2

        vaux_dict = np.vectorize(dict_old_to_new_atom_indices.__getitem__)
        bond_atom1_index_array = bond_atom1_index_array[mask]
        bond_atom1_index_array = vaux_dict(bond_atom1_index_array)
        bond_atom2_index_array = bond_atom2_index_array[mask]
        bond_atom2_index_array = vaux_dict(bond_atom2_index_array)
        
        coordinates_array = coordinates_array[:,atom_indices_to_be_kept,:]
        b_factor_array = b_factor_array[atom_indices_to_be_kept]


    # coordinates, box, bioassembly, b-factor

    coordinates_array = puw.quantity(coordinates_array, 'angstroms')
    coordinates_array = puw.standardize(coordinates_array)

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
        old_chain_id_to_chain_index = {jj:ii for ii,jj in enumerate(chain_id_array)}
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

    b_factor_array = puw.quantity(np.array(b_factor_array), unit='angstroms**2', standardized=True)

    n_atoms = atom_name_array.shape[0]
    n_groups = group_name_array.shape[0]
    n_chains = chain_name_array.shape[0]
    n_entities = entity_name_array.shape[0]

    tmp_item = MolSys(n_atoms=n_atoms, n_groups=n_groups, n_chains=n_chains, n_entities=n_entities)

    tmp_item.topology.atoms["atom_name"] = atom_name_array
    tmp_item.topology.atoms["atom_id"] = atom_id_array
    tmp_item.topology.atoms["atom_type"] = atom_type_array
    tmp_item.topology.atoms["group_index"] = atom_group_index_array
    tmp_item.topology.atoms["chain_index"] = atom_chain_index_array

    tmp_item.topology.groups["group_name"] = group_name_array
    tmp_item.topology.groups["group_id"] = group_id_array

    tmp_item.topology.chains["chain_name"] = chain_name_array
    tmp_item.topology.chains["chain_id"] = chain_id_array

    tmp_item.topology.entities["entity_name"] = entity_name_array
    tmp_item.topology.entities["entity_id"] = entity_id_array
    tmp_item.topology.entities["entity_type"] = entity_type_array

    tmp_item.topology.rebuild_groups(redefine_ids=False, redefine_types=True)

    tmp_item.structures.append(coordinates=coordinates_array, box=box, alternate_location=alternate_location,
                              b_factor=b_factor_array)

    tmp_item.structures.bioassembly=bioassembly

    if len(atoms_without_bonds):
         
        missing_bonds = get_missing_bonds(tmp_item, selection=atoms_without_bonds, with_templates=False,
                                          skip_digestion=False)

        if len(missing_bonds):
            missing_bonds_array = np.array(missing_bonds)
            bond_atom1_index_array = np.concatenate([bond_atom1_index_array, missing_bonds_array[:,0]])
            bond_atom2_index_array = np.concatenate([bond_atom2_index_array, missing_bonds_array[:,1]])

    n_bonds = bond_atom1_index_array.shape[0]

    tmp_item.topology.bonds._reset(n_bonds=n_bonds)
    tmp_item.topology.bonds["atom1_index"] = bond_atom1_index_array
    tmp_item.topology.bonds["atom2_index"] = bond_atom2_index_array
    tmp_item.topology.bonds._remove_empty_columns()
    tmp_item.topology.bonds._sort_bonds()

    tmp_item.topology.rebuild_components(redefine_indices=True, redefine_ids=True,
                                         redefine_names=False, redefine_types=True)

    molecule_index = -1

    dict_components_to_groups = tmp_item.topology.groups.groupby('component_index').groups
    dict_chain_to_components = {ii:[] for ii in range(n_chains)}

    polymers_dict_aux = {}

    molecule_name_array = []
    molecule_entity_index_array = []

    for component_index in range(tmp_item.topology.components.shape[0]):

        component_type = tmp_item.topology.components.iat[component_index,2]
        group_indices = dict_components_to_groups[component_index]
        chain_id = group_chain_id_array[group_indices[0]]
        entity_id = group_entity_id_array[group_indices[0]]
        entity_index = np.where(tmp_item.topology.entities['entity_id']==entity_id)[0][0]
        entity_type = tmp_item.topology.entities.iat[entity_index,2]
        entity_name = tmp_item.topology.entities.iat[entity_index,1]

        match component_type:

            case 'water':

                molecule_index += 1
                tmp_item.topology.components.iat[component_index,3]=molecule_index
                tmp_item.topology.components.iat[component_index,1]='water'
                molecule_name_array.append('water')
                molecule_entity_index_array.append(entity_index)

            case 'ion':

                molecule_index += 1
                tmp_item.topology.components.iat[component_index,3]=molecule_index
                tmp_item.topology.components.iat[component_index,1]=entity_name
                molecule_name_array.append(entity_name)
                molecule_entity_index_array.append(entity_index)

            case 'small molecule':

                molecule_index += 1
                tmp_item.topology.components.iat[component_index,3]=molecule_index
                tmp_item.topology.components.iat[component_index,1]=entity_name
                molecule_name_array.append(entity_name)
                molecule_entity_index_array.append(entity_index)

            case 'saccharide':

                molecule_index += 1
                tmp_item.topology.components.iat[component_index,3]=molecule_index
                tmp_item.topology.components.iat[component_index,1]=entity_name
                molecule_name_array.append(entity_name)
                molecule_entity_index_array.append(entity_index)
        
            case 'lipid':

                molecule_index += 1
                tmp_item.topology.components.iat[component_index,3]=molecule_index
                tmp_item.topology.components.iat[component_index,1]=entity_name
                molecule_name_array.append(entity_name)
                molecule_entity_index_array.append(entity_index)

            case 'peptide':

                if chain_id not in polymers_dict_aux:
                    molecule_index += 1
                    polymers_dict_aux[chain_id] = molecule_index
                    molecule_name_array.append(entity_name)
                    molecule_entity_index_array.append(entity_index)
                tmp_item.topology.components.iat[component_index,3]=polymers_dict_aux[chain_id]
                tmp_item.topology.components.iat[component_index,1]=entity_name

            case 'protein':

                if chain_id not in polymers_dict_aux:
                    molecule_index += 1
                    polymers_dict_aux[chain_id] = molecule_index
                    molecule_name_array.append(entity_name)
                    molecule_entity_index_array.append(entity_index)
                tmp_item.topology.components.iat[component_index,3]=polymers_dict_aux[chain_id]
                tmp_item.topology.components.iat[component_index,1]=entity_name

            case _:

                raise ValueError(f'Component type not recognized {component_type}')


    molecule_name_array = np.array(molecule_name_array, dtype=object)
    molecule_entity_index_array = np.array(molecule_entity_index_array, dtype=int)
    n_molecules = molecule_index+1

    tmp_item.topology.reset_molecules(n_molecules=n_molecules)
    tmp_item.topology.molecules['molecule_name']=molecule_name_array
    tmp_item.topology.molecules['entity_index']=molecule_entity_index_array
    tmp_item.topology.rebuild_molecules(redefine_indices=False, redefine_ids=True, redefine_names=False,
                                        redefine_types=True)
    tmp_item.topology.rebuild_entities(redefine_indices=False, redefine_ids=True, redefine_names=False, redefine_types=True)
    tmp_item.topology.rebuild_chains(redefine_ids=True, redefine_types=True, redefine_names=False)
    old_chain_id_to_chain_index = {jj:ii for ii,jj in enumerate(chain_id_array)}
    del(atom_name_array, atom_id_array, atom_type_array, atom_group_index_array, atom_chain_index_array)
    del(group_name_array, group_id_array)
    del(chain_name_array, chain_id_array)
    del(entity_name_array, entity_id_array, entity_type_array)
    del(bond_atom1_index_array, bond_atom2_index_array)

    models = np.unique(atom_num_model_array)
    n_models = models.shape[0]

    if n_models>1:

        item_per_model = []
        for model_index in models:
            aux_atom_indices = np.where(atom_num_model_array==model_index)[0].tolist()
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

            print('Warning! The models have different molecular systems. They will be returned separately.')

            tmp_item = item_per_model

            return tmp_item

    del(atom_num_model_array)

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

