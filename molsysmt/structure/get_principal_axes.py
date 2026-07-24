from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.weighted_geometry import prepare_weights
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def get_principal_axes(molecular_system, selection='all', structure_indices='all',
        weights=None, principal_axes_type='inertia', syntax='MolSysMT', engine='MolSysMT',
        use_gpu=None, skip_digestion=False):
    """
    Computing principal axes for a selection of atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms used for axis computation.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to evaluate.
    weights : array-like, quantity, 'masses' or None, default None
        Non-negative weights per atom. ``None`` assigns unit weight to every
        atom. Use ``'masses'`` for physical principal inertia axes.
    principal_axes_type : {'inertia', 'geometric'}, default 'inertia'
        Kind of principal axes to compute.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    use_gpu : bool or 'auto', optional
        Whether to use a supported GPU backend.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    tuple
        ``(axes, moments)`` where ``axes`` has shape
        ``(n_structures, 3, 3)`` and ``moments`` has shape
        ``(n_structures, 3)``. Moments are geometric variances or inertia
        moments, depending on ``principal_axes_type``.

    Raises
    ------
    ArgumentError
        If the atom or frame selection is empty, or weights are invalid.
    ArgumentLengthError
        If the number of weights does not match the selected atoms.
    NotImplementedMethodError
        If the engine is unsupported.

    Notes
    -----
    Axes are returned as rows, ordered by ascending eigenvalue, and form a
    right-handed orthonormal basis. Individual axis signs are mathematically
    arbitrary. Degenerate eigenvalues define a subspace rather than unique
    individual axes.

    See Also
    --------
    :func:`molsysmt.structure.align_principal_axes`
        Align coordinates to a target principal-axis basis.
    :func:`molsysmt.structure.get_center`
        Compute geometric or weighted centers.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> axes, moments = msm.structure.get_principal_axes(
    ...     molsys, structure_indices=0, weights='masses'
    ... )
    >>> axes.shape, moments.shape
    ((1, 3, 3), (1, 3))
    >>> round(float(np.linalg.det(axes[0])), 12)
    1.0

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_principal_axes`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get
    from molsysmt._private.structure_indices import ensure_nonempty_structure_indices

    ensure_nonempty_structure_indices(
        structure_indices,
        caller="molsysmt.structure.get_principal_axes",
    )

    if engine=='MolSysMT':

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)
        coordinates, _ = puw.get_value_and_unit(coordinates)
        coordinates = np.asarray(coordinates, dtype=np.float64)

        weights = prepare_weights(
            weights,
            coordinates.shape[1],
            molecular_system=molecular_system,
            selection=atom_indices,
            syntax=syntax,
            caller="molsysmt.structure.get_principal_axes",
        )

        from molsysmt._private.gpu import resolve_use_gpu
        payload = coordinates.shape[0] * coordinates.shape[1] * 3
        _use_gpu = resolve_use_gpu(use_gpu, payload)

        if principal_axes_type == 'geometric':
            if _use_gpu:
                from molsysmt.lib.structure.get_principal_axes_cuda import (
                    get_principal_geometric_axes as _gpu_geo,
                )
                variances, axes = _gpu_geo(coordinates, weights)
            else:
                variances, axes = _kernels.get_principal_geometric_axes(coordinates, weights)
            moments = variances

        elif principal_axes_type == 'inertia':
            if _use_gpu:
                from molsysmt.lib.structure.get_principal_axes_cuda import (
                    get_principal_inertia_axes as _gpu_inertia,
                )
                moments, axes = _gpu_inertia(coordinates, weights)
            else:
                moments, axes = _kernels.get_principal_inertia_axes(coordinates, weights)

        for structure_index in range(axes.shape[0]):
            if np.linalg.det(axes[structure_index]) < 0.0:
                axes[structure_index, 2] *= -1.0

        del(coordinates, atom_indices, weights)

        gc.collect()

        return axes, moments

    else:

        raise NotImplementedMethodError()
