import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest


@arg_digest()
def wrap_to_mic(
    molecular_system,
    selection="all",
    structure_indices="all",
    mic_origin="[0,0,0] nanometers",
    center_of_selection=None,
    center_coordinates="[0,0,0] nanometers",
    weights=None,
    compact="component",
    syntax="MolSysMT",
    engine="MolSysMT",
    in_place=False,
    skip_digestion=False,
):
    """
    Wrapping coordinates into the minimum image convention (MIC) box.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    mic_origin : PyUnitWizard quantity, default='[0,0,0] nanometers'
        Origin of the minimum-image cell in units of length.
    center_of_selection : str, list, tuple, or numpy.ndarray, or None, default=None
        Atoms whose center defines the translation reference. When supplied,
        they must belong to ``selection`` so the entire reference moves together.
    center_coordinates : PyUnitWizard quantity or None, default='[0,0,0] nanometers'
        Coordinates to which the selected center is translated, in units of length.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
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
        If True, publish the final coordinates into the original input and
        return None, including when centering is requested. Otherwise return
        an independent system in the input form.
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
    minimum-image bond displacements and translated as complete units.

    Centering is evaluated on an independent working system before wrapping.
    Only the requested atoms and structures are published to the original
    input when ``in_place=True``. Other coordinates, topology and boxes are
    preserved. Native setters invalidate stored interaction coverage only for
    edited structures. Validation failure before publication preserves the
    input, and an independent centered result reuses the working copy.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0, 8, 3])
    >>> before = msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True), to_unit='nm').copy()
    >>> result = msm.pbc.wrap_to_mic(molsys, center_of_selection=[0, 1],
    ...     compact=False, structure_indices=[2, 0], in_place=True)
    >>> result is None
    True
    >>> after = msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True), to_unit='nm')
    >>> np.array_equal(after[1], before[1]) and not np.array_equal(after[[2, 0]], before[[2, 0]])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Wrap_to_mic` for compact wrapping and edit ownership.


    .. versionadded:: 1.0.0
    """

    if engine == "MolSysMT":
        from molsysmt.basic import copy, get, select, set
        from molsysmt.structure import center

        atom_indices = select(
            molecular_system, selection=selection, syntax=syntax, skip_digestion=True
        )

        working_system = molecular_system
        if center_of_selection is not None:
            working_system = center(
                molecular_system,
                selection=atom_indices,
                source_center_selection=center_of_selection,
                weights=weights,
                target_coordinates=center_coordinates,
                structure_indices=structure_indices,
                syntax=syntax,
                in_place=False,
                skip_digestion=True,
            )

        coordinates = get(
            working_system,
            element="atom",
            selection=atom_indices,
            structure_indices=structure_indices,
            coordinates=True,
            skip_digestion=True,
        )
        box = get(
            working_system,
            element="system",
            structure_indices=structure_indices,
            box=True,
            skip_digestion=True,
        )

        original_length_units = puw.get_unit(coordinates)
        coordinates, length_units = puw.get_value_and_unit(
            coordinates, standardized=True
        )
        coordinates = np.asarray(coordinates, dtype=np.float64)
        from molsysmt._private.pbc_validation import validate_box_array

        if box is None:
            validate_box_array(
                box,
                coordinates.shape[0],
                caller="molsysmt.pbc.wrap_to_mic",
            )
        box = puw.get_value(box, standardized=True)
        box = validate_box_array(
            box,
            coordinates.shape[0],
            caller="molsysmt.pbc.wrap_to_mic",
        )

        mic_origin = puw.get_value(mic_origin, standardized=True)
        mic_origin = np.asarray(mic_origin, dtype=np.float64)

        if np.all(np.isclose(mic_origin, 0, atol=1e-4)):
            mic_origin = np.zeros((3), dtype=np.float64)

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
                    working_system,
                    element="atom",
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
                    caller="molsysmt.pbc.wrap_to_mic",
                ) from error

            if bonded_pairs is not None and len(bonded_pairs) > 0:
                compact_pairs = localize_bonded_pairs(atom_indices, bonded_pairs)

        if compact_pairs is not None:
            from molsysmt._private.pbc_reconstruction import (
                reconstruct_and_wrap_covalent_blocks,
            )

            bonded_pairs = compact_pairs
            reconstruct_and_wrap_covalent_blocks(
                coordinates,
                box,
                bonded_pairs,
                origin=mic_origin,
                mode="mic",
            )
        else:
            _kernels.wrap_to_mic(coordinates, box, mic_origin)

        coordinates = puw.quantity(coordinates, length_units)
        coordinates = puw.convert(coordinates, to_unit=original_length_units)

        del box

    else:
        raise NotImplementedMethodError()

    if in_place:
        set(
            molecular_system,
            selection=atom_indices,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
            skip_digestion=True,
        )

        del (coordinates, atom_indices, structure_indices)

        pass

    else:
        tmp_molecular_system = (
            working_system
            if center_of_selection is not None
            else copy(molecular_system, skip_digestion=True)
        )
        set(
            tmp_molecular_system,
            selection=atom_indices,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
            skip_digestion=True,
        )

        del (coordinates, atom_indices, structure_indices)

        return tmp_molecular_system
