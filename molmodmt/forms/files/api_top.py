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
    if selection is not 'all':
        from molmodmt import extract
        tmp_item = extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molmodmt_Structure(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_structure import from_gromacs_Topology
    return from_gromacs_Topology(item, selection=None, syntaxis='MDTraj')

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    from mdtraj.core.topology import Topology
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = Topology.from_openmm(tmp_item)

    return tmp_item

def to_openmm_GromacsTopFile(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app import GromacsTopFile
    if selection is not None:
        raise ValueError("The method `to_openmm_GromacsTopFile` from api_top.py does not admit selections")
    return GromacsTopFile(item)

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    tmp_item = to_openmm_GromacsTopFile(item)
    tmp_item = tmp_item.topology
    if selection is not 'all':
        tmp_item = extract(tmp_item, atom_indices=None, frame_indices=None)
    return tmp_item

def to_top(item, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    tmp_item = to_parmed_GromacsTopologyFile(item)
    if selection is not 'all':
        tmp_item = extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    tmp_item.save(filename)
    pass

