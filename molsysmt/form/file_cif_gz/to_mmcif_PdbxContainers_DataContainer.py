from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:cif.gz')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from mmcif.io.IoAdapterCore import IoAdapterCore
    from smonitor.integrations import emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    io = IoAdapterCore()
    containers = io.readFile(item)

    if len(containers)>1:
        emit_from_catalog(CATALOG['warnings']['MultiContainerWarning'], extra={'caller': 'to_mmcif_PdbxContainers_DataContainer', 'format': 'CIF_GZ'})

    tmp_item = containers[0]

    return tmp_item
