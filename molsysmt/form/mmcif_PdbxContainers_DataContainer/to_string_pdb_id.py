from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_pdb_id(item, skip_digestion=False):
    """
    Converting from mmcif.PdbxContainers.DataContainer to string.pdb.id.

    Parameters
    ----------
    item : mmcif.PdbxContainers.DataContainer
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.pdb.id
        Converted molecular system representation.
    """

    return item.getObj('entry').getValue('id')

