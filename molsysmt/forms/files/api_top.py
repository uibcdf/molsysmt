from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='top'

is_form = {
    'top': form_name
    }

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_parameters=False

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_parmed_GromacsTopologyFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs

    tmp_item=_parmed_from_gromacs(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.structure.classes import from_gromacs_Topology

    tmp_item = from_gromacs_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology

    tmp_item = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Topology.from_openmm(tmp_item)

    return tmp_item

def to_openmm_GromacsTopFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import GromacsTopFile
    from molsysmt.forms.classes.api_openmm_GromacsTopFile import extract as extract_gromacstopfile

    tmp_item = GromacsTopFile(item)
    tmp_item = extract_extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.formats.classes.api_openmm_Topology import extract as extract_openmm_topology

    tmp_item = to_openmm_GromacsTopFile(item, molecular_system)
    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_top(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.forms.classes.api_openmm_GromacsTopFile import extract as extract_gromacstopfile

    tmp_item = to_parmed_GromacsTopologyFile(item, molecular_system)
    tmp_item = extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.save(output_filename)
    del(tmp_item)

    return output_filename

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

## system

