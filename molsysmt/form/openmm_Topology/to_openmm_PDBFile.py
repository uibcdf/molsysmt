from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_PDBFile(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from openmm.Topology to openmm.PDBFile.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.PDBFile
        Resulting object in openmm.PDBFile form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.string_pdb_text.to_string_pdb_text import to_string_pdb_text
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)

    tmp_io = StringIO()
    tmp_io.read(string_pdb_text)
    tmp_item = PDBFile.readFile(tmp_io)

    return tmp_item

