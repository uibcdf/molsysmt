# Interactions selection-query contract

**Role:** normative public query and migration contract
**Tracking:** uibcdf/molsysmt#346; consumer adoption: uibcdf/molsysviewer#168
**Introduced:** 0.23.0 pre-1.0 stabilization

## Selecting stored observations

Queries filter observations already present in an analysis. For an atom selection
S, let P be the union of all atom indices in the relation's participants.
Individual roles and compound participants contribute every constituent atom:
donor, hydrogen and acceptor all count in a hydrogen bond, and every atom of
each ring counts in a ring interaction. The selection boundary does not mean
the boundary of a molecule or group.

| Public `query(mode=...)` value | Predicate |
| --- | --- |
| `involving_selection` (default) | P intersects S. |
| `within_selection` | Every atom in P belongs to S. |
| `across_selection_boundary` | P has atoms both inside and outside S. |

An empty atom selection yields no observations in each mode. With
`atom_indices=None`, no atom filter is applied. Explicit structure selections
remove duplicates while retaining their first-seen order. Selected evaluated
structures with zero observations remain in coverage; unevaluated structures
do not become evaluated by querying them. Observation handles, participant roles,
measurements, images, source maps and sparse storage retain their existing contract.

`between_selections(A, B, ..., exclusive=False)` is a separate public operation,
not a fourth value of `query(mode=...)`. A and B must be disjoint atom-index
selections. A relation must touch both sets. Additional atoms outside their
union are allowed unless `exclusive=True`; exclusivity requires every atom in P
to belong to A or B. An empty A or B yields no observations. Structure and
interaction-type filters behave as in `query`. Both methods validate arguments
through ArgDigest and retain keyword-only `skip_digestion=False`.

Packed results, query views, invalidated snapshots and recalculated structure
blocks expose these same operations. The private selective HDF5 reader uses the
same query-mode vocabulary without becoming a new public file-query API.

## Compatibility and persisted data

Only the canonical names are supported. The maintainer removes the initial
compatibility spellings before public adoption: `incident`, `internal` and `cross`
are rejected query modes, and the `between` method is absent. This applies to
normal validation and trusted `skip_digestion=True` routes. Use:

| Previous query spelling | Supported operation |
| --- | --- |
| `query(mode='incident')` | `query(mode='involving_selection')` |
| `query(mode='internal')` | `query(mode='within_selection')` |
| `query(mode='cross')` | `query(mode='across_selection_boundary')` |
| `between(A, B, ...)` | `between_selections(A, B, ...)` |

MolSysViewer owns migration of its executable calls and saved display
filters/history/session fields. Map previous query names to the four explicit
names while preserving selected atom and structure axes, both selections and
exclusivity. A consumer still using the previous vocabulary must update before
adopting this provider source; the earlier consumer commit is not certified
against this changed API. No consumer-only query alias is needed.

Calculation `selection_mode` and result `evaluation_mode` remain separate
contracts. Their existing `internal`, `incident` and `between` values describe
the searched atom sets and universe, not a display filter. A query cannot widen
that search or turn unevaluated atoms/structures into evaluated evidence.
Detectors retain their current selection modes, defaults and scientific criteria.
In particular, there is no new detector mode for `across_selection_boundary`.

H5MSM 0.5 and InteractionsDict v1/v2 store scientific evaluation metadata, not a
standard query-filter field. Preserve those values, detector parameters and
execution provenance on load/save. No interaction-schema or H5MSM version bump
is required. Do not globally replace matching strings inside user metadata or
saved scientific records. A consumer's saved query filter can be migrated only
when its field is known to carry query/display semantics.

## Verification boundary

The public workflow regression selection covers the canonical vocabulary and rejection of previous query spellings,
compound rings, hydrogen-bond roles, parallel observations, selected structures,
evaluated-empty coverage, exclusivity, argument validation and edited snapshots.
Typed-dictionary and public MolSys/H5MSM round trips retain each of the three
scientific evaluation modes. Existing schema-v1, selective HDF5 and native edit
guards remain applicable. Provider tests do not certify adoption by the Viewer
Python API, Studio, canvas or saved sessions; uibcdf/molsysviewer#168 owns that.
