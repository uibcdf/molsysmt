from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_string_amino_acids_1(item, skip_digestion=False):
    """
    Converting from file:pir to string:amino_acids_1.

    Parameters
    ----------
    item : file:pir
        Source item in file:pir form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.

    .. versionadded:: 1.0.0
    """

    from .to_biopython_SeqRecord import to_biopython_SeqRecord

    tmp_item = to_biopython_SeqRecord(item, skip_digestion=True)

    if isinstance(tmp_item, list):
        return [str(record.seq) for record in tmp_item]

    return str(tmp_item.seq)
