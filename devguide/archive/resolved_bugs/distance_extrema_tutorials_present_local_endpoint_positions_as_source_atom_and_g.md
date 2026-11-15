---
summary: Distance-extrema tutorials present local endpoint positions as source atom and group indices
issue: uibcdf/molsysmt#757
status: resolved
opened: 2026-11-14
closed: 2026-11-14
severity: medium
verification: reproduced
area: [docs, structure]
guard: tests/documentation/test_distance_extrema_tutorials.py
normative:
blocked_by: []
supersedes: []
---

# Distance-extrema tutorials confuse endpoint positions with source indices

**Reported:** 2026-11-14 during the admitted #334 geometry-example review.
**Status:** resolved; the existing calculation API is unchanged.

## What

The minimum/maximum-distance tutorials print local positions returned by the
reduction as if they were source atom indices. The minimum-distance lesson also
prints centroid population positions as source group indices. A calculation can
run correctly while its reported atoms or groups belong to another selection.

## How

`get_minimum_distances` and `get_maximum_distances` document ordered endpoint
positions. The tutorials interpolate those integers directly into atom/group
labels without mapping through their actual selected memberships.

## Why

Users following the primary examples can inspect or visualize the wrong atoms.
The numerical extrema are not the demonstrated defect. Preserve the API and
map the returned positions explicitly; also state that geometric extrema do
not automatically filter covalent bonds or align different structures.

## What is measured and what is assumed

All nine selected geometry/box notebooks are being executed in fresh kernels
on frozen 6deb0200c source. Executability is separate from correct scientific
interpretation. The regression will execute the actual example cells and check
reported source memberships and distances against independent NumPy coordinate
calculations. No full-corpus, browser, installed or final-pair claim is made.

## What was refuted

Changing the reduction API to return global indices would change the maintained
contract and hide the missing educational mapping. It is unnecessary.

## Scope and exclusions

Correct the two extrema lessons, preserve all scenarios/plots/anchors and
receive their actual saved outputs. Existing calculation methods, providers,
compiled routines and public return values remain unchanged.

## Acceptance criteria

- Printed atom/group indices belong to the intended source populations.
- Independent coordinates reproduce the extrema associated with those indices.
- All selected notebooks execute, retaining their scenarios and figures.
- Relevant regression, schema, documentation and governance checks pass.

## Provenance

Linux shared host; existing Python 3.14 development interpreter and recorded
support overlays. Exact source/native/runtime identities, original negative
controls and monitored resource limits will accompany the completion receipt.

## Resolution — 2026-11-14

Five regressions fail on the original examples. For example, the first minimum
prints source atoms 4 and 3, although the second endpoint population starts at
36; the actual minimum pair is 4 and 39. The inter-chain report's second atom
belongs to chain 0, and the centroid report's group 12 belongs to the first
chain rather than the second. Numerical extrema are not the defect.

The lessons now map each reduced population separately. Per-atom minima map
through the target atom list; center extrema map through aligned group lists.
The first maximum and all-atom displacement examples explain when local
positions happen to equal source indices. The adjacent distance lesson no
longer identifies arbitrarily selected groups 0 and 4 as peptide termini.
Geometric extrema do not imply nonbonded filtering, chemical interactions,
alignment, unwrapped motion or binding affinity. All examples and plots remain.

The actual-cell regression uses independent NumPy coordinate/membership
expectations. The final selected command passes **21 cases, zero skips**:
ten numerical cases across nm/ps and pm/fs, seven saved-plot guards and four
existing bounded-pose/Common Core cases. Its published receptor reader agrees
with complete same-invocation JUnit. The five expected legacy-H5MSM warnings
remain explicit. Existing validated public calls and PyUnitWizard contexts
are used; no new argument/dependency/diagnostic or attribution boundary is
introduced, and no third-party scientific method is added.

Nine complete tool notebooks execute in fresh kernels: **81 distinct code
cells and twelve actual figures**. The maintained runner writes their marks;
code/Markdown content and existing IDs survive output adoption. The strict
complete Sphinx build produces 1,400 HTML files with zero warnings. All nine
actual articles and the twelve byte-identical PNG payloads are received.

The first operator harness used the noninteractive Agg backend and omitted
figures despite successful numerical execution. Seven new guards reject those
outputs. That configuration is corrected to Jupyter's inline backend before
adopting the final outputs. The initial receipt-name collision starts no
kernel; a first Sphinx child is intentionally interrupted after discovering
missing figures. Those unsuccessful/limited attempts remain separate evidence,
not library failures or passing final documentation. The [receipt](../../../devtools/data/geometry_documentation_receiving_334_757_20261114.json)
retains their native outcomes and exact compositions.

All work uses the existing Python 3.14 environment and frozen source basis
6deb0200c plus the recorded documentation/test delta, with the unchanged
4ffb82e4 native binary. One-CPU/two-GiB services monitor a 6.5-GiB host reserve;
at most two run together. No native rebuild, installation, hosted matrix,
package, tag or publication occurs. The separate #758 course defect is queued;
this finite receiving does not qualify the full notebook corpus, browser,
installed pair or final candidate.
