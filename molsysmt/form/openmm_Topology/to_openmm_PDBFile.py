from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_PDBFile(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from openmm.Topology to openmm.PDBFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.PDBFile
        Resulting object in openmm.PDBFile form.


    .. versionadded:: 1.0.0
    """

    from .to_string_pdb_text import to_string_pdb_text
    from io import StringIO
    from openmm.app import PDBFile

    string_pdb_text = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)

    tmp_io = StringIO(string_pdb_text)
    tmp_item = PDBFile(tmp_io)

    return tmp_item

