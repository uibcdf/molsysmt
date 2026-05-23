from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='cupy_ndarray')
def copy(item, skip_digestion=False):
    return item.copy()
