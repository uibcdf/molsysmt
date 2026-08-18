from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:gro to openmm.GromacsGroFile.

    Parameters
    ----------
    item : file:gro
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.GromacsGroFile
        Converted molecular system representation.
    """

    from openmm.app import GromacsGroFile
    from ..openmm_GromacsGroFile.extract import extract as extract_openmm_GromacsGroFile

    tmp_item = GromacsGroFile(item)
    tmp_item = extract_openmm_GromacsGroFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

