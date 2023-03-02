from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_mdtraj_Topology(item, atom_indices='all'):

    from . import to_openmm_Topology
    from ..openmm_Topology import openmm_Topology_to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices)

    return tmp_item

def _to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    return to_mdtraj_Topology(item, atom_indices=atom_indices)

