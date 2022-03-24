from molsysmt._private.exceptions import *
from molsysmt.api_forms.common_gets import *
import numpy as np
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt._private.files_and_directories import temp_filename

form_name='file:top'
from_type='file'

is_form = {
        'file:top':form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds']:
    has[ii]=True

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    tmp_item, tmp_molecular_system = to_parmed_GromacsTopologyFile(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def to_parmed_GromacsTopologyFile(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from parmed.gromacs import GromacsTopologyFile
    from molsysmt.api_forms.api_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile as parmed_GromacsTopologyFile_to_parmed_GromacsTopologyFile

    tmp_item = GromacsTopologyFile(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item = parmed_GromacsTopologyFile_to_parmed_GromacsTopologyFile(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from mdtraj.core.topology import Topology

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = Topology.from_openmm(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_GromacsTopFile(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from openmm.app import GromacsTopFile
    from molsysmt.api_forms.api_openmm_GromacsTopFile import to_openmm_GromacsTopFile as openmm_GromacsTopFile_to_openmm_GromacsTopFile

    tmp_item = GromacsTopFile(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_GromacsTopFile_to_openmm_GromacsTopFile(tmp_item, tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.formats.classes.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    tmp_item = to_openmm_GromacsTopFile(item)
    tmp_item = tmp_item.topology
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_file_top(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=False):

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
        output_filename = temp_filename(extension='top')

    if (atom_indices is 'all') and (structure_indices is 'all'):

        raise NotImplementedError()

    else:
        tmp_item, _ = to_openmm_GromacsTopologyFile(item, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_item.save(output_filename)
        del(tmp_item)

        tmp_item = output_filename

    return tmp_item

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

## system

