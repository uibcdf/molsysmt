from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="biopython.Seq")
@dep_digest("Bio")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting selected sequence positions from form biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Source sequence.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Sequence-position indices to include, retaining the legacy adapter
        parameter name. These are group positions, not an atomic topology.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Unused for this sequence-only form, which has no structures.
    copy_if_all : bool, default=True
        Whether an all-position extraction creates an independent copy.
        If False, return the source object for that extraction.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices):
        if copy_if_all:
            from .copy import copy

            tmp_item = copy(item, skip_digestion=True)
        else:
            tmp_item = item
    else:
        from Bio.Seq import Seq

        tmp_item = Seq("".join(str(item[index]) for index in atom_indices))

    return tmp_item
