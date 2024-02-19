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


with gzip.open(path('molsysmt.data.databases.amino_acids','group_names.pkl.gz'), 'rb') as fff:
    group_names = pickle.load(fff)

