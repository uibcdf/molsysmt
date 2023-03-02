from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_nglview_NGLWidget(item, coordinates, box, atom_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, coordinates=coordinates, box=box, atom_indices=atom_indices)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

def _to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

    return to_nglview_NGLWidget(item, coordinates=coordinates, box=box, atom_indices=atom_indices)

