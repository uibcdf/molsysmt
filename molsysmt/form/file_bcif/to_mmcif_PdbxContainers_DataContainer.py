from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:bcif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:bcif to mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        Resulting object in mmcif.PdbxContainers.DataContainer form.


    .. versionadded:: 1.0.0
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
                caller='molsysmt.form.file_bcif.to_mmcif_PdbxContainers_DataContainer',
                operation='parse',
                extra={'format': 'BCIF'},
            ),
        )

    tmp_item = containers[0]

    return tmp_item
