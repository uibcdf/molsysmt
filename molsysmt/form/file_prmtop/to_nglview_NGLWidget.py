from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None, digest=True):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, digest=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, digest=False)

    return tmp_item


