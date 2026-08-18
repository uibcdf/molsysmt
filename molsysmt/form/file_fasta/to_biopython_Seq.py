from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:fasta')
@dep_digest('Bio')
def to_biopython_Seq(item, skip_digestion=False):
    """
    Converting from file:fasta to biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    from .to_biopython_SeqRecord import to_biopython_SeqRecord

    tmp_item = to_biopython_SeqRecord(item, skip_digestion=True)

    if isinstance(tmp_item, list):
        return [record.seq for record in tmp_item]

    return tmp_item.seq
