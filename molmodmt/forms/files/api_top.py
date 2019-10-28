from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'top': form_name
    }

def to_parmed_Structure(item, atom_indices=None, frame_indices=None):

    return to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices,
                                         frame_indices=frame_indices)

def to_parmed_GromacsTopologyFile(item, atom_indices=None, frame_indices=None):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(item)
    tmp_item = extract_subsystem(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molmodmt_Structure(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_structure import from_gromacs_Topology
    return from_gromacs_Topology(item, selection=atom_indices)

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    from mdtraj.core.topology import Topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Topology.from_openmm(tmp_item)
    return tmp_item

def to_openmm_GromacsTopFile(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app import GromacsTopFile
    from molmodmt.forms.classes.api_openmm_GromacsTopFile import extract_subsystem as extract_gromacstopfile
    tmp_item = GromacsTopFile(item)
    tmp_item = extract_extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    from molmodmt.formats.classes.api_openmm_Topology import extract_subsystem as extract_openmm_topology
    tmp_item = to_openmm_GromacsTopFile(item)
    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_top(item, output_file_path=None, atom_indices=None, frame_indices=None):

    from molmodmt.forms.classes.api_openmm_GromacsTopFile import extract_subsystem as extract_gromacstopfile
    tmp_item = to_parmed_GromacsTopologyFile(item)
    tmp_item = extract_gromacstopfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.save(output_file_path)
    del(tmp_item)
    pass

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        raise NotImplementedError

def duplicate(item):

    raise NotImplementedError

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

