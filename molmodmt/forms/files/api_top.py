from os.path import basename as _basename
from molmodmt.utils.exceptions import *

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'top': form_name
    }

def to_parmed(item, selection=None, syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, selection=selection, syntaxis=syntaxis)

def to_parmed_Structure(item, selection=None, syntaxis='MDTraj'):
    return to_parmed_GromacsTopologyFile(item, selection=selection, syntaxis=syntaxis)

def to_parmed_GromacsTopologyFile(item, selection=None, syntaxis='MDTraj'):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    tmp_item=_parmed_from_gromacs(item)
    if selection is not 'all':
        from molmodmt import trim
        trim(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_molmodmt_Structure(item, selection=None, syntaxis='MDTraj'):

    from molmodmt.native.io_structure import from_gromacs_Topology
    return from_gromacs_Topology(item, selection=None, syntaxis='MDTraj')

def to_mdtraj_Topology(item, selection=None, syntaxis='MDTraj'):

    from molmodmt import extract
    from mdtraj.core.topology import Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = Topology.from_openmm(tmp_item)
    if selection is not 'all':
        tmp_item = extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return tmp_item

def to_openmm_GromacsTopFile(item, selection=None, syntaxis='MDTraj'):

    from simtk.openmm.app import GromacsTopFile
    if selection is not None:
        raise ValueError("The method `to_openmm_GromacsTopFile` from api_top.py does not admit selections")
    return GromacsTopFile(item)

def to_openmm_Topology(item, selection=None, syntaxis='MDTraj'):

    if True:
        tmp_item = to_openmm_GromacsTopFile(item)
        tmp_item = tmp_item.topology
        if selection is not None:
            from molmodmt import trim
            trim(tmp_item, selection=selection, syntaxis=syntaxis, mode='keeping_selection')
        return tmp_item
    else:
        tmp_item = to_parmed_GromacsTopologyFile(item)
        return tmp_item.topology

def to_top(item, selection='all', syntaxis='MDTraj'):

    from molmodmt import extract
    tmp_item = to_parmed_GromacsTopologyFile(item)
    if selection is not 'all':
        tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    tmp_item.save(filename)
    pass

