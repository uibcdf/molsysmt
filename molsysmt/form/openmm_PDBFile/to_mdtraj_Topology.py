from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_mdtraj_Topology(item, atom_indices='all', syntax='MolSysMT'):

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item)

    return tmp_item

