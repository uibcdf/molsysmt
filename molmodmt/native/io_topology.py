from .topology import Topology as _Topology

def from_mdtraj(item=None, atom_indices=None, frame_indices=None):

    return from_mdtraj_Topology(item.topology, atom_indices=None, frame_indices=None)

def from_mdtraj_Topology(item=None, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    return extract(item, selection=atom_indices)

def to_mdtraj_Topology(item=None, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    return extract(item, selection=atom_indices)

def from_openmm_Topology(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, form='mdtraj.Topology', selection=atom_indices)

def from_openmm_Modeller(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, form='mdtraj.Topology', selection=atom_indices)

def from_openmm_Topology(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, form='mdtraj.Topology', selection=atom_indices)

def from_molmod_Structure(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, form='mdtraj.Topology', selection=atom_indices)

def from_pdb(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, 'mdtraj.Topology', selection=atom_indices)

def from_hdf5(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, 'mdtraj.Topology', selection=atom_indices)

def from_top(item=None, atom_indices=None, frame_indices=None):
    from molmodmt import convert
    return convert(item, 'mdtraj.Topology', selection=atom_indices)
