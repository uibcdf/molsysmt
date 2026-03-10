from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:bcif.gz')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    from mmcif.io.BinaryCifReader import BinaryCifReader
    from smonitor.integrations import context_extra, emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(item)

    if len(containers)>1:
        emit_from_catalog(
            CATALOG['warnings']['MultiContainerWarning'],
            extra=context_extra(
                caller='molsysmt.form.file_bcif_gz.to_mmcif_PdbxContainers_DataContainer',
                operation='parse',
                extra={'format': 'BCIF_GZ'},
            ),
        )

    if len(containers)==0:
        raise ValueError('The PDB ID does not have any DataContainer')

    tmp_item = containers[0]

    return tmp_item
