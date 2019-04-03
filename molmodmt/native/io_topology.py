from .topology import Topology as _Topology

def from_mdtraj_Topology(item=None, selection=None, syntaxis='mdtraj'):

    from molmodmt.formats.classes.api_mdtraj_Topology import to_openmm_Topology as _to_openmm_Topology

    return _to_openmm_Topology(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Topology(item=None, selection=None, syntaxis='mdtraj'):

    from molmodmt.formats.classes.api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    return _to_mdtraj_Topology(item, selection=selection, syntaxis=syntaxis)

def from_openmm_Topology(item=None, selection=None, syntaxis='mdtraj'):
    from molmodmt import extract as _extract
    return _extract(item, selection=selection, syntaxis=syntaxis)

def from_molmod_Structure(item=None, selection=None, syntaxis='mdtraj'):
    from molmodmt import extract as _extract
    return _extract(item.topology, selection=selection, syntaxis=syntaxis)

