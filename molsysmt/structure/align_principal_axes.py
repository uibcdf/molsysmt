from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

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
        System whose coordinates will be rotated.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to rotate.
    principal_axes_of_selection : str, list, tuple or numpy.ndarray, optional
        Atoms used to compute principal axes; defaults to `selection`.
    principal_axes_type : {'inertia', 'geometric'}, default 'inertia'
        Type of principal axes to compute.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to align.
    weights : array-like, quantity, 'masses' or None, default None
        Non-negative weights used for both the axes and center. ``None`` uses
        unit weights. Use ``'masses'`` for physical inertia axes.
    axes : array-like shape (3,3), default identity
        Target axes to align to.
    center : bool, default False
        If True, recenter coordinates after rotation.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    in_place : bool, default False
        If True, modify the input system; otherwise return a rotated copy.

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
    >>> molsys = msm.convert(
    ...     msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    ... )
    >>> aligned = msm.structure.align_principal_axes(
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
            gc.collect()

        else:

            tmp_molecular_system = copy(molecular_system)
            set(tmp_molecular_system, selection=atom_indices, structure_indices=structure_indices,
                syntax=syntax, coordinates=coordinates)
            del(coordinates, aux_center, aux_axes, moments, atom_indices)
            gc.collect()

            return tmp_molecular_system

    else:

        raise NotImplementedMethodError()
