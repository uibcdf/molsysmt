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

def to_mdtraj(item):
    from molmodmt.native.io_molmod import to_mdtraj as _to_mdtraj
    tmp_mdtraj_item = _to_mdtraj(item)
    del(_to_mdtraj)
    return tmp_mdtraj_item

def get_info(item, atoms_list=None, **kwargs):
    raise NotImplementedError(NotImplementedMessage)

def select_with_mdtraj(item, selection):
    return item.select_with_mdtraj(selection)

def extract_atoms_list(item, atoms_list):
    return item.extract(atoms_list)

def get_molecules(item,with_bonds=False):
    return item.get_molecules(with_bonds)

