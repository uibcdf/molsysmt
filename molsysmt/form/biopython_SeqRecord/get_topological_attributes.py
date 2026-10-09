from molsysmt._private.argdigest import arg_digest

__all__ = ["get_group_index_from_group", "get_group_name_from_group"]


@arg_digest(form="biopython.SeqRecord")
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    """Getting source sequence-position indices from a Biopython record.

    Parameters
    ----------
    item : biopython.SeqRecord
        Record whose sequence supplies the ordered group positions.
    indices : str or list of int, default='all'
        Positions to query; supplied order and repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Source sequence positions, without renumbering a selected subset.
        A record without a sequence returns ``None``.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> from Bio.SeqRecord import SeqRecord
    >>> get_group_index_from_group(SeqRecord(Seq('aGx')), indices=[2, 0])
    [2, 0]

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.biopython_Seq.get_topological_attributes import (
        get_group_index_from_group,
    )

    if item.seq is None:
        return None
    return get_group_index_from_group(item.seq, indices=indices, skip_digestion=True)


@arg_digest(form="biopython.SeqRecord")
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    """Getting sequence characters as group names from a Biopython record.

    Parameters
    ----------
    item : biopython.SeqRecord
        Record whose sequence supplies the ordered group positions.
    indices : str or list of int, default='all'
        Positions to query; supplied order and repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str or none
        Sequence characters preserving their original case and alphabet.
        No conversion to three-letter names or chemical assignments is inferred.
        Missing, undefined or partially defined sequences return ``None``; a
        defined empty sequence returns an empty list.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> from Bio.SeqRecord import SeqRecord
    >>> get_group_name_from_group(SeqRecord(Seq('aGx')), indices=[2, 0])
    ['x', 'a']

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.biopython_Seq.get_topological_attributes import (
        get_group_name_from_group,
    )

    if item.seq is None:
        return None
    return get_group_name_from_group(item.seq, indices=indices, skip_digestion=True)
