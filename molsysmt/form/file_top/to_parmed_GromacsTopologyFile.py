from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:top')
@dep_digest('parmed')
def to_parmed_GromacsTopologyFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:top to parmed.GromacsTopologyFile.

    Parameters
    ----------
    item : file:top
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.GromacsTopologyFile
        Converted molecular system representation.
    """

    import parmed

    tmp_item = parmed.load_file(item)

    return tmp_item
