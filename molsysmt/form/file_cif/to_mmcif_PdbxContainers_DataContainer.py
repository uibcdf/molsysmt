from molsysmt._private.digestion import digest

@digest(form='file:cif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from mmcif.io.IoAdapterCore import IoAdapterCore

    io = IoAdapterCore()
    containers = io.readFile(item)

    if len(containers)>1:
        import warnings
        warnings.warn('BCIF file has more than one DataContainer; using the first one.', stacklevel=2)

    tmp_item = containers[0]

    return tmp_item
