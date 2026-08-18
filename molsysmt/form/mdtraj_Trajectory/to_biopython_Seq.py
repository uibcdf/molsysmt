from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='mdtraj.Trajectory')
def to_biopython_Seq(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to biopython.Seq.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    biopython.Seq
        Resulting object in biopython.Seq form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.string_amino_acids_1.to_string_amino_acids_1 import to_string_amino_acids_1
    from molsysmt.form.string_amino_acids_1.to_biopython_Seq import to_biopython_Seq as string_amino_acids_1_to_biopython_Seq

    tmp_item = to_string_amino_acids_1(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    tmp_item = string_amino_acids_1_to_biopython_Seq(tmp_item, skip_digestion=True)

    return tmp_item

