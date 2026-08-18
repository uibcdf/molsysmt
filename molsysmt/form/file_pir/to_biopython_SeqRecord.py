from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, skip_digestion=False):
    """
    Converting from file:pir to biopython.SeqRecord.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.


    .. versionadded:: 1.0.0
    """

    from Bio import SeqIO

    records = list(SeqIO.parse(item, 'pir'))

    if len(records) == 1:
        return records[0]

    return records
