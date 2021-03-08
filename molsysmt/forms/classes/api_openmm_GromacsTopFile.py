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

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Set

## Atom


## System


