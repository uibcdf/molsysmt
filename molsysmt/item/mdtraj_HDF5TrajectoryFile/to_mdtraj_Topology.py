from molsysmt._private.digestion import digest

@digest(form='mdtraj.HDF5TrajectoryFile')
def to_mdtraj_Topology(item, atom_indices='all'):

    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item

