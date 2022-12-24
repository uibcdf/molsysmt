from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_mdtraj_Topology(item, atom_indices='all', syntax='MolSysMT', digest=True):

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item, digest=False)

    return tmp_item

