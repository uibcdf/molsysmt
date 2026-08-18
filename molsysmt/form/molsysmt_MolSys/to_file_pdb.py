from molsysmt._private.argdigest import *

@arg_digest(form='molsysmt.MolSys')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from molsysmt.MolSys to file:pdb.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.

    .. versionadded:: 1.0.0
    """

    from .to_string_pdb_text import to_string_pdb_text

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    with open(output_filename, "w") as fff:
        fff.write(tmp_item)

    return output_filename

