from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.Universe')
@dep_digest('MDAnalysis')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        multiframe=True, skip_digestion=False):
    """
    Converting from MDAnalysis.Universe to file.pdb.

    Parameters
    ----------
    item : MDAnalysis.Universe
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    atom_group = item.atoms if is_all(atom_indices) else item.atoms[atom_indices]
    frames = 'all' if is_all(structure_indices) else structure_indices
    atom_group.write(output_filename, frames=frames, multiframe=multiframe)

    return output_filename
