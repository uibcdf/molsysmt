from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:crd')
def to_openmm_CharmmCrdFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:crd to openmm.CharmmCrdFile.


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
    openmm.CharmmCrdFile
        Resulting object in openmm.CharmmCrdFile form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import CharmmCrdFile
    from ..openmm_CharmmCrdFile.extract import extract as extract_openmm_CharmmCrdFile

    tmp_item = CharmmCrdFile(item)
    tmp_item = extract_openmm_CharmmCrdFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

