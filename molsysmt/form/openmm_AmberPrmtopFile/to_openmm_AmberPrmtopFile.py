from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def to_openmm_AmberPrmtopFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from openmm.AmberPrmtopFile to openmm.AmberPrmtopFile.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
        Source item in openmm.AmberPrmtopFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.AmberPrmtopFile
        Resulting object in openmm.AmberPrmtopFile form.

    .. versionadded:: 1.0.0
    """


    from molsysmt._private.variables import is_all
    import os

    if isinstance(item, (str, os.PathLike)):
        from openmm.app import AmberPrmtopFile
        tmp_item = AmberPrmtopFile(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item


