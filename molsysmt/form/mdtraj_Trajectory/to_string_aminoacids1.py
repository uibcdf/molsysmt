from molsysmt._private.digestion import digest_item, digest_group_indices

def to_string_aminoacids1(item, group_indices='all', check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        group_indices = digest_group_indices(group_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_string_aminoacids1 as mdtraj_Topology_to_string_aminoacids1

    tmp_item = to_mdtraj_Topology(item, check=False)
    tmp_item = mdtraj_Topology_to_string_aminoacids1(tmp_item, group_indices=group_indices, check=False)

    return tmp_item

