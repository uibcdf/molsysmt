from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, skip_digestion=False):
    """
    Converting from openmm.Topology to file.pdb.

    Parameters
    ----------
    item : openmm.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.pdb
        Converted molecular system representation.
    """

    from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)

    with open(output_filename, 'w') as file:
        file.write(string_pdb_text)
    tmp_item = output_filename

    return tmp_item

