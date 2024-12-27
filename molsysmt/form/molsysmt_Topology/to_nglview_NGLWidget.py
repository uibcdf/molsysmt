from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_nglview_NGLWidget(item, coordinates, box, atom_indices='all', skip_digestion=False):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, coordinates=coordinates, box=box, atom_indices=atom_indices)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)

    return tmp_item

