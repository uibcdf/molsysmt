from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, skip_digestion=False):
    """
    Converting from file:pir to biopython.SeqRecord.

    Parameters
    ----------
    item : file:pir
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.SeqRecord
        Converted molecular system representation.
    """

    from Bio import SeqIO

    records = list(SeqIO.parse(item, 'pir'))

    if len(records) == 1:
        return records[0]

    return records
