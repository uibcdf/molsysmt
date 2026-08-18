from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def to_biopython_SeqRecord(item, group_indices='all', id=None, name=None, description=None, skip_digestion=False):
    """
    Converting from biopython.Seq to biopython.SeqRecord.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    id : object, default=None
        Argument id.
    name : object, default=None
        Argument name.
    description : object, default=None
        Argument description.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.


    .. versionadded:: 1.0.0
    """

    from Bio.SeqRecord import SeqRecord as Bio_SeqRecord
    from .extract import extract

    if id is None:
        id = 'None'
    if name is None:
        name = 'None'
    if description is None:
        description = 'None'

    tmp_item = extract(
        item,
        atom_indices=group_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
    tmp_item = Bio_SeqRecord(tmp_item, id=id, name=name, description=description)

    return tmp_item
