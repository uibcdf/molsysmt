from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_mdtraj_Topology(item, atom_indices='all', syntax='MolSysMT', skip_digestion=False):

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item

