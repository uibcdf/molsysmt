from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from molsysmt._private.execution import Reducer
from molsysmt._private.variables import is_all
from smonitor import signal
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


class _RMSFReducer(Reducer):
    """Combine chunk fluctuations with the parallel variance formula."""

    def initialize(self, metadata):
        self._count = 0
        self._mean = None
        self._m2 = None

    def consume(self, chunk):
        coordinates = np.asarray(chunk["coordinates"], dtype=np.float64)
        chunk_count = coordinates.shape[0]
        if chunk_count == 0:
            return
        chunk_mean = np.mean(coordinates, axis=0)
        deviations = coordinates - chunk_mean
        chunk_m2 = np.sum(deviations * deviations, axis=(0, 2))
        if self._count == 0:
            self._count = chunk_count
            self._mean = chunk_mean
            self._m2 = chunk_m2
            return
        total = self._count + chunk_count
        delta = chunk_mean - self._mean
        self._m2 += chunk_m2 + np.sum(delta * delta, axis=1) * (
            self._count * chunk_count / total
        )
        self._mean += delta * (chunk_count / total)
        self._count = total

    def finalize(self):
        return np.sqrt(self._m2 / self._count)

    def checkpoint(self):
        return {
            "count": self._count,
            "mean": None if self._mean is None else self._mean.tolist(),
            "m2": None if self._m2 is None else self._m2.tolist(),
        }

    def restore(self, state):
        self._count = state["count"]
        self._mean = None if state["mean"] is None else np.asarray(state["mean"], dtype=np.float64)
        self._m2 = None if state["m2"] is None else np.asarray(state["m2"], dtype=np.float64)

    def merge(self, other):
        if other._count == 0:
            return
        if self._count == 0:
            self._count = other._count
            self._mean = other._mean.copy()
            self._m2 = other._m2.copy()
            return
        total = self._count + other._count
        delta = other._mean - self._mean
        self._m2 += other._m2 + np.sum(delta * delta, axis=1) * (
            self._count * other._count / total
        )
        self._mean += delta * (other._count / total)
        self._count = total


from molsysmt.configure import with_configure_overrides


@signal(tags=['api', 'structure'])
@arg_digest()
@with_configure_overrides
def get_rmsf(molecular_system, selection='atom_type!="H"', structure_indices='all',
             syntax='MolSysMT', engine='MolSysMT', heavy_mode='auto',
             parallel=None, num_threads=None, skip_digestion=False):
    """
    Computing root-mean-square fluctuations per atom over a set of structures.

    The RMSF of atom *i* is defined as:

    .. math::

        \\mathrm{RMSF}_i = \\sqrt{\\frac{1}{T} \\sum_{t=1}^{T}
        \\left| \\mathbf{r}_i(t) - \\langle \\mathbf{r}_i \\rangle \\right|^2}

    where :math:`\\langle \\mathbf{r}_i \\rangle` is the time-averaged position of atom *i*
    and *T* is the number of structures.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'atom_type!="H"'
        Atom selection for which RMSF is computed.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the computation.
    heavy_mode : str, default 'auto'
        Chunked execution path: 'auto' | 'force' | 'off'.
    parallel : bool or str, optional
        Parallel mode override: True | False | 'auto'.
    num_threads : int, optional
        Number of threads override.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        RMSF per selected atom as a PyUnitWizard quantity in length units.
        Shape: (n_atoms,).

    Raises
    ------
    ArgumentError
        If the atom or frame selection is empty.
    NotImplementedMethodError
        If an unsupported engine is requested.

    Notes
    -----
    All structures must be pre-aligned to a common reference frame before calling
    this function if positional fluctuations relative to a reference are intended.
    Use :func:`molsysmt.structure.least_rmsd_align` to align first.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], to_form='molsysmt.MolSys')
    >>> msm.structure.get_rmsf(molsys, selection='all').shape[0] == msm.get(molsys, n_atoms=True)
    True

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.structure_indices import ensure_nonempty_structure_indices

    ensure_nonempty_structure_indices(
        structure_indices,
        caller="molsysmt.structure.get_rmsf",
    )

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt._private import rust_backend as _kernels

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        n_atoms = len(np.atleast_1d(atom_indices))
        if n_atoms == 0:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError(
                "selection",
                value=selection,
                caller="molsysmt.structure.get_rmsf",
                message="The atom selection must contain at least one atom.",
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
                operation='get_rmsf',
                reducer=_RMSFReducer(),
                atom_indices=atom_indices,
                structure_indices=None if is_all(structure_indices) else structure_indices,
                heavy_mode=heavy_mode,
                attributes=['coordinates'],
            )
            rmsf_val = executor.execute()
            length_unit = puw.get_standard_units(dimensionality={'[L]': 1})
            return puw.quantity(rmsf_val, length_unit)

        coordinates = get(molecular_system, element='atom', selection=atom_indices,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        rmsf_val = _kernels.get_rmsf(coordinates)
        rmsf = puw.quantity(rmsf_val, length_unit)
        rmsf = puw.standardize(rmsf)

        del coordinates, length_unit
        gc.collect()

        return rmsf

    else:

        raise NotImplementedMethodError()
