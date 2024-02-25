# wget https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

from molsysmt.element.group.amino_acid import group_names as valid_names

output = {}

#### Auxiliary functions ####

def get_amino_acids_from_gromacs_rtp(path):

    output = {}
    section=None
    group_name=None
    group_dict={'atoms':[], 'bonds':[]}
    
    with open(path,'r') as fff:
        for line in fff:
            if line.startswith('['):
                if len(group_dict['atoms']):
                    output[group_name]=group_dict
                group_name = line.split(' ')[1]
                group_dict = {'atoms':[], 'bonds':[]}
            elif line.startswith(' [ atoms'):
                section='atoms'
            elif line.startswith(' [ bonds'):
                section='bonds'
            elif line.startswith(' [ '):
                section=None
            else:
                fields = line.split()
                if section=='atoms' and len(fields)==4:
                    group_dict['atoms'].append(fields[0])
                elif section=='bonds' and len(fields)==2:
                    if fields[0][0] not in ['-', '+'] and fields[1][0] not in ['-', '+']:
                        group_dict['bonds'].append([fields[0], fields[1]])
    output[group_name]=group_dict

    return output

def is_in(group_name, atoms, bonds, output):

    for ii in output['topology']:
        if set(atoms) == set(ii['atoms']):
            set1 = set(tuple(sorted(par)) for par in bonds)
            set2 = set(tuple(sorted(par)) for par in ii['bonds'])
            if set1 == set2:
                return True

    return False

#### Protein Data Bank ####
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

types = ['"L-PEPTIDE LINKING"',
         '"D-PEPTIDE LINKING"',
         '"L-peptide linking"',
         '"D-peptide linking"',
         '"PEPTIDE LINKING"',
         '"peptide linking"',
         '"L-peptide NH3 amino terminus"',
         '"L-peptide COOH carboxy terminus"',
         '"L-PEPTIDE COOH CARBOXY TERMINUS"',
         '"D-PEPTIDE NH3 AMINO TERMINUS"',
         '"D-peptide NH3 amino terminus"']

data = []
for ii in types:
    data += types_dict[ii]

output_pdb = {}

for value in data:
    
    key = cif_entries[value]

    tmp_dict={}

    tmp_dict['name']=key['_chem_comp']['name']
    tmp_dict['topology']=[]
    tmp_dict['topology'].append({'atoms':key['_chem_comp_atom']['atom_id'], 'bonds':[]})
    tmp_dict['topology'].append({'atoms':key['_chem_comp_atom']['alt_atom_id'], 'bonds':[]})   
    if '_chem_comp_bond' in key:
        for atom1,atom2 in zip(key['_chem_comp_bond']['atom_id_1'], key['_chem_comp_bond']['atom_id_2']):
            tmp_dict['topology'][0]['bonds'].append([atom1,atom2])
            ii = tmp_dict['topology'][0]['atoms'].index(atom1)
            jj = tmp_dict['topology'][0]['atoms'].index(atom2)
            atom1 = tmp_dict['topology'][1]['atoms'][ii]
            atom2 = tmp_dict['topology'][1]['atoms'][jj]
            tmp_dict['topology'][1]['bonds'].append([atom1,atom2])

    output_pdb[value]=tmp_dict

for valid_name in valid_names:
    if valid_name in output_pdb:
        output[valid_name]=output_pdb[valid_name]

del(output_pdb)

#### Gromacs ####

gromacs_top_path = '/usr/local/gromacs/share/gromacs/top/'

forcefield_dirs = ['amber03.ff', 'amber94.ff', 'amber96.ff', 'amber99.ff', 'amber99sb.ff', 'amber99sb-ildn.ff', 'amberGS.ff',
                   'charmm27.ff', 'gromos43a1.ff', 'gromos43a2.ff', 'gromos45a3.ff', 'gromos53a5.ff', 'gromos53a6.ff',
                   'gromos54a7.ff', 'oplsaa.ff']

for forcefield_dir in forcefield_dirs: 
    path = f'/usr/local/gromacs/share/gromacs/top/{forcefield_dir}/aminoacids.rtp'
    output_rtp=get_amino_acids_from_gromacs_rtp(path)
    for ii,jj in output_rtp.items():
        if ii in valid_names and len(jj['bonds']):
            if ii in output:
                if not is_in(ii, jj['atoms'], jj['bonds'], output[ii]):
                    output[ii]['topology'].append(jj)
            else:
                tmp_dict = {}
                tmp_dict['name']=None
                tmp_dict['topology']=[]
                tmp_dict['topology'].append(jj)
                output[ii]=tmp_dict

#### End ####

split_output = {}
for name,value in output.items():
    if name[0] not in split_output:
        split_output[name[0]]={}
    split_output[name[0]][name]=value

import gzip

for file_name, aux_output in split_output.items():
    with gzip.open(file_name+'.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(aux_output, fff)

