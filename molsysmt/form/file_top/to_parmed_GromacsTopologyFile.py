from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:top')
@dep_digest('parmed')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:top to parmed.GromacsTopologyFile.


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
    parmed.GromacsTopologyFile
        Resulting object in parmed.GromacsTopologyFile form.


    .. versionadded:: 1.0.0
    """

    import parmed

    tmp_item = parmed.load_file(item)

    return tmp_item
