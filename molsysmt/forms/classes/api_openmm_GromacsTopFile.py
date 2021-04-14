from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm.app import GromacsTopFile as _openmm_GromacsTopFile
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.GromacsTopFile'

is_form={
    _openmm_GromacsTopFile : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'ff_parameters']:
    has[ii]=True

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = item.topology

    return tmp_item

def to_openmm_GromacsTopFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        raise NotImplementedError
    else:
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


