from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_mdtraj_Topology(item, atom_indices='all', digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import openmm_Topology_to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, digest=False)
    tmp_item = openmm_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, digest=False)

    return tmp_item

