from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory')
def to_pytraj_Topology(item, atom_indices='all'):

    from ..pytraj_Topology import extract as extract_pytraj_Topology

    tmp_item = item.topology
    tmp_item = extract_pytraj_Topology(item, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item

def _to_pytraj_Topology(item, atom_indices='all', structure_indices='all'):

    return to_pytraj_Topology(item, atom_indices=atom_indices)

