from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to openmm.PDBFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.PDBFile
        Resulting object in openmm.PDBFile form.


    .. versionadded:: 1.0.0
    """

    from io import StringIO
    from openmm.app.pdbfile import PDBFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = StringIO(tmp_item)
    tmp_item = PDBFile(tmp_item)

    return tmp_item

