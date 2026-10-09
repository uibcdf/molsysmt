from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

__all__ = ["get_group_index_from_group", "get_group_name_from_group"]


@arg_digest(form="biopython.Seq")
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    """Getting source sequence-position indices from a Biopython sequence.

    Parameters
    ----------
    item : biopython.Seq
        Sequence supplying the ordered group positions.
    indices : str or list of int, default='all'
        Positions to query; supplied order and repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int
        Source sequence positions, without renumbering a selected subset.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> get_group_index_from_group(Seq('aGx'), indices=[2, 0])
    [2, 0]

    .. versionadded:: 1.0.0
    """
    output = list(range(len(item)))
    return output if is_all(indices) else [output[index] for index in indices]


@arg_digest(form="biopython.Seq")
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    """Getting sequence characters as group names from a Biopython sequence.

    Parameters
    ----------
    item : biopython.Seq
        Sequence supplying the ordered group positions.
    indices : str or list of int, default='all'
        Positions to query; supplied order and repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str or none
        Sequence characters preserving their original case and alphabet.
        No conversion to three-letter names or chemical assignments is inferred.
        Undefined or partially defined sequences return ``None``; a defined
        empty sequence returns an empty list.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> get_group_name_from_group(Seq('aGx'), indices=[2, 0])
    ['x', 'a']

    .. versionadded:: 1.0.0
    """
    if not item.defined:
        return None
    output = list(str(item))
    return output if is_all(indices) else [output[index] for index in indices]
