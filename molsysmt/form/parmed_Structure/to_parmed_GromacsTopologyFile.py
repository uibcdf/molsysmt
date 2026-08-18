from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : parmed.Structure
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.GromacsTopologyFile
        Converted molecular system representation.
    """

    from . import extract
    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)

    return tmp_item

