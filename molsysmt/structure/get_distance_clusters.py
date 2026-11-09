"""Clustering a bounded unit-bearing dissimilarity matrix."""

import hashlib

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@signal(tags=["api", "structure"])
@arg_digest()
def get_distance_clusters(
    distances,
    cutoff_distance,
    method="complete_linkage",
    representative="medoid",
    member_keys=None,
    max_work=100000000,
    skip_digestion=False,
):
    """Clustering physical dissimilarities with an explicit inclusive cutoff.

    Parameters
    ----------
    distances : quantity
        Finite nonnegative square length matrix, exactly symmetric with zero
        diagonal. Row/column positions define the ordered member population.
    cutoff_distance : quantity or str
        Finite nonnegative scalar length; merge when linkage distance <= cutoff.
    method : {'complete_linkage', 'single_linkage'}, default='complete_linkage'
        Maximum or minimum distance between members of two clusters.
    representative : {'medoid', 'first'}, default='medoid'
        Member minimizing the within-cluster distance sum, or earliest member.
        Exact medoid ties choose the earliest input member. No scores are used.
    member_keys : list or tuple of str or None, default=None
        Unique opaque member labels in matrix order. None uses position labels.
    max_work : int, default=100000000
        Maximum conservative scan estimate n_members**2 * (n_members - 1).
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached cluster_indices per input member, cluster_offsets and flattened
        member_indices, representative_indices, member_keys, cluster_diameters
        length quantity, cutoff, method, deterministic rules and producer
        references. Clusters and their members are ordered by original positions.
        matrix_sha256 identifies canonical nm float64 numeric values and shape,
        not chemical identity, correspondence or authenticity.

    Raises
    ------
    ArgumentError
        If units, cutoff, shape, member keys or named rules are invalid.
    StructuralInconsistencyError
        If distances are negative, nonfinite, asymmetric or nonzero on diagonal.
    MemoryBudgetExceededError
        If numeric matrix/output estimates exceed the configured working budget.
    UnsupportedHeavyOperationError
        If the conservative scan estimate exceeds max_work.

    Notes
    -----
    Experimental API. This is a bounded NumPy implementation of the primitive
    agglomerative procedure and min/max updates described in Müllner (2011),
    sections 2.1 and 2.4, figures 1–2, https://arxiv.org/abs/1109.2378.
    It does not implement the optimized algorithms proposed there or call SciPy.
    Global-minimum ties choose the lexicographically earliest pair of smallest
    original cluster members. Tied partitions may change on input reordering.
    Complete linkage bounds each resulting diameter by the inclusive cutoff.
    Single linkage may chain distant members; reported diameters expose this.
    No metric/triangle inequality is required; no missing distance is repaired.

    Matrix and cutoff are converted directly to float64 nm for comparison.
    The caller's output-unit policy affects returned quantities, not membership.
    Comparison is inclusive on the represented canonical values, without a
    hidden tolerance. Earlier caller conversions or geometric arithmetic may
    already have changed those floating-point values.

    The primitive algorithm uses quadratic numeric storage and cubic worst-case
    scans. Numeric RAM estimates exclude caller storage, Python objects and
    total process RSS. Empty input gives offsets [0]; duplicate members may merge
    at zero cutoff. A cluster is geometric grouping, not probability, free energy,
    independent sampling, affinity or biological validation.

    See Also
    --------
    get_pairwise_rmsd
        Construct dissimilarities without fitting or periodic reconstruction.

    Examples
    --------
    >>> import molsysmt as msm
    >>> distances = msm.pyunitwizard.quantity([[0., 1., 2.],
    ...                                       [1., 0., 1.],
    ...                                       [2., 1., 0.]], 'nm')
    >>> result = msm.structure.get_distance_clusters(distances, '1 nm')
    >>> result['cluster_indices'].tolist()
    [0, 0, 1]
    >>> msm.structure.get_distance_clusters(distances, '1 nm',
    ...     method='single_linkage')['cluster_indices'].tolist()
    [0, 0, 0]
    >>> with msm.pyunitwizard.context(standard_units=['pm', 'fs']):
    ...     clusters = msm.structure.get_distance_clusters(distances, '1 nm')
    >>> clusters['cluster_indices'].tolist()
    [0, 0, 1]

    .. admonition:: User guide

       See :ref:`Tutorial_Get_distance_clusters`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__
    from molsysmt._private.scientific_attribution import attach_scientific_attribution

    from ._pairwise_geometry import (
        check_budget,
        member_labels,
    )

    caller = "molsysmt.structure.get_distance_clusters"
    raw = np.asarray(puw.get_value(distances))
    if raw.ndim != 2 or raw.shape[0] != raw.shape[1] or raw.dtype.kind not in "fiu":
        raise ArgumentError("distances", caller=caller)
    count = len(raw)
    work = count * count * max(0, count - 1)
    numeric_bytes = 40 * count * count + 128 * count
    check_budget(numeric_bytes, work, max_work, caller)
    keys = member_labels(member_keys, count, caller)
    values = np.array(
        puw.get_value(distances, to_unit="nm"), dtype=np.float64, copy=True, order="C"
    )
    cutoff = np.asarray(puw.get_value(cutoff_distance, to_unit="nm"))
    if cutoff.ndim or not np.isfinite(cutoff) or cutoff < 0:
        raise ArgumentError("cutoff_distance", caller=caller)
    cutoff = float(cutoff)
    if (
        not np.isfinite(values).all()
        or np.any(values < 0)
        or np.any(np.diag(values) != 0)
        or not np.array_equal(values, values.T)
    ):
        raise StructuralInconsistencyError(
            reason="Distances must be finite, nonnegative, exactly symmetric and zero on diagonal.",
            caller=caller,
        )
    digest = hashlib.sha256()
    digest.update(np.asarray(values.shape, dtype="<i8").tobytes())
    for row in values:
        digest.update(np.asarray(row, dtype="<f8").tobytes())
    working = values.copy()
    np.fill_diagonal(working, np.inf)
    clusters = {index: [index] for index in range(count)}
    update = np.maximum if method == "complete_linkage" else np.minimum
    merges = 0
    while len(clusters) > 1:
        first, second = np.unravel_index(np.argmin(working), working.shape)
        if working[first, second] > cutoff:
            break
        # Symmetry and row-major argmin ensure first < second. Retaining first
        # makes cluster labels equal their smallest original member position.
        working[first] = update(working[first], working[second])
        working[:, first] = working[first]
        working[second, :] = np.inf
        working[:, second] = np.inf
        working[first, first] = np.inf
        clusters[first] = sorted(clusters[first] + clusters.pop(second))
        merges += 1
    cluster_indices = np.empty(count, dtype=np.int64)
    offsets = [0]
    members, representatives, diameters = [], [], []
    for cluster_index, population in enumerate(clusters.values()):
        cluster_indices[population] = cluster_index
        local = values[np.ix_(population, population)]
        # Divide before summing so finite large distances do not overflow.
        medoid = int(np.argmin((local / len(population)).sum(axis=1)))
        representatives.append(population[medoid if representative == "medoid" else 0])
        diameters.append(float(local.max()))
        members.extend(population)
        offsets.append(len(members))
    result = dict(
        schema="molsysmt.distance_clusters@1",
        cluster_indices=cluster_indices,
        cluster_offsets=np.asarray(offsets, dtype=np.int64),
        member_indices=np.asarray(members, dtype=np.int64),
        member_keys=keys,
        representative_indices=np.asarray(representatives, dtype=np.int64),
        cluster_diameters=puw.standardize(
            puw.quantity(np.asarray(diameters, dtype=np.float64), "nm")
        ),
        cutoff_distance=puw.standardize(puw.quantity(cutoff, "nm")),
        method=method,
        inequality="<=",
        representative=representative,
        tie_break="earliest_original_member_pair",
        representative_tie_break="earliest_original_member",
        matrix_sha256=digest.hexdigest(),
        execution=dict(
            estimated_work=work,
            max_work=max_work,
            estimated_numeric_bytes=numeric_bytes,
            merges=merges,
        ),
        software=dict(molsysmt=__version__, numpy=np.__version__),
    )
    attach_scientific_attribution(
        result,
        caller,
        [
            dict(
                id="arxiv:1109.2378",
                type="article",
                title="Modern hierarchical, agglomerative clustering algorithms",
                authors=["Müllner, Daniel"],
                year=2011,
                url="https://arxiv.org/abs/1109.2378",
                roles=["scientific_criterion"],
            )
        ],
    )
    return result
