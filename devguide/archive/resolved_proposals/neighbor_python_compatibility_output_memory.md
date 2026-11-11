---
summary: Account for compatibility-output memory beyond native neighbor CSR admission.
issue: uibcdf/molsysmt#693
status: resolved
opened: 2026-11-10
closed: 2026-11-11
verification: measured
area: [structure, performance]
guard: tests/structure/get_neighbors/test_compatibility_output_memory.py
normative:
blocked_by: []
supersedes: []
---

# Account for compatibility-output memory beyond native neighbor CSR admission.

## What

Measure and account for memory in existing Python compatibility outputs beyond
#690's native numerical input/grid/scratch/CSR estimate. Do not equate that
estimate with process RSS or an OS reservation.

## How

Source inspection finds default neighbor object arrays retain per-row NumPy
view headers/object slots. Contact pair output keeps its Boolean map while
upper-triangle/nonzero/column-stack intermediates and `.tolist()` create arrays
and Python objects. The new native guard reserves the Boolean map and reduces
map filling, but does not claim to bound these separate legacy costs. No OOM
or incorrect result is reproduced for this representation scope.

## Why

A sparse search does not make dense or boxed compatibility results small. The
[guarded native repair](../resolved_bugs/native_neighbor_cell_grids_can_allocate_gigabytes_for_two_atoms_and_a_small_cutoff.md)
must not imply a whole-process guarantee.

## Acceptance and exclusions

Measure representative row/occurrence populations under finite cgroup limits;
choose a justified estimate, bounded conversion or explicit representation
recommendation. Reuse existing CSR and iteration tools. Preserve public shapes,
units, indices, empty results and scientific values. Unsupported output sizes
need a clean refusal or documented bounded alternative. No speculative API,
dependency or automatic new pre-1.0 blocker is introduced.

## Delivery and measurements — 2026-11-10/11

**Contract-tested:** eligible default neighbor output reserves two NumPy view
headers/object slots per query row before native admission. PyUnitWizard's
constructor retains the CSR distance storage instead of multiplying the object
array and copying its distance rows. Flat CSR output avoids row objects and its
unit wrapper also uses the constructor. Dense/fixed-count fallback output admits
returned numeric/row storage and conservative row-sort workspace. Legacy
pair-label output has additional scalar-quantity/list headroom; a separate warm
Pint control measured about 237–244 bytes per occurrence and the model allows
1 KiB. This is a conservative working estimate, not a universal backend/RSS proof.

Contact conversion counts output in bounded slabs, admits Python integers/lists,
mapped labels and scratch before boxing, and packs directly in final label
space. It avoids whole-map triangular/nonzero/column-stack intermediates.
Native CSR filling buffers are retired before boxing; the requested dense
Boolean map remains resident. Sorting occurs in place before publication.
Unsupported representation sizes raise the existing catalogued
MemoryBudgetExceededError without changing source coordinates. No output
format, scientific cutoff, periodic criterion, dependency or signature changed.

The [reproducible receipt](../../../devtools/data/compatibility_output_memory_693_20261110.json)
contains 18 legacy/current projection samples, exact producer-file hashes,
Python/NumPy/platform identity, traced allocations and untraced timings. Run
`python devtools/scripts/profile_compatibility_output_memory.py --output <file>`
inside an OS memory limit. Legacy formulas are frozen measurement controls;
inputs and runtime imports precede tracing. Timings use two warmups and five
untraced samples, GC before timing and result retirement excluded. They concern
projection only, not a molecular search or total RSS.

Representative additional allocation peaks, in decimal MB:

| Projection | Population | Legacy | Current |
| --- | --- | ---: | ---: |
| Neighbor rows | 50,000 rows, 150,000 occurrences | 19.20 | 12.00 |
| Unmapped contact pairs | 512 atoms, 130,816 pairs | 18.82 | 15.10 |
| Atom-mapped contact pairs | same | 35.57 | 19.33 |

The neighbor sample's separate CSR payload is 2,800,008 bytes. Smaller unmapped
contact samples can have greater projection peaks because bounded slab/guard
overheads dominate. All samples, including those adverse cases, remain in the
receipt. Warm projection time roughly halves for neighbor rows and mapped
512-atom contacts improve, but unmapped self-contact packing is slower by
roughly 48–85% in these samples. At 512 atoms its median is about 36.7 ms versus
21.7 ms. The [existing advisory work](../../pending_proposals/neighbor_allocation_safety_performance_followup.md)
retains that warning. Under #567, correct outputs remain available; neither a
speed claim for the whole tool nor a performance release blocker follows.

The profile ran inside a one-CPU, 1-GiB/no-swap user scope. The **181 passing
geometry cases**, including **15 new representation guards**, ran with two
workers in a CPU-quota-200%, memory-high/max-3/4-GiB scope. They cover native/dense
contacts, nonconsecutive structures, multiple slabs, ordered/remapped/sorted
pairs, self triangles, empty CSR versus costly row output, fixed counts, source
immutability, nm/angstrom/pm and returned-storage lifetime. The two existing
MemoryPressureWarning observations concern deliberately tiny per-query budgets,
not demonstrated host pressure. No OOM or incorrect scientific result was
reproduced. Host sampled availability remained above 12 GiB during this work,
with no active swapping in the sampled interval; other processes were untouched.

Pint and OpenMM row-quantity construction were received separately. unyt and
Astropy reject this ragged object representation through both the prior and
current routes; flat numeric CSR distances work in all four. The existing
limitation and capability/diagnostic proposal are reported in
uibcdf/pyunitwizard#148. QuantityRecord's numeric/object rejection is unchanged.
That proposal is not a blocker or claimed provider acceptance.

The docstrings, two Toolbox tutorials, Foundations, big-data Cookbook and
Common Core iteration lesson describe the admitted scope and bounded
alternatives. Notebook changes preserve all code, outputs and metadata.
Source-runtime and allocator costs outside the stated model remain explicit.

Seven selected HTML pages are built and inspected with notebook execution and
autosummary source rewriting disabled. All 254 public docstrings, optional-import
checks, unchanged public signatures, four stored notebook schemas, course
structure, focused Ruff/format checks and developer-guide lifecycle checks pass.
The existing four human-edited RST files are byte-identical to their pre-task
snapshots. This is a source-level implementation/representation qualification;
native performance #692, final installed candidates and publication remain open.

Final public-example receiving, 2026-11-11: both modified geometry modules pass
their **two doctests** in addition to the 181 geometry cases above.
