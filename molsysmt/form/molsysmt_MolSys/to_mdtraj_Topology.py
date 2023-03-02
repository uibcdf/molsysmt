from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_mdtraj_Topology(item, atom_indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Topology(item, atom_indices=atom_indices)


