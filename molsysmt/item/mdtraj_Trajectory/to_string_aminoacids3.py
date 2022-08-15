from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_string_aminoacids3(item, group_indices='all'):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3

    tmp_item = to_mdtraj_Topology(item)
    tmp_item = mdtraj_Topology_to_string_aminoacids3(tmp_item, group_indices=group_indices)

    return tmp_item

