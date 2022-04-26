from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.HDF5TrajectoryFile')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item = mdtraj_Topology_to_openmm_Topology(item, check=False)

    return tmp_item

