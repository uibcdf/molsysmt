from molsysmt._private.argdigest import arg_digest

@arg_digest(form='biopython.Seq')
def to_biopython_SeqRecord(item, group_indices='all', id=None, name=None, description=None, skip_digestion=False):
    """
    Converting from biopython.Seq to biopython.SeqRecord.

    Parameters
    ----------
    item : biopython.Seq
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.SeqRecord
        Converted molecular system representation.
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
