from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm import Context as _openmm_Context
from molsysmt import puw
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.Context'

is_form={
    _openmm_Context : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'box', 'coordinates', 'ff_parameters', 'mm_parameters', 'thermo_state', 'simulation']:
    has[ii]=True

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

##### Get

