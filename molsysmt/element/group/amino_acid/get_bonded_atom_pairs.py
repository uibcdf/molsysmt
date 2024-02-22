import pickle
import sys
import gzip
import numpy as np
from molsysmt.element.group.amino_acid import group_names

if sys.version_info[1]==10:
    from importlib.resources import files
    def path(package, file):
        return files(package).joinpath(file)
elif sys.version_info[1] in (8,9):
    from pathlib import PurePath
    parent = PurePath(__file__).parent
    def path(package, file):
        data_dir = package.split('.')[-1]
        return parent.joinpath('../data/'+data_dir+'/'+file).__str__()

def get_bonded_atom_pairs(group_name, atom_indices=None, atom_names=None):

    if group_name not in group_names:
        raise ValueError
    
    with gzip.open(path('molsysmt.data.databases.amino_acids',group_name[0]+'.pkl.gz'), 'rb') as fff:
        dbs = pickle.load(fff)

    db = dbs[group_name]

    if atom_names is None:
        atom_names = db['atom_name']
    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    
    is_in = -1
    for ii,db_atom_names in enumerate(db['atom_name']):
        if np.all(np.isin(atom_names, db_atom_names)):
            is_in=ii

    if is_in!=-1:

        atom_int_indices = []
        _aux_dict = {}
        bonds = []
        unk_atom_indices = []

        for jj, atom_name in enumerate(atom_names):

            ii = db['atom_name'][is_in].index(atom_name)
            atom_int_indices.append(ii)
            _aux_dict[ii]=atom_indices[jj]

        for ii,jj in db['bonds']:

            if ii in atom_int_indices:
                if jj in atom_int_indices:
                    iii = _aux_dict[ii]
                    jjj = _aux_dict[jj]
                    if iii<jjj:
                        bonds.append([iii,jjj])
                    else:
                        bonds.append([jjj,iii])

        return sorted(bonds), unk_atom_indices

    else:

        return [], atom_indices

