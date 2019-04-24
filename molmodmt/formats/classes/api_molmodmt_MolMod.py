from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt import MolMod as _molmodmt_MolMod

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_MolMod : form_name,
    'molmod': form_name
}

def to_molmodmt(item):
    return item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_mdtraj as _to_mdtraj
    from molmodmt import extract as _extract
    tmp_item = _to_mdtraj(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    from molmodmt import extract as _extract
    tmp_item = _to_mdtraj_Trajectory(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def get(item, atoms_list=None, **kwargs):
    raise NotImplementedError(NotImplementedMessage)

def select_with_mdtraj(item, selection):
    return item.select_with_mdtraj(selection)

def extract_atoms_list(item, atoms_list):
    return item.extract(atoms_list)

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)


