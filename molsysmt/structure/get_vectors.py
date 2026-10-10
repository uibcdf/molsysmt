"""Public directed geometry between atoms or centers of selections."""

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.execution import ChunkedExecutor
from molsysmt._private.execution.memory_policy import decide_mode
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    NotImplementedMethodError,
    UnsupportedHeavyOperationError,
)
from molsysmt.configure import with_configure_overrides

from ._vectors import CALLER, Endpoint, VectorsReducer


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def get_vectors(
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
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """Computing directed vectors between atoms or centers of selections.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates and the requested attributes.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        First endpoint atoms. Nested selections define separate centers. With
        pairs=True and no selection_2 or center flag, a two-column array defines
        ordered pairs; [a, b] defines one pair. Set a center flag or selection_2
        explicitly to disambiguate paired nested centers.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        First source structure indices. Order and repetitions are preserved.
    center_of_atoms : bool, default=False
        Whether to use one center for a flat selection; nested selections each
        produce a center regardless of this flag.
    weights : list, tuple, numpy.ndarray, str, or quantity, default=None
        First center weights; None gives geometric centers and 'masses' gives
        centers of mass. Nested weights follow nested atom memberships.
    molecular_system_2 : molecular system or None, default=None
        Second source; None uses the first molecular system. Sources must share
        a Cartesian reference for their vectors to have the intended meaning.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Second endpoint atoms; None uses the first selection. For implicit
        second endpoints, center_of_atoms and weights are inherited as well.
    structure_indices_2 : int, list, tuple, numpy.ndarray, or None, default=None
        Second source structure indices; None uses the first requested indices.
        Both lists must have equal length and are paired by position.
    center_of_atoms_2 : bool, default=False
        Whether an explicitly selected second endpoint is a center.
    weights_2 : list, tuple, numpy.ndarray, str, or quantity, default=None
        Second center weights, with the same semantics as weights.
    pairs : bool, default=False
        Whether corresponding endpoints are paired. Otherwise compute their
        Cartesian product, independently for each aligned structure pair.
    pbc : bool, default=True
        Whether to use MIC when the first source has periodic boxes. The first
        structure's box is the reference even when the second box differs.
        Center memberships must occupy one anchor-relative MIC image in that
        reference box; split memberships raise rather than being reconstructed.
    output_type : {'numpy.ndarray', 'dictionary'}, default='numpy.ndarray'
        Return a length quantity, or a flat dictionary also containing distances,
        dimensionless directions, int32 image vectors and source memberships.
    output_indices : {'selection', 'atom', 'group'} or None, default=None
        For array output, prepend endpoint positions ('selection') or source
        atom memberships ('atom'). Generic group labels are not implemented.
        Dictionary output always contains source atom memberships.
    output_structure_indices : {'selection', 'structure'} or None, default=None
        For array output, prepend local positions or both source structure axes.
        Dictionary output always includes both source structure axes.
    engine : str, default='MolSysMT'
        Calculation backend. Only the bundled MolSysMT Rust backend is supported.
    syntax : str, default='MolSysMT'
        Selection syntax for both molecular systems.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Coordinate streaming policy. Forced streaming requires both sources'
        declared coordinate delivery support. Resident output must fit the budget.
    parallel : bool or None, default=None
        Whether to use the session's CPU parallel execution policy.
    num_threads : int or None, default=None
        CPU worker count, or None to use the configured default.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity, tuple, or dict
        Vectors point from the first endpoint to the second and have shape
        (n_structure_pairs, n_first, n_second, 3), or
        (n_structure_pairs, n_pairs, 3) with pairs=True. Length quantities follow
        the session's standard length unit. Optional array index outputs precede
        vectors in a tuple. Dictionary keys are vectors, distances, directions,
        image_vectors, atom_indices, atom_offsets, atom_indices_2, atom_offsets_2,
        structure_indices, structure_indices_2, pairs, pbc, method, parameters
        and software. Parameters retain center flags and relative numeric weights;
        their absolute scale cancels within each center.
        Zero vectors have zero distance and NaN directions. Empty axes retain
        defined shapes and types. Images shift the second endpoint only.

    Raises
    ------
    ArgumentError
        If indices, endpoint counts, structure alignment or weights are invalid.
    StructuralInconsistencyError
        If coordinates are nonfinite, requested boxes are absent or singular,
        or native geometry cannot be represented.
    NotImplementedMethodError
        If engine/group output is unsupported or periodic centers are split.
    MemoryBudgetExceededError
        If resident output or required numerical work exceeds the RAM budget.
    UnsupportedHeavyOperationError
        If forced streaming has no declared delivery route.

    Notes
    -----
    For row-vector boxes, v = r_second + image_vectors @ box_first - r_first.
    The shared Rust minimum-image primitive defines tie behavior. A tied minimum
    is deterministic but reversal need not select its opposite image. This is
    endpoint geometry, not an unwrapped travel-distance reconstruction.

    Rust releases the GIL, computes independent structures in the configured
    Rayon pool and derives dictionary distances/directions in the same pass.
    Explicit pairs never materialize a Cartesian-product matrix. Input delivery
    is chunked; the complete output remains resident. Numerical memory estimates
    include block output and unit-conversion buffers, not all process RSS.
    Inputs and stored interactions are never modified. This experimental tool
    supplies geometry, not chemical site recognition or lone-pair assignments.

    See Also
    --------
    molsysmt.structure.get_distances
        Computing the corresponding scalar distances.
    molsysmt.structure.get_center
        Computing geometric or weighted centers.
    molsysmt.physchem.get_hbond_sites
        Recognizing fixed-state donor-H pairs and acceptor candidates.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> msm.structure.get_vectors(molsys, selection=[[0, 1]], pairs=True, pbc=False).shape
    (1, 1, 3)

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_vectors` for centers, structure pairs and PBC.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__, configure
    from molsysmt.basic import get
    from molsysmt.pbc import has_pbc

    if engine != "MolSysMT" or output_indices == "group":
        raise NotImplementedMethodError(caller=CALLER)
    if pairs and selection_2 is None and not (center_of_atoms or center_of_atoms_2):
        if isinstance(selection, (list, tuple, np.ndarray)) and len(selection):
            try:
                pair_array = np.asarray(selection)
            except ValueError as error:
                raise ArgumentError(
                    "selection",
                    caller=CALLER,
                    message="Specify selection_2 explicitly for paired nested centers.",
                ) from error
            if (
                pair_array.ndim == 2
                and pair_array.shape[1] == 2
                and pair_array.dtype.kind in "iu"
            ):
                selection, selection_2 = pair_array[:, 0], pair_array[:, 1]
            elif len(selection) == 2 and all(
                isinstance(item, str) for item in selection
            ):
                selection, selection_2 = selection
            elif (
                pair_array.ndim == 1
                and pair_array.size == 2
                and pair_array.dtype.kind in "iu"
            ):
                selection, selection_2 = pair_array[:1], pair_array[1:]
    implicit = selection_2 is None
    second_source = (
        molecular_system if molecular_system_2 is None else molecular_system_2
    )
    first = Endpoint(
        molecular_system, selection, structure_indices, center_of_atoms, weights, syntax
    )
    second = Endpoint(
        second_source,
        selection if implicit else selection_2,
        structure_indices if structure_indices_2 is None else structure_indices_2,
        (center_of_atoms or center_of_atoms_2) if implicit else center_of_atoms_2,
        weights if implicit and weights_2 is None else weights_2,
        syntax,
    )
    if len(first.frames) != len(second.frames):
        raise ArgumentError(
            "structure_indices_2",
            caller=CALLER,
            message="Structure lists must have equal length.",
        )
    if pairs and first.count != second.count:
        raise ArgumentError(
            "selection_2", caller=CALLER, message="Paired endpoint counts must match."
        )
    periodic = bool(len(first.frames) and pbc and has_pbc(molecular_system))
    shared = first.source is second.source and np.array_equal(
        first.frames, second.frames
    )
    universe = (
        np.union1d(first.universe, second.universe)
        if shared and not np.array_equal(first.universe, second.universe)
        else first.universe
    )
    details = output_type == "dictionary"
    ns = len(first.frames)
    nv = first.count if pairs else first.count * second.count
    # Final output + length presentation copies + packed metadata. Block work
    # includes projected sources, packed centers and simultaneous Rust outputs.
    output_bytes = ns * nv * (100 if details else 48)
    fixed = (
        sum(
            array.nbytes
            for endpoint in (first, second)
            for array in (
                endpoint.frames,
                endpoint.atoms,
                endpoint.offsets,
                endpoint.universe,
                endpoint.positions,
            )
        )
        + universe.nbytes
        + sum(
            endpoint.weights.nbytes if endpoint.weights is not None else 0
            for endpoint in (first, second)
        )
    )
    if details:
        fixed *= 2  # Detached source memberships and parameter arrays.
    per_structure = (
        96
        * (len(universe) + len(second.universe) + len(first.atoms) + len(second.atoms))
        + nv * (68 if details else 24)
        + 4096
    )
    budget = int(configure.max_ram_usage)
    available = budget - output_bytes - fixed
    mode = decide_mode(output_bytes + fixed + ns * per_structure, heavy_mode)
    if available < (per_structure if ns else 0):
        raise MemoryBudgetExceededError(
            reason="Vector output and one work block exceed the numerical budget.",
            predicted_bytes=output_bytes + fixed + (per_structure if ns else 0),
            available_bytes=budget,
            caller=CALLER,
        )
    heavy = mode == "heavy"
    if not heavy and ns * per_structure > available:
        raise MemoryBudgetExceededError(
            reason="Eager vector work exceeds the numerical budget; use streaming.",
            predicted_bytes=output_bytes + fixed + ns * per_structure,
            available_bytes=budget,
            caller=CALLER,
        )
    if heavy and not (first.streaming and second.streaming):
        raise UnsupportedHeavyOperationError(
            operation="get_vectors",
            form=str((first.form, second.form)),
            reason="Both endpoints require streamed coordinates.",
        )
    reducer = VectorsReducer(first, second, universe, pairs, periodic, details, heavy)
    attributes = ["coordinates", "box"] if periodic else ["coordinates"]
    if first.streaming:
        values = ChunkedExecutor(
            molecular_system,
            first.form,
            "get_vectors",
            reducer=reducer,
            atom_indices="all" if len(universe) == first.n_atoms else universe,
            structure_indices=first.frames,
            attributes=attributes,
            heavy_mode="force" if heavy else "off",
            max_chunk_size=max(1, available // per_structure),
        ).execute()
    else:
        reducer.initialize({})
        if ns:
            coordinates = get(
                molecular_system,
                selection=universe,
                structure_indices=first.frames,
                coordinates=True,
            )
            box = (
                get(molecular_system, structure_indices=first.frames, box=True)
                if periodic
                else None
            )
            reducer.consume(
                ChunkedExecutor._build_chunk(
                    {
                        "coordinates": coordinates,
                        "box": box,
                        "structure_indices": first.frames,
                    }
                )
            )
        values = reducer.finalize()
    vectors, distances, directions, images = values
    vectors = puw.standardize(puw.quantity(vectors, "nm"))
    if details:
        return dict(
            vectors=vectors,
            distances=puw.standardize(puw.quantity(distances, "nm")),
            directions=directions,
            image_vectors=images,
            atom_indices=first.atoms.copy(),
            atom_offsets=first.offsets.copy(),
            atom_indices_2=second.atoms.copy(),
            atom_offsets_2=second.offsets.copy(),
            structure_indices=first.frames.copy(),
            structure_indices_2=second.frames.copy(),
            pairs=pairs,
            pbc=periodic,
            method="directed_minimum_image" if periodic else "directed_cartesian",
            parameters={
                "center_of_atoms": first.center,
                "center_of_atoms_2": second.center,
                "relative_weights": None
                if first.weights is None
                else first.weights.copy(),
                "relative_weights_2": None
                if second.weights is None
                else second.weights.copy(),
                "periodic_reference": "first_structure" if periodic else None,
                "sense": "first_to_second",
            },
            software={"molsysmt": __version__},
        )
    outputs = []
    if output_indices is not None:
        outputs.extend(
            (np.arange(first.count), np.arange(second.count))
            if output_indices == "selection"
            else (
                [
                    first.atoms[a:b].copy()
                    for a, b in zip(first.offsets[:-1], first.offsets[1:])
                ]
                if first.center
                else first.atoms.copy(),
                [
                    second.atoms[a:b].copy()
                    for a, b in zip(second.offsets[:-1], second.offsets[1:])
                ]
                if second.center
                else second.atoms.copy(),
            )
        )
    if output_structure_indices is not None:
        outputs.extend(
            (first.frames.copy(), second.frames.copy())
            if output_structure_indices == "structure"
            else (np.arange(ns), np.arange(ns))
        )
    outputs.append(vectors)
    return tuple(outputs) if len(outputs) > 1 else vectors
