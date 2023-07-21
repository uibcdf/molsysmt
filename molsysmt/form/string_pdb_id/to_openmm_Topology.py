from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    from . import to_string_pdb_text
    from ..string_pdb_text import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = string_pdb_text_to_openmm_Topology(tmp_item)

    return tmp_item

