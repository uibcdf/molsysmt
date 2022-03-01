from molsysmt._private_tools.exceptions import *
from molsysmt.native.molecular_mechanics import MolecularMechanics as _molsysmt_MolecularMechanics
from molsysmt.native.molecular_system import molecular_system_components

form_name='molsysmt.MolecularMechanics'
from_type='class'

is_form={
    _molsysmt_MolecularMechanics : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['ff_parameters', 'mm_parameters']:
    has[ii]=True

def to_MolecularMechanicsDict(item, molecular_system, atom_indices='all', structure_indices='all'):

    tmp_item = item.to_dict()
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolecularMechanics(item, molecular_system, atom_indices='all', structure_indices='all', copy_if_all=True):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        tmp_item = item.copy()
    else:
        raise NotWithThisFormError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisFormError()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

