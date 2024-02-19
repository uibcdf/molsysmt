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

output = {}

for value in data:
    
    key = cif_entries[value]

    aux_dict={}

    aux_dict['name']=key['_chem_comp']['name']
    aux_dict['three_letter_code']=key['_chem_comp']['three_letter_code']
    aux_dict['atom_name']=key['_chem_comp_atom']['atom_id']
    aux_dict['alt_atom_name']=key['_chem_comp_atom']['alt_atom_id']
    aux_dict['atom_type']=key['_chem_comp_atom']['type_symbol']
    aux_dict['charge']=[float(ii) for ii in key['_chem_comp_atom']['charge']]
    if '_chem_comp_bond' in key:
        aux_dict['bonds']=[[ii,jj] for ii,jj in zip(key['_chem_comp_bond']['atom_id_1'],
                                                    key['_chem_comp_bond']['atom_id_2'])]
    else:
        aux_dict['bonds']=[]

    output[value]=aux_dict

#with open('small_molecules_db.pkl', 'wb') as fff:
#    pickle.dump(output, fff)

import gzip
with gzip.open('small_molecules_db.pkl.gz', 'wb', compresslevel=9) as fff:
    pickle.dump(output, fff)

