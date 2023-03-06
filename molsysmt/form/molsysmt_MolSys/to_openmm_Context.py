from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_openmm_Context(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Context as openmm_Topology_to_openmm_Context

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_openmm_Context(tmp_item)

    return tmp_item

def _to_openmm_Context(item, atom_indices='all', structure_indices='all'):

    return to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)

