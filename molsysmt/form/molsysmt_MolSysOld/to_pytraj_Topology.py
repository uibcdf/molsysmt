from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_pytraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

