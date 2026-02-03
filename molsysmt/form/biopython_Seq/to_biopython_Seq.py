from molsysmt._private.digestion import arg_digest

@arg_digest(form='biopython.Seq')
def to_biopython_Seq(item, group_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, group_indices=group_indices, copy_if_all=copy_if_all, skip_digestion=True)

