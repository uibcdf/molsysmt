import pickle
import sys
import gzip
import numpy as np
from molsysmt.element.group.small_molecule import group_names

if sys.version_info[1] in (10,11):
    from importlib.resources import files
    def path(package, file):
        return files(package).joinpath(file)
elif sys.version_info[1] in (8,9):
    from pathlib import PurePath
    parent = PurePath(__file__).parent
    def path(package, file):
        data_dir = package.split('.')[-1]
        return parent.joinpath('../../../data/databases/'+data_dir+'/'+file).__str__()


def get_group_db(group_name):

    if group_name not in group_names:
        raise ValueError
    
    with gzip.open(path('molsysmt.data.databases.small_molecules',group_name[0]+'.pkl.gz'), 'rb') as fff:
        dbs = pickle.load(fff)

    db = dbs[group_name]

    return db
