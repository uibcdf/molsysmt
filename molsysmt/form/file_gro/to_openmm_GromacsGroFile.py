from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to openmm.GromacsGroFile.


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
    openmm.GromacsGroFile
        Resulting object in openmm.GromacsGroFile form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile.extract import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

