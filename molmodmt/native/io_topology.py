from .topology import Topology as _Topology

def from_mdtraj(item=None, selection='all', syntaxis='MDTraj'):

    return from_mdtraj_Topology(item.topology, selection=selection, syntaxis=syntaxis)

def from_mdtraj_Topology(item=None, selection='all', syntaxis='MDTraj'):

    from molmodmt import extract as _extract
    return _extract(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Topology(item=None, selection='all', syntaxis='MDTraj'):

    from molmodmt import extract as _extract
    return _extract(item, selection=selection, syntaxis=syntaxis)

def from_openmm_Topology(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, form='mdtraj.Topology', selection=selection, syntaxis=syntaxis)

def from_openmm_Modeller(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, form='mdtraj.Topology', selection=selection, syntaxis=syntaxis)

def from_openmm_Topology(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, form='mdtraj.Topology', selection=selection, syntaxis=syntaxis)

def from_molmod_Structure(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, form='mdtraj.Topology', selection=selection, syntaxis=syntaxis)

def from_pdb(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, 'mdtraj.Topology', selection=selection, syntaxis=syntaxis)

def from_hdf5(item=None, selection='all', syntaxis='MDTraj'):
    from molmodmt import convert as _convert
    return _convert(item, 'mdtraj.Topology', selection=selection, syntaxis=syntaxis)

