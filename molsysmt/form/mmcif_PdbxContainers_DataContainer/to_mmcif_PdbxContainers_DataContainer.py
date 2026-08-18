from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to mmcif.PdbxContainers.DataContainer.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item in mmcif.PdbxContainers.DataContainer form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mmcif.PdbxContainers.DataContainer
        Resulting object in mmcif.PdbxContainers.DataContainer form.

    .. versionadded:: 1.0.0
    """

    if isinstance(item, str):
        from mmcif.io.PdbxReader import PdbxReader
        import gzip
        
        if item.endswith('.gz'):
            with gzip.open(item, 'rt') as f:
                reader = PdbxReader(f)
                data = []
                reader.read(data)
                tmp_item = data[0]
        else:
            with open(item, 'r') as f:
                reader = PdbxReader(f)
                data = []
                reader.read(data)
                tmp_item = data[0]
    else:
        tmp_item = item

    from molsysmt._private.variables import is_all
    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, 
                           copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item
