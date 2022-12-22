from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_mdtraj_Topology(item, atom_indices='all', digest=True):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = to_molsysmt_Topology(item, digest=False)
    tmp_item = molsysmt_Topology_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

