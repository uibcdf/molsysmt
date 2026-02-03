from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:amino_acids_1')
def to_string_amino_acids_1(item, group_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

