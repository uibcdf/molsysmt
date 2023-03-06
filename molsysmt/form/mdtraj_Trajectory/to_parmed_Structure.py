from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_parmed_Structures as openmm_Topology_to_parmed_Structures

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_parmed_Structures(tmp_item)

    return tmp_item

def _to_parmed_Structure(item, atom_indices='all', structure_indices='all'):

    return to_parmed_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

