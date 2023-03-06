from molsysmt._private.digestion import digest

@digest(form='mdtraj.HDF5TrajectoryFile')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

def _to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)

