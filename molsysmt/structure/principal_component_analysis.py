from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private import rust_backend as _kernels
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def principal_component_analysis(molecular_system, selection='all', structure_indices='all',
        weights=None, syntax='MolSysMT', engine='MolSysMT', use_gpu=None,
        skip_digestion=False):
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
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to include in the PCA.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to analyze.
    weights : array-like, optional
        Dimensionless weights per atom. Unit weights are used by default.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

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
    NotImplementedMethodError
        If the engine is unsupported.

    Notes
    -----
    The covariance uses population normalization by ``n_structures``. Each row
    of the first output is an eigenvector; eigenvector signs are arbitrary. The
    first row captures the largest mean squared dispersion. The output does not
    contain per-structure projections.

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

    .. admonition:: Tutorial with more examples

       See the User Guide tutorial on principal component analysis.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        if weights is None:
            weights = np.ones((coordinates.shape[1]), dtype=np.float64)

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

        del(coordinates, atom_indices, weights)

        gc.collect()

        return eigenvectors, eigenvalues

    else:

        raise NotImplementedMethodError()

# https://manual.gromacs.org/documentation/2019-rc1/reference-manual/analysis/covariance-analysis.html
