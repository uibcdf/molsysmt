from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .get import get_box_from_system
    from ..molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology

    box = get_box_from_system(item, structure_indices=structure_indices)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item, box=box)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


