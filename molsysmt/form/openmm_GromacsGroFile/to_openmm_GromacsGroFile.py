from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.GromacsGroFile')
@dep_digest('openmm')
def to_openmm_GromacsGroFile(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from openmm.GromacsGroFile to openmm.GromacsGroFile.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.GromacsGroFile
        Resulting object in openmm.GromacsGroFile form.


    .. versionadded:: 1.0.0
    """


    from molsysmt._private.variables import is_all
    import os

    if isinstance(item, (str, os.PathLike)):
        from openmm.app import GromacsGroFile
        tmp_item = GromacsGroFile(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item


