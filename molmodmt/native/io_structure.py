from .structure import Structure as _Structure
# The native structure object is the ParmEd structure object.

def from_gromacs_Topology(item=None, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    from molmodmt.fix_topological_properties import fix_chains as _fix_chains
    tmp_item=_parmed_from_gromacs(item)
    _fix_chains(tmp_item)
    tmp_item=_extract(tmp_item,selection=selection,syntaxis=syntaxis)

    return tmp_item

def from_openmm_Topology(item=None, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from parmed import load_topology as _parmed_load_topology

    tmp_item=_parmed_load_topology(item)
    tmp_item=_extract(tmp_item,selection=selection,syntaxis=syntaxis)
    return tmp_item

def from_molmod_Topology(item=None, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from parmed import load_topology as _parmed_load_topology
    tmp_item=_parmed_load_topology(item)
    tmp_item=_extract(tmp_item,selection=selection,syntaxis=syntaxis)
    return tmp_item
