from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def copy(item, skip_digestion=False):

    return item.copy()

