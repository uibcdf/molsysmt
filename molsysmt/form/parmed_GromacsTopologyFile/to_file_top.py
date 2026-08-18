from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.GromacsTopologyFile')
@dep_digest('parmed')
def to_file_top(item, atom_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to file.top.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.top
        Converted molecular system representation.
    """

    item.write(output_filename)

    return output_filename
