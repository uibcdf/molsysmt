from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from nglview import show_parmed
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False)
    tmp_item = show_parmed(tmp_item)

    return tmp_item

