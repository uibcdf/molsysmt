import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from molsysmt._private.variables import is_all


def _flat_atoms(molecular_system, selection, syntax, argument):
    from molsysmt.basic import select

    indices = select(molecular_system, selection=selection, syntax=syntax)
    try:
        indices = np.asarray(indices)
        if (
            indices.ndim == 1
            and indices.size
            and indices.dtype.kind in "iu"
            and np.all(indices >= 0)
        ):
            return indices
    except (TypeError, ValueError):
        pass
    raise ArgumentError(
        argument,
        caller="molsysmt.structure.center",
        message="Centering requires a nonempty flat population of atom indices.",
    )


def _target_values(target_coordinates, centers, structure_indices):
    caller = "molsysmt.structure.center"
    if (
        centers.ndim != 3
        or centers.shape[1:] != (1, 3)
        or centers.shape[0] == 0
        or not np.all(np.isfinite(centers))
    ):
        raise ArgumentError(
            "source_center_selection",
            caller=caller,
            message="Centering requires one finite reference center per selected structure.",
        )
    targets = (
        np.zeros((1, 1, 3))
        if target_coordinates is None
        else np.asarray(puw.get_value(target_coordinates, to_unit="nm"))
    )
    if targets.shape not in ((1, 1, 3), centers.shape) or not np.all(
        np.isfinite(targets)
    ):
        raise ArgumentError(
            "target_coordinates",
            caller=caller,
            message="target_coordinates must contain one finite point or one point per selected structure.",
        )
    targets = np.broadcast_to(targets, centers.shape)
    if structure_indices is not None and not is_all(structure_indices):
        previous = {}
        for index, point in zip(structure_indices, targets):
            if int(index) in previous and not np.array_equal(
                point, previous[int(index)]
            ):
                raise ArgumentError(
                    "target_coordinates",
                    caller=caller,
                    message="Repeated structure indices must have identical target points.",
                )
            previous[int(index)] = point
    return targets


@signal(tags=["api", "structure"])
@arg_digest()
def center(
    molecular_system,
    selection="all",
    source_center_selection=None,
    target_center_selection=None,
    target_coordinates=None,
    weights=None,
    structure_indices="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    in_place=False,
    skip_digestion=False,
):
    """
    Centering an atom population by translating its reference center to a target.

    All atoms in ``selection`` receive the same translation in each selected
    structure. Their relative positions are preserved. The source center is
    computed from ``source_center_selection``, which defaults to ``selection``.
    Its atoms must all belong to the moving population.

    The destination is either ``target_coordinates`` or the initial geometric
    center of ``target_center_selection``. These arguments are mutually
    exclusive. With neither argument, the destination is the coordinate origin.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing readable and writable
        coordinates and the attributes needed to resolve the selections.
    selection : str, int, list, tuple, or numpy.ndarray, default='all'
        Atoms to translate rigidly. Atoms outside this selection remain unchanged.
    source_center_selection : str, int, list, tuple, numpy.ndarray, or None, default=None
        Atoms defining the center to place at the destination. None uses
        ``selection``. This population must be nonempty and contained in
        ``selection``. Repeated indices contribute repeatedly to its center.
    target_center_selection : str, int, list, tuple, numpy.ndarray, or None, default=None
        Atoms whose initial geometric center defines the destination in each
        selected structure. They need not belong to ``selection``. The center
        is captured before any edit, including when the two populations overlap.
    target_coordinates : quantity, str, or None, default=None
        Destination with length units. Supply one point with shape (3,), (1, 3)
        or (1, 1, 3), or one point per requested structure with shape
        (n_selected_structures, 1, 3). Rows follow ``structure_indices`` order.
        Repeated structure indices must have identical destination points.
        Mutually exclusive with ``target_center_selection``. With both unset,
        the destination is the origin. Lengths are converted through PyUnitWizard.
    weights : list, tuple, numpy.ndarray, str, or None, default=None
        Weights for ``source_center_selection`` in its selected order, including
        repeated indices. None uses the geometric center; 'masses' obtains atomic
        masses. Numeric weights must be finite, nonnegative and have positive
        total weight. The target selection always uses its geometric center;
        compute a weighted target with ``get_center`` and pass its coordinates.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Nonnegative structure indices to process. Nonconsecutive and repeated indices are
        supported. Other structures remain unchanged.
    syntax : str, default='MolSysMT'
        Selection syntax used for all three atom selections.
    engine : str, default='MolSysMT'
        Backend used to compute the centers. Only 'MolSysMT' is supported.
    in_place : bool, default=False
        If True, update the input and return None. Otherwise return an
        independent copy in the input form.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated internal calls.

    Returns
    -------
    molecular system or None
        Independent translated system when ``in_place=False``; None otherwise.

    Raises
    ------
    ArgumentError
        If a population is empty or nested, the source population is not
        contained in the moving selection, both destinations are supplied,
        weights are invalid, or centers or destination shapes are invalid.
    NotImplementedMethodError
        If an unsupported engine is requested.

    Notes
    -----
    The translation is ``target_center - source_center``. The destination is a
    snapshot of the original coordinates, not a constraint that the source and
    target populations remain coincident after both move. No periodic wrapping
    or reconstruction is performed; make the source and target populations
    compact with the appropriate ``molsysmt.pbc`` tool beforehand if needed.
    Native coordinate edits invalidate stored interaction coverage for the
    edited structures through the normal coordinate setter. A residual correction above 1e-12 nm
    refines centering on the same output without making a second system copy.

    This pre-1.0 contract replaces ``center_of_selection`` with
    ``source_center_selection`` and ``center_coordinates`` with
    ``target_coordinates``. The old keyword names are not accepted.

    See Also
    --------
    molsysmt.structure.get_center : Computing geometric or weighted centers.
    molsysmt.structure.translate : Applying an explicit translation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0])
    >>> molsys_centered = msm.structure.center(
    ...     molsys, source_center_selection='atom_name=="CA"',
    ...     target_coordinates='[1, 2, 3] nm')
    >>> center = msm.structure.get_center(
    ...     molsys_centered, selection='atom_name=="CA"')
    >>> import numpy as np
    >>> np.allclose(msm.pyunitwizard.get_value(center, to_unit='nm'), [1, 2, 3])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Center` for both destination modes and selected scopes.

    .. versionadded:: 1.0.0
    """

    from . import get_center, translate

    if engine == "MolSysMT":
        moving = _flat_atoms(molecular_system, selection, syntax, "selection")
        if target_coordinates is not None and target_center_selection is not None:
            raise ArgumentError(
                "target_coordinates",
                caller="molsysmt.structure.center",
                message="Supply either target_coordinates or target_center_selection, not both.",
            )
        reference = (
            moving
            if source_center_selection is None
            else _flat_atoms(
                molecular_system,
                source_center_selection,
                syntax,
                "source_center_selection",
            )
        )
        if not np.all(np.isin(reference, moving)):
            raise ArgumentError(
                "source_center_selection",
                caller="molsysmt.structure.center",
                message="source_center_selection must be contained in selection; all source-center atoms must move together.",
            )
        moving = np.unique(moving)
        if target_center_selection is not None:
            destination = _flat_atoms(
                molecular_system,
                target_center_selection,
                syntax,
                "target_center_selection",
            )
            target_coordinates = get_center(
                molecular_system,
                selection=destination,
                structure_indices=structure_indices,
                syntax="MolSysMT",
                engine=engine,
            )
        coordinates_selection_center = get_center(
            molecular_system,
            selection=reference,
            weights=weights,
            structure_indices=structure_indices,
            syntax="MolSysMT",
            engine=engine,
        )

        centers = np.asarray(puw.get_value(coordinates_selection_center, to_unit="nm"))
        targets = _target_values(target_coordinates, centers, structure_indices)
        displacement = targets - centers
        if not np.all(np.isfinite(displacement)):
            raise ArgumentError(
                "target_coordinates",
                caller="molsysmt.structure.center",
                message="The centering displacement must be finite.",
            )
        translation = puw.quantity(displacement, "nm")

        del coordinates_selection_center

        output = translate(
            molecular_system,
            translation=translation,
            selection=moving,
            structure_indices=structure_indices,
            syntax="MolSysMT",
            in_place=in_place,
        )

        target = molecular_system if in_place else output
        residual_center = get_center(
            target,
            selection=reference,
            weights=weights,
            structure_indices=structure_indices,
            syntax="MolSysMT",
            engine=engine,
        )
        residual = puw.get_value(residual_center, to_unit="nm")

        correction = targets - residual
        needs_correction = not np.allclose(correction, 0.0, rtol=0.0, atol=1e-12)

        if needs_correction:
            translate(
                target,
                translation=puw.quantity(correction, "nm"),
                selection=moving,
                structure_indices=structure_indices,
                syntax="MolSysMT",
                in_place=True,
            )

        return None if in_place else output

    else:
        raise NotImplementedMethodError(caller="molsysmt.structure.center")
