from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:bcif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from mmcif.io.BinaryCifReader import BinaryCifReader

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(item)

    if len(containers)>1:
        import warnings
        warnings.warn('BCIF file has more than one DataContainer; using the first one.', stacklevel=2)

    tmp_item = containers[0]

    return tmp_item
