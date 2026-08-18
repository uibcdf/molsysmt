from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, skip_digestion=False):
    """
    Converting from openmm.Topology to file:pdb.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
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

    from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)

    with open(output_filename, 'w') as file:
        file.write(string_pdb_text)
    tmp_item = output_filename

    return tmp_item

