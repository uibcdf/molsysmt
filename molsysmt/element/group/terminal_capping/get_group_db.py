import pickle
import sys
import json
import numpy as np
from molsysmt.element.group.terminal_capping import n_terminal_capping_names, c_terminal_capping_names

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

    if group_name in n_terminal_capping_names:
        with open(path('molsysmt.data.databases.terminal_cappings','n_terminal.json'), 'r') as fff:
            dbs = json.load(fff)
    elif group_name in c_terminal_capping_names:
        with open(path('molsysmt.data.databases.terminal_cappings','c_terminal.json'), 'r') as fff:
            dbs = json.load(fff)
    else:
        raise ValueError

    db = dbs[group_name]

    return db
