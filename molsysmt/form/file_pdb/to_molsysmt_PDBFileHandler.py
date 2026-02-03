from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):

    from molsysmt.native import PDBFileHandler

    return PDBFileHandler(item, io_mode='r')

