from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import lib as msmlib
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc

@arg_digest()
def principal_component_analysis(molecular_system, selection='all', structure_indices='all',
        weights=None, syntax='MolSysMT', engine='MolSysMT', skip_digestion=False):
    """
    Performing principal component analysis (PCA) on selected atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to include in the PCA.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to analyze.
    weights : array-like, optional
        Weights per atom.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    tuple
        `(principal_components, variances)` as returned by the backend.

    Raises
    ------
    NotImplementedMethodError
        If the engine is unsupported.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get

    if engine=='MolSysMT':

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                structure_indices=structure_indices, coordinates=True)
        coordinates, length_unit = puw.get_value_and_unit(coordinates)

        if weights is None:
            weights = np.ones((coordinates.shape[1]), dtype=np.float64)

        variances, principal_components = msmlib.structure.principal_component_analysis(coordinates, weights)

        del(coordinates, atom_indices, weights)

        gc.collect()

        return principal_components, variances

    else:

        raise NotImplementedMethodError()

# https://manual.gromacs.org/documentation/2019-rc1/reference-manual/analysis/covariance-analysis.html
