from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='file:fasta')
def to_file_fasta(item, atom_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Converting from file:fasta to file:fasta.

    Parameters
    ----------
    item : file:fasta
        Source item in file:fasta form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:fasta
        Resulting object in file:fasta form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, output_filename=output_filename,
                   copy_if_all=copy_if_all, skip_digestion=True)
