---
summary: H5MSM 0.5 queries read full coordinate series before applying selection.
issue: uibcdf/molsysmt#643
status: active
opened: 2026-11-07
closed:
severity: high
verification: measured
area: [form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bounded queries must not materialize an entire H5MSM coordinate series

## What

Public `get(path, n_structures=True)`, numeric `select(path, ...)` and selected
coordinate `get(path, ...)` materialize all H5MSM 0.5 coordinates before applying
the query. The returned values are correct in the reproduced population, but
unnecessary I/O, allocation and latency scale with the complete trajectory. A
small or scalar request can therefore exhaust memory on a large file.

The problem surfaced in the accepted #421 external-reference GUI workflow.
That prototype retains only five selected reference atoms in one structure
(120 float64 bytes), but a lower-level HDF5 read spy correctly refuses its
unrequested full-series reads. Do not weaken that guard or introduce a private
file reader inside the GUI to conceal the public query behavior.

Related consumer: uibcdf/molsysviewer#315. This is provider work in MolSysMT.
It is separate from #336's deferred detector-to-file/resumable interactions and
#438's ownership/location review of implementation modules. No format bump is
required.

## How and evidence

On published baseline `07f04d9e8b7702348dc1c365796558435e195c97`, an independent
probe writes a small structures-only H5MSM 0.5 with 5,000 structures, ten atoms
and canonical nm coordinates. A spy on `h5py.Dataset.__getitem__` records the
coordinate dataset access while running these public operations separately:

```python
msm.get(path, n_structures=True)
msm.select(path, selection=[1, 4, 3, 2, 0],
           structure_indices=[4999], chemical_state='reference')
msm.get(path, element='atom', selection=[1, 4, 3, 2, 0],
        structure_indices=[4999], coordinates=True)
```

Each operation reads coordinate blocks `slice(0, 4369)` and
`slice(4369, 5000)`, covering the entire series. A scalar count should read no
coordinate values; numeric atom selection needs only axis metadata; the last
operation needs one structure and the five requested atoms in their stated
order. The file holds 150,000 coordinate scalars (1,200,000 uncompressed bytes),
so this reproduction is small and deterministic rather than a machine-memory
stress test. The 120-byte retained snapshot is not a claim about peak RAM or I/O.

The trace reaches `basic.get._get` / `basic.select`, then
`_private.h5msm.maybe_read_modular_h5msm`, `read_molsys_file`,
`read_modular_file`, `read_independent_structures` and
`_StructureArray._from_reader`. The compatibility bridge unconditionally
materializes the file before public query dispatch. Source inspection also
shows that unrequested domains can be loaded by the same bridge; the probe's
executed measurement covers coordinates, not every unrelated domain.

The local external-reference prototype is retained at `ca59736a4`, not merged
or advertised as delivered. It passes 339 directed cases before the stronger
I/O guard; the expanded population has 340 passes and one failure at that guard.
Initial 324-case receiving preceded the expanded cases. These campaigns overlap
and are not additive. No public GUI milestone is credited yet.

An independent provider-only checkout now reproduces this on the same public
runtime bytes, without the GUI prototype. The standalone form regression has
**18 failures**, refusing unrequested `structure_id` payload reads before the
requested scalar or projection. It watches ordinary indexing, `read_direct`
and implicit array conversion. The separate 5,000-structure primitive probe
still records both complete coordinate blocks for each operation and verifies
the correct returned values. Its native exit 0 is diagnostic success, not query
contract acceptance. The [baseline receipt](../../devtools/data/modular_h5_query_baseline_643_20261107.json)
records source blob correspondence, commands and contradictory I/O evidence.

## Implementation strategy

1. Reproduce at the owning public `get` / `select` boundary with standalone
   offline form tests, independent of Viewer or the GUI prototype. Protect
   metadata-only counts and numeric selection, reordered/repeated axes, units,
   empty results and input/error integrity. Record actual dataset windows, not
   just the small shape of a result retained after an eager read.
2. Reuse the existing modular axis metadata, field/schema/unit validation,
   typed layer readers, projected iterator and index validators. Review their
   precise admission and lifetime contracts before adding another abstraction.
3. Implement schema-aware query delivery at the file-form/general-query owner.
   Preserve the public `file:h5msm` identity and signatures. Keep the explicit
   legacy-handler 0.3/0.4 contract; do not pretend a 0.5 file has the old topology
   layout or silently enable unreceived legacy setters. Reuse the existing
   getter-delegation factory if generating validated adapter functions.
4. Counts/axis validation must inspect metadata only. Structural getters must
   read only requested fields and numeric windows, preserving atom/structure
   order and repetitions, explicit units, shape and typed empty results.
   Inventory/chemistry queries must load only the required independent domains,
   not coordinate trajectories or named analyses. Bulk extraction should share
   its minimal decoded context rather than reconstruct each domain per field.
5. Preserve selection semantics, composites, explicit chemical-state context,
   association/index-space validation and native structured diagnostics. Rich
   selections may need geometry, but only the structures actually requested.
   Validate queried schemas/units and required axis links; do not silently map
   ambiguous domains or infer missing chemistry. Document any remaining bounded
   admission or deliberately eager operation rather than claiming universal
   laziness. Full resident conversion remains a distinct operation.
6. Qualify the general provider independently, then receive #421's unchanged
   public-query composition. No GUI-only HDF5 access, copied scientific method,
   fake native domain or full-trajectory placeholder is accepted as a fix.

## Acceptance and closeout

- Scalar and axis-only queries read zero coordinate payload; the projected
  coordinate case reads only the requested atom/structure windows.
- Values, physical units, source index spaces and ordering match the supported
  native routes, including repeated/nonconsecutive indices and empty selections.
- Optional domain combinations, actual attributes, chemical context and required
  associations remain explicit; requested malformed schemas/units/indices fail
  before returning partial results.
- Pure static inventory/chemistry queries do not read coordinates or unrelated
  named-analysis occurrence columns. Mixed/bulk/composite queries retain their
  documented output and select the minimal valid source context.
- Legacy 0.3/0.4 reads, deprecation warnings, handler lifetime/rejection,
  conversion/iterator behavior and untouched source bytes remain protected.
- Tests cover the actual failure mechanism. Public lifecycle documentation and
  the scalability/benchmark guidance describe the executed scope and limits.
- Hand the published provider fix back to the #421 external-reference workflow,
  then finish its actual Jupyter/Mol*/popup acceptance. This issue's correction
  is not by itself that GUI milestone or installed/final-candidate acceptance.

## Current execution position — 2026-11-07

**Implemented and contract/parity-tested locally**, not yet public delivery.
The file-form owner now routes schema 0.5 queries to one scoped reader while
retaining the real file form and the separate legacy handler. Public query
boundaries no longer invoke the resident bridge. Structural codecs accept a
field projection; original atom/structure order and repetitions survive. Static
native domains and existing selectors are reused without fake coordinate
arrays, competing chemical stores, new dependencies or native-kernel changes.
The lexical query scope shares required static decodes and closes owned handles
on success and failure. No file cache survives a call.

The [receiving receipt](../../devtools/data/modular_h5_query_receiving_643_20261107.json)
retains every executed attempt. Original provider baseline: 18 failures.
Receiving-1: sixteen passes/two empty-index failures. Integrated-1: 1,552
passes/five alternate-site regressions. Integrated-2: 1,591 passes/three eager
chemical-selector failures and one incorrect fixture expectation. `None`
validly resolves the declared reference; this now has a positive guard, while
invalid/ambiguous states explicitly require `StructuralInconsistencyError`.
Integrated-3 passes 1,595, integrated-4 passes 1,619, and the final wider
receiving passes **1,921**. These populations overlap and are not additive.
The final population contains **eighty new provider cases**, real nonempty
unrequested interaction observations, physical-unit contexts, malformed schemas,
spatial masks, scoped chemistry, composites, lifetime and immutable-source
checks. Three public doctest nodes and all fourteen fast gates pass. Source
fingerprints stay unchanged during each recorded campaign. Course edits change
only narrative cells; code and saved outputs are preserved.

The independent 5,000-structure probe now observes **zero coordinate reads**
for counts and numeric selection, and one `(4999, [0, 1, 2, 3, 4], ...)` read
for the five requested atoms, returned in their original requested order.
That is fifteen coordinate scalars/120 uncompressed bytes logically selected,
instead of 150,000/1,200,000 per operation. This is dataset-window evidence,
not a physical-disk, decompression, total-RAM or timing measurement.

Static domains and required explicit association maps can still be decoded in
full; sparse alternate-site queries can retain complete offset/index vectors.
The projected expression guarantee covers MolSysMT syntax. External selection
backends retain their conversion behavior. Resident conversion/layer loads and
downstream result accumulation remain separately budgeted. These limits are
explicit in the public guide and scalability contract; the change does not
claim a universal lazy molecular-system object.

HTML builds with exit 0 and six retained existing title-underline warnings;
the rendered query section and its limits are checked. Next: finish clean
exact-source scientific qualification, receive the
original external-reference I/O guard, then publish/verify the owning source and
close this bug with its executable guard. Actual external-reference GUI
Jupyter/Mol*/popup acceptance remains with #421. Milestone progress remains
approximately 61%, graphical acceptance 22/50, source closeouts 32; no prototype
or discovered prerequisite receives bonus milestone credit.
