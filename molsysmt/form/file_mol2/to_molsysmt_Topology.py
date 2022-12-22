from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_molsysmt_Topology(item, atom_indices='all', digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item = mdtraj_Topology_to_molsysmt_Topology(tmp_item, digest=False)

    return tmp_item

