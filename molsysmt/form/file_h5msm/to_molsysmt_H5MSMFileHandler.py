from molsysmt._private.digestion import digest

@digest(form='file:h5msm')
def to_molsysmt_H5MSMFileHandler(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import H5MSMFileHandler

    return H5MSMFileHandler(item, io_mode='r')
