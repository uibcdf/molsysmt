from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from . import to_pytraj_Topology
    from ..pytraj_Topology import to_molsysmt_TopologyOld

    tmp_item = to_pytraj_Topology(item)
    tmp_item = pytraj_Topology_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

