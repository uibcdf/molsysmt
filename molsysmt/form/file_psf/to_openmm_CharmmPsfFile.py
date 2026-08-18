from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:psf')
@dep_digest('openmm')
def to_openmm_CharmmPsfFile(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:psf to openmm.CharmmPsfFile.

    Parameters
    ----------
    item : file:psf
        Source item in file:psf form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.CharmmPsfFile
        Resulting object in openmm.CharmmPsfFile form.

    .. versionadded:: 1.0.0
    """

    from openmm.app import CharmmPsfFile
    from molsysmt.form.openmm_CharmmPsfFile.extract import extract as extract_openmm_CharmmPsfFile
    import os

    if isinstance(item, os.PathLike):
        item = str(item)

    tmp_item = CharmmPsfFile(item)
    tmp_item = extract_openmm_CharmmPsfFile(tmp_item, atom_indices=atom_indices, copy_if_all=False,
                                            skip_digestion=True)

    return tmp_item
