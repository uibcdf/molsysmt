from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
import numpy as np
import gc

@arg_digest()
def unwrap(molecular_system, selection='all', structure_indices='all',
        syntax='MolSysMT', engine='MolSysMT', in_place=False, skip_digestion=False):
    """
    Unwrapping coordinates across periodic boundaries to produce continuous trajectories.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to unwrap.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to process.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    in_place : bool, default False
        If True, modify the input system; otherwise return an unwrapped copy.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    molecular system or None
        Unwrapped system when `in_place=False`, otherwise `None`.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If box vectors are missing, malformed, non-finite, or singular.

    Notes
    -----
    This operation restores temporal continuity independently for every atom.
    It does not reconstruct a molecule within one frame. Use
    :func:`molsysmt.pbc.wrap_to_pbc` or :func:`molsysmt.pbc.wrap_to_mic` with
    ``keep_covalent_bonds=True`` for covalent reconstruction.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import get, set, copy

        coordinates = get(
            molecular_system,
            element='atom',
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=True,
            skip_digestion=True,
        )
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True, skip_digestion=True)

        coordinates, length_units = puw.get_value_and_unit(coordinates)
        from molsysmt._private.pbc_validation import validate_box_array

        if box is None:
            validate_box_array(
                box,
                np.asarray(coordinates).shape[0],
                caller="molsysmt.pbc.unwrap",
            )
        box = puw.get_value(box, to_unit=length_units)

        coordinates = np.asarray(coordinates, dtype=np.float64)
        box = validate_box_array(
            box,
            coordinates.shape[0],
            caller="molsysmt.pbc.unwrap",
        )

        _kernels.unwrap(coordinates, box)

        coordinates=puw.quantity(coordinates, length_units)

    else:

        raise NotImplementedMethodError()

    if in_place:

        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates, skip_digestion=True)

        del(coordinates, box)

        gc.collect()

    else:

        tmp_molecular_system = copy(molecular_system, skip_digestion=True)

        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax='MolSysMT', coordinates=coordinates, skip_digestion=True)

        del(coordinates, box)
        
        gc.collect()

        return tmp_molecular_system
