from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.molmod import MolMod as _molmodmt_MolMod

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_MolMod : form_name,
    'molmodmt': form_name
}

def to_molmodmt(item):
    return item

def to_mdtraj(item):
    from molmodmt.native.io_molmod import to_mdtraj as _to_mdtraj 
    tmp_mdtraj_item = _to_mdtraj(item)
    del(_to_mdtraj)
    return tmp_mdtraj_item

def get_shape(item):
    raise NotImplementedError(NotImplementedMessage)

def select_with_mdtraj(item, selection):
    return item.topology.select(selection)

def extract_atoms_list(item, atoms_list):
    raise NotImplementedError(NotImplementedMessage)

