from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:cif')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:cif to mmcif.PdbxContainers.DataContainer.

    Parameters
    ----------
    item : file:cif
        Source item in file:cif form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        Resulting object in mmcif.PdbxContainers.DataContainer form.

    .. versionadded:: 1.0.0
    """

    from mmcif.io.IoAdapterCore import IoAdapterCore
    from smonitor.integrations import context_extra, emit_from_catalog
    from molsysmt._private.smonitor import CATALOG

    io = IoAdapterCore()
    containers = io.readFile(item)

    if len(containers)>1:
        emit_from_catalog(
            CATALOG['warnings']['MultiContainerWarning'],
            extra=context_extra(
                caller='molsysmt.form.file_cif.to_mmcif_PdbxContainers_DataContainer',
                operation='parse',
                extra={'format': 'CIF'},
            ),
        )

    tmp_item = containers[0]

    return tmp_item
