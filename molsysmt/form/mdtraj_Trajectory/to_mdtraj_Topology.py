from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

