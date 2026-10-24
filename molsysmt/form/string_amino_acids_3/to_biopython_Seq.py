from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_3")
@dep_digest("Bio")
def to_biopython_Seq(
    item, group_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from string:amino_acids_3 to biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Sequence text in the declared alphabet; an explicit amino_acids prefix is supported.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Original group positions in requested order; repetitions are retained.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    Notes
    -----
    Biopython is an optional dependency for this explicitly requested output.
    Native recognition, group selection and one/three-letter translation do not
    require it. Three-letter terminal caps are omitted after group selection.
    Empty selections produce empty Biopython sequence objects.

    Examples
    --------
    >>> str(to_biopython_Seq('AlaGly'))
    'AG'
    >>> str(to_biopython_Seq('amino_acids_3:AceAlaGlyNme', group_indices=[2, 1]))
    'GA'

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.string_amino_acids_1.to_biopython_Seq import (
        to_biopython_Seq as to_sequence,
    )

    from .extract import extract
    from .to_string_amino_acids_1 import to_string_amino_acids_1

    selected = extract(
        item,
        group_indices=group_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    letters = to_string_amino_acids_1(selected, skip_digestion=True)
    return to_sequence(letters, skip_digestion=True)
