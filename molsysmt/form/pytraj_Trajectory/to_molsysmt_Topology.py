from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='pytraj.Trajectory')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_pytraj_Topology import to_pytraj_Topology
    from ..pytraj_Topology.to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = to_pytraj_Topology(item, skip_digestion=True)
    tmp_item = pytraj_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=False)

    return tmp_item

