from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', digest=True):

    from . import to_string_pdb_text
    from ..string_pdb_text import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)
    tmp_item = string_pdb_text_to_molsysmt_Topology(tmp_item, digest=False)

    return tmp_item

