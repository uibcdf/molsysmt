---
summary: Support indexed and bounded-memory iteration over large PDBQT structure ensembles
issue: uibcdf/molsysmt#434
status: resolved
opened: 2026-10-23
closed: 2026-10-23
verification: measured
area: [form, performance]
guard: tests/native/test_pdbqt_indexed_file_handler.py
normative:
blocked_by: []
supersedes: []
---

# Large PDBQT documents through form-specific structure iterators

**Reported:** 2026-10-23, during the maintainer's PDBQT handler review.
**Status:** Resolved for the documented uncompressed indexed profile.
The resident checkpoint below is historical; the indexed implementation and
qualification sections record the completed scope.

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
At opening, no large-file scalability benchmark had been executed. The dated
indexed qualification below supersedes that initial evidence status.

Initial hypothesis: shared indexed/streaming delivery would reduce
trajectory-sized allocations. The completed measurements below support the
memory benefit, not a speedup.

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
[`pdbqt_handler_20261023.json`](../../../devtools/data/pdbqt_handler_20261023.json).

## Indexed-file implementation — 2026-10-23

The maintainer authorizes completing the uncompressed indexed profile now.
`PDBQTFileHandler(..., storage_mode='indexed')` retains a binary descriptor,
byte ranges, MODEL IDs and one parsed reference model. The resident default
retains its original snapshot behavior. File-form getters and iterators use
indexed temporary owners, so the unchanged universal facade does not first
read the source into a complete text string during metadata resolution.

MODEL grammar is shared between text and file offset producers. UTF-8 and CRLF
byte/character differences are guarded. Every model is validated up front;
source identity, size and nanosecond timestamps are checked around selected
reads. An edited, replaced or removed source requires reopening. This is an
operational consistency guard, not authentication or a filesystem snapshot.

Copies share a locked source lease with independent close ownership. Python
copies and abandoned handles release their leases; context managers provide
deterministic release. Owned iterators release on exhaustion, errors and
interruption; borrowed handlers remain caller-owned. File output is atomic and
bounded: full-atom source ranges use byte chunks, and rigid atom subsets use
one selected model at a time. An output string, resident selection/extraction
or complete requested coordinate/native output still materializes that result.
The known-source mapped reader remains eager in its source metadata.

The existing ChunkedExecutor consumes coordinate chunks without another
trajectory API; center parity is guarded. Operation-specific scientific
qualification remains separate, including the reported distances defect
uibcdf/molsysmt#441. This registration is not a claim that every heavy
geometry combination is already qualified.

### Measurements and limits

The [benchmark procedure](../../benchmarking/pdbqt.md) and
[trial receipt](../../../devtools/data/pdbqt_storage_benchmark_20261023.json) retain
12 fresh-process trials over 256, 2,048 and 8,192 structures × 64 atoms.
For the 39.67 MiB largest file, additional process peak is approximately
79.38 MiB resident and 5.44 MiB indexed. Opening is approximately 8.46 versus
9.00 seconds; selected four-structure queries are 4.00 versus 4.32 ms. Thus the
measured gain is working memory, with some I/O/check overhead, not uniform
speedup. Full validation still dominates first-block latency. The OS page
cache is uncontrolled; no cold-disk claim or timing threshold is introduced.
Source hashing rejects mixed-source benchmark runs.

Working memory also depends on range/ID metadata, the reference model, retained
preamble, a current model and coordinate blocks; large individual metadata can
dominate it. The allocation regression rejects a source-sized input-text copy
under tracemalloc, while separate RSS measurements cover actual process memory.
Original Vina fixtures and an engine-generated ensemble provide bounded
real-input and coordinate references, not chemical preparation validation.

### Explicit scope decisions

- Supported: uncompressed UTF-8 files, resident text, ordered/repeated query axes,
  unique serialized structure selections, concurrent copied-handle reads,
  source binding, deterministic ownership and bounded file output.
- No persistent index is written. Reopening revalidates; a reusable sidecar
  would need its own source/schema identity and stale-index policy.
- Compressed random access is unsupported. Ordinary gzip seeking does not
  acquire a validated indexed contract merely because an iterator exists.
- Descriptor access is serialized; no parallel decoder or Rust parser speedup
  is claimed. Windows may prevent replacement/unlink of an open source, in
  which case the mutation is denied and the original remains valid.
- No new H5MSM schema, full/installed release matrix, tag or package publication.

### Final qualification receipt — 2026-10-23

The combined indexed/resident handler, file/text adapters, known-source poses,
conversion truth, units and argument/plugin regression passed **520 tests**
in 38.26 seconds with `--receptor=llm -n 12`. The 37 warnings are 30 legacy
H5MSM reads, six MDAnalysis mass deprecations and one previously tracked NumPy
binary-size warning. No failure or skip occurred. The allocation guard, source
mutation/atomic-output guards, resource/interruption guards and original Vina
ensemble check ran in that selection.

The executable handler guide example passed, course module 19 executed,
250 selected docstrings passed and all 14 fast repository gates passed. The
Sphinx build completed with existing documentation warnings. The principal
Iterator implementation is unchanged. The scoped machine-readable receipt is
[`pdbqt_indexed_qualification_20261023.json`](../../../devtools/data/pdbqt_indexed_qualification_20261023.json).

The primary guard inspects requested byte reads, rejects a source-sized text
allocation, checks copied resource ownership and verifies atomic output on
source failure. Together these assertions protect the promised storage
behavior rather than merely accepting an iterator-shaped result. No installed
release matrix or publication is implied.
