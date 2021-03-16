from molsysmt._private_tools.exceptions import *
from molsysmt.native.molecular_mechanics import MolecularMechanics as _molsysmt_MolecularMechanics
from molsysmt.molecular_system import molecular_system_components

form_name='molsysmt.MolecularMechanics'

is_form={
    _molsysmt_MolecularMechanics : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['ff_parameters', 'mm_parameters']:
    has[ii]=True

def to_MolecularMechanicsDict(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item = item.to_dict()

    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def copy(item):

    return item.copy()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotWithThisFormError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisFormError()


