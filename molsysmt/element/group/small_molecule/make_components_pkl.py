# wget https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

from molsysmt.native import CIFFileHandler
import pickle

handler = CIFFileHandler('components.cif')
cif_entries = handler.parse()
output = {}

for value, key in cif_entries.items():
    output[key['_chem_comp']['three_letter_code']]=key['_chem_comp']['name']

with open('components.pkl', 'wb') as fp:
    pickle.dump(output, fp)

