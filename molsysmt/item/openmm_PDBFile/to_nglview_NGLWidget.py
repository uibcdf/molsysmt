from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', syntax='MolSysMT'):

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_Topology_to_nglview_NGLWidget(tmp_item, coordinates=coordinates)

    return tmp_item

