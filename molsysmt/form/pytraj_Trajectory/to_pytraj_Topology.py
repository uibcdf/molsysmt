from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all', digest=True):

    from ..pytraj_Topology import extract as extract_pytraj_Topology

    tmp_item = item.topology
    tmp_item = extract_pytraj_Topology(item, atom_indices=atom_indices, copy_if_all=False, digest=False)

    return tmp_item

