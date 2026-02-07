from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:bcif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from mmcif.io.BinaryCifReader import BinaryCifReader
    from smonitor.integrations import emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(item)

    if len(containers)>1:
        emit_from_catalog(CATALOG['warnings']['MultiContainerWarning'], extra={'caller': 'to_mmcif_PdbxContainers_DataContainer', 'format': 'BCIF'})

    tmp_item = containers[0]

    return tmp_item
