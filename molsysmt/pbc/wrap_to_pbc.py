from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
import numpy as np
import gc

@arg_digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                box_origin='[0,0,0] nanometers', box_center=None,
                center_of_selection=None, weights=None, center_coordinates='[0,0,0] nanometers',
                keep_covalent_bonds=False, syntax='MolSysMT', engine='MolSysMT', in_place=False,
                skip_digestion=False):
    """
    Wrap coordinates into the primary periodic box.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to wrap.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to process.
    box_origin : quantity, default '[0,0,0] nanometers'
        Origin of the periodic box.
    box_center : quantity, optional
        Center of the box; if provided, uses center-based wrapping.
    center_of_selection : str or array-like, optional
        Selection to center before wrapping (uses `center_coordinates`).
    weights : array-like, optional
        Weights for centering when `center_of_selection` is given.
    center_coordinates : quantity, default '[0,0,0] nanometers'
        Target coordinates for centering the `center_of_selection`.
    keep_covalent_bonds : bool, default False
        Whether to reconstruct bonded atoms through minimum-image displacements
        and wrap each connected block as a unit. Requires topology with bonds.
    syntax : str, default 'MolSysMT'
        Selection syntax for string selections.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    in_place : bool, default False
        If True, modify the input system; otherwise return a wrapped copy.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    molecular system or None
        Wrapped system when `in_place=False`, otherwise `None`.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If box vectors are invalid, or if ``keep_covalent_bonds=True`` and
        bonds are unavailable.

    Notes
    -----
    With ``keep_covalent_bonds=False``, atoms are wrapped independently. With
    ``keep_covalent_bonds=True``, bonded blocks are reconstructed with
    minimum-image bond displacements and each block center is wrapped into the
    requested cell.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, copy
        from molsysmt.structure import center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        if center_of_selection is not None:

            molecular_system = center(molecular_system, selection=atom_indices,
                                      center_of_selection=center_of_selection, weights=weights,
                                      center_coordinates=center_coordinates, syntax=syntax, in_place=False,
                                      skip_digestion=True)

        coordinates= get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                         coordinates=True, skip_digestion=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True, skip_digestion=True)

        original_length_units = puw.get_unit(coordinates)
        coordinates, length_units = puw.get_value_and_unit(coordinates, standardized=True)
        coordinates = np.asarray(coordinates, dtype=np.float64)
        from molsysmt._private.pbc_validation import validate_box_array

        if box is None:
            validate_box_array(
                box,
                coordinates.shape[0],
                caller="molsysmt.pbc.wrap_to_pbc",
            )
        box = puw.get_value(box, standardized=True)
        box = validate_box_array(
            box,
            coordinates.shape[0],
            caller="molsysmt.pbc.wrap_to_pbc",
        )

        if keep_covalent_bonds:
            from molsysmt._private.pbc_reconstruction import (
                localize_bonded_pairs,
                reconstruct_and_wrap_covalent_blocks,
            )
            from molsysmt._private.smonitor import (
                NotImplementedConversionError,
                NotImplementedMethodError,
                NotSupportedFormError,
                StructuralInconsistencyError,
            )

            try:
                bonded_pairs = get(
                    molecular_system,
                    element='atom',
                    selection=atom_indices,
                    inner_bonded_atom_pairs=True,
                    skip_digestion=True,
                )
            except (
                NotImplementedConversionError,
                NotImplementedMethodError,
                NotSupportedFormError,
            ) as error:
                raise StructuralInconsistencyError(
                    reason="keep_covalent_bonds requires a topology that provides bonds.",
                    caller="molsysmt.pbc.wrap_to_pbc",
                ) from error
            bonded_pairs = localize_bonded_pairs(atom_indices, bonded_pairs)
            if box_center is None:
                origin = np.asarray(
                    puw.get_value(box_origin, standardized=True), dtype=np.float64
                )
                mode = 'pbc'
            else:
                origin = np.asarray(
                    puw.get_value(box_center, standardized=True), dtype=np.float64
                )
                mode = 'pbc_center'
            reconstruct_and_wrap_covalent_blocks(
                coordinates,
                box,
                bonded_pairs,
                origin=origin,
                mode=mode,
            )

        elif box_center is None:

            box_origin = puw.get_value(box_origin, standardized=True)
            box_origin = np.asarray(box_origin, dtype=np.float64)

            if np.all(np.isclose(box_origin, 0, atol=1e-4)):
                box_origin = np.zeros((3), dtype=np.float64)

            _kernels.wrap_to_pbc(coordinates, box, box_origin)

        else:

            box_center = puw.get_value(box_center, standardized=True)
            box_center = np.asarray(box_center, dtype=np.float64)

            if np.all(np.isclose(box_center, 0, atol=1e-4)):
                box_origin = np.zeros((3), dtype=np.float64)

            _kernels.wrap_to_pbc_center(coordinates, box, box_center)


        coordinates=puw.quantity(coordinates, length_units)
        coordinates=puw.convert(coordinates, to_unit=original_length_units)

        del(box)

    else:

        raise NotImplementedMethodError()



    if in_place:

        set(molecular_system, selection=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system
