from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:cif.gz")
def to_mmcif_PdbxContainers_DataContainer(
    item, atom_indices="all", skip_digestion=False
):
    """Converting a compressed CIF file into its first mmCIF data container.

    Parameters
    ----------
    item : str or pathlib.Path
        Path to the compressed CIF file to read.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based), retained for adapter compatibility. Parsing
        returns the whole data container; native conversion applies selection.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        First parsed data container. Multiple containers emit the existing
        catalog warning before returning the first one.

    Notes
    -----
    Each read uses an independent temporary directory for decompression and
    parser artifacts. The input directory need not be writable, and existing
    neighboring files are preserved. Temporary artifacts are removed on success
    or failure. Parsing still uses the installed mmCIF backend and is eager;
    this does not introduce a streaming molecular-system reader.

    Examples
    --------
    >>> import gzip
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     source = Path(directory) / "example.cif.gz"
    ...     with gzip.open(source, "wt") as handle:
    ...         _ = handle.write("data_example\\n_entry.id example\\n#\\n")
    ...     container = to_mmcif_PdbxContainers_DataContainer(source)
    >>> container.getName()
    'example'


    .. versionadded:: 1.0.0
    """

    from tempfile import TemporaryDirectory

    from mmcif.io import IoAdapter
    from smonitor.integrations import context_extra, emit_from_catalog

    from molsysmt._private.smonitor import CATALOG

    io = IoAdapter()
    with TemporaryDirectory(prefix="molsysmt-cif-") as directory:
        containers = io.readFile(item, outDirPath=directory)

    if len(containers) > 1:
        emit_from_catalog(
            CATALOG["warnings"]["MultiContainerWarning"],
            extra=context_extra(
                caller="molsysmt.form.file_cif_gz.to_mmcif_PdbxContainers_DataContainer",
                operation="parse",
                extra={"format": "CIF_GZ"},
            ),
        )

    tmp_item = containers[0]

    return tmp_item
