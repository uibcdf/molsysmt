from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='top'

is_form = {
    'top': form_name
    }

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds']:
    has[ii]=True

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item, tmp_molecular_system = to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile
    from molsysmt.forms.classes.api_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile as parmed_GromacsTopologyFile_to_parmed_GromacsTopologyFile

    tmp_item = GromacsTopologyFile(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item = parmed_GromacsTopologyFile_to_parmed_GromacsTopologyFile(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.structure.classes import from_gromacs_Topology

    tmp_item, tmp_molecular_system = from_gromacs_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Topology.from_openmm(tmp_item)
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_GromacsTopFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import GromacsTopFile
    from molsysmt.forms.classes.api_openmm_GromacsTopFile import to_openmm_GromacsTopFile as openmm_GromacsTopFile_to_openmm_GromacsTopFile

    tmp_item = GromacsTopFile(item)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = openmm_GromacsTopFile_to_openmm_GromacsTopFile(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.formats.classes.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    tmp_item = to_openmm_GromacsTopFile(item, molecular_system)
    tmp_item = tmp_item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_top(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None, copy_if_all=False):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        raise NotImplementedError()

    else:

        tmp_item = to_openmm_GromacsTopologyFile(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item.save(output_filename)
        del(tmp_item)

        tmp_item = output_filename

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

## system

