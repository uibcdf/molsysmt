from molsysmt._private.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private.files_and_directories import temp_filename

form_name='file:mdcrd'
from_type='file'

is_form = {
        'file:mdcrd':form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['coordinates', 'box']:
    has[ii]=True

info = ["AMBER mdcrd file format","https://ambermd.org/FileFormats.php#trajectory"]

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.molsys import from_mdcrd as mdcrd_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.topology import from_mdcrd as mdcrd_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Structures(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.trajectory import from_mdcrd as mdcrd_to_molsysmt_Structures

    tmp_item, tmp_molecular_system = mdcrd_to_molsysmt_Structures(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def to_file_mdcrd(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item, output_filename=output_filename)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=output_filename)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all', output_filename=None):

    if output_filename is None:
        output_filename = temp_filename(extension='mdcrd')

    if (atom_indices is 'all') and (structure_indices is 'all'):
        raise NotImplementedError()
    else:
        raise NotImplementedError()

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

###### Get

# System

def get_n_structures_from_system (item, indices='all', structure_indices='all'):

    return NotImplementedError

def get_n_atoms_from_system (item, indices='all', structure_indices='all'):

    return NotImplementedError

