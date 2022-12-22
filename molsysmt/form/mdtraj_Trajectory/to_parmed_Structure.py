from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_parmed_Structures as openmm_Topology_to_parmed_Structures

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item = openmm_Topology_to_parmed_Structures(tmp_item, digest=False)

    return tmp_item

