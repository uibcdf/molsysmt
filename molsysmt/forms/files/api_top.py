from os.path import basename as _basename
from molsysmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'top': form_name
    }

info=["",""]
with_topology=True
with_trajectory=False

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    return to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices,
                                         frame_indices=frame_indices)

def to_parmed_GromacsTopologyFile(item, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Structure(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.structure.classes import from_gromacs_Topology
    return from_gromacs_Topology(item, selection=atom_indices)

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj.core.topology import Topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Topology.from_openmm(tmp_item)
    return tmp_item

def to_openmm_GromacsTopFile(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import GromacsTopFile
    from molsysmt.forms.classes.api_openmm_GromacsTopFile import extract as extract_gromacstopfile
    tmp_item = GromacsTopFile(item)
    tmp_item = extract_extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.formats.classes.api_openmm_Topology import extract as extract_openmm_topology
    tmp_item = to_openmm_GromacsTopFile(item)
    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_top(item, output_filepath=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_GromacsTopFile import extract as extract_gromacstopfile
    tmp_item = to_parmed_GromacsTopologyFile(item)
    tmp_item = extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.save(output_filepath)
    del(tmp_item)
    pass

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

