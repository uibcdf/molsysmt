from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import StructuralInconsistencyError
from smonitor import signal
import numpy as np
from molsysmt import pyunitwizard as puw

@signal(tags=['api', 'structure'])
@arg_digest()
def translate(molecular_system, translation=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False, skip_digestion=False):
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
        broadcasting modes for the given coordinate array.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, copy

    coordinates = get(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
                      syntax=syntax, coordinates=True, skip_digestion=True)

    coordinates, length_unit = puw.get_value_and_unit(coordinates)
    translation = puw.get_value(translation, to_unit=length_unit)

    if translation.shape==(1,1,3):
        coordinates += translation[0,0,:]
    elif translation.shape==(coordinates.shape[0],1,3):
        for ii in range(coordinates.shape[0]):
            coordinates[ii,:,:] += translation[ii,0,:]
    elif np.all(translation.shape[:]==coordinates.shape[:]):
        coordinates += translation
    else:
        raise StructuralInconsistencyError(
            reason=f"The shape of the translation vector {translation.shape} is not compatible with the coordinates shape {coordinates.shape}.",
            caller="molsysmt.structure.translate"
        )

    coordinates = puw.quantity(coordinates, length_unit)

    if in_place:
        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates, skip_digestion=True)
        del(coordinates, translation)
    else:
        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates, skip_digestion=True)
        del(coordinates, translation)
        return tmp_molecular_system
