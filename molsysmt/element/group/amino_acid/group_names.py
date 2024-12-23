import pickle
import sys
import gzip

from importlib.resources import files
def path(package, file):
    return files(package).joinpath(file)

try:
    with gzip.open(path('molsysmt.data.databases.amino_acids','group_names.pkl.gz'), 'rb') as fff:
        group_names = pickle.load(fff)
except:
    group_names = None
    print('The file molsysmt.data.databases.amino_acids.group_names.pkl.gz was not loaded.')
