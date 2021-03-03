from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm.app import GromacsTopFile as _openmm_GromacsTopFile

form_name='openmm.GromacsTopFile'

is_form={
    _openmm_GromacsTopFile : form_name,
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_bonds=True
with_parameters=True

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = item.topology

    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import _select

    tmp_item = to_molsysmt_Topology(item)
    atom_indices = _select(tmp_item, selection)
    return atom_indices

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

##### Set

## Atom


## System


