import pickle
import sys
import gzip
import numpy as np
from molsysmt.element.group.amino_acid import group_names

def get_bonded_atom_pairs(group_name, atom_indices=None, atom_names=None):

    if group_name not in group_names:
        raise ValueError
    
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

    with gzip.open(path('molsysmt.data.databases.amino_acids',group_name[0]+'.pkl.gz'), 'rb') as fff:
        dbs = pickle.load(fff)

    db = dbs[group_name]

    if atom_names is None:
        atom_names = db['atom_name']
    if atom_indices is None:
        atom_indices = np.arange(len(atom_names), dtype=int).tolist()

    
    atom_int_indices = []
    unk_atom_indices = []
    _aux_dict = {}
    
    for jj, atom_name in enumerate(atom_names):

        try:
            ii = db['atom_name'].index(atom_name)
        except:
            try:
                ii = db['alt_atom_name'].index(atom_name)
            except:
                ii = None
        if ii is not None:
            atom_int_indices.append(ii)
            _aux_dict[ii]=atom_indices[jj]
        else:
            unk_atom_indices.append(atom_indices[jj])

    bonds = []

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
