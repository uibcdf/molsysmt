from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_GROFileHandler(item, skip_digestion=False):

    from molsysmt.native import GROFileHandler

    return GROFileHandler(item, io_mode='r')

