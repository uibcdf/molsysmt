# wget https://files.wwpdb.org/pub/pdb/data/monomers/components.cif

output = {}

#### Protein Data Bank ####
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

for value in data:
    
    key = cif_entries[value]

    tmp_dict={}

    tmp_dict['name']=key['_chem_comp']['name']
    tmp_dict['three_letter_code']=key['_chem_comp']['three_letter_code']
    tmp_dict['atom_name']=[key['_chem_comp_atom']['atom_id']]
    tmp_dict['atom_name'].append(key['_chem_comp_atom']['atom_id'])
    if '_chem_comp_bond' in key:
        bonds = []
        for ii,jj in zip(key['_chem_comp_bond']['atom_id_1'], key['_chem_comp_bond']['atom_id_2']):
            iii = tmp_dict['atom_name'][0].index(ii)
            jjj = tmp_dict['atom_name'][0].index(jj)
            if iii>jjj:
                bonds.append([jjj,iii])
            else:
                bonds.append([iii,jjj])
        tmp_dict['bonds']=bonds
    else:
        tmp_dict['bonds']=[]

    output[value]=tmp_dict

#with open('small_molecules_db.pkl', 'wb') as fff:
#    pickle.dump(output, fff)

#### Gromacs ####

import networkx as nx
from molsysmt.element.atom.get_atom_type import _get_atom_type_from_atom_name

residues_path = '/usr/local/gromacs/share/gromacs/top/residues.xml'

aux_dict={}

with open(residues_path, 'r') as fff:

    for line in fff.readlines():

        if '<residue restype' in line:
            resname = line.split('"')[1]
            aux_dict[resname]={'atoms':[], 'bonds':[]}
        elif '<ratom name' in line:
            iii = line.split('"')
            aux_dict[resname]['atoms'].append(iii[1])
        elif '<rbond a1' in line:
            iii =  line.split('"')
            aux_dict[resname]['bonds'].append([iii[1], iii[3]])

for ii in ['ACE', 'HOH', 'HEME', 'NAC', 'NH2', 'OCT']:
    del aux_dict[ii]

for resname in aux_dict:

    if resname in output:

        old_graph = nx.Graph()
        new_graph = nx.Graph()

        for bond in output[resname]['bonds']:
            old_graph.add_edge(bond[0], bond[1])

        for bond in aux_dict[resname]['bonds']:
            new_graph.add_edge(bond[0], bond[1])

        new_graph.remove_node('-C')

        matcher = nx.algorithms.isomorphism.GraphMatcher(old_graph, new_graph)

        is_subgraph_isomorphic = matcher.subgraph_is_isomorphic()
        
        if is_subgraph_isomorphic:

            eq_max=0
            candidato=None
            for mapping in matcher.subgraph_isomorphisms_iter():
                mask=[]
                eq=0
                for ii,jj in mapping.items():
                    iii = _get_atom_type_from_atom_name(output[resname]['atom_name'][0][ii])
                    jjj = _get_atom_type_from_atom_name(jj)
                    mask.append(iii==jjj)
                    if output[resname]['atom_name'][0][ii]==jj:
                        eq+=1
                if all(mask):
                    if eq_max<eq:
                        eq_max=eq
                        candidato=mapping

            n_atoms = len(output[resname]['atom_name'][0])
            new_atoms = ['' for ii in range(n_atoms)]
            for ii,jj in candidato.items():
                new_atoms[ii]=jj
            output[resname]['atom_name'].append(new_atoms)

        else:

            print(f'{resname} with problems')

    else: 

        tmp_dict={}
        bonds = []

        tmp_dict['name']=resname
        tmp_dict['three_letter_code']=resname
        tmp_dict['atom_name']=[aux_dict[resname]['atoms']]
        for ii,jj in aux_dict[resname]['bonds']:
            if ii!='-C' and jj!='-C':
                iii = aux_dict[resname]['atoms'].index(ii)
                jjj = aux_dict[resname]['atoms'].index(jj)
                if iii>jjj:
                    bonds.append([jjj,iii])
                else:
                    bonds.append([iii,jjj])
                tmp_dict['bonds']=bonds

        output[resname]=tmp_dict

#### End ####

split_output = {}
for name,value in output.items():
    if name[0] not in split_output:
        split_output[name[0]]={}
    split_output[name[0]][name]=value

import gzip

for file_name, aux_output in split_output.items():
    with gzip.open('amino_acids/'+file_name+'.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(aux_output, fff)

with gzip.open('amino_acids/group_names.pkl.gz', 'wb', compresslevel=9) as fff:
        pickle.dump(list(output.keys()), fff)

