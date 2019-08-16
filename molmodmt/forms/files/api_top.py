from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'top': form_name
    }

def to_parmed(item):
    return to_parmed_GromacsTopologyFile(item)

def to_parmed_Structure(item):
    return to_parmed_GromacsTopologyFile(item)

def to_parmed_GromacsTopologyFile(item):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_molmod_Structure=_parmed_from_gromacs(item)
    return tmp_molmod_Structure

def to_molmodmt_Structure(item):

    from molmodmt.native.io_structure import from_gromacs_Topology
    return from_gromacs_Topology(item)

def to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj'):

    from molmodmt import extract
    from mdtraj.core.topology import Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = Topology.from_openmm(tmp_item)
    if selection is not 'all':
        tmp_item = extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return Topology.from_openmm(tmp_item)

def to_openmm_GromacsTopFile(item):

    from simtk.openmm.app import GromacsTopFile
    return GromacsTopFile(item)

def to_openmm_Topology(item):

    from simtk.openmm.app import GromacsTopFile
    return GromacsTopFile(item).topology

    #from parmed import load_file
    #return load_file(item)

def to_top(item, selection='all', syntaxis='mdtraj'):

    from molmodmt import extract
    tmp_item = to_parmed_GromacsTopologyFile(item)
    if selection is not 'all':
        tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    tmp_item.save(filename)
    pass

