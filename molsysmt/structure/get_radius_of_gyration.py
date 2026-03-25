from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from smonitor import signal
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


@signal(tags=['api', 'structure'])
@arg_digest()
def get_radius_of_gyration(molecular_system, selection='all', structure_indices='all',
                           weights=None, syntax='MolSysMT', engine='MolSysMT',
                           use_gpu=None):
    """
    Radius of gyration of a selection of atoms over one or more structures.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection over which the radius of gyration is computed.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    weights : None or 'masses', default None
        If None, all atoms have equal weight (geometric radius of gyration).
        If 'masses', atoms are weighted by their atomic mass.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the computation.

    Returns
    -------
    quantity
        Radius of gyration per structure as a PyUnitWizard quantity in length units.
        Shape: (n_structures,).

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt import lib as msmlib

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        n_atoms = len(np.atleast_1d(atom_indices))

        if weights is None:
            weights_arr = np.ones(n_atoms, dtype=np.float64)
        elif weights == 'masses':
            from molsysmt.physchem import get_mass
            masses = get_mass(molecular_system, element='atom', selection=selection, syntax=syntax)
            weights_arr = np.asarray(puw.get_value(masses), dtype=np.float64)
        else:
            weights_arr = np.asarray(weights, dtype=np.float64)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                          structure_indices=structure_indices, coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        from molsysmt._private.gpu import resolve_use_gpu
        payload = coordinates.shape[0] * coordinates.shape[1] * 3
        if resolve_use_gpu(use_gpu, payload):
            from molsysmt.lib.structure.get_radius_of_gyration_cuda import (
                get_radius_of_gyration as _gpu_kernel,
            )
            rg_val = _gpu_kernel(coordinates, weights_arr)
        else:
            rg_val = msmlib.structure.get_radius_of_gyration(coordinates, weights_arr)
        rg = puw.quantity(rg_val, length_unit)
        rg = puw.standardize(rg)

        del coordinates, weights_arr, length_unit
        gc.collect()

        return rg

    else:

        raise NotImplementedMethodError()
