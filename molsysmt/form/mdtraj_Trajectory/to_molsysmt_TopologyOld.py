from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_molsysmt_TopologyOld as mdtraj_Topology_to_molsysmt_TopologyOld

    tmp_item = to_mdtraj_Topology(item)
    tmp_item = mdtraj_Topology_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

