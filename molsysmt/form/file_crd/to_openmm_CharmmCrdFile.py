from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:crd')
def to_openmm_CharmmCrdFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:crd to openmm.CharmmCrdFile.

    Parameters
    ----------
    item : file:crd
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.CharmmCrdFile
        Converted molecular system representation.
    """

    from openmm.app import CharmmCrdFile
    from ..openmm_CharmmCrdFile.extract import extract as extract_openmm_CharmmCrdFile

    tmp_item = CharmmCrdFile(item)
    tmp_item = extract_openmm_CharmmCrdFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

