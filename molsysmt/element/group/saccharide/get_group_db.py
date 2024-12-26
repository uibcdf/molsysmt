import pickle
import sys
import gzip
import numpy as np
from molsysmt.element.group.saccharide import group_names

from importlib.resources import files
def path(package, file):
    return files(package).joinpath(file)


def get_group_db(group_name):

    if group_name not in group_names:
        raise ValueError
    
    with gzip.open(path('molsysmt.data.databases.saccharides',group_name[0]+'.pkl.gz'), 'rb') as fff:
        dbs = pickle.load(fff)

    db = dbs[group_name]

    return db
