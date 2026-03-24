from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def center(molecular_system, selection='all', center_of_selection='all', weights=None, center_coordinates=None,
           structure_indices='all', syntax='MolSysMT', engine='MolSysMT', in_place=False, skip_digestion=False):
    """
    Translate a selection of atoms so that a reference center lies at a target point.

    The function computes the center of ``center_of_selection`` (optionally weighted),
    then applies a translation to ``selection`` so that the reference center moves to
    ``center_coordinates``.  If ``center_coordinates`` is ``None`` the reference center
    is moved to the origin.  A second-pass correction is applied when floating-point
    residuals exceed 1e-12 nm.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms that are physically moved by the translation.
    center_of_selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms whose center defines the reference point to be relocated.
    weights : array-like, optional
        Per-atom weights for computing the center of ``center_of_selection``.
        When ``None``, all atoms have equal weight (centroid).
    center_coordinates : quantity or None, default None
        Target position for the center.  Must be a PyUnitWizard length quantity
        with shape compatible with ``(n_structures, 1, 3)``.
        When ``None`` the center is moved to the origin.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the operation is performed.
    syntax : str, default 'MolSysMT'
        Selection syntax used when ``selection`` or ``center_of_selection`` are strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for center computation and translation.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is returned.
        If ``False`` a new copy is returned with the translated coordinates.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    molecular system or None
        A new molecular system with the translated coordinates when ``in_place=False``;
        ``None`` when ``in_place=True``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    from . import get_center
    from . import translate

    if engine=='MolSysMT':

        coordinates_selection_center = get_center(molecular_system, selection=center_of_selection, weights=weights,
                                                  structure_indices=structure_indices, syntax=syntax, engine=engine)

        if center_coordinates is None:
            translation = -coordinates_selection_center
        else:
            translation = center_coordinates-coordinates_selection_center

        del(coordinates_selection_center)

        output = translate(molecular_system, translation=translation, selection=selection,
                           structure_indices=structure_indices, syntax='MolSysMT',
                           in_place=in_place)

        target = molecular_system if in_place else output
        residual_center = get_center(target, selection=center_of_selection, weights=weights,
                                     structure_indices=structure_indices, syntax=syntax, engine=engine)
        residual = puw.get_value(residual_center, to_unit='nm')

        if center_coordinates is None:
            needs_correction = not np.allclose(residual, 0.0, atol=1e-12)
            correction = -residual_center
        else:
            target_center = puw.get_value(center_coordinates, to_unit='nm')
            needs_correction = not np.allclose(residual, target_center, atol=1e-12)
            correction = center_coordinates - residual_center

        if needs_correction:
            output = translate(target, translation=correction, selection=selection,
                               structure_indices=structure_indices, syntax='MolSysMT',
                               in_place=in_place)
            if in_place:
                output = molecular_system

        return output

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.center')
