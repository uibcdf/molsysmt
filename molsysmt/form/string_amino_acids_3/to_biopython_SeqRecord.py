from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
@dep_digest("Bio")
def to_biopython_SeqRecord(item, group_indices="all", skip_digestion=False):
    """
    Converting from string:amino_acids_3 to biopython.SeqRecord.


    Parameters
    ----------
    item : molecular system
        Sequence text in the declared alphabet; an explicit amino_acids prefix is supported.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.SeqRecord
        Resulting object in biopython.SeqRecord form.


    Notes
    -----
    Biopython is an optional dependency for this explicitly requested output.
    Native recognition, group selection and one/three-letter translation do not
    require it. Three-letter terminal caps are omitted after group selection.
    Empty selections produce empty Biopython sequence objects.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.biopython_Seq.to_biopython_SeqRecord import (
        to_biopython_SeqRecord as to_record,
    )

    from .to_biopython_Seq import to_biopython_Seq

    sequence = to_biopython_Seq(item, group_indices=group_indices, skip_digestion=True)
    return to_record(sequence, skip_digestion=True)
