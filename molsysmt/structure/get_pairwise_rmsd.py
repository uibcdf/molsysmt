"""Computing bounded pose dissimilarities in declared common Cartesian axes."""

from copy import deepcopy

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.configure import with_configure_overrides


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
@dep_digest("rdkit", when={"method": "symmetry_corrected"})
def get_pairwise_rmsd(
    molecular_system,
    selection='atom_type!="H"',
    structure_indices="all",
    method="positional",
    chemical_state="reference",
    correspondences=None,
    max_matches=100000,
    tie_tolerance="1e-12 nm",
    member_keys=None,
    max_work=100000000,
    syntax="MolSysMT",
    heavy_mode="auto",
    parallel=None,
    num_threads=None,
    skip_digestion=False,
):
    """Computing a bounded pairwise positional RMSD matrix without fitting.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates on one declared common atom axis.
        The caller declares compatible Cartesian axes and periodic images.
    selection : str, list, tuple or numpy.ndarray, default='atom_type!="H"'
        Nonempty unique atom population. Numeric results use sorted source indices.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Ordered source structure indices; repetitions remain distinct members.
    method : {'positional', 'symmetry_corrected'}, default='positional'
        Declared atom ordering, or minimum over chemical permutations of one state.
    chemical_state : str or int, default='reference'
        Fixed chemical state for symmetry comparison; ignored for positional RMSD.
    correspondences : dict or None, default=None
        Validated get_atom_correspondences result mapping this population to itself.
        Symmetry maps must include identity and be closed under inversion. None
        constructs all chemical maps. Positional comparison requires None.
    max_matches : int, default=100000
        Enumeration bound when constructing chemical maps.
    tie_tolerance : quantity or str, default='1e-12 nm'
        Absolute nonnegative length tolerance for near-optimal map counts.
    member_keys : list or tuple of str or None, default=None
        Unique opaque member labels, in requested order. None uses member positions.
    max_work : int, default=100000000
        Maximum unordered-pair count times selected atoms times admitted maps.
    syntax : str, default='MolSysMT'
        Selection syntax.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Coordinate delivery policy. Selected coordinates and output remain resident.
    parallel : bool or None, default=None
        Whether to override the configured Rust CPU parallelization policy.
    num_threads : int or None, default=None
        Rust worker count, or None for the configured session value.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached rmsd length quantity of shape (n_members, n_members), original
        atom_indices/structure_indices, member_keys, shared chemical evidence and
        execution/producer metadata. pair_indices has shape (n_pairs, 2): each row
        is (query member, reference member), query > reference, reference first
        in ascending order. Mapping winners and near-tie counts refer only to
        that orientation. Positional winners are -1 and counts are one.

    Raises
    ------
    ArgumentError
        If populations, member keys or correspondence symmetry are invalid.
    StructuralInconsistencyError
        If coordinates or declared chemistry cannot support the comparison.
    MemoryBudgetExceededError
        If estimated numeric resident storage exceeds its configured budget.
    UnsupportedHeavyOperationError
        If work/enumeration bounds or coordinate delivery are unsupported.

    Notes
    -----
    Experimental API. No alignment, reflection, centering or periodic imaging is
    performed. Positional comparison does not validate chemical equivalence.
    Independent saved systems require explicit mapping and preparation before
    composition; equal counts or IDs do not prove correspondence or common axes.
    Symmetry reuses the declared-graph profile of get_symmetry_corrected_rmsd,
    including its complete chemical context and fixed indexed-H representation.
    Restricted inverse-closed maps define a symmetric dissimilarity, not necessarily
    a metric. No missing comparison is repaired or silently symmetrized.

    Dense output is quadratic in members. Selected coordinates are also resident;
    only input delivery and per-reference map evaluation are chunked. Numeric
    estimates exclude source objects, Python chemistry and total process RSS.
    Empty requests do not evaluate coordinates or chemistry. Singleton coordinates
    are still validated before returning zero. Attribution records actual methods
    and software once per completed operation, not once per pair.

    See Also
    --------
    get_distance_clusters
        Cluster a unit-bearing distance matrix with an explicit physical cutoff.
    get_symmetry_corrected_rmsd
        Compare a population against one reference with chemical correspondences.
    molsysmt.basic.concatenate_structures
        Compose already prepared compatible coordinate populations.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.native import Structures
    >>> molsys = Structures()
    >>> molsys.coordinates = msm.pyunitwizard.quantity([[[0., 0., 0.]],
    ...                                                [[1., 0., 0.]]], 'nm')
    >>> result = msm.structure.get_pairwise_rmsd(molsys, selection='all')
    >>> msm.pyunitwizard.get_value(result['rmsd'], to_unit='nm').tolist()
    [[0.0, 1.0], [1.0, 0.0]]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_pairwise_rmsd`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__, configure
    from molsysmt._private import rust_backend as kernels
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.scientific_attribution import attach_scientific_attribution
    from molsysmt._private.variables import is_all
    from molsysmt.basic import get, select

    from ._pairwise_geometry import (
        CoordinatePopulation,
        check_budget,
        member_labels,
        symmetric_maps,
    )
    from ._symmetry_rmsd import SymmetryRMSDReducer

    caller = "molsysmt.structure.get_pairwise_rmsd"
    dimensions = modular_h5msm_dimensions(molecular_system)
    total = int(
        dimensions[1]
        if dimensions is not None
        else get(molecular_system, n_structures=True)
    )
    total_atoms = int(
        dimensions[0] if dimensions is not None else get(molecular_system, n_atoms=True)
    )
    all_structures = structure_indices is None or is_all(structure_indices)
    count = total if all_structures else len(structure_indices)
    pairs = count * (count - 1) // 2
    # Reject quadratic output before materializing an unrestricted structure axis.
    base_bytes = 24 * count * count + 40 * pairs + 64 * count
    check_budget(base_bytes, pairs, max_work, caller)
    frames = (
        np.arange(total, dtype=np.int64)
        if all_structures
        else np.asarray(structure_indices, dtype=np.int64)
    )
    if frames.ndim != 1 or np.any((frames < 0) | (frames >= total)):
        raise ArgumentError("structure_indices", caller=caller)
    keys = member_labels(member_keys, count, caller)
    atoms = np.asarray(
        select(molecular_system, selection=selection, syntax=syntax), dtype=np.int64
    )
    if (
        atoms.ndim != 1
        or len(np.unique(atoms)) != len(atoms)
        or (count and not len(atoms))
        or np.any((atoms < 0) | (atoms >= total_atoms))
    ):
        raise ArgumentError("selection", caller=caller)
    atoms = np.sort(atoms)
    n_atoms = len(atoms)
    if method == "positional" and correspondences is not None:
        raise ArgumentError("correspondences", caller=caller)
    numeric_bytes = base_bytes + 48 * count * n_atoms + 128 * n_atoms
    check_budget(numeric_bytes, pairs * n_atoms, max_work, caller)
    maps, evidence = None, None
    software = dict(molsysmt=__version__)
    scope = "declared_atom_order" if method == "positional" else "not_evaluated"
    if method == "symmetry_corrected" and count:
        from rdkit import rdBase

        from molsysmt.chemical_states import get_atom_correspondences
        from molsysmt.chemical_states._atom_correspondences import (
            ChemicalGraph,
            validate_correspondence_result,
        )

        if correspondences is None:
            evidence = get_atom_correspondences(
                molecular_system,
                selection=atoms,
                structure_indices=frames,
                reference_molecular_system=molecular_system,
                reference_selection=atoms,
                reference_structure_indices=frames,
                chemical_state=chemical_state,
                reference_chemical_state=chemical_state,
                max_matches=max_matches,
                syntax=syntax,
            )
        else:
            graph = ChemicalGraph(
                molecular_system, atoms, frames, chemical_state, syntax, caller
            )
            validate_correspondence_result(
                correspondences, graph, graph, "declared_graph_isomorphism", caller
            )
            evidence = correspondences
        table = np.asarray(evidence["atom_correspondences"], dtype=np.int64)
        if not len(table):
            raise StructuralInconsistencyError(
                reason="No admitted chemical correspondence.", caller=caller
            )
        numeric_bytes += 8 * table.size + 64 * len(table) * n_atoms
        numeric_bytes += 2 * sum(
            np.asarray(evidence[name]).nbytes
            for name in (
                "context_atom_correspondences",
                "fixed_atom_correspondence",
                "candidate_atom_correspondences",
            )
            if evidence.get(name) is not None
        )
        check_budget(numeric_bytes, pairs * n_atoms * len(table), max_work, caller)
        maps = symmetric_maps(table, atoms, caller)
        software["rdkit"] = rdBase.rdkitVersion
        scope = evidence.get("search_scope", "all_chemical_correspondences")
    n_maps = 1 if maps is None else len(maps)
    block_size = min(
        configure.chunk_size,
        configure.max_ram_usage // 4 // (4096 + 96 * n_atoms + 32 * n_maps),
    )
    if count > 1 and block_size < 1:
        from molsysmt._private.smonitor import UnsupportedHeavyOperationError

        raise UnsupportedHeavyOperationError(
            operation=caller,
            form="RMSD maps",
            reason="One numeric comparison block exceeds the configured budget.",
        )
    population = CoordinatePopulation(count, n_atoms, caller)
    if count:
        execute_projected_geometry(
            molecular_system,
            universe=atoms,
            frames=frames,
            reducer=population,
            per_frame_bytes=4096 + 96 * n_atoms,
            pbc=False,
            heavy_mode=heavy_mode,
            caller=caller,
        )
    else:
        population.initialize({})
        population.finalize()
        population.metadata["execution"]["execution"] = "empty"
    check_budget(numeric_bytes, pairs * n_atoms * n_maps, max_work, caller)
    matrix = np.zeros((count, count), dtype=np.float64)
    pair_indices = np.empty((pairs, 2), dtype=np.int64)
    winners = np.full(pairs, -1, dtype=np.int64)
    ties = np.ones(pairs, dtype=np.int64)
    offset, blocks = 0, 0
    tolerance = float(puw.get_value(tie_tolerance, to_unit="nm"))
    coordinates = population.coordinates
    for reference in range(count - 1):
        for start in range(reference + 1, count, block_size):
            end = min(count, start + block_size)
            size = end - start
            if maps is None:
                values = kernels.get_rmsd_with_single_reference_structure(
                    coordinates[start:end], coordinates[reference]
                )
            else:
                reducer = SymmetryRMSDReducer(
                    frames[start:end],
                    coordinates[reference],
                    maps,
                    None,
                    tolerance,
                    caller,
                )
                reducer.initialize({})
                reducer.consume({"coordinates": coordinates[start:end]})
                reducer.finalize()
                values = reducer.rmsd
                winners[offset : offset + size] = reducer.winners
                ties[offset : offset + size] = reducer.tie_counts
            if not np.isfinite(values).all():
                raise StructuralInconsistencyError(
                    reason="Pairwise RMSD arithmetic is not finite.", caller=caller
                )
            matrix[start:end, reference] = values
            matrix[reference, start:end] = values
            pair_indices[offset : offset + size, 0] = np.arange(start, end)
            pair_indices[offset : offset + size, 1] = reference
            offset, blocks = offset + size, blocks + 1
    result = dict(
        schema="molsysmt.pairwise_rmsd@1",
        rmsd=puw.standardize(puw.quantity(matrix, "nm")),
        member_indices=np.arange(count, dtype=np.int64),
        member_keys=keys,
        structure_indices=frames.copy(),
        atom_indices=atoms.copy(),
        index_space="source_positions",
        source_n_structures=total,
        source_n_atoms=total_atoms,
        pair_indices=pair_indices,
        correspondence_indices=winners,
        n_near_optimal_correspondences=ties,
        correspondences=deepcopy(evidence),
        method=method,
        search_scope=scope,
        chemistry_checked=evidence is not None,
        chemical_state=chemical_state if evidence is not None else None,
        correspondence_profile="declared_graph_isomorphism"
        if evidence is not None
        else None,
        alignment="none",
        periodic_imaging="none",
        cartesian_axes="caller_declared_common",
        tie_tolerance=puw.standardize(puw.quantity(tolerance, "nm")),
        execution=dict(
            population.metadata["execution"],
            pair_blocks=blocks,
            estimated_numeric_bytes=numeric_bytes,
            estimated_work=pairs * n_atoms * n_maps,
            max_work=max_work,
        ),
        software=software,
    )
    if evidence is not None:
        from molsysmt._private.scientific_attribution import attach_graph_attribution

        attach_graph_attribution(result, caller)
    else:
        attach_scientific_attribution(result, caller)
    return result
