from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from nglview import show_molsysmt

    tmp_item = show_molsysmt(item, selection=atom_indices, structure_indices=structure_indices)

    return tmp_item

