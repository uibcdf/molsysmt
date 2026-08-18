from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_pdb_id(item, skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to string:pdb_id.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item in mmcif.PdbxContainers.DataContainer form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_id
        Resulting object in string:pdb_id form.

    .. versionadded:: 1.0.0
    """

    return item.getObj('entry').getValue('id')

