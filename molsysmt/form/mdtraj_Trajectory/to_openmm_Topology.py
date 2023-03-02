from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_openmm_Topology(item, atom_indices='all'):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices)
    tmp_item = mdtraj_Topology_to_openmm_Topology(tmp_item)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

