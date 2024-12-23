import pickle
import sys
import json
import numpy as np
from molsysmt.element.group.terminal_capping import n_terminal_capping_names, c_terminal_capping_names

from importlib.resources import files
def path(package, file):
    return files(package).joinpath(file)

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
