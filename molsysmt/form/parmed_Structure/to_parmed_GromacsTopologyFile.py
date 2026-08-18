from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : parmed.Structure
        Source item in parmed.Structure form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.GromacsTopologyFile
        Resulting object in parmed.GromacsTopologyFile form.

    .. versionadded:: 1.0.0
    """

    from . import extract
    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)

    return tmp_item

