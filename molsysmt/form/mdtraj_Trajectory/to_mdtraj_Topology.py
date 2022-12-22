from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_mdtraj_Topology(item, atom_indices='all', digest=True):

    from ..mdtraj_Topology import extract as extract_mdtraj_Topology

    tmp_item = item.topology
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

