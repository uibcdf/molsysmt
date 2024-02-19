# wget https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

from molsysmt.native import CIFFileHandler
import pickle

handler = CIFFileHandler('components.cif')
cif_entries = handler.parse()

types_dict = {}

for ii in cif_entries:
    jj = cif_entries[ii]['_chem_comp']['type']
    if jj in types_dict:
        types_dict[jj].append(ii)
    else:
        types_dict[jj] = [ii]

types = ['NON-POLYMER', 'non-polymer', 'other']
data = []
for ii in types:
    data += types_dict[ii]
data.remove('UNL')

# quito iones
ions = []
for value in data:
    key = cif_entries[value]
    if key['_chem_comp']['name'].endswith(' ION"') or key['_chem_comp']['name'].endswith(' ion"'):
        ions.append(value)

output = {}

for value in ions:
    
    key = cif_entries[value]

    aux_dict={}

    aux_dict['name']=key['_chem_comp']['name']
    aux_dict['three_letter_code']=key['_chem_comp']['three_letter_code']
    aux_dict['formal_charge']=float(key['_chem_comp']['pdbx_formal_charge'])
    aux_dict['atom_name']=key['_chem_comp_atom']['atom_id']
    aux_dict['alt_atom_name']=key['_chem_comp_atom']['alt_atom_id']
    aux_dict['atom_type']=key['_chem_comp_atom']['type_symbol']
    try:
        charge = []
        for ii in key['_chem_comp_atom']['charge']:
            charge.append(float(ii))
        aux_dict['charge']=charge
    except:
        aux_dict['charge']=[]
    if '_chem_comp_bond' in key:
        aux_dict['bonds']=[[ii,jj] for ii,jj in zip(key['_chem_comp_bond']['atom_id_1'],
                                                    key['_chem_comp_bond']['atom_id_2'])]
    else:
        aux_dict['bonds']=[]

    output[value]=aux_dict

#with open('small_molecules_db.pkl', 'wb') as fff:
#    pickle.dump(output, fff)

split_output = {}
for name,value in output.items():
    if name[0] not in split_output:
        split_output[name[0]]={}
    split_output[name[0]][name]=value

import gzip

for file_name, aux_output in split_output.items():
    with gzip.open('ions/'+file_name+'.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(aux_output, fff)

with gzip.open('ions/group_names.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(list(output.keys()), fff)


