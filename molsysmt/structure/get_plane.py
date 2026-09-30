"""Public boundary for general least-squares plane geometry."""

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.execution import ChunkedExecutor
from molsysmt._private.execution.memory_policy import decide_mode
from molsysmt._private.h5msm import modular_h5msm_dimensions
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.sparse_membership import pack_membership
from molsysmt._private.variables import is_all, is_iterable_of_iterables

from ._plane import PlaneReducer


@signal(tags=["api", "structure"])
@arg_digest()
def get_plane(molecular_system, selection="all", structure_indices="all", pbc=False,
              syntax="MolSysMT", heavy_mode="auto", skip_digestion=False):
    """
    Fitting unweighted least-squares planes to selected atom groups.

    Coordinates alone suffice; connectivity and aromaticity are not required.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format providing coordinates.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection for one plane, or nested selections for multiple planes.
        Each group must contain at least three distinct atoms. Repeated atoms
        are removed; group order is preserved and groups may overlap.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process. Requested order and
        repetitions are preserved. An explicit empty list returns typed empties.
    pbc : bool, default=False
        Whether to require a nonsingular box and complete participants in one
        periodic image. Split groups are rejected; coordinates are not unwrapped.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Policy controlling coordinate streaming through ChunkedExecutor.
        Forced streaming requires the source form's declared heavy support.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        `centers` and dimensionless `normals` have shape
        (n_selected_structures, n_groups, 3). `rms_deviation` and `max_deviation`
        have shape (n_selected_structures, n_groups) and measure orthogonal atom
        distances from the plane. Length quantities are standardized to the
        session's length unit. `atom_indices` and `atom_offsets` are packed int64
        source memberships; `structure_indices` are int64 source indices.
        `method` is 'unweighted_orthogonal_least_squares'.

    Raises
    ------
    ArgumentError
        If a group has fewer than three distinct atoms or indices are invalid.
    StructuralInconsistencyError
        If coordinates are nonfinite, a unique normal cannot be determined,
        or a requested periodic box is missing or singular.
    NotImplementedMethodError
        If a group requires internal periodic image reconstruction.
    MemoryBudgetExceededError
        If the dense result or estimated numerical work exceeds the RAM budget.
    UnsupportedHeavyOperationError
        If the source cannot supply the required streamed attributes.

    Notes
    -----
    The plane passes through the arithmetic centroid and minimizes the sum of
    squared orthogonal distances. The normal is the last right singular vector
    of centered, scaled coordinates. A smallest/middle singular-value gap no
    greater than 1e-12 times the largest singular value rejects collinear and
    degenerate geometries. Equal in-plane singular values are permitted.

    The largest absolute normal component is positive (first component wins an
    exact tie). This gives a deterministic representation, not temporal sign
    continuity. Compare unoriented planes using the absolute normal dot product.
    A fitted plane or small deviation does not establish aromaticity.

    Periodic box singularity is checked after dividing each box by its largest
    absolute component: normalized determinant magnitude must exceed 1e-12.
    This check is invariant to uniform coordinate/box scaling.

    Numeric H5MSM 0.5 selections read metadata and projected structural blocks,
    without loading topology or saved analyses. Rich selections may materialize
    the input through the ordinary selection route. Output remains in RAM;
    numerical working estimates are not a process-RSS guarantee. Inputs are never
    modified. This experimental tool does not return an Interactions analysis.

    See Also
    --------
    molsysmt.structure.get_center
        Computing centroids or weighted centers.
    molsysmt.structure.get_principal_axes
        Computing inertia or geometric principal axes.
    molsysmt.physchem.get_aromatic_rings
        Obtaining declared aromatic ring memberships.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.structure.get_plane import get_plane
    >>> plane = get_plane(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'], selection=[0, 1, 2])
    >>> plane['normals'].shape
    (1, 1, 3)
    >>> plane['atom_offsets'].tolist()
    [0, 3]

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Get_plane` for planarity, groups, units and PBC examples.

    .. versionadded:: 1.0.0
    """
    from molsysmt import configure
    from molsysmt.basic import get, get_form, select
    from molsysmt.form import _dict_modules

    caller = "molsysmt.structure.get_plane"
    dimensions = modular_h5msm_dimensions(molecular_system)
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    n_atoms, n_structures = map(int, dimensions)
    frames = np.arange(n_structures, dtype=np.int64) if is_all(structure_indices) else np.asarray(structure_indices)
    if frames.ndim != 1 or frames.dtype.kind not in "iu" or np.any((frames < 0) | (frames >= n_structures)):
        raise ArgumentError("structure_indices", caller=caller, message="Use valid source structure indices.")
    frames = frames.astype(np.int64, copy=False)
    multiple = is_iterable_of_iterables(selection) or (
        isinstance(selection, (list, tuple)) and len(selection) > 0
        and all(isinstance(group, str) for group in selection)
    )
    selections = selection if multiple else [selection]
    if len(selections) == 0:
        raise ArgumentError("selection", caller=caller, message="At least one plane group is required.")
    groups = []
    for group in selections:
        if dimensions is not None and is_all(group):
            atoms = np.arange(n_atoms, dtype=np.int64)
        elif not isinstance(group, str) and group is not None:
            atoms = np.asarray(group)
        else:
            atoms = np.asarray(select(molecular_system, selection=group,
                                      structure_indices=structure_indices, syntax=syntax, skip_digestion=True))
        if atoms.ndim != 1 or atoms.dtype.kind not in "iu" or np.any((atoms < 0) | (atoms >= n_atoms)):
            raise ArgumentError("selection", caller=caller, message="Plane groups require valid atom indices.")
        atoms = np.unique(atoms).astype(np.int64, copy=False)
        if len(atoms) < 3:
            raise ArgumentError("selection", caller=caller, message="Each plane requires at least three distinct atoms.")
        groups.append(atoms)
    atoms, offsets = pack_membership(groups)
    universe = np.unique(atoms)
    positions = np.searchsorted(universe, atoms)
    # Reserve a second output-sized buffer for quantity standardization and
    # group-wise SVD workspace. This bounds numeric buffers, not total RSS.
    fixed = atoms.nbytes + offsets.nbytes + frames.nbytes + universe.nbytes + positions.nbytes
    output_work = fixed + 2 * 64 * len(frames) * len(groups)
    per_frame = 24 * len(universe) + 192 * max(map(len, groups)) + 256 * len(groups) + 72
    available = int(configure.max_ram_usage) - output_work
    if available < per_frame and len(frames):
        raise MemoryBudgetExceededError(reason="Plane output and one coordinate work block exceed the numerical budget.",
                                        predicted_bytes=output_work + per_frame,
                                        available_bytes=int(configure.max_ram_usage), caller=caller)
    if output_work > configure.max_ram_usage:
        raise MemoryBudgetExceededError(reason="Plane output exceeds the numerical budget.",
                                        predicted_bytes=output_work, available_bytes=int(configure.max_ram_usage), caller=caller)
    mode = decide_mode(output_work + per_frame * len(frames), heavy_mode)
    if mode == "eager" and per_frame * len(frames) > available:
        raise MemoryBudgetExceededError(reason="Eager plane work exceeds the numerical budget; use coordinate streaming.",
                                        predicted_bytes=output_work + per_frame * len(frames),
                                        available_bytes=int(configure.max_ram_usage), caller=caller)
    form = get_form(molecular_system)
    reducer = PlaneReducer(offsets, positions, len(universe), pbc, caller)
    attributes = ["coordinates", "box"] if pbc else ["coordinates"]
    if isinstance(form, str) and getattr(_dict_modules[form], "_heavy_support", {}).get("coordinates", False):
        outputs = ChunkedExecutor(
            molecular_system, form, "get_plane", reducer=reducer, atom_indices=universe,
            structure_indices=frames, attributes=attributes,
            heavy_mode="force" if mode == "heavy" else "off",
            max_chunk_size=max(1, available // per_frame),
        ).execute()
    else:
        if mode == "heavy":
            raise UnsupportedHeavyOperationError(operation="get_plane", form=str(form),
                                                 reason="No streamed structural delivery route.")
        reducer.initialize({"n_structures": len(frames)})
        if len(frames):
            coordinates = get(molecular_system, selection=universe, structure_indices=frames,
                              coordinates=True, skip_digestion=True)
            box = get(molecular_system, structure_indices=frames, box=True, skip_digestion=True) if pbc else None
            reducer.consume(ChunkedExecutor._build_chunk({
                "coordinates": coordinates, "box": box, "structure_indices": frames,
            }))
        outputs = reducer.finalize()
    centers, normals, rms, maximum = outputs
    return {
        "centers": puw.standardize(puw.quantity(centers, "nm")), "normals": normals,
        "rms_deviation": puw.standardize(puw.quantity(rms, "nm")),
        "max_deviation": puw.standardize(puw.quantity(maximum, "nm")),
        "atom_indices": atoms, "atom_offsets": offsets, "structure_indices": frames.copy(),
        "method": "unweighted_orthogonal_least_squares",
    }
