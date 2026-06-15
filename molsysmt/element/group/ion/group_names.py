import pickle
import gzip

from importlib.resources import files
def path(package, file):
    return files(package).joinpath(file)

try:
    with gzip.open(path('molsysmt.data.databases.ions','group_names.pkl.gz'), 'rb') as fff:
        group_names = pickle.load(fff)
except Exception:
    group_names = None
    print('The file molsysmt.data.databases.ions.group_names.pkl.gz was not loaded.')

# Neutral dummy / placeholder residues (atoms named DUM or X). They are single,
# bondless atoms, so they are recognised as standalone ion-type groups. Appended
# preserving the original list type/contract.
_DUMMY_GROUP_NAMES = ['DUM', 'X']
if group_names is None:
    group_names = list(_DUMMY_GROUP_NAMES)
else:
    for _name in _DUMMY_GROUP_NAMES:
        if _name not in group_names:
            group_names.append(_name)
