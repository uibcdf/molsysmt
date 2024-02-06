from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def to_molsysmt_TopologyOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_string_pdb_text
    from ..string_pdb_text import to_molsysmt_TopologyOld as string_pdb_text_to_molsysmt_TopologyOld

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    tmp_item = string_pdb_text_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices,
                                                       structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

