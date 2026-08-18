from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.GromacsTopologyFile')
@dep_digest('parmed')
def to_file_top(item, atom_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from parmed.GromacsTopologyFile to file:top.

    Parameters
    ----------
    item : parmed.GromacsTopologyFile
        Source item in parmed.GromacsTopologyFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:top
        Resulting object in file:top form.

    .. versionadded:: 1.0.0
    """

    item.write(output_filename)

    return output_filename
