import pickle
import sys
import json

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

try:
    with open(path('molsysmt.data.databases.terminal_cappings','c_terminal.json'), 'r') as fff:
        c_terminal_capping_names = json.load(fff)
except:
    c_terminal_capping_names = None
    print('The file molsysmt.data.databases.terminal_cappings.c_terminal.json was not loaded.')

try:
    with open(path('molsysmt.data.databases.terminal_cappings','n_terminal.json'), 'r') as fff:
        n_terminal_capping_names = json.load(fff)
except:
    n_terminal_capping_names = None
    print('The file molsysmt.data.databases.terminal_cappings.n_terminal.json was not loaded.')

group_names = []
if n_terminal_capping_names is not None:
    group_names += list(n_terminal_capping_names.keys())
if c_terminal_capping_names is not None:
    group_names += list(c_terminal_capping_names.keys())

