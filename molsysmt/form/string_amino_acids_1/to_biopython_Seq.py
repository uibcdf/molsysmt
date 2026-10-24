from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:amino_acids_1")
@dep_digest("Bio")
def to_biopython_Seq(item, group_indices="all", skip_digestion=False):
    """
    Converting from string:amino_acids_1 to biopython.Seq.


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
    biopython.Seq
        Resulting object in biopython.Seq form.


    Notes
    -----
    Biopython is an optional dependency for this explicitly requested output.
    Native recognition, group selection and one/three-letter translation do not
    require it. Three-letter terminal caps are omitted after group selection.
    Empty selections produce empty Biopython sequence objects.

    .. versionadded:: 1.0.0
    """

    from Bio.Seq import Seq as bio_Seq

    from .extract import extract

    selected = extract(item, group_indices=group_indices, skip_digestion=True)
    return bio_Seq(selected.removeprefix("amino_acids_1:"))
