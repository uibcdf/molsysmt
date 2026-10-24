import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from molsysmt._private.weighted_geometry import prepare_weights
from molsysmt.configure import with_configure_overrides
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def principal_component_analysis(
    molecular_system,
    selection="all",
    structure_indices="all",
    weights=None,
    syntax="MolSysMT",
    engine="MolSysMT",
    use_gpu=None,
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """
    Computing covariance eigenvectors and eigenvalues for selected atoms.

    The selected Cartesian coordinates are flattened in ``x``, ``y``, ``z``
    blocks, centered over the requested structures, and used to construct the
    population covariance matrix. The function returns its eigenvectors and
    eigenvalues in descending eigenvalue order. The first row is therefore the
    principal vector that captures the largest mean squared dispersion. The
    function does not project the input trajectory onto those eigenvectors.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    weights : numpy.ndarray, list, tuple, or quantity, default=None
        One finite nonnegative numerical factor per selected atom, in selection
        order. The sum must be positive; individual zeros are allowed. None uses
        ones. Dimensionless quantities are converted to numerical factors.
        Named weight models and dimensional quantities are unsupported.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    use_gpu : bool, default=None
        Whether to perform computation using GPU acceleration.
    parallel : bool or None, default=None
        Whether to use CPU parallelism, or `None` to use the configured default.
    num_threads : int or None, default=None
        Number of CPU worker threads, or `None` to use the configured default.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple
        ``(eigenvectors, eigenvalues)``. Eigenvectors are a dimensionless
        ``numpy.ndarray`` with shape ``(3*n_atoms, 3*n_atoms)`` and one
        eigenvector per row, ordered from largest to smallest eigenvalue.
        Eigenvalues are a quantity with shape
        ``(3*n_atoms,)`` and squared-coordinate units (normally ``nm**2``).


    Raises
    ------
    ArgumentError
        If coordinates are nonfinite, either observation axis is empty, or
        weights have an invalid dimension, shape or numerical domain.
    ArgumentLengthError
        If the weight count differs from the selected atom count.
    NotImplementedMethodError
        If the engine is unsupported.


    Notes
    -----
    The covariance uses population normalization by ``n_structures``. Each row
    of the first output is an eigenvector; eigenvector signs are arbitrary. The
    first row captures the largest mean squared dispersion. The output does not
    contain per-structure projections. Flattening uses all selected x coordinates,
    then y, then z. Each centered feature is multiplied by the square root of
    its atom's weight before constructing the covariance. Weights are not
    normalized by their sum: multiplying all weights by a positive factor scales
    eigenvalues by that factor. Repeated structures contribute repeated
    observations. One structure gives a zero covariance. Degenerate eigenvalues
    admit different orthonormal bases, so compare their subspaces or covariance
    equations rather than individual vector components. Alignment and periodic
    reconstruction, when needed, must precede this calculation.


    See Also
    --------
    :func:`molsysmt.structure.get_principal_axes` :
        Compute geometric or inertia principal axes for individual structures.


    Examples
    --------
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> from molsysmt.native import Structures
    >>> coordinates = np.array([[[-1.0, 0.0, 0.0]], [[1.0, 0.0, 0.0]]])
    >>> system = Structures(coordinates=coordinates * msm.pyunitwizard.unit('nm'))
    >>> eigenvectors, eigenvalues = msm.structure.principal_component_analysis(
    ...     system, use_gpu=False
    ... )
    >>> eigenvectors.shape
    (3, 3)
    >>> msm.pyunitwizard.get_value(eigenvalues, to_unit='nm**2').tolist()
    [1.0, 0.0, 0.0]
    >>> _, weighted_values = msm.structure.principal_component_analysis(
    ...     system, weights=[4.0], use_gpu=False
    ... )
    >>> msm.pyunitwizard.get_value(weighted_values, to_unit='nm**2').tolist()
    [4.0, 0.0, 0.0]


    .. admonition:: Tutorial with more examples

       See the User Guide tutorial on principal component analysis.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, select

    if engine == "MolSysMT":
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(
            molecular_system,
            element="atom",
            selection=atom_indices,
            structure_indices=structure_indices,
            coordinates=True,
        )
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        caller = "molsysmt.structure.principal_component_analysis"
        if (
            coordinates.ndim != 3
            or coordinates.shape[-1] != 3
            or coordinates.shape[0] == 0
            or not np.all(np.isfinite(coordinates))
        ):
            raise ArgumentError(
                "coordinates",
                caller=caller,
                message="PCA requires finite Cartesian coordinates and at least one structure.",
            )
        if isinstance(weights, str):
            raise ArgumentError(
                "weights",
                caller=caller,
                message="Provide numerical atom weights in selection order, not a named model.",
            )
        if puw.is_quantity(weights):
            if not puw.check(weights, dimensionality={}):
                raise ArgumentError(
                    "weights",
                    caller=caller,
                    message="PCA weights must be dimensionless numerical factors.",
                )
            weights = puw.get_value(weights, to_unit="dimensionless")
        if np.iscomplexobj(weights):
            raise ArgumentError(
                "weights",
                caller=caller,
                message="PCA weights must be real numerical factors.",
            )
        weights = prepare_weights(weights, coordinates.shape[1], caller=caller)

        from molsysmt._private.gpu import resolve_use_gpu

        n_features = coordinates.shape[1] * 3
        payload = coordinates.shape[0] * n_features * n_features
        if resolve_use_gpu(use_gpu, payload):
            from molsysmt.lib.structure.principal_component_analysis_cuda import (
                principal_component_analysis as _gpu_pca,
            )

            eigenvalues, eigenvectors = _gpu_pca(coordinates, weights)
        else:
            eigenvalues, eigenvectors = _kernels.principal_component_analysis(
                coordinates, weights
            )

        eigenvalues = eigenvalues[::-1].copy()
        eigenvectors = eigenvectors[::-1].copy()
        eigenvalues = puw.quantity(eigenvalues, length_unit**2)
        eigenvalues = puw.standardize(eigenvalues)

        del (coordinates, atom_indices, weights)

        return eigenvectors, eigenvalues

    else:
        raise NotImplementedMethodError()


# https://manual.gromacs.org/documentation/2019-rc1/reference-manual/analysis/covariance-analysis.html
