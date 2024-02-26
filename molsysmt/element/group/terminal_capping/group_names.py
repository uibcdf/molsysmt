import pickle
import sys
import gzip

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

try:
    with gzip.open(path('molsysmt.data.databases.terminal_cappings','group_names_c_terminal.pkl.gz'), 'rb') as fff:
        c_terminal_capping_names = pickle.load(fff)
except:
    c_terminal_capping_names = None
    print('The file molsysmt.data.databases.terminal_cappings.group_names_c_terminal.pkl.gz was not loaded.')

try:
    with gzip.open(path('molsysmt.data.databases.terminal_cappings','group_names_n_terminal.pkl.gz'), 'rb') as fff:
        n_terminal_capping_names = pickle.load(fff)
except:
    n_terminal_capping_names = None
    print('The file molsysmt.data.databases.terminal_cappings.group_names_n_terminal.pkl.gz was not loaded.')

group_names = []
if n_terminal_capping_names is not None:
    group_names += n_terminal_capping_names
if c_terminal_capping_names is not None:
    group_names += c_terminal_capping_names

