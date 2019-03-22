from .topology import Topology as _Topology

def from_mdtraj_Topology(item=None):

    from molmodmt.formats.classes.api_mdtraj_Topology import to_openmm_Topology as _to_openmm_Topology

    return _to_openmm_Topology(item)

def to_mdtraj_Topology(item=None):

    from molmodmt.formats.classes.api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    return _to_mdtraj_Topology(item)

def from_openmm_Topology(item=None):

    return item

def from_molmod_Structure(item=None):

    return item.topology

