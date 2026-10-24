import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.execution import Reducer
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
)
from molsysmt._private.variables import (
    is_all,
    is_iterable_of_iterables,
    is_iterable_of_pairs,
)


def _validate_coordinate_pair(first, second=None, *, paired=False):
    if not np.isfinite(first).all() or (
        second is not None and not np.isfinite(second).all()
    ):
        raise StructuralInconsistencyError(
            reason="Distance coordinates must be finite.",
            caller="molsysmt.structure.get_distances",
        )
    if second is not None and first.shape[0] != second.shape[0]:
        raise ArgumentError(
            "structure_indices_2",
            caller="molsysmt.structure.get_distances",
            message="Structure lists must have equal length; repeat indices explicitly to reuse a structure.",
        )
    if paired and (second is None or first.shape[1] != second.shape[1]):
        raise ArgumentError(
            "selection_2",
            caller="molsysmt.structure.get_distances",
            message="Paired distances require equal endpoint counts.",
        )


def _validate_boxes(box, n_structures):
    from molsysmt.pbc._whole_participants import validate_periodic_boxes

    validate_periodic_boxes(
        box, n_structures, caller="molsysmt.structure.get_distances"
    )


class _DistancesReducer(Reducer):
    """Reducing selected endpoint blocks with the scalar Rust distance kernels."""

    def __init__(self, first, second, universe, pbc, scale):
        self.first, self.second = first, second
        self._pbc, self.scale = pbc, scale
        self.shared = np.array_equal(first.frames, second.frames)
        self.first_positions = np.searchsorted(universe, first.atoms)
        self.second_positions = (
            np.searchsorted(universe, second.atoms) if self.shared else None
        )
        self.first_identity = np.array_equal(
            self.first_positions, np.arange(len(universe))
        )
        self.second_identity = self.shared and np.array_equal(
            self.second_positions, np.arange(len(universe))
        )
        self.symmetric = self.shared and np.array_equal(first.atoms, second.atoms)

    def estimate_output_shape(self, metadata):
        """Plan actual selected output axes, never the global atom count."""
        import molsysmt.configure as config

        shape = (metadata["n_structures"], self.first.count, self.second.count)
        return shape if np.prod(shape) * 8 > config.max_ram_usage else None

    def initialize(self, metadata):
        self._frame_offset = 0
        self._output_handle = metadata.get("output_handle")
        if self._output_handle is None:
            self._values = np.empty(
                (len(self.first.frames), self.first.count, self.second.count)
            )
        else:
            self._values = self._output_handle

    def consume(self, chunk):
        from ._geometry_endpoints import read_coordinates

        size = len(chunk["coordinates"])
        end = self._frame_offset + size
        coordinates = chunk["coordinates"]
        first = np.ascontiguousarray(
            coordinates if self.first_identity else coordinates[:, self.first_positions]
        )
        if self.symmetric:
            second = first
        elif self.shared:
            second = np.ascontiguousarray(
                coordinates
                if self.second_identity
                else coordinates[:, self.second_positions]
            )
        else:
            second = self.second.geometry(
                read_coordinates(
                    self.second, self.second.frames[self._frame_offset : end], True
                ),
                None,
            )
        _validate_coordinate_pair(first, second)
        box = chunk.get("box") if self._pbc else None
        if box is not None:
            _validate_boxes(box, size)
            result = (
                _kernels.get_mic_distances_single_system(first, box)
                if self.symmetric
                else _kernels.get_mic_distances(first, second, box)
            )
        else:
            result = (
                _kernels.get_distances_single_system(first)
                if self.symmetric
                else _kernels.get_distances(first, second)
            )
        # Convert each block before storage, avoiding a full disk-result copy.
        if self.scale != 1.0:
            result *= self.scale
        self._values[self._frame_offset : end] = result
        self._frame_offset = end

    def finalize(self):
        if self._output_handle is not None:
            self._output_handle.flush()
        return self._values


# Keep this decorator import beside the public function below.
from molsysmt.configure import with_configure_overrides  # noqa: E402


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def get_distances(
    molecular_system,
    selection="all",
    structure_indices="all",
    center_of_atoms=False,
    weights=None,
    molecular_system_2=None,
    selection_2=None,
    structure_indices_2=None,
    center_of_atoms_2=False,
    weights_2=None,
    pairs=False,
    pbc=True,
    output_type="numpy.ndarray",
    output_indices=None,
    output_structure_indices=None,
    engine="MolSysMT",
    syntax="MolSysMT",
    heavy_mode="auto",
    use_gpu=None,
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """
    Computing distances between atoms or centers of selections.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    molecular_system_2 : molecular system or None, default=None
        Second molecular system to compare with the first one.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    pairs : bool, default=False
        Whether corresponding selections define explicit pairs instead of a Cartesian product.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    output_type : str, default='numpy.ndarray'
        Representation used for the returned result.
    output_indices : {'selection', 'atom', 'group'} or None, default=None
        Index convention included with the returned values.
    output_structure_indices : {'selection', 'structure'} or None, default=None
        Structure-index convention included with the returned values.
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Policy controlling the chunked path for memory-intensive calculations.
        Flat atom populations in one system use bounded coordinate blocks and
        the requested, positionally paired structure lists. Internal nm blocks
        are converted to the active PyUnitWizard length standard for output.
        Centers, explicit atom pairs and two-system calculations use the eager
        route. Output exceeding the RAM budget is stored in a disk-backed handle.
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
    quantity, tuple or dict
        Distances with shape `(n_structures, n_selection[, n_selection_2])`
        or structured dictionaries, depending on `output_type`. Heavy output
        exceeding the RAM budget has a PersistentResultHandle magnitude; index
        it in blocks and call its `cleanup()` after use.


    Raises
    ------
    NotImplementedMethodError
        If a requested path/output is not supported.
    ArgumentError
        If structure lists or explicit pair populations differ in length, or weights are supplied for raw atoms.
    MemoryBudgetExceededError
        If one selected scalar slab exceeds the numerical work budget.


    Notes
    -----
    - Uses minimum image convention when `pbc=True` and box is available.
    - When `pairs=True`, expects equal-length explicit pairs; otherwise use Cartesian products.
    - Structure lists are paired positionally, with explicit repeated indices for reuse.
    - Dictionary outputs retain each requested structure pair. Atom keys apply to
      raw atoms; centers require local selection keys. Disk-backed results require
      ndarray output and explicit cleanup by the caller.


    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems["pentalanine"]["traj_pentalanine.h5msm"]
    >>> result = get_distances(molsys, selection=[0, 2, 4], selection_2=[1, 3],
    ...                        structure_indices=[0], pbc=False, heavy_mode="force")
    >>> result.shape
    (1, 3, 2)

    .. admonition:: User guide

       See :ref:`user-tools-distance-family`.

    .. versionadded:: 1.0.0
    """

    # center_of_atoms and center_of_atoms_2: bool
    # output_type in ['numpy.ndarray','dictionary']

    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc = has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection = np.array(selection)
            selection_2 = selection[:, 1]
            selection = selection[:, 0]
        elif len(selection) == 2:
            selection_2 = selection[1]
            selection = selection[0]

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if molecular_system_2 is not None:
        if selection_2 is None:
            selection_2 = selection
        if structure_indices_2 is None:
            structure_indices_2 = structure_indices
        atom_indices_2 = select(
            molecular_system_2, selection=selection_2, syntax=syntax
        )
    else:
        if selection_2 is not None:
            atom_indices_2 = select(
                molecular_system, selection=selection_2, syntax=syntax
            )
        else:
            atom_indices_2 = None

    if len(atom_indices) and is_iterable_of_iterables(atom_indices):
        center_of_atoms = True

    if (
        atom_indices_2 is not None
        and len(atom_indices_2)
        and is_iterable_of_iterables(atom_indices_2)
    ):
        center_of_atoms_2 = True

    if (weights is not None and not center_of_atoms) or (
        weights_2 is not None and not center_of_atoms_2
    ):
        raise ArgumentError(
            "weights",
            caller="molsysmt.structure.get_distances",
            message="Weights require the corresponding center-of-atoms endpoint.",
        )
    if output_indices == "atom" and (center_of_atoms or center_of_atoms_2):
        raise NotImplementedMethodError(caller="molsysmt.structure.get_distances")

    if engine == "MolSysMT":
        # Decide eager vs heavy based on footprint
        from molsysmt._private.execution.memory_policy import (
            decide_mode,
            estimate_footprint,
        )
        from molsysmt.basic import get as msm_get

        if is_all(atom_indices):
            _n_atoms_est = msm_get(molecular_system, element="system", n_atoms=True)
        else:
            _n_atoms_est = len(atom_indices)
        _n_structures_est = msm_get(
            molecular_system, element="system", n_structures=True
        )
        footprint = estimate_footprint(_n_atoms_est, _n_structures_est)
        mode = decide_mode(footprint, heavy_mode)

        heavy_eligible = (
            molecular_system_2 is None
            and not center_of_atoms
            and not center_of_atoms_2
            and not pairs
        )

        if mode == "heavy" and heavy_eligible:
            import molsysmt.configure as config
            from molsysmt._private.execution import ChunkedExecutor

            from ._geometry_endpoints import Endpoint

            caller = "molsysmt.structure.get_distances"
            first = Endpoint(
                molecular_system,
                atom_indices,
                structure_indices,
                False,
                None,
                syntax,
                caller=caller,
            )
            second = Endpoint(
                molecular_system,
                atom_indices if atom_indices_2 is None else atom_indices_2,
                structure_indices
                if structure_indices_2 is None
                else structure_indices_2,
                False,
                None,
                syntax,
                caller=caller,
            )
            if len(first.frames) != len(second.frames):
                raise ArgumentError(
                    "structure_indices_2",
                    caller=caller,
                    message="Structure lists must have equal length.",
                )
            shared = np.array_equal(first.frames, second.frames)
            universe = (
                np.union1d(first.universe, second.universe)
                if shared
                else first.universe
            )
            unit_probe = puw.standardize(puw.quantity(1.0, "nm"))
            output_unit = puw.get_unit(unit_probe)
            scale = float(puw.get_value(unit_probe))
            reducer = _DistancesReducer(first, second, universe, pbc, scale)
            # Include the scalar pair slab when bounding work, rather than only
            # the much smaller coordinate input. One structure is the minimum.
            work_bytes = 16 * first.count * second.count + 48 * (
                len(universe) + len(second.universe)
            )
            if len(first.frames) and work_bytes > config.max_ram_usage:
                raise MemoryBudgetExceededError(
                    reason="One selected distance slab exceeds the numerical work budget.",
                    predicted_bytes=work_bytes,
                    available_bytes=config.max_ram_usage,
                    caller=caller,
                )
            max_chunk_size = max(
                1, int(config.max_ram_usage * 0.1) // max(1, work_bytes)
            )
            dist_val = ChunkedExecutor(
                molecular_system=molecular_system,
                form=first.form,
                operation="get_distances",
                reducer=reducer,
                atom_indices=universe,
                structure_indices=first.frames,
                heavy_mode="force",
                attributes=["coordinates", "box"] if pbc else ["coordinates"],
                max_chunk_size=max_chunk_size,
            ).execute()
            distances = puw.quantity(dist_val, output_unit)

        else:
            distances = _get_distances_in_memory(
                molecular_system,
                selection=atom_indices,
                structure_indices=structure_indices,
                center_of_atoms=center_of_atoms,
                weights=weights,
                molecular_system_2=molecular_system_2,
                selection_2=atom_indices_2,
                structure_indices_2=structure_indices_2,
                center_of_atoms_2=center_of_atoms_2,
                weights_2=weights_2,
                pairs=pairs,
                pbc=pbc,
                syntax=syntax,
                use_gpu=use_gpu,
            )

    else:
        raise NotImplementedMethodError

    if output_type == "numpy.ndarray":
        output_list = []

        if output_indices is not None:
            if pairs:
                raise NotImplementedMethodError(
                    caller="molsysmt.structure.get_distances"
                )

            else:
                if output_indices == "selection":  # works also with center of atoms
                    atom_indices = list(range(distances.shape[-2]))
                    output_list.append(atom_indices)

                    if atom_indices_2 is not None:
                        atom_indices_2 = list(range(distances.shape[-1]))
                        output_list.append(atom_indices_2)

                elif output_indices == "atom":
                    output_list.append(atom_indices)

                    if atom_indices_2 is not None:
                        output_list.append(atom_indices_2)

                elif output_indices == "group":
                    raise NotImplementedMethodError(
                        caller="molsysmt.structure.get_distances"
                    )

        if output_structure_indices is not None:
            if output_structure_indices == "selection":
                structure_indices = list(range(distances.shape[0]))
                output_list.append(structure_indices)

                if structure_indices_2 is not None:
                    structure_indices_2 = list(range(distances.shape[0]))
                    output_list.append(structure_indices_2)

            elif output_structure_indices == "structure":
                if is_all(structure_indices):
                    structure_indices = list(range(distances.shape[0]))
                    output_list.append(structure_indices)
                else:
                    output_list.append(structure_indices.tolist())

                if structure_indices_2 is not None:
                    if is_all(structure_indices_2):
                        structure_indices_2 = list(range(distances.shape[0]))
                        output_list.append(structure_indices_2)
                    else:
                        output_list.append(structure_indices_2.tolist())

        output_list.append(distances)

        if len(output_list) == 1:
            output = output_list[0]
        else:
            output = tuple(output_list)

    elif output_type == "dictionary":
        from ._distance_output import dictionary

        output = dictionary(
            distances,
            atom_indices,
            atom_indices_2,
            structure_indices,
            structure_indices_2,
            pairs,
            output_indices,
            output_structure_indices,
            center_of_atoms or center_of_atoms_2,
        )

    return output


def _get_distances_in_memory(
    molecular_system,
    selection="all",
    structure_indices="all",
    center_of_atoms=False,
    weights=None,
    molecular_system_2=None,
    selection_2=None,
    structure_indices_2=None,
    center_of_atoms_2=False,
    weights_2=None,
    pairs=False,
    pbc=True,
    syntax="MolSysMT",
    use_gpu=None,
):
    """Internal helper to compute distances entirely in memory (no file-backed forms)."""

    from molsysmt.basic import get
    from molsysmt.lib.structure._kernel_inputs import (
        align_coordinates_values_and_unit,
        extract_coordinates_value_and_unit,
    )

    from .get_center import get_center

    if center_of_atoms:
        coordinates = get_center(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            weights=weights,
        )

    else:
        coordinates = get(
            molecular_system,
            element="atom",
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=True,
        )

    if center_of_atoms_2:
        if selection_2 is None:
            selection_2 = selection
        if molecular_system_2 is None:
            molecular_system_2 = molecular_system

        if structure_indices_2 is None:
            structure_indices_2 = structure_indices

        coordinates_2 = get_center(
            molecular_system_2,
            selection=selection_2,
            structure_indices=structure_indices_2,
            weights=weights_2,
        )

    else:
        if (selection_2 is None) and (structure_indices_2 is None):
            if molecular_system_2 is None:
                coordinates_2 = None

            else:
                structure_indices_2 = structure_indices
                selection_2 = selection

                coordinates_2 = get(
                    molecular_system_2,
                    element="atom",
                    selection=selection_2,
                    structure_indices=structure_indices_2,
                    syntax=syntax,
                    coordinates=True,
                )

        else:
            if structure_indices_2 is None:
                structure_indices_2 = structure_indices

            if selection_2 is None:
                selection_2 = selection

            if molecular_system_2 is None:
                molecular_system_2 = molecular_system

            coordinates_2 = get(
                molecular_system_2,
                element="atom",
                selection=selection_2,
                structure_indices=structure_indices_2,
                syntax=syntax,
                coordinates=True,
            )

    from molsysmt._private.gpu import resolve_use_gpu

    if not pairs:
        if coordinates_2 is None:
            coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)
            _validate_coordinate_pair(coordinates)
            payload = coordinates.shape[0] * coordinates.shape[1] * coordinates.shape[1]
            _use_gpu = resolve_use_gpu(use_gpu, payload)

            if pbc:
                box = get(
                    molecular_system,
                    element="system",
                    structure_indices=structure_indices,
                    box=True,
                )
                if box is not None and box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                    _validate_boxes(box, len(coordinates))
                    if _use_gpu:
                        from molsysmt.lib.structure.get_mic_distances_cuda import (
                            get_mic_distances_single_system as _gpu_mic_dist,
                        )

                        distances = _gpu_mic_dist(coordinates, box)
                    else:
                        distances = _kernels.get_mic_distances_single_system(
                            coordinates, box
                        )
                elif _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances_single_system as _gpu_dist,
                    )

                    distances = _gpu_dist(coordinates)
                else:
                    distances = _kernels.get_distances_single_system(coordinates)
            else:
                if _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances_single_system as _gpu_dist,
                    )

                    distances = _gpu_dist(coordinates)
                else:
                    distances = _kernels.get_distances_single_system(coordinates)

        else:
            coordinates, coordinates_2, length_unit = align_coordinates_values_and_unit(
                coordinates, coordinates_2
            )
            _validate_coordinate_pair(coordinates, coordinates_2)
            payload = (
                coordinates.shape[0] * coordinates.shape[1] * coordinates_2.shape[1]
            )
            _use_gpu = resolve_use_gpu(use_gpu, payload)

            if pbc:
                box = get(
                    molecular_system,
                    element="system",
                    structure_indices=structure_indices,
                    box=True,
                )
                if box is not None and box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                    _validate_boxes(box, len(coordinates))
                    if _use_gpu:
                        from molsysmt.lib.structure.get_mic_distances_cuda import (
                            get_mic_distances as _gpu_mic_dist2,
                        )

                        distances = _gpu_mic_dist2(coordinates, coordinates_2, box)
                    else:
                        distances = _kernels.get_mic_distances(
                            coordinates, coordinates_2, box
                        )
                elif _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances as _gpu_dist2,
                    )

                    distances = _gpu_dist2(coordinates, coordinates_2)
                else:
                    distances = _kernels.get_distances(coordinates, coordinates_2)
            else:
                if _use_gpu:
                    from molsysmt.lib.structure.get_distances_cuda import (
                        get_distances as _gpu_dist2,
                    )

                    distances = _gpu_dist2(coordinates, coordinates_2)
                else:
                    distances = _kernels.get_distances(coordinates, coordinates_2)

    else:  # pairs=True
        coordinates, coordinates_2, length_unit = align_coordinates_values_and_unit(
            coordinates, coordinates_2
        )
        _validate_coordinate_pair(coordinates, coordinates_2, paired=True)

        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=structure_indices,
                box=True,
            )
            if box is not None and box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                _validate_boxes(box, len(coordinates))
                distances = _kernels.get_mic_distances_pairs(
                    coordinates, coordinates_2, box
                )
            else:
                distances = _kernels.get_distances_pairs(coordinates, coordinates_2)
        else:
            distances = _kernels.get_distances_pairs(coordinates, coordinates_2)

    distances = puw.quantity(distances, length_unit)
    # We do NOT force standardize here to save time.
    # The result is already in a coherent physical unit.

    return distances
