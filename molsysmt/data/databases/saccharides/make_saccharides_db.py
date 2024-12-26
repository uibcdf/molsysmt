# wget https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

from molsysmt.native import CIFFileHandler
import pickle

handler = CIFFileHandler('../components.cif')
cif_entries = handler.parse()

types_dict = {}

for ii in cif_entries:
    jj = cif_entries[ii]['_chem_comp']['type']
    if jj in types_dict:
        types_dict[jj].append(ii)
    else:
        types_dict[jj] = [ii]

# Adding only non-polymer and other
types = ['saccharide', 'D-saccharide', '"L-saccharide, beta linking"', '"L-saccharide, alpha linking"',
        'D-SACCHARIDE', 'L-saccharide', '"D-saccharide, beta linking"', '"D-saccharide, alpha linking"',
        'L-SACCHARIDE', 'SACCHARIDE']

data = []
for ii in types:
    data += types_dict[ii]

output = {}

for value in data:
    
    key = cif_entries[value]

    tmp_dict={}

    tmp_dict['name']=key['_chem_comp']['name']
    tmp_dict['topology']=[]
    tmp_dict['topology'].append({'atoms':key['_chem_comp_atom']['atom_id'], 'bonds':[]})
    tmp_dict['topology'].append({'atoms':key['_chem_comp_atom']['alt_atom_id'], 'bonds':[]})   
    if '_chem_comp_bond' in key:
        if not isinstance(key['_chem_comp_bond']['atom_id_1'],list):
            key['_chem_comp_bond']['atom_id_1'] = [key['_chem_comp_bond']['atom_id_1']]
            key['_chem_comp_bond']['atom_id_2'] = [key['_chem_comp_bond']['atom_id_2']]
        for atom1,atom2 in zip(key['_chem_comp_bond']['atom_id_1'], key['_chem_comp_bond']['atom_id_2']):
            tmp_dict['topology'][0]['bonds'].append([atom1,atom2])
            ii = tmp_dict['topology'][0]['atoms'].index(atom1)
            jj = tmp_dict['topology'][0]['atoms'].index(atom2)
            atom1 = tmp_dict['topology'][1]['atoms'][ii]
            atom2 = tmp_dict['topology'][1]['atoms'][jj]
            tmp_dict['topology'][1]['bonds'].append([atom1,atom2])

    output[value]=tmp_dict

split_output = {}
for name,value in output.items():
    if name[0] not in split_output:
        split_output[name[0]]={}
    split_output[name[0]][name]=value

import gzip

for file_name, aux_output in split_output.items():
    with gzip.open(file_name+'.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(aux_output, fff)

with gzip.open('group_names.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(sorted(list(output.keys())), fff)

