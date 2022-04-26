from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:h5')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_molsysmt_MolSys
    from .molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                  structure_indices=structure_indices, check=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, check=False)

    return tmp_item

