from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_molsysmt_TopologyOld(item, atom_indices='all', skip_digestion=False):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_molsysmt_TopologyOld as mdtraj_Topology_to_molsysmt_TopologyOld

    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

