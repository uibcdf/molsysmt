from .structure import Structure as _Structure
# The native structure object is the ParmEd structure object.

def from_gromacs_Topology(item=None):

    from parmed.gromacs import GromacsTopologyFile as _parmed_from_gromacs
    from molmodmt.fix_topological_properties import fix_chains as _fix_chains
    tmp_molmod_Structure=_parmed_from_gromacs(item)
    _fix_chains(tmp_molmod_Structure)
    return tmp_molmod_Structure

def from_openmm_Topology(item=None):

    from parmed import load_topology as _parmed_load_topology

    return _parmed_load_topology(item)

def from_molmod_Topology(item=None):

    from parmed import load_topology as _parmed_load_topology

    return _parmed_load_topology(item)
