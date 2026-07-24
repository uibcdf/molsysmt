from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from molsysmt._private.execution import Reducer
from molsysmt._private.variables import is_all
from molsysmt._private.weighted_geometry import prepare_weights
from smonitor import signal
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


class _RadiusOfGyrationReducer(Reducer):

    def __init__(self, weights):
        self._weights = weights
        self._chunks = []

    def initialize(self, metadata):
        self._chunks = []

    def consume(self, chunk):
        from molsysmt._private import rust_backend as _kernels

        coordinates = np.array(chunk["coordinates"], dtype=np.float64)
        self._chunks.append(
            _kernels.get_radius_of_gyration(coordinates, self._weights)
        )

    def finalize(self):
        return np.concatenate(self._chunks)

    def checkpoint(self):
        return {"chunks": [chunk.tolist() for chunk in self._chunks]}

    def restore(self, state):
        self._chunks = [np.asarray(chunk, dtype=np.float64) for chunk in state["chunks"]]

    def merge(self, other):
        self._chunks.extend(other._chunks)


from molsysmt.configure import with_configure_overrides


@signal(tags=['api', 'structure'])
@arg_digest()
@with_configure_overrides
def get_radius_of_gyration(molecular_system, selection='all', structure_indices='all',
                           weights=None, syntax='MolSysMT', engine='MolSysMT',
                           heavy_mode='auto', use_gpu=None, parallel=None,
                           num_threads=None, skip_digestion=False):
    """
    Computing the radius of gyration over one or more structures.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection over which the radius of gyration is computed.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    weights : array-like, 'masses' or None, default None
        If None, all atoms have equal weight (geometric radius of gyration).
        If 'masses', atoms are weighted by their atomic mass. Explicit weights
        must be non-negative and have a positive sum.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the computation.
    heavy_mode : str, default 'auto'
        Chunked execution path: 'auto' | 'force' | 'off'.
    use_gpu : bool or 'auto', optional
        Whether to use a supported GPU backend on the eager path.
    parallel : bool or str, optional
        Parallel mode override: True | False | 'auto'.
    num_threads : int, optional
        Number of threads override.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Radius of gyration per structure as a PyUnitWizard quantity in length units.
        Shape: (n_structures,).

    Raises
    ------
    ArgumentError
        If the atom or frame selection is empty, or weights are non-finite,
        negative, or have zero total weight.
    ArgumentLengthError
        If the number of weights does not match the selected atoms.
    NotImplementedMethodError
        If an unsupported engine is requested.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    >>> msm.structure.get_radius_of_gyration(molsys).shape
    (1,)

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.structure_indices import ensure_nonempty_structure_indices

    ensure_nonempty_structure_indices(
        structure_indices,
        caller="molsysmt.structure.get_radius_of_gyration",
    )

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt._private import rust_backend as _kernels

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        n_atoms = len(np.atleast_1d(atom_indices))

        weights_arr = prepare_weights(
            weights,
            n_atoms,
            molecular_system=molecular_system,
            selection=atom_indices,
            syntax=syntax,
            caller="molsysmt.structure.get_radius_of_gyration",
        )

        n_structures = get(molecular_system, element='system', n_structures=True)
        from molsysmt._private.execution.memory_policy import estimate_footprint, decide_mode
        from molsysmt.basic import get_form

        form = get_form(molecular_system)
        mode = decide_mode(estimate_footprint(n_atoms, n_structures), heavy_mode)

        if mode == 'heavy':
            from molsysmt._private.execution import ChunkedExecutor

            executor = ChunkedExecutor(
                molecular_system=molecular_system,
                form=form,
                operation='get_radius_of_gyration',
                reducer=_RadiusOfGyrationReducer(weights_arr),
                atom_indices=atom_indices,
                structure_indices=None if is_all(structure_indices) else structure_indices,
                heavy_mode=heavy_mode,
                attributes=['coordinates'],
            )
            rg_val = executor.execute()
            length_unit = puw.get_standard_units(dimensionality={'[L]': 1})
            return puw.quantity(rg_val, length_unit)

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
            rg_val = _kernels.get_radius_of_gyration(coordinates, weights_arr)
        rg = puw.quantity(rg_val, length_unit)
        rg = puw.standardize(rg)

        del coordinates, weights_arr, length_unit
        gc.collect()

        return rg

    else:

        raise NotImplementedMethodError()
