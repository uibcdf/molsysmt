from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_biopython_Seq(item, group_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Argument item.
    group_indices : int, list, tuple, or numpy.ndarray, default='all'
        Argument group_indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    from .to_string_amino_acids_1 import to_string_amino_acids_1
    from molsysmt.form.string_amino_acids_1.to_biopython_Seq import to_biopython_Seq as string_amino_acids_1_to_biopython_Seq

    tmp_item = to_string_amino_acids_1(item, group_indices=group_indices, skip_digestion=True)
    tmp_item = string_amino_acids_1_to_biopython_Seq(tmp_item, skip_digestion=True)

    return tmp_item
