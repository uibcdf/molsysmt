import numpy as np
from molsysmt._private_tools.exceptions import *
import pyunitwizard as puw
from molsysmt.molecular_system import molecular_system_components

form_name='MolecularMechanicsDict'

is_form={
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['ff_parameters', 'mm_parameters']:
    has[ii]=True

def this_dict_is_MolecularMechanicsDict(item):

    from molsysmt._private_tools.molecular_mechanics import is_molecular_mechanics_dict

    return is_molecular_mechanics_dict(item)

def to_molsysmt_MolecularMechanics(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molecular_mechanics import MolecularMechanics as molsysmt_MolecularMechanics

    tmp_item = molsysmt_MolecularMechanics(**item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_MolecularMechanicsDict(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        tmp_item = item.copy()
    else:
        raise NotImplementedError()

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

