from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import lib as msmlib
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt._private.execution import Reducer
from molsysmt._private.weighted_geometry import prepare_weights
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


class _CenterReducer(Reducer):
    """
    Reducer for get_center heavy path.
    Accumulates per-chunk center arrays and concatenates them on finalize.
    """

    def __init__(self, weights, atoms_per_group=None):
        self._weights = weights
        self._atoms_per_group = atoms_per_group
        self._n_groups = 1 if atoms_per_group is None else len(atoms_per_group)
        self._chunks = []

    def initialize(self, metadata):
        self._chunks = []

    def consume(self, chunk):
        coords = chunk['coordinates']  # (chunk_size, n_atoms, 3), float64, read-only
        coords_w = np.array(coords, dtype=np.float64)  # writable copy for kernel
        if self._atoms_per_group is None:
            result = msmlib.structure.get_center(coords_w, self._weights)
        else:
            result = msmlib.structure.get_center_groups_of_atoms(coords_w, self._atoms_per_group, self._weights)
        self._chunks.append(result)

    def finalize(self):
        return np.concatenate(self._chunks, axis=0)

    # --- optional extensions ---

    def checkpoint(self):
        return {'chunks': [c.tolist() for c in self._chunks]}

    def restore(self, state):
        self._chunks = [np.array(c, dtype=np.float64) for c in state['chunks']]

    def merge(self, other):
        self._chunks.extend(other._chunks)


from molsysmt.configure import with_configure_overrides

@signal(tags=['api', 'structure'])
@arg_digest()
@with_configure_overrides
def get_center(molecular_system, selection='all', weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT',
        heavy_mode='auto', parallel=None, num_threads=None, skip_digestion=False):
    """
    Computing centers (centroids or weighted centers) of atom selections.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms (or groups of atoms) to center; nested iterables are treated as groups.
    weights : array-like or 'masses', optional
        Non-negative weights per atom (or per group) when computing centers.
        Use ``'masses'`` to compute centers of mass. Every group must have a
        positive total weight.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames over which centers are computed.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    heavy_mode : str, default 'auto'
        Chunked execution mode: 'auto' | 'force' | 'off'.
    parallel : bool or str, optional
        Parallel mode override: True | False | 'auto'.
    num_threads : int, optional
        Number of threads override.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Centers as a PyUnitWizard quantity in length units.

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
    >>> msm.structure.get_center(molsys, weights='masses').shape
    (1, 1, 3)

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get
    from molsysmt._private.structure_indices import ensure_nonempty_structure_indices

    ensure_nonempty_structure_indices(
        structure_indices,
        caller="molsysmt.structure.get_center",
    )

    if engine == 'MolSysMT':

        atom_indices = select(molecular_system, selection=selection)

        if not is_iterable_of_iterables(atom_indices):

            n_atoms = len(np.atleast_1d(atom_indices)) if not is_all(atom_indices) else \
                get(molecular_system, element='system', n_atoms=True)
            n_structures = get(molecular_system, element='system', n_structures=True)

            weights_arr = prepare_weights(
                weights,
                n_atoms,
                molecular_system=molecular_system,
                selection=atom_indices,
                syntax=syntax,
                caller="molsysmt.structure.get_center",
            )

            from molsysmt._private.execution import ChunkedExecutor
            from molsysmt._private.execution.memory_policy import estimate_footprint, decide_mode
            from molsysmt.basic import get_form

            form = get_form(molecular_system)
            footprint = estimate_footprint(n_atoms, n_structures)
            mode = decide_mode(footprint, heavy_mode)

            if mode == 'heavy':
                reducer = _CenterReducer(weights=weights_arr)
                executor = ChunkedExecutor(
                    molecular_system=molecular_system,
                    form=form,
                    operation='get_center',
                    reducer=reducer,
                    atom_indices=atom_indices,
                    structure_indices=None if is_all(structure_indices) else structure_indices,
                    heavy_mode=heavy_mode,
                    attributes=['coordinates'],
                )
                center_val = executor.execute()  # (n_structures, 1, 3), float64, nm
                length_unit = puw.get_standard_units(dimensionality={'[L]': 1})
                center = puw.quantity(center_val, length_unit)
            else:
                coordinates = get(molecular_system, element='atom', selection=atom_indices,
                        structure_indices=structure_indices, coordinates=True)
                coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

                center = msmlib.structure.get_center(coordinates, weights_arr)
                center = puw.quantity(center, length_unit)

                del coordinates, length_unit

        else:

            atoms_per_group = np.array([len(group) for group in atom_indices], dtype=np.int64)
            groups_of_atoms = np.concatenate(atom_indices)
            n_atoms_flat = len(groups_of_atoms)
            n_structures = get(molecular_system, element='system', n_structures=True)

            if weights is not None and not isinstance(weights, str):
                if is_iterable_of_iterables(weights):
                    weights = np.concatenate(weights)
            weights_arr = prepare_weights(
                weights,
                n_atoms_flat,
                molecular_system=molecular_system,
                selection=groups_of_atoms,
                syntax=syntax,
                group_sizes=atoms_per_group,
                caller="molsysmt.structure.get_center",
            )

            from molsysmt._private.execution.memory_policy import estimate_footprint, decide_mode
            from molsysmt.basic import get_form

            form = get_form(molecular_system)
            footprint = estimate_footprint(n_atoms_flat, n_structures)
            mode = decide_mode(footprint, heavy_mode)

            if mode == 'heavy':
                reducer = _CenterReducer(weights=weights_arr, atoms_per_group=atoms_per_group)
                from molsysmt._private.execution import ChunkedExecutor
                executor = ChunkedExecutor(
                    molecular_system=molecular_system,
                    form=form,
                    operation='get_center',
                    reducer=reducer,
                    atom_indices=groups_of_atoms,
                    structure_indices=None if is_all(structure_indices) else structure_indices,
                    heavy_mode=heavy_mode,
                    attributes=['coordinates'],
                )
                center_val = executor.execute()  # (n_structures, n_groups, 3)
                length_unit = puw.get_standard_units(dimensionality={'[L]': 1})
                center = puw.quantity(center_val, length_unit)
            else:
                coordinates = get(molecular_system, element='atom', selection=groups_of_atoms,
                        structure_indices=structure_indices, coordinates=True)
                coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

                center = msmlib.structure.get_center_groups_of_atoms(coordinates, atoms_per_group, weights_arr)
                center = puw.quantity(center, length_unit)

                del coordinates, length_unit, groups_of_atoms, weights_arr

        center = puw.standardize(center)

        gc.collect()

        return center

    else:

        raise NotImplementedMethodError()
