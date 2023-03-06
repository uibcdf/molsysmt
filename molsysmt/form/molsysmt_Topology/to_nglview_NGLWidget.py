from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_nglview_NGLWidget(item, coordinates, box, atom_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, coordinates=coordinates, box=box, atom_indices=atom_indices)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

def _to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    return to_nglview_NGLWidget(item, coordinates=coordinates, box=box, atom_indices=atom_indices)

