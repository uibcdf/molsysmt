from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Universe')
@dep_digest('MDAnalysis')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        multiframe=True, skip_digestion=False):
    """
    Converting from MDAnalysis.Universe to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    multiframe : object, default=True
        Argument multiframe.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    .. versionadded:: 1.0.0
    """

    atom_group = item.atoms if is_all(atom_indices) else item.atoms[atom_indices]
    frames = 'all' if is_all(structure_indices) else structure_indices
    atom_group.write(output_filename, frames=frames, multiframe=multiframe)

    return output_filename
