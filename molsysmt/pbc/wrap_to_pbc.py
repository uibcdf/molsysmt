from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
import numpy as np

@arg_digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                box_origin='[0,0,0] nanometers', box_center=None,
                center_of_selection=None, weights=None, center_coordinates='[0,0,0] nanometers',
                compact='component', syntax='MolSysMT', engine='MolSysMT', in_place=False,
                skip_digestion=False):
    """
    Wrap coordinates into the primary periodic box.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    box_origin : PyUnitWizard quantity, default='[0,0,0] nanometers'
        Periodic box origin in units of length.
    box_center : PyUnitWizard quantity or None, default=None
        Periodic box center in units of length; `None` derives it from the box.
    center_of_selection : str, list, tuple, or numpy.ndarray, or None, default=None
        Atoms whose center defines the translation reference.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    center_coordinates : PyUnitWizard quantity or None, default='[0,0,0] nanometers'
        Coordinates to which the selected center is translated, in units of length.
    compact : False or str, default='component'
        Element kept whole when wrapping. ``'component'`` translates each covalent
        component as one piece, so no bond is stretched across the cell. ``False``
        wraps every atom independently, which is what a simulation engine does and
        what leaves a molecule split across opposite faces.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    in_place : bool, default=False
        Whether to modify the input molecular system in place.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        Wrapped system when `in_place=False`, otherwise `None`.


    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If box vectors are invalid, or if ``compact`` names an element and
        bonds are unavailable.


    Notes
    -----
    With ``compact=False``, atoms are wrapped independently. With
    ``compact='component'``, bonded blocks are reconstructed with
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

        # With no bonds every atom is a covalent component of its own, so compacting by
        # component is atom-wise wrapping. That is the degenerate answer rather than a
        # fallback, and it is taken through the atom-wise kernel because walking one
        # block per atom would cost far more than the operation it stands for.
        compact_pairs = None
        if compact:
            from molsysmt._private.pbc_reconstruction import localize_bonded_pairs
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
                    reason="compact requires a topology that provides bonds.",
                    caller="molsysmt.pbc.wrap_to_pbc",
                ) from error

            if bonded_pairs is not None and len(bonded_pairs) > 0:
                compact_pairs = localize_bonded_pairs(atom_indices, bonded_pairs)

        if compact_pairs is not None:
            from molsysmt._private.pbc_reconstruction import (
                reconstruct_and_wrap_covalent_blocks,
            )
            bonded_pairs = compact_pairs
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


        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=atom_indices, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)


        return tmp_molecular_system
