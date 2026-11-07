import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError


@signal(tags=["api", "structure"])
@arg_digest()
def translate(
    molecular_system,
    translation=None,
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    in_place=False,
    skip_digestion=False,
):
    """
    Apply a translation vector to atomic coordinates of a selection.

    The function supports three translation broadcasting modes determined
    automatically from the shape of ``translation``:

    * **Single vector** — shape ``(1, 1, 3)``: the same displacement is applied
      to all atoms in all frames.
    * **Per-frame vector** — shape ``(n_structures, 1, 3)``: each frame receives
      its own displacement; all atoms within a frame move by the same amount.
    * **Per-atom-per-frame array** — shape ``(n_structures, n_atoms, 3)``: each
      atom in each frame can have a different displacement.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    translation : PyUnitWizard quantity or None, default=None
        Translation vector in units of length.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    in_place : bool, default=False
        Whether to modify the input molecular system in place.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        A new molecular system with the translated coordinates when
        ``in_place=False``; ``None`` when ``in_place=True``.


    Raises
    ------
    StructuralInconsistencyError
        If the shape of ``translation`` is not compatible with any of the supported
        broadcasting modes for the given coordinate array, or if an in-place
        floating update targets integer XYZ storage.


    Notes
    -----
    Independent outputs leave the source unchanged. XYZ inputs of shape (3,),
    (n_atoms, 3) or (n_structures, n_atoms, 3) retain their original shape, units
    and quantity library. Independent results promote integer XYZ storage to
    float64 while keeping existing floating dtype. In-place edits require
    floating XYZ storage: floating updates to integer destinations reject
    before any write. This avoids fractional coordinate truncation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> point = msm.pyunitwizard.quantity(np.array([1, 0, 0]), 'nm')
    >>> moved = msm.structure.translate(point, translation='[0.25, 0, 0] nm')
    >>> msm.pyunitwizard.get_value(moved, to_unit='nm').tolist()
    [1.25, 0.0, 0.0]
    >>> msm.pyunitwizard.get_value(point).tolist()
    [1, 0, 0]

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.coordinate_edit import (
        copy_for_coordinate_edit,
        editable_coordinate_values,
    )
    from molsysmt.basic import get, set

    coordinates = get(
        molecular_system,
        element="atom",
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        coordinates=True,
        skip_digestion=True,
    )

    coordinates, length_unit = puw.get_value_and_unit(coordinates)
    # A getter may return borrowed XYZ storage; publish edits only after success.
    coordinates = editable_coordinate_values(coordinates)
    translation = puw.get_value(translation, to_unit=length_unit)

    if translation.shape == (1, 1, 3):
        coordinates += translation[0, 0, :]
    elif translation.shape == (coordinates.shape[0], 1, 3):
        for ii in range(coordinates.shape[0]):
            coordinates[ii, :, :] += translation[ii, 0, :]
    elif np.all(translation.shape[:] == coordinates.shape[:]):
        coordinates += translation
    else:
        raise StructuralInconsistencyError(
            reason=f"The shape of the translation vector {translation.shape} is not compatible with the coordinates shape {coordinates.shape}.",
            caller="molsysmt.structure.translate",
        )

    coordinates = puw.quantity(coordinates, length_unit)

    if in_place:
        set(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
            skip_digestion=True,
        )
        del (coordinates, translation)
    else:
        tmp_molecular_system = copy_for_coordinate_edit(molecular_system)
        set(
            tmp_molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
            skip_digestion=True,
        )
        del (coordinates, translation)
        return tmp_molecular_system
