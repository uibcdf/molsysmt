from molsysmt._private.digestion import digest

@digest(form='file:cif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from .. import CIFFileHandler

    return CIFFileHandler(item, io_mode='r')
