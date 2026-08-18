from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_biopython_Seq(item, skip_digestion=False):
    """
    Converting from file:pir to biopython.Seq.

    Parameters
    ----------
    item : file:pir
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Converted molecular system representation.
    """

    from .to_biopython_SeqRecord import to_biopython_SeqRecord

    tmp_item = to_biopython_SeqRecord(item, skip_digestion=True)

    if isinstance(tmp_item, list):
        return [record.seq for record in tmp_item]

    return tmp_item.seq
