from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='biopython.Seq')
@dep_digest('Bio')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of atoms or structures from form biopython.Seq.

    Parameters
    ----------
    item : biopython.Seq
        Source item.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection to extract.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices to extract.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    biopython.Seq
        Extracted subset in the same form.
    """

    if is_all(atom_indices):

        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        from Bio.Seq import Seq

        tmp_item = Seq(''.join(str(item[index]) for index in atom_indices))

    return tmp_item
