from molsysmt._private.digestion import digest

@digest(form='pytraj.Trajectory')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_pytraj_Topology
    from ..pytraj_Topology import to_molsysmt_Topology

    tmp_item = to_pytraj_Topology(item)
    tmp_item = pytraj_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices)

