from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='nglview.NGLWidget')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_string_pdb_text import to_string_pdb_text
    from ..string_pdb_text.to_openmm_Topology import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = string_pdb_text_to_openmm_Topology(tmp_item, skip_digestion=True)

    return tmp_item

