from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from simtk.openmm.app import AmberPrmtopFile as _openmm_AmberPrmtopFile

form_name='openmm.AmberPrmtopFile'

is_form={
    _openmm_AmberPrmtopFile : form_name,
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_bonds=True
with_parameters=True

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = to_openmm_Topology(item, molecular_system)
    tmp_item = openmm_Topology_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

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

##### Set

## Atom

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## System

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

