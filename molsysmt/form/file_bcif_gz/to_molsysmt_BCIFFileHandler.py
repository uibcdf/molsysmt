from molsysmt._private.digestion import digest

@digest(form='file:cif.gz')
def to_molsysmt_CIFFileHandler(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import CIFFileHandler

    return CIFFileHandler(item, io_mode='r')
