from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, digest=False)

    return tmp_item

