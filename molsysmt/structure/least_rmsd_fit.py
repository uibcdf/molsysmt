from molsysmt._private.smonitor import (
    warn,
    NotImplementedMethodError,
    StructuralInconsistencyError,
)
from smonitor import signal
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt import lib as msmlib
from molsysmt._private import rust_backend as _kernels
from molsysmt import pyunitwizard as puw
import gc

from molsysmt.configure import with_configure_overrides


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def least_rmsd_fit(
    molecular_system=None,
    selection="all",
    selection_fit='atom_type!="H"',
    structure_indices="all",
    reference_molecular_system=None,
    reference_selection_fit=None,
    reference_structure_index=0,
    to_form=None,
    in_place=False,
    syntax="MolSysMT",
    engine="MolSysMT",
    parallel=None,
    num_threads=None,
    use_gpu=None,
    gpu_backend=None,
    precision=None,
    skip_digestion=False,
):
    """
    Superpose a molecular system onto a reference using the Kabsch least-RMSD algorithm.

    The optimal rotation matrix and translation vector that minimise the RMSD
    between ``selection_fit`` atoms and their counterparts in the reference are
    computed via the Kabsch algorithm.  The resulting rigid-body transformation is
    then applied to the broader ``selection`` (which may include more atoms than
    ``selection_fit``).

    Parameters
    ----------
    molecular_system : molecular system
        System to be fitted, in any form supported by MolSysMT.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        All atoms that will be physically moved by the fitted transformation.
        This is usually a superset of ``selection_fit`` (e.g., all atoms in a
        chain, while fitting is done on C-alpha only).
    selection_fit : str, list, tuple or numpy.ndarray, default 'atom_type!="H"'
        Subset of atoms used to compute the optimal superposition (heavy atoms
        by default).  Must resolve to the same number of atoms as
        ``reference_selection_fit``.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices of the query system to fit.
    reference_molecular_system : molecular system or None, default None
        Reference system.  When ``None``, ``molecular_system`` itself is used.
    reference_selection_fit : str, list, tuple or numpy.ndarray or None, default None
        Atoms in the reference used to compute the superposition.  When ``None``,
        the same expression as ``selection_fit`` is applied to the reference.
    reference_structure_index : int, default 0
        Single frame index in the reference system to fit to.
    to_form : str or None, default None
        Convert the output to the specified MolSysMT form before returning.
        When ``None``, the same form as the input is kept.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the fitted
        coordinates.
    syntax : str, default 'MolSysMT'
        Selection syntax used for all selections.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the Kabsch rotation computation.
    parallel : bool or str, optional
        Parallel mode override: True | False | 'auto'.
    num_threads : int, optional
        Number of threads override.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    molecular system or None
        A new molecular system with the fitted coordinates (optionally converted
        to ``to_form``) when ``in_place=False``; ``None`` when ``in_place=True``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If the number of atoms resolved by ``selection_fit`` and
        ``reference_selection_fit`` differ, or if either fit selection is
        collinear and therefore cannot define a unique three-dimensional
        rigid transformation.

    Notes
    -----
    A unique three-dimensional rotation requires at least three non-collinear
    fit atoms in both systems. A fit based on one atom, two atoms, or collinear
    atoms is rejected instead of returning an arbitrary rotation.

    See Also
    --------
    :func:`molsysmt.structure.get_rmsd`
        Compute RMSD without changing coordinates.
    :func:`molsysmt.structure.rotate`
        Apply an explicit proper rotation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(
    ...     msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0, 1],
    ... )
    >>> fitted = msm.structure.least_rmsd_fit(
    ...     molsys, selection_fit='atom_type!="H"', structure_indices=[0, 1],
    ...     reference_structure_index=0, use_gpu=False
    ... )
    >>> msm.get(fitted, element='system', n_structures=True)
    2

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Least_rmsd_fit`.

    .. versionadded:: 1.0.0
    """

    if engine == "MolSysMT":
        from molsysmt.basic import select, get, copy, convert, set
        from molsysmt.lib.structure._kernel_inputs import (
            align_coordinates_values_and_unit,
            extract_coordinates_value_and_unit,
        )
        from . import rotate, translate
        from molsysmt._private.gpu import resolve_use_gpu
        import molsysmt.configure as config

        # Obtain query fit coordinates
        coordinates = get(
            molecular_system,
            element="atom",
            selection=selection_fit,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=True,
        )

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection_fit is None:
            reference_selection_fit = selection_fit

        # Obtain reference fit coordinates
        reference_coordinates = get(
            reference_molecular_system,
            element="atom",
            selection=reference_selection_fit,
            structure_indices=reference_structure_index,
            syntax=syntax,
            coordinates=True,
        )

        # Align coordinate arrays and units
        fit_coords, ref_coords, length_unit = align_coordinates_values_and_unit(
            coordinates,
            reference_coordinates,
        )

        if fit_coords.shape[1] != ref_coords.shape[1]:
            raise StructuralInconsistencyError(
                reason="reference selection and selection needs to have the same number of atoms",
                caller="molsysmt.structure.least_rmsd_fit",
            )

        def _has_unique_rotation(frame):
            centered = frame - np.mean(frame, axis=0)
            return np.linalg.matrix_rank(centered) >= 2

        if not all(_has_unique_rotation(frame) for frame in fit_coords):
            raise StructuralInconsistencyError(
                reason=(
                    "selection_fit must contain at least three non-collinear "
                    "points to define a unique three-dimensional rotation"
                ),
                caller="molsysmt.structure.least_rmsd_fit",
            )
        if not all(_has_unique_rotation(frame) for frame in ref_coords):
            raise StructuralInconsistencyError(
                reason=(
                    "reference_selection_fit must contain at least three "
                    "non-collinear points to define a unique three-dimensional rotation"
                ),
                caller="molsysmt.structure.least_rmsd_fit",
            )

        # Estimate payload size and resolve GPU execution
        payload = fit_coords.shape[0] * fit_coords.shape[1]
        _use_gpu = resolve_use_gpu(use_gpu, payload)

        fitted_coords = None

        if _use_gpu:
            # Extract coordinates for the selection to be moved
            selection_coordinates = get(
                molecular_system,
                element="atom",
                selection=selection,
                structure_indices=structure_indices,
                syntax=syntax,
                coordinates=True,
            )

            # Align coordinates to move to the fit length unit
            coords_dtype = np.float32 if config.precision == "single" else np.float64
            coords_to_move = np.asarray(
                puw.get_value(selection_coordinates, to_unit=length_unit),
                dtype=coords_dtype,
            )

            # Taichi Lang backend
            if config.gpu_backend == "taichi":
                try:
                    import taichi

                    taichi_available = True
                except ImportError:
                    taichi_available = False
                    import warnings
                    from molsysmt._private.smonitor import GpuNotAvailableWarning

                    warn(
                        GpuNotAvailableWarning(
                            reason="the taichi package is not installed"
                        )
                    )

                if taichi_available:
                    from molsysmt.lib.structure.get_least_rmsd_taichi import (
                        least_rmsd_fit as _kernel,
                    )

                    fitted_coords = _kernel(coords_to_move, fit_coords, ref_coords)

            # Retired experimental CUDA branch.
            if fitted_coords is None:
                from molsysmt.lib.structure.get_least_rmsd_cuda import (
                    least_rmsd_fit as _kernel,
                )

                fitted_coords = _kernel(coords_to_move, fit_coords, ref_coords)

            # Wrap coordinates back to quantity
            fitted_coords = puw.quantity(fitted_coords, length_unit)
            del (
                coordinates,
                reference_coordinates,
                fit_coords,
                ref_coords,
                coords_to_move,
                selection_coordinates,
            )

            if in_place:
                set(
                    molecular_system,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    coordinates=fitted_coords,
                    skip_digestion=True,
                )
                del fitted_coords
                gc.collect()
                return None
            else:
                tmp_molecular_system = copy(molecular_system)
                set(
                    tmp_molecular_system,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    coordinates=fitted_coords,
                    skip_digestion=True,
                )
                del fitted_coords
                gc.collect()

                if config.precision == "single":
                    if puw.is_quantity(tmp_molecular_system):
                        tmp_molecular_system = puw.quantity(
                            puw.get_value(tmp_molecular_system).astype(np.float32),
                            puw.get_unit(tmp_molecular_system),
                        )

                if to_form is None:
                    return tmp_molecular_system
                else:
                    tmp_molecular_system = convert(
                        tmp_molecular_system, to_form=to_form
                    )
                    return tmp_molecular_system

        # CPU JIT pipeline fallback
        if fitted_coords is None:
            fit_coords = fit_coords.astype(np.float64)
            ref_coords = ref_coords.astype(np.float64)

            if fit_coords.shape[0] == 1 and ref_coords.shape[0] > 1:
                rotation_center, rotation, translation = (
                    _kernels.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        ref_coords, fit_coords[0]
                    )
                )
            elif fit_coords.shape[0] > 1 and ref_coords.shape[0] == 1:
                rotation_center, rotation, translation = (
                    _kernels.get_least_rmsd_rotation_and_translation_with_single_reference_structure(
                        fit_coords, ref_coords[0]
                    )
                )
            else:
                rotation_center, rotation, translation = (
                    _kernels.get_least_rmsd_rotation_and_translation(
                        fit_coords, ref_coords
                    )
                )

            rotation_center = puw.quantity(
                rotation_center, length_unit, standardized=True
            )
            translation = puw.quantity(translation, length_unit, standardized=True)

            del (coordinates, reference_coordinates, fit_coords, ref_coords)

            if in_place:
                rotate(
                    molecular_system,
                    rotation=rotation,
                    rotation_center=rotation_center,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    in_place=True,
                )

                translate(
                    molecular_system,
                    translation=translation,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    in_place=True,
                )

                # Post-apply precision settings if single precision is configured
                if config.precision == "single":
                    coords = get(
                        molecular_system,
                        element="atom",
                        selection=selection,
                        structure_indices=structure_indices,
                        syntax=syntax,
                        coordinates=True,
                        skip_digestion=True,
                    )
                    coords_val, coords_unit = puw.get_value_and_unit(coords)
                    set(
                        molecular_system,
                        selection=selection,
                        structure_indices=structure_indices,
                        syntax=syntax,
                        coordinates=puw.quantity(
                            coords_val.astype(np.float32), coords_unit
                        ),
                        skip_digestion=True,
                    )

                del (rotation, rotation_center, translation)
                gc.collect()
                return None

            else:
                tmp_molecular_system = copy(molecular_system)

                rotate(
                    tmp_molecular_system,
                    rotation=rotation,
                    rotation_center=rotation_center,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    in_place=True,
                )

                translate(
                    tmp_molecular_system,
                    translation=translation,
                    selection=selection,
                    structure_indices=structure_indices,
                    syntax=syntax,
                    in_place=True,
                )

                # Post-apply precision settings if single precision is configured
                if config.precision == "single":
                    if puw.is_quantity(tmp_molecular_system):
                        tmp_molecular_system = puw.quantity(
                            puw.get_value(tmp_molecular_system).astype(np.float32),
                            puw.get_unit(tmp_molecular_system),
                        )
                    else:
                        coords = get(
                            tmp_molecular_system,
                            element="atom",
                            selection=selection,
                            structure_indices=structure_indices,
                            syntax=syntax,
                            coordinates=True,
                            skip_digestion=True,
                        )
                        coords_val, coords_unit = puw.get_value_and_unit(coords)
                        set(
                            tmp_molecular_system,
                            selection=selection,
                            structure_indices=structure_indices,
                            syntax=syntax,
                            coordinates=puw.quantity(
                                coords_val.astype(np.float32), coords_unit
                            ),
                            skip_digestion=True,
                        )

                del (rotation, rotation_center, translation)
                gc.collect()

                if to_form is None:
                    return tmp_molecular_system
                else:
                    tmp_molecular_system = convert(
                        tmp_molecular_system, to_form=to_form
                    )
                    return tmp_molecular_system

    else:
        raise NotImplementedMethodError()
