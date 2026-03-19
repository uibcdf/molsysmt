from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt import lib as msmlib
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


class _CenterReducer:
    """
    Reducer for get_center heavy path.
    Accumulates per-chunk center arrays and concatenates them on finalize.
    """

    def __init__(self, weights, atoms_per_group=None):
        self._weights = weights
        self._atoms_per_group = atoms_per_group
        self._chunks = []
        self._length_unit = None

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


@signal(tags=['api', 'structure'])
@arg_digest()
def get_center(molecular_system, selection='all', weights=None,
        structure_indices='all', syntax='MolSysMT', engine='MolSysMT',
        heavy_mode='auto', skip_digestion=False):
    """
    Computing centers (centroids or weighted centers) of atom selections.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms (or groups of atoms) to center; nested iterables are treated as groups.
    weights : array-like, optional
        Weights per atom (or concatenated per group) when computing centers.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames over which centers are computed.
    syntax : str, default 'MolSysMT'
        Selection syntax when using strings.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    heavy_mode : str, default 'auto'
        Chunked execution mode: 'auto' | 'force' | 'off'.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Centers as a PyUnitWizard quantity in length units.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, get

    if engine == 'MolSysMT':

        atom_indices = select(molecular_system, selection=selection)

        if not is_iterable_of_iterables(atom_indices):

            n_atoms = len(np.atleast_1d(atom_indices)) if not is_all(atom_indices) else \
                get(molecular_system, element='system', n_atoms=True)
            n_structures = get(molecular_system, element='system', n_structures=True)

            if weights is None:
                weights_arr = np.ones((n_atoms,), dtype=np.float64)
            else:
                weights_arr = np.asarray(weights, dtype=np.float64)

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

            if weights is None:
                weights_arr = np.ones((n_atoms_flat,), dtype=np.float64)
            else:
                weights_arr = np.concatenate(weights).astype(np.float64)

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
