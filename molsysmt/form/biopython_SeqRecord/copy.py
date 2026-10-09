from molsysmt._private.argdigest import arg_digest


@arg_digest(form="biopython.SeqRecord")
def copy(item, skip_digestion=False):
    """Creating an independent copy of a Biopython sequence record.

    Parameters
    ----------
    item : biopython.SeqRecord
        Source record, including its sequence and nested metadata to copy.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Independent object preserving source content and record metadata.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> from Bio.SeqRecord import SeqRecord
    >>> molsys = SeqRecord(Seq('AGX'), id='chain-z')
    >>> copied = copy(molsys)
    >>> copied is molsys
    False
    >>> str(copied.seq)
    'AGX'

    .. versionadded:: 1.0.0
    """
    from copy import deepcopy

    return deepcopy(item)
