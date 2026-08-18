from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError, InternalAlgorithmError, FormatError

@arg_digest(form='file:bcif.gz')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:bcif.gz to mmcif.PdbxContainers.DataContainer.

    Parameters
    ----------
    item : file:bcif.gz
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        Converted molecular system representation.
    """

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
        raise FormatError("PDB ID has no DataContainer", caller="molsysmt.form.file_bcif_gz.to_mmcif_PdbxContainers_DataContainer")

    tmp_item = containers[0]

    return tmp_item
