from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None, skip_digestion=False):

    from . import to_string_pdb_text as to_string_pdb_text
    from ..string_pdb_text import to_nglview_NGLWidget as string_pdb_text_to_nglview_NGLWidget

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)
    tmp_item = string_pdb_text_to_nglview_NGLWidget(tmp_item, skip_digestion=True)

    return tmp_item

