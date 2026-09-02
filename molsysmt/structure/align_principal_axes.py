from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@signal(tags=['api', 'structure'])
@arg_digest()
def align_principal_axes(molecular_system, selection='all',
        principal_axes_of_selection=None, principal_axes_type='inertia',
        structure_indices='all', weights=None, axes=None, center=False,
        syntax='MolSysMT', engine='MolSysMT', in_place=False):
    """
    Aligning selected atoms to reference principal axes.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    principal_axes_of_selection : str, list, tuple, or numpy.ndarray, or None, default=None
        Atoms used to calculate the principal axes for alignment.
    principal_axes_type : {'inertia', 'geometric'}, default='inertia'
        Definition used to calculate the principal axes.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    axes : array-like or None, default=None
        Right-handed orthonormal target axes supplied as three row vectors.
    center : bool, default=False
        Whether to leave the aligned selection centered at the origin.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    in_place : bool, default=False
        Whether to modify the input molecular system in place.

    Returns
    -------
    molecular system or None
        Rotated system when `in_place=False`, otherwise `None`.


    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.
    StructuralInconsistencyError
        If target axes are not a right-handed orthonormal basis or if principal
        moments are degenerate and do not define three unique axes.


    Notes
    -----
    Target axes are supplied as rows. Alignment is intentionally rejected when
    two principal moments are equal within numerical tolerance because the
    corresponding individual axes are not uniquely defined.


    See Also
    --------
    :func:`molsysmt.structure.get_principal_axes`
        Compute principal axes and moments without changing coordinates.
    :func:`molsysmt.structure.least_rmsd_fit`
        Fit coordinates to an explicit reference structure.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.structure.align_principal_axes import align_principal_axes
    >>> molsys = msm.convert(
    ...     msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    ... )
    >>> aligned = align_principal_axes(
    ...     molsys, structure_indices=0, weights='masses', center=True
    ... )
    >>> axes, _ = msm.structure.get_principal_axes(
    ...     aligned, structure_indices=0, weights='masses'
    ... )
    >>> np.allclose(np.abs(axes[0]), np.eye(3), atol=1.0e-10)
    True


    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Align_principal_axes`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get, set, copy
    from . import get_principal_axes, get_center

    if engine=='MolSysMT':

        if axes is None:
            axes = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        
        axes = np.array(axes, dtype=np.float64, copy=True)

        if not np.all(np.isfinite(axes)):
            raise StructuralInconsistencyError(
                reason="Target axes must contain only finite values.",
                caller="molsysmt.structure.align_principal_axes",
            )
        if not np.allclose(axes @ axes.T, np.eye(3), rtol=0.0, atol=1.0e-10):
            raise StructuralInconsistencyError(
                reason="Target axes must be orthonormal.",
                caller="molsysmt.structure.align_principal_axes",
            )
        if not np.isclose(np.linalg.det(axes), 1.0, rtol=0.0, atol=1.0e-10):
            raise StructuralInconsistencyError(
                reason="Target axes must form a right-handed basis.",
                caller="molsysmt.structure.align_principal_axes",
            )

        if principal_axes_of_selection is None:

            principal_axes_of_selection = selection

        aux_axes, moments = get_principal_axes(molecular_system,
                selection=principal_axes_of_selection, structure_indices=structure_indices,
                principal_axes_type=principal_axes_type,
                weights=weights, syntax=syntax)

        for structure_index, structure_moments in enumerate(moments):
            scale = max(
                float(np.max(np.abs(structure_moments))),
                np.finfo(np.float64).tiny,
            )
            if np.any(np.diff(structure_moments) <= 1.0e-10 * scale):
                raise StructuralInconsistencyError(
                    reason=(
                        "Principal axes are not unique because structure "
                        f"{structure_index} has degenerate principal moments."
                    ),
                    caller="molsysmt.structure.align_principal_axes",
                )

        aux_center = get_center(molecular_system, selection=principal_axes_of_selection,
                structure_indices=structure_indices, weights=weights, syntax=syntax)

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)

        coordinates, length_unit = puw.get_value_and_unit(coordinates)
        aux_center, _ = puw.get_value_and_unit(aux_center)

        n_structures = coordinates.shape[0]

        for ii in range(n_structures):
            coordinates[ii,:,:]=coordinates[ii,:,:]-aux_center[ii,0,:]
            coordinates[ii,:,:]=coordinates[ii,:,:] @ aux_axes[ii].T @ axes
            if not center:
                coordinates[ii,:,:]=coordinates[ii,:,:]+aux_center[ii]

        coordinates = puw.quantity(coordinates, unit=length_unit)

        if in_place:

            set(molecular_system, selection=atom_indices, structure_indices=structure_indices,
                syntax=syntax, coordinates=coordinates)
            del(coordinates, aux_center, aux_axes, moments, atom_indices)

        else:

            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, selection=atom_indices, structure_indices=structure_indices,
                syntax=syntax, coordinates=coordinates)
            del(coordinates, aux_center, aux_axes, moments, atom_indices)

            return tmp_molecular_system

    else:

        raise NotImplementedMethodError()
