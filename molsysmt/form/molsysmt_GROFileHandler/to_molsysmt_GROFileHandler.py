from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.GROFileHandler')
def to_molsysmt_GROFileHandler(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

