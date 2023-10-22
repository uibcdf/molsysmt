from molsysmt._private.digestion import digest

@digest(form='file:msmh5')
def to_molsysmt_MSMH5FileHandler(item, atom_indices='all'):

    from molsysmt.native import MSMH5FileHandler

    return MSMH5FileHandler(item, io_mode='r')
