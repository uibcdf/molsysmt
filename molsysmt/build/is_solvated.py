import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    NotWithThisFormError,
    StructuralInconsistencyError,
)


@signal(tags=["build", "audit"])
@arg_digest()
def is_solvated(molecular_system, skip_digestion=False, *, structure_indices="all"):
    """
    Checking a water-number-density solvation criterion for selected structures.

    Each selected structure passes when indexed water molecules are present and
    their global number density exceeds 15 molecules per cubic nanometer in its
    periodic box. No first/any/all aggregation is applied across structures.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process. Explicit order and
        repetitions are preserved. None is not a structure selection.

    Returns
    -------
    bool or numpy.ndarray
        A Python bool for one selected structure; otherwise a one-dimensional
        Boolean array in selection order, including shape ``(0,)`` for an empty
        selection. No waters or no box yields False per selected structure.
        An inventory without a structure axis or box yields False.

    Raises
    ------
    ArgumentError
        If structure indices are malformed, negative or out of range.
    NotWithThisFormError
        If the input cannot supply its indexed water count.
    StructuralInconsistencyError
        If available box volumes are nonpositive, nonfinite or not aligned with
        the selected structure axis.

    Notes
    -----
    This is the existing global water-count/box-volume heuristic. It does not
    check solvent coverage, molecular containment, equilibration, hydrogen-bond
    structure, solvent chemistry or ionic strength. Other solvents alone do not
    satisfy its water prerequisite. Coordinates are not required by the predicate;
    native inputs do not materialize them. File and foreign-form inputs retain
    their adapters' conversion/loading costs. Reuse a resident native system for
    repeated queries when those costs matter.
    Volumes are converted explicitly to cubic nanometers with PyUnitWizard,
    independently of the active standard-unit policy. The comparison is strictly
    greater than 15; equality does not pass. Densities within eight machine epsilons
    relative to the threshold are treated as equal, to avoid changing the result
    solely through roundoff in equivalent length-unit representations. This is
    a numerical tolerance, not a physical density margin.

    Use ``result.all()`` or ``result.any()`` explicitly when an array result needs
    an aggregate interpretation. Neither the molecular system nor its named
    interaction analyses are modified.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['chicken villin HP35']['1vii.bcif.gz'])
    >>> msm.build.is_solvated(molsys)
    False
    >>> msm.build.is_solvated(molsys, structure_indices=[0, 0]).tolist()
    [False, False]

    .. admonition:: Tutorial

       See :ref:`Tutorial_Is_solvated`.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get

    caller = "molsysmt.build.is_solvated"
    if structure_indices is None:
        raise ArgumentError(
            "structure_indices",
            value=None,
            caller=caller,
            message="Select structure indices or 'all'; None is not a selection.",
        )

    observations = get(
        molecular_system,
        element="system",
        structure_indices=structure_indices,
        output_type="dictionary",
        get_missing_bonds=False,
        n_waters=True,
        box_volume=True,
        structure_index=True,
        skip_digestion=True,
    )
    n_waters = observations["n_waters"]
    volume = observations["box_volume"]
    indices = observations["structure_index"]

    if n_waters is None:
        raise NotWithThisFormError(
            caller=caller,
            requested_attribute="n_waters",
            message="The solvation predicate requires an indexed water inventory.",
        )
    if indices is None:
        return False

    result = np.zeros(len(indices), dtype=bool)
    if volume is not None:
        volumes = np.atleast_1d(puw.get_value(volume, to_unit="nm**3"))
        if (
            volumes.shape != result.shape
            or not np.isfinite(volumes).all()
            or np.any(volumes <= 0)
        ):
            raise StructuralInconsistencyError(
                caller=caller,
                reason="Solvation density requires positive finite box volumes aligned with the selected structures.",
            )
        densities = n_waters / volumes
        tolerance = 8 * np.finfo(densities.dtype).eps
        result = (densities > 15.0) & ~np.isclose(
            densities, 15.0, rtol=tolerance, atol=0.0
        )

    return bool(result[0]) if result.size == 1 else result
