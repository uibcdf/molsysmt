from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'nglview.NGLWidget')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_string_pdb_text
    from ..string_pdb_text import to_molsysmt_Topology as string_pdb_text_to_molsysmt_Topology

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = string_pdb_text_to_molsysmt_Topology(tmp_item, check=False)

    return tmp_item

