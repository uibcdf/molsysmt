---
summary: Support indexed and bounded-memory iteration over large PDBQT structure ensembles
issue: uibcdf/molsysmt#434
status: partial
opened: 2026-10-23
closed:
verification: reproduced
area: [form, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Large PDBQT documents through form-specific structure iterators

**Reported:** 2026-10-23, during the maintainer's PDBQT handler review.
**Status:** Partial. Resident indexed snapshots and form-specific coordinate
blocks are implemented and contract-tested. Disk-backed reads, large-file
measurements and remaining scalability features stay pending after 1.0.

## What

Represent docking poses on the MolSysMT structure axis and implement efficient
`StructuresIterator` classes in the `iterators.py` modules for
`molsysmt.PDBQTFileHandler`, `file:pdbqt` and `string:pdbqt_text`.
These classes consume the existing `msm.Iterator` contract. This proposal does
not require changing the principal `molsysmt.basic.Iterator` implementation.

The iterators must read requested blocks without first converting every pose
into a MolSys or allocating the complete coordinate trajectory. File input can
remain on disk; text input is already resident and should avoid additional
whole-document copies and parsed-per-atom objects for every structure.

## How

- Share the PDBQT parser and one structural iteration kernel between adapters.
  Let handler iteration borrow the caller's resource; file/text iterators own
  and release resources they create. Cover exhaustion, errors, early close,
  context exit and interruption without closing a borrowed handler.
- For files, scan MODEL/ENDMDL boundaries and retain compact offsets plus source
  structure IDs. Read selected structures with seeks instead of repeated full
  scans. Consider a persistent index only with version/source binding, stale
  index rejection and an explicit reuse contract.
- Preserve start/stop/step/chunk behavior and ordered, repeated, nonconsecutive
  structure indices. Do not confuse MODEL labels with source structure indices.
  Return coordinate blocks shaped (n_selected_structures, n_selected_atoms, 3),
  including the final short block and a defined empty selection.
- Apply PyUnitWizard at the explicit angstrom boundary and preserve charges in
  elementary-charge units. Keep declared trees and opaque remarks separately
  from a complete molecular graph. Do not infer missing chemistry.
- Define homogeneous ensemble identity checks and validation coverage. A
  selected-block read cannot be advertised as validation of untouched models.
  Measure the up-front cost of full validation versus an explicitly deferred
  validation profile before changing the existing known-source pose guarantee.
- Integrate the form-specific iterators with existing ChunkedExecutor consumers;
  avoid a second independent trajectory-processing API.

## Why

A class named Iterator is insufficient if its setup materializes the entire
file/trajectory. The owning form classes can instead keep only an atom-scale
reference record, structure indexing metadata and the current block. This also
avoids changing a generic facade to solve a format-specific I/O problem.

For text, the caller has already paid for the input string: report additional
working memory separately from that resident input. For files, include the
handler's buffers/index and any validation caches in peak RSS.

## What is measured and what is assumed

Contract-tested: the PDBQT adapters support homogeneous MODEL ensembles, and
the known-source reader preserves the declared source chemistry. The generic
Iterator delegates structural requests to each form's StructuresIterator.
No large-file scalability benchmark has been executed for this proposal.

Assumed: a shared indexed/streaming implementation will reduce repeated I/O and
trajectory-sized allocations. This is a design hypothesis, not measured speedup.

## Acceptance criteria

- Exercise all three forms through their StructuresIterator and the unchanged
  public Iterator facade: single/unwrapped records, MODEL ensembles, explicit
  nonconsecutive/repeated structure lists, atom selections and short/empty blocks.
- Guards observe bytes/records read and actual allocations or peak RSS, not only
  correct output shape. Fail if producing the first chunk materializes the full
  coordinate trajectory or retains per-atom records for every pose.
- Measure cold scan/index, time to first block, sequential throughput, random
  lookup, repeated lookups and peak/additional RAM across increasing ensemble
  sizes with fixed block size. Record source hashes, versions, storage and scope.
- Verify equality of streamed/eager selected values against literal and real
  fixtures under non-default unit policies. Preserve source IDs and axes.
- Cover malformed/truncated models, changed atom axes/trees/charges, stale source
  contents, source replacement and independently owned copies/resources.
- Qualify interruption/cleanup and distinguish full-document validation from
  selected-only inspection. No silent dialect or chemistry expansion.

## Scope and exclusions

This is storage/iteration and scalability qualification, not Vina execution,
chemical preparation, pose scoring or graph recovery. Compressed-file indexing,
index persistence and concurrent/random-access policies need explicit supported
profiles; ordinary gzip is not assumed to provide cheap random access.
No arbitrary new release blocker, full/installed matrix or package publication
is authorized by opening this issue.

Related work: uibcdf/molsysmt#214 (forms), uibcdf/molsysmt#226 (known-source poses),
uibcdf/molsysmt#223 (correspondence) and uibcdf/molsysmt#334 (release scope).
DockingMT is the first consumer; adoption remains consumer-owned.

## Resident implementation checkpoint — 2026-10-23

`PDBQTFileHandler` retains one immutable text snapshot, compact character ranges
and MODEL IDs, one parsed reference model and an optional atom-scale native
cache. Opening validates every model, including invariant atom identities,
charges, types and torsion trees. It does not retain parsed atom dictionaries
for every structure. Explicit text input keeps the original string; file input
currently reads the complete UTF-8 source into memory. These are character
ranges in text, not seekable disk offsets or a persistent file index.

The three `StructuresIterator` classes in their respective `iterators.py`
modules share an internal kernel. Requested coordinate/occupancy/B-factor
attributes parse each requested model once per block. Atom order, nonconsecutive
and repeated structure positions, empty selections and short final blocks are
covered. Metadata conversion uses the reference model without materializing all
coordinates. The principal `molsysmt/basic/iterator.py` is unchanged.

Direct iterators close owned handlers on exhaustion, read failure, explicit
close and context exit. Iterating an existing handler borrows it and does not
close it. With the universal facade, an explicit handler context provides early
exit ownership without adding a second lifecycle API to `msm.Iterator`.

Primary guard: `tests/native/test_pdbqt_file_handler.py`. A record-read spy checks
that requesting the first selected block reads only those model bodies after
opening; it does not qualify the up-front validation cost or prove bounded RSS.
The new handler's direct/public conversion routes are also exercised by
`tests/conversion_truth/test_declared_docking_edges.py`.

Remaining acceptance: actual disk seeks/source binding, persistent-index policy,
compressed input policy, interruption/concurrent access, large-file RSS and I/O
measurements, cold validation/index and first-block latency, throughput and
real-ensemble qualification. No large-file speedup or bounded total file-input
memory is claimed. This issue remains open/partial.

### Validation receipt — 2026-10-23

The combined PDBQT/known-source poses/naming/atom-map/conversion execution,
argument/plugin and preparation-tool selection passed **661 tests** in
39.94 seconds with `--receptor=llm -n 12` (32 warnings: 25 legacy-H5MSM,
6 MDAnalysis mass deprecations and the known optional binary-size warning).
The final shaped-empty-ID follow-up is covered by the handler guard. The
four public-tool/reader doctests passed; the file-reader example also passed
again after using its own strict file namespace. Both maintained course modules
executed successfully. All 14 fast repository gates passed. No full scientific
or installed release matrix was run, and no large-file benchmark is claimed.

The machine-readable scope, source hashes and limitations are recorded in
[`pdbqt_handler_20261023.json`](../../devtools/data/pdbqt_handler_20261023.json).
