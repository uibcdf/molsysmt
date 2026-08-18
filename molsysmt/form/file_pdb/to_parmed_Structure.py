from depdigest import dep_digest
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
@dep_digest('parmed')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to parmed.Structure.


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
    parmed.Structure
        Resulting object in parmed.Structure form.


    .. versionadded:: 1.0.0
    """

    from parmed import load_file

    from molsysmt.form.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=False)

    return tmp_item

