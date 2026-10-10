from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest

__all__ = ["get_box_from_system"]


@arg_digest(form="file:prmtop")
@dep_digest("openmm")
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting periodic box vectors stored in an AMBER topology file.

    Parameters
    ----------
    item : file:prmtop
        Input AMBER topology file, read through the existing OpenMM adapter.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Positions in the single stored box record. None returns None.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or none
        Box vectors with shape (1, 3, 3) before selection, standardized to the
        configured length unit. A nonperiodic topology returns None.

    Notes
    -----
    A stored box does not supply coordinates or a coordinate structure.
    Box lengths, angles, shape and volume use the general box tools.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['pentalanine']['pentalanine.prmtop']
    >>> get_box_from_system(molsys).shape
    (1, 3, 3)

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.openmm_AmberPrmtopFile.get_structural_attributes import (
        get_box_from_system as get_box,
    )

    from .to_openmm_AmberPrmtopFile import to_openmm_AmberPrmtopFile

    if structure_indices is None:
        return None
    parsed = to_openmm_AmberPrmtopFile(item, skip_digestion=True)
    return get_box(parsed, structure_indices=structure_indices, skip_digestion=True)
