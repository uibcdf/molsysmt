from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_string_amino_acids_1(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Topology to string:amino_acids_1.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_1
        Resulting object in string:amino_acids_1 form.


    .. versionadded:: 1.0.0
    """

    from .to_string_amino_acids_3 import to_string_amino_acids_3
    from molsysmt.form.string_amino_acids_3.to_string_amino_acids_1 import to_string_amino_acids_1 as string_amino_acids_3_to_string_amino_acids_1

    tmp_item = to_string_amino_acids_3(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = string_amino_acids_3_to_string_amino_acids_1(tmp_item, skip_digestion=True)

    return tmp_item

