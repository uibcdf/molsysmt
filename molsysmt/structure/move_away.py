import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from molsysmt._private.vector_normalization import unit_vectors

_CALLER = "molsysmt.structure.move_away"


def _single_structure(molecular_system, indices, argument):
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get
    from molsysmt.basic._index_validation import validate_element_indices

    indices = validate_element_indices(
        molecular_system, indices, "structure", argument, _CALLER
    )
    if indices is None or is_all(indices):
        count = get(molecular_system, n_structures=True)
        if count != 1:
            raise NotImplementedMethodError(caller=_CALLER)
        return [0]
    if len(indices) == 0:
        raise ArgumentError(
            argument, caller=_CALLER, message="At least one structure must be selected."
        )
    if len(indices) != 1:
        raise NotImplementedMethodError(caller=_CALLER)
    return indices


def _finite_center(quantity, argument):
    center = np.asarray(puw.get_value(quantity, to_unit="nm"))
    if center.shape != (1, 1, 3):
        raise NotImplementedMethodError(caller=_CALLER)
    if not np.all(np.isfinite(center)):
        raise ArgumentError(
            argument,
            caller=_CALLER,
            message="Displacement centers must contain finite coordinates.",
        )
    return center


@signal(tags=["api", "structure"])
@arg_digest()
def move_away(
    molecular_system,
    selection="all",
    center_of_selection="all",
    weights=None,
    structure_indices=0,
    reference_molecular_system=None,
    reference_center_of_selection="all",
    reference_weights=None,
    reference_structure_indices=None,
    direction=None,
    distance="3 angstroms",
    in_place=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Moving an atom population relative to an initial reference center.

    With ``direction=None``, add ``distance`` along the initial reference-to-source
    direction. With an explicit direction, place the source center at the initial
    reference center plus ``distance`` along the normalized direction. These are
    different operations: automatic displacement preserves the initial separation
    as well as adding the requested offset.

    Both modes support exactly one structure and one center in each system.
    Repeated structure indices still request multiple rows and are unsupported.
    Undefined directions and unsupported axes reject before coordinate writes.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing readable and writable
        coordinates and the attributes required to resolve its selections.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atoms to translate rigidly. Other atoms and structures remain unchanged.
    center_of_selection : str, list, tuple, numpy.ndarray, or None, default='all'
        Population defining the source center. In explicit mode it must be
        contained in ``selection``; None then uses the moving population, as in
        ``center``. Automatic mode requires a nonempty source population.
    weights : numpy.ndarray, list, tuple, str, or None, default=None
        Source-center weights in the selected atom order. None uses the geometric
        center; 'masses' obtains atomic masses. Numeric weights must be finite,
        nonnegative and have positive sum. Repeated center atoms contribute
        repeatedly; each moving atom is translated once.
    structure_indices : int, list, tuple, or numpy.ndarray, default=0
        One nonnegative structure index. A singleton list is accepted. 'all' or
        None is supported only when the input has exactly one structure.
    reference_molecular_system : molecular system or None, default=None
        Readable reference system in any supported form; None uses the input.
        Its selected center is captured before the moving system is modified.
    reference_center_of_selection : str, list, tuple, numpy.ndarray, default='all'
        Population defining one initial reference center. It may overlap moving
        atoms when the reference is the input system.
    reference_weights : numpy.ndarray, list, tuple, str, or None, default=None
        Reference-center weights, with the same rules as ``weights``.
    reference_structure_indices : int, list, tuple, numpy.ndarray, or None, default=None
        One reference structure index. None uses ``structure_indices``. There is
        no multi-structure broadcasting between input and reference.
    direction : array-like or None, default=None
        One finite nonzero unit-free vector, shaped (3,) or (1, 3); normalized
        without modifying its input. None infers the direction from distinct
        finite centers. Coincident centers have no automatic direction, even
        when ``distance`` is zero.
    distance : quantity or str, default='3 angstroms'
        One finite length value, converted through PyUnitWizard. Automatic mode
        adds this signed displacement to the current separation. Explicit mode
        uses it as a signed offset from the initial reference center. Zero is
        accepted with a defined direction; a negative value reverses the offset.
    in_place : bool, default=False
        If True, update the input and return None; otherwise return an independent
        copy in the input form.
    syntax : str, default='MolSysMT'
        Selection syntax used for the moving, source and reference populations.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated internal calls.

    Returns
    -------
    molecular system or None
        Independent displaced system when ``in_place=False``; None otherwise.

    Raises
    ------
    ArgumentError
        If directions are zero or nonfinite, automatic centers coincide, a center
        or distance is nonfinite, a population is empty, weights are invalid, or
        the explicit source-center atoms are not contained in the moving population.
    NotImplementedMethodError
        If more than one structure, direction or center is requested.

    Notes
    -----
    Positions use stored Cartesian coordinates. No periodic reconstruction or
    minimum-image correction is performed; prepare compact components with the
    appropriate ``molsysmt.pbc`` tool when needed. Boxes remain unchanged. Native
    coordinate publication invalidates interaction coverage for the edited
    structure through the usual setter; rejected inputs preserve that coverage.
    The explicit destination is prepared before invoking ``center``. It does
    not first publish an intermediate centering edit.

    See Also
    --------
    molsysmt.structure.center : Placing a source center at a target.
    molsysmt.structure.translate : Applying a known Cartesian displacement.
    molsysmt.structure.get_center : Computing geometric or weighted centers.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> displaced = msm.structure.move_away(molsys, direction=[1, 0, 0],
    ...     distance='2 angstrom')
    >>> before = msm.structure.get_center(molsys)
    >>> after = msm.structure.get_center(displaced)
    >>> import numpy as np
    >>> np.allclose(msm.pyunitwizard.get_value(after - before, to_unit='nm'),
    ...     [[[0.2, 0, 0]]])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Move_away` for both displacement modes and rejection rules.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select
    from molsysmt.structure import center, get_center, translate

    if reference_molecular_system is None:
        reference_molecular_system = molecular_system
    if reference_structure_indices is None:
        reference_structure_indices = structure_indices

    structure_indices = _single_structure(
        molecular_system, structure_indices, "structure_indices"
    )
    reference_structure_indices = _single_structure(
        reference_molecular_system,
        reference_structure_indices,
        "reference_structure_indices",
    )
    length = np.asarray(puw.get_value(distance, to_unit="nm"))
    if np.iscomplexobj(length) or length.size != 1 or not np.all(np.isfinite(length)):
        raise ArgumentError(
            "distance",
            caller=_CALLER,
            message="distance must contain one finite length value.",
        )
    length = float(length.reshape(-1)[0])

    reference = get_center(
        reference_molecular_system,
        selection=reference_center_of_selection,
        structure_indices=reference_structure_indices,
        weights=reference_weights,
        syntax=syntax,
    )
    reference = _finite_center(reference, "reference_center_of_selection")

    if direction is None:
        source = get_center(
            molecular_system,
            selection=center_of_selection,
            weights=weights,
            structure_indices=structure_indices,
            syntax=syntax,
        )
        source = _finite_center(source, "center_of_selection")
        with np.errstate(over="ignore", invalid="ignore"):
            displacement = source[0] - reference[0]
        try:
            direction = unit_vectors(displacement)
        except ValueError as error:
            raise ArgumentError(
                "direction",
                caller=_CALLER,
                message="Automatic displacement requires distinct finite source and reference centers.",
            ) from error
        # Resolve against the requested coordinate scope and pass only validated
        # numeric atoms to the general translation tool.
        moving = select(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
        )
        moving = np.asarray(moving)
        if moving.ndim != 1 or moving.size == 0:
            raise ArgumentError(
                "selection",
                caller=_CALLER,
                message="Displacement requires one nonempty atom population.",
            )
        return translate(
            molecular_system,
            selection=np.unique(moving),
            structure_indices=structure_indices,
            translation=puw.quantity((length * direction)[None, :, :], "nm"),
            in_place=in_place,
        )

    # Explicit direction is normalized at the public digestion boundary. Its
    # supported cardinality must be checked before invoking a coordinate editor.
    direction = np.asarray(direction)
    if direction.shape != (1, 3):
        raise NotImplementedMethodError(caller=_CALLER)
    if not np.all(np.isfinite(direction)) or not np.any(direction):
        raise ArgumentError("direction", caller=_CALLER)
    with np.errstate(over="ignore", invalid="ignore"):
        target = reference + length * direction[None, :, :]
    if not np.all(np.isfinite(target)):
        raise ArgumentError(
            "distance",
            caller=_CALLER,
            message="The requested displacement destination must be finite.",
        )
    # One destination replaces center-then-translate. The centering owner checks
    # source containment, weights and target geometry before its first write.
    return center(
        molecular_system,
        selection=selection,
        source_center_selection=center_of_selection,
        weights=weights,
        target_coordinates=puw.quantity(target, "nm"),
        structure_indices=structure_indices,
        syntax=syntax,
        in_place=in_place,
    )
