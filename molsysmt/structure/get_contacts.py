import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    warn,
)
from molsysmt._private.variables import is_iterable_of_pairs
from molsysmt.configure import with_configure_overrides


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def get_contacts(
    molecular_system,
    selection=None,
    center_of_atoms=False,
    weights=None,
    structure_indices="all",
    selection_2=None,
    center_of_atoms_2=False,
    weights_2=None,
    structure_indices_2=None,
    threshold="12 angstroms",
    pairs=False,
    pbc=True,
    syntax="MolSysMT",
    output_type="numpy.ndarray",
    output_indices=None,
    use_gpu=None,
    gpu_backend=None,
    cell_list=None,
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """
    Computing a boolean contact map between two sets of atoms (or atom-group centers).

    Internally calls ``get_distances`` and applies a distance threshold to produce
    a contact map.  When only one selection is provided the contact map is computed
    between all pairs within that selection.  When both ``selection`` and
    ``selection_2`` are provided the map is computed between the two sets.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default=None
        Selection string or boolean/integer array specifying elements.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    threshold : float or quantity, default='12 angstroms'
        Distance cutoff threshold quantity.
    pairs : bool, default=False
        Whether corresponding selections define explicit pairs instead of a Cartesian product.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    output_type : str, default='numpy.ndarray'
        Representation used for the returned result.
    output_indices : {'selection', 'atom', 'group'} or None, default=None
        Index convention included with the returned values.
    use_gpu : bool, default=None
        Whether to perform computation using GPU acceleration.
    gpu_backend : str or None, default=None
        GPU array backend, or `None` to use the configured backend.
    cell_list : {'auto'}, bool, or None, default=None
        Whether to use cell-list acceleration for eligible contact calculations.
    parallel : bool or None, default=None
        Whether to use CPU parallelism, or `None` to use the configured default.
    num_threads : int or None, default=None
        Number of CPU worker threads, or `None` to use the configured default.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or list
        Contact map as a boolean ``numpy.ndarray`` (``output_type='numpy.ndarray'``)
        or as a list of contacting pairs per structure (``output_type='pairs'`` or
        ``'sorted pairs'``).


    Raises
    ------
    ArgumentError
        If a threshold or endpoint population is invalid.
    MemoryBudgetExceededError
        If the resident boolean map exceeds the configured numeric-output budget.
    NotImplementedMethodError
        If output labels or representation are unsupported.

    Notes
    -----
    Contacts include distances equal to the finite nonnegative threshold. An
    implicit same-structure dense self map includes its diagonal; pair output
    retains only its strict upper triangle. Explicit endpoint structures retain
    all directed entries. Atom-index pair output uses resolved selections.
    The full boolean map remains resident, including when pairs are returned.
    Coordinate preparation for accelerated dispatch has its own RAM cost;
    internal disk distance intermediates are consumed by structure and retired.
    This function has no molecular_system_2 argument. Actual GPU qualification
    is separate from CPU fallback when a GPU selector is unavailable.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['particles 4']['traj_particles_4.xyznpy']
    >>> contacts = get_contacts(source, selection=[0], selection_2=[1, 2],
    ...     threshold='2 nm', pbc=False, cell_list=False, use_gpu=False)
    >>> contacts.shape, str(contacts.dtype)
    ((3, 1, 2), 'bool')

    .. admonition:: User guide

       See :ref:`user-tools-distance-family`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, select
    from molsysmt.pbc import has_pbc
    from molsysmt.structure.get_distances import (
        _validate_boxes,
        _validate_coordinate_pair,
        get_distances,
    )

    caller = "molsysmt.structure.get_contacts"
    cutoff_nm = puw.get_value(threshold, to_unit="nm")
    if np.ndim(cutoff_nm) != 0 or not np.isfinite(cutoff_nm) or cutoff_nm < 0:
        raise ArgumentError(
            "threshold",
            caller=caller,
            message="Cutoffs must be finite nonnegative scalar lengths.",
        )
    if (
        output_type not in {"numpy.ndarray", "pairs", "sorted pairs"}
        or output_indices == "group"
    ):
        raise NotImplementedMethodError(caller=caller)
    if selection is None:
        selection = "all"

    if pbc:
        pbc = has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection = np.array(selection)
            selection_2 = selection[:, 1]
            selection = selection[:, 0]
        elif len(selection) == 2:
            selection, selection_2 = selection[0], selection[1]
        else:
            raise ArgumentError(
                "selection",
                caller=caller,
                message="Provide two endpoint selections or explicit atom pairs.",
            )

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if selection_2 is None:
        atom_indices_2 = None
    else:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)

    from molsysmt._private.variables import is_iterable_of_iterables

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
            caller=caller,
            message="Weights require the corresponding center endpoint.",
        )
    if output_indices == "atom" and (center_of_atoms or center_of_atoms_2):
        raise NotImplementedMethodError(caller=caller)

    # Check if GPU execution is requested and resolved
    import molsysmt.configure as config
    from molsysmt._private.gpu import resolve_use_gpu
    from molsysmt.lib.structure._kernel_inputs import (
        align_coordinates_values_and_unit,
        extract_coordinates_value_and_unit,
    )

    # 1. Fetch coordinates
    if center_of_atoms:
        from molsysmt.structure.get_center import get_center

        coordinates = get_center(
            molecular_system,
            selection=atom_indices,
            structure_indices=structure_indices,
            weights=weights,
        )
    else:
        coordinates = get(
            molecular_system,
            element="atom",
            selection=atom_indices,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=True,
        )

    if (
        atom_indices_2 is not None
        or structure_indices_2 is not None
        or center_of_atoms_2
    ):
        second_atoms = atom_indices if atom_indices_2 is None else atom_indices_2
        if center_of_atoms_2:
            from molsysmt.structure.get_center import get_center

            coordinates_2 = get_center(
                molecular_system,
                selection=second_atoms,
                structure_indices=structure_indices
                if structure_indices_2 is None
                else structure_indices_2,
                weights=weights_2,
            )
        else:
            coordinates_2 = get(
                molecular_system,
                element="atom",
                selection=second_atoms,
                structure_indices=structure_indices
                if structure_indices_2 is None
                else structure_indices_2,
                syntax=syntax,
                coordinates=True,
            )
    else:
        coordinates_2 = None

    # Calculate payload size
    coords_val, length_unit = extract_coordinates_value_and_unit(coordinates)
    if coordinates_2 is None:
        coords_2_val = None
        if pairs:
            payload = coords_val.shape[0] * coords_val.shape[1]
        else:
            payload = coords_val.shape[0] * coords_val.shape[1] * coords_val.shape[1]
    else:
        _, coords_2_val, _ = align_coordinates_values_and_unit(
            coordinates, coordinates_2
        )
        if pairs:
            payload = coords_val.shape[0] * coords_val.shape[1]
        else:
            payload = coords_val.shape[0] * coords_val.shape[1] * coords_2_val.shape[1]

    _validate_coordinate_pair(coords_val, coords_2_val, paired=pairs)
    output_bytes = payload
    if output_bytes > config.max_ram_usage:
        raise MemoryBudgetExceededError(
            reason="The resident boolean contact map exceeds the configured budget.",
            predicted_bytes=output_bytes,
            available_bytes=config.max_ram_usage,
            caller=caller,
        )

    # Resolve GPU execution
    _use_gpu = resolve_use_gpu(use_gpu, payload)

    # If GPU is resolved, choose the backend
    contact_map = None
    if _use_gpu:
        # Convert threshold value to length unit of coordinates
        threshold_val = puw.get_value(threshold, to_unit=length_unit)

        # Get box if pbc is requested
        box = None
        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=structure_indices,
                box=True,
            )
            if box is not None and box[0] is not None:
                box = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                _validate_boxes(box, len(coords_val))
            else:
                box = None

        # Check if we should use Taichi Lang backend
        if config.gpu_backend == "taichi":
            try:
                __import__("taichi")

                taichi_available = True
            except ImportError:
                taichi_available = False
                from molsysmt._private.smonitor import GpuNotAvailableWarning

                warn(
                    GpuNotAvailableWarning(reason="the taichi package is not installed")
                )

            if taichi_available:
                if pairs:
                    if coords_2_val is None:
                        coords_2_val = coords_val
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_mic_contacts_pairs as _kernel,
                        )

                        contact_map = _kernel(
                            coords_val, coords_2_val, box, threshold_val
                        )
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_contacts_pairs as _kernel,
                        )

                        contact_map = _kernel(coords_val, coords_2_val, threshold_val)
                elif coords_2_val is None:
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_mic_contacts_single_system as _kernel,
                        )

                        contact_map = _kernel(coords_val, box, threshold_val)
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_contacts_single_system as _kernel,
                        )

                        contact_map = _kernel(coords_val, threshold_val)
                else:
                    if box is not None:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_mic_contacts as _kernel,
                        )

                        contact_map = _kernel(
                            coords_val, coords_2_val, box, threshold_val
                        )
                    else:
                        from molsysmt.lib.structure.get_contacts_taichi import (
                            get_contacts as _kernel,
                        )

                        contact_map = _kernel(coords_val, coords_2_val, threshold_val)

        # Retired experimental CUDA branch.
        if contact_map is None:
            if pairs:
                if coords_2_val is None:
                    coords_2_val = coords_val
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_mic_contacts_pairs as _kernel,
                    )

                    contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_contacts_pairs as _kernel,
                    )

                    contact_map = _kernel(coords_val, coords_2_val, threshold_val)
            elif coords_2_val is None:
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_mic_contacts_single_system as _kernel,
                    )

                    contact_map = _kernel(coords_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_contacts_single_system as _kernel,
                    )

                    contact_map = _kernel(coords_val, threshold_val)
            else:
                if box is not None:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_mic_contacts as _kernel,
                    )

                    contact_map = _kernel(coords_val, coords_2_val, box, threshold_val)
                else:
                    from molsysmt.lib.structure.get_contacts_cuda import (
                        get_contacts as _kernel,
                    )

                    contact_map = _kernel(coords_val, coords_2_val, threshold_val)

    # Fallback to CPU pipeline if GPU was not used
    if contact_map is None:
        _use_cell_list = config.cell_list
        if _use_cell_list == "auto":
            # The cell-list beats the dense O(N^2) matrix from ~500 query atoms (measured
            # 8-180x); below ~300 both paths are sub-ms. The threshold is tuned for the
            # Supported Rust kernel.
            _use_cell_list = coords_val.shape[1] > 400

        if (
            _use_cell_list
            and not pairs
            and cutoff_nm > 0
            and coords_val.shape[0] > 0
            and coords_val.shape[1] > 0
            and (coords_2_val is None or coords_2_val.shape[1] > 0)
        ):
            if coords_2_val is None:
                tmp_coords_2_val = coords_val
                is_self = True
            else:
                tmp_coords_2_val = coords_2_val
                is_self = False

            threshold_val = puw.get_value(threshold, to_unit=length_unit)

            box_val = None
            if pbc:
                box = get(
                    molecular_system,
                    element="system",
                    structure_indices=structure_indices,
                    box=True,
                )
                if box is not None and box[0] is not None:
                    box_val = puw.get_value(box, to_unit=length_unit, dtype=np.float64)
                    _validate_boxes(box_val, len(coords_val))
                else:
                    box_val = None

            num_structures = coords_val.shape[0]
            n_elements_1 = coords_val.shape[1]
            n_elements_2 = tmp_coords_2_val.shape[1]
            contact_map = np.zeros(
                (num_structures, n_elements_1, n_elements_2), dtype=bool
            )

            # One parallel multi-structure neighbour search over the flattened
            # (structure, query-atom) space, then a vectorised fill of the map.
            from molsysmt._private.rust_backend import neighbor_list_csr_multi

            ref_val = None if is_self else tmp_coords_2_val
            offsets, indices, _ = neighbor_list_csr_multi(
                coords_val,
                ref_val,
                box=box_val,
                cutoff=threshold_val,
                exclude_self=is_self,
                sort_by_distance=False,
            )
            counts = np.diff(offsets)
            w_of_entry = np.repeat(np.arange(num_structures * n_elements_1), counts)
            s_of_entry = w_of_entry // n_elements_1
            iq_of_entry = w_of_entry % n_elements_1
            contact_map[s_of_entry, iq_of_entry, indices] = True

            if is_self:
                contact_map[:, np.arange(n_elements_1), np.arange(n_elements_1)] = True
        else:
            all_dists = get_distances(
                molecular_system=molecular_system,
                selection=atom_indices,
                center_of_atoms=center_of_atoms,
                weights=weights,
                structure_indices=structure_indices,
                selection_2=atom_indices_2,
                center_of_atoms_2=center_of_atoms_2,
                weights_2=weights_2,
                structure_indices_2=structure_indices_2,
                pairs=pairs,
                pbc=pbc,
                skip_digestion=True,
            )

            length_units = puw.get_unit(all_dists)
            threshold = puw.get_value(threshold, to_unit=length_units)
            all_dists = puw.get_value(all_dists)

            from molsysmt._private.execution import PersistentResultHandle

            contact_map = np.empty(all_dists.shape, dtype=bool)
            slab = None
            try:
                for structure in range(all_dists.shape[0]):
                    slab = all_dists[structure]
                    contact_map[structure] = slab <= threshold
            finally:
                slab = None
                if isinstance(all_dists, PersistentResultHandle):
                    all_dists.cleanup()

    output = None

    if output_type == "numpy.ndarray":
        output = contact_map

    elif output_type in ["pairs", "sorted pairs"]:
        output = []
        n_contact_maps = contact_map.shape[0]

        if pairs:
            if output_indices == "selection":
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii, :])[0]
                    output.append(aux_pairs.tolist())
            elif output_indices == "atom":
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii, :])[0]
                    output.append(
                        [
                            [int(atom_indices[index]), int(atom_indices_2[index])]
                            for index in aux_pairs
                        ]
                    )

        else:
            if coordinates_2 is None:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(np.triu(contact_map[ii], k=1))
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)
            else:
                for ii in range(n_contact_maps):
                    aux_pairs = np.nonzero(contact_map[ii])
                    aux_pairs = np.column_stack(aux_pairs).tolist()
                    output.append(aux_pairs)

            if output_indices == "atom":
                atom_indices = np.array(atom_indices)

                if atom_indices_2 is None:
                    for ii in range(n_contact_maps):
                        output[ii] = atom_indices[output[ii]].tolist()
                else:
                    atom_indices_2 = np.array(atom_indices_2)
                    for ii in range(n_contact_maps):
                        aux_pairs = np.asarray(output[ii], dtype=np.int64).reshape(
                            -1, 2
                        )
                        output[ii] = np.column_stack(
                            [
                                atom_indices[aux_pairs[:, 0]],
                                atom_indices_2[aux_pairs[:, 1]],
                            ]
                        ).tolist()

        if output_type == "sorted pairs":
            for ii in range(n_contact_maps):
                output[ii] = sorted(output[ii])

    return output
