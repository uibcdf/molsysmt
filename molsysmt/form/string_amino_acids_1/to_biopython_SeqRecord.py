from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:amino_acids_1')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, group_indices='all', skip_digestion=False):
    """
    Converting from string:amino_acids_1 to biopython.SeqRecord.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.


    .. versionadded:: 1.0.0
    """

    from .to_biopython_Seq import to_biopython_Seq
    from molsysmt.form.biopython_Seq.to_biopython_SeqRecord import (
        to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord,
    )

    tmp_item = to_biopython_Seq(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = biopython_Seq_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item
