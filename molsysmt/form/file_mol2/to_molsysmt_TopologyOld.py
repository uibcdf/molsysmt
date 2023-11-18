from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_molsysmt_TopologyOld as mdtraj_Topology_to_molsysmt_TopologyOld

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices)
    tmp_item = mdtraj_Topology_to_molsysmt_TopologyOld(tmp_item)

    return tmp_item

