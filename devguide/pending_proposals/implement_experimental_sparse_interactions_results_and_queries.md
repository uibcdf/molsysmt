---
summary: Implement experimental sparse Interactions results and queries
issue: uibcdf/molsysmt#252
status: partial
opened: 2026-09-28
closed:
verification: measured
area: [api, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Implement experimental sparse Interactions results and queries

## Nine-family provider qualification — 2026-10-01

**Contract-tested and parity-tested:** clean MolSysMT source commit
`3b12fba501909a052fd115b09ddb11aae875ee66` passed **729 tests**, with no skips:
687 interaction and reusable scientific-tool cases, plus 42 charge-center,
native collection and typed-dictionary cases. The selected modules cover all
nine experimental families, including one- and two-water paths, compound
participant queries, nonconsecutive frames, evaluated-empty coverage,
non-default units, observed periodic images, named persistence, remapping,
producer versions and detached attribution. Existing frozen independent-oracle
comparisons ran within these tests; reference programs were not regenerated.

The existing real MolSysViewer qualification command also returned exit 0 on
this provider revision, unchanged and clean before and after the run. All four
workloads below retained their observations; the combined run passed geometry,
query and persistence checks. MolSysViewer was at `ca6a3cda9eefcbd878775bcced8e21e7cb9bc069`
with 290 pre-existing dirty entries; Ackredit was at
`e4ff20a30f4eb862472e82144d582f101c2a5fd6` with nine dirty entries and 35 commits
behind its fetched upstream. Those worktrees were preserved. Their HEAD hashes
alone do not identify complete sources. The bounded suite-status inspection
reported these differences; no sibling merge, checkout or edit was performed.

Commands, environment, exact provider identity, qualification-script hash,
test outcomes and consumer observations are recorded in
[the dated qualification artifact](../../devtools/data/interactions_provider_qualification_20261001.json).
The recorded installed MolSysMT version differs from the source revision; it
must not replace that revision when identifying this editable-source test.
Runtime dependency validation, Ruff and the public stability checks passed.

**Consumer boundary:** the inspected Viewer projects `hbond` and
`disulfide_candidate` geometry. Its other interaction types are currently
counted as skipped by that projection. This run therefore does not establish
visual support for the other seven families. It also does not establish a new
browser/WebGL run, a published dependency pair or the complete exact-candidate
release gate. Those remain with the consumer and release owners.

The current experimental provider delivery is ready for the next consumer
review. No public method, default, result schema or stability classification
changed during this qualification. The original checkpoint below remains
historical evidence for its earlier provider revision.

## Consumer and attribution checkpoint — 2026-10-01

The experimental packed result, named `MolSys.interactions` collection and
public H5MSM 0.5 codecs are implemented. At the measured consumer checkpoint
below, five detector families produced supported results: hydrogen bonds,
disulfide candidates, ionic, pi-pi and cation-pi. The current nine-family
inventory, including subsequently implemented detectors, is maintained in
[the interaction-family roadmap](organize_interaction_detection_by_family_before_1_0.md).
Legacy tuple defaults remain available; scientific/descriptive method selectors
and exact profiles preserve previously validated numerical behavior. Optional
attribution is analysis metadata, not an occurrence column. Current contracts
belong in [Interaction Analysis API](../interactions_api.md) and
[H5MSM Format Contract](../h5msm_format.md). The dated checkpoints below are
implementation history, not the current outstanding-work list.

**Measured consumer qualification:** The real MolSysViewer qualification tool
was run against clean provider commit
`e21f03d9992b87af2cc9285211adee888462be41`, unchanged before and after the run.
The consumer checkout was on `a8aa669c9e3b712f4433511bdf990c5e8df54e30` with existing
human changes preserved; its head hash alone does not identify that dirty tree.
It passed with process exit 0:

| Case | Observed workload | Verified behavior |
| --- | --- | --- |
| Pentalanine trajectory | 62 atoms, source structures `[4999, 0, 73, 3]`, evaluated local structures `[3, 0, 2]`, 56 observations | Nonconsecutive/atom-set queries and complete H5MSM, analysis-only H5MSM and MSV session round trips. |
| Controlled periodic reimaging | 62 atoms, 76 observations, 16 with nonzero images | A real residue translated by one box vector; independently reconstructed geometry under an angstrom unit policy. |
| Solvated villin | 4,369 atoms, one structure, 2,439 observations, 299 with nonzero images | Real sparse Buch output and image geometry; numeric analysis arrays occupy 562,168 bytes. |
| 2HGR sulfur proximity | 55,628 atoms, eight candidates at 0.205 nm | Candidate geometry without modifying declared covalent connectivity. |

The trajectory case took 5,645 ms including its workflow; the villin case took
1,765 ms. Peak RSS was 860.7 MiB for the entire importing/qualifying process, not
the interaction arrays alone. These one-run observations are not comparative
performance guarantees. Installed MolSysMT metadata reported
`0.21.0+606.ga03eb4bf6`; the source commit above identifies the provider tested.
The JSON result is the last log line. Reproduce with the real consumer tool:

```bash
python ../molsysviewer/devtools/qualify_interactions.py /tmp/molsysmt-viewer-qualification
```

The tool is maintained by the consumer under `uibcdf/molsysviewer#114`; no sibling
documentation path is treated as a contract. This evidence covers Python API,
canvas-message geometry and persistence. It is not a fresh browser/WebGL run,
an installed published pair, or the final exact-candidate 1.0 gate.

**Attribution guard:**
`tests/interactions/test_scientific_attribution.py::test_real_viewer_preserves_original_bibliography_in_named_analyses_and_sessions`
uses real optional Ackredit and MolSysViewer public APIs. A successful
Baker–Hubbard calculation credits its producer session; named metadata, queries,
complete/analysis-only H5MSM and session recovery retain the same detached
bibliography and original versions. Evaluated-empty frames and occurrence indices
survive. A fresh reader session remains uncredited. This optional client guard
must be run with Ackredit and the experimental Viewer interactions API installed;
older clients without that API skip, and a skipped test is not client evidence.
The final focused attribution module run passed all 18 tests in 13.46 seconds.

**Remaining:** exact-candidate consumer/release qualification, result stabilization
after agreed client evidence, and separately scoped incremental editing or public
bounded file access. Current immutable snapshots and resident sparse detector
results are not an incremental editor or a streaming writer. Halogen,
hydrophobic, metal and one-/two-water bridge detectors are now implemented
experimentally under #250. The earlier consumer measurement above does not
qualify these later additions; final consumer evidence must identify the actual
provider and client candidates tested.

## Luzard-Chandler result adapter (2026-09-29)

`get_luzard_chandler_hbonds(..., output_type="molsysmt.Interactions")` now
returns automatic donor/hydrogen/acceptor roles, the actual eligible
participant scope, evaluated-empty coverage, D-A distances in nm, H-D-A
angles in rad, method criteria, evidence, and producer versions. Periodic
images independently unwrap D-H and D-A from the donor, matching the angle
kernel. The adapter checks both distance and angle; an inconsistent
hydrogen image is rejected even when D-A distance still agrees.

The tuple default retains rectangular arrays when per-frame counts agree
and returns aligned lists with shaped empty entries when they differ. The
one- and two-selection paths share packing and handle donor-free directions.
The return failures reproduced under `uibcdf/molsysmt#259` are corrected.
The angle cutoff remains strict; no distance or chemical criterion changes.
Shared result packing leaves Buch's two-column output unchanged.

The optional output has the same current scope limits as Buch: automatic
roles, one selection, two disjoint eligible universes, or identical roles.
Supplied roles, a second structure axis, and partially overlapping universes
are explicitly unsupported. The calculation is eager, and the observed-image
pass is not yet benchmarked at trajectory scale. This checkpoint supersedes
earlier pending-adapter statements below. MolSysViewer excludes the method
from its initial integration; its Buch/disulfide integration still proceeds.

Validation: 110 focused tests passed across interaction results, both legacy
hydrogen-bond APIs, InteractionsDict, and public H5MSM conversion. Two detector
doctests passed. The LC tutorial executed all six code cells and its new
sparse example reported 36 observations with nm/rad measures and the captured
producer version. Expected bundled H5MSM 0.4 deprecation warnings remain.
Ruff passed. Scientific fixtures include direct nonperiodic distance/angle
checks and explicit periodic image reconstruction, not only codec parity.

## Accepted attachment responsibility (2026-09-29)

The maintainer accepts declared correspondence for the pre-1.0 contract:
the writer owns the correspondence of system and analysis layers, and the
caller owns the alignment of an independently loaded analysis with the target
system. The [normative attachment policy](../interactions_api.md#associating-analyses-with-a-system)
states the current checks and the meaning of `source_id` and source maps.
Automatic origin verification and fingerprints are optional future work,
not remaining 1.0 gates. This refines the earlier source-fingerprint proposals
in this report without removing invalidation for known scientific changes.
MolSysViewer's request and the accepted decision are recorded in
[the result design proposal](design_a_sparse_public_interactions_result_and_serialization_contract.md).
MolSysViewer accepts this policy after reviewing `2e79b5f29`, reports 27
focused passing tests, and excludes Luzard-Chandler from its initial client
scope. `Interactions.software` now preserves the calculation-time version
through views, edits, dictionaries, and H5MSM. Buch and disulfide candidates
populate it; old payloads without it remain unknown rather than adopting
the reader version. The guard is `tests/interactions/test_software_provenance.py`.
Luzard–Chandler remains in the MolSysMT implementation scope.

## Buch detector result adapter (2026-09-29)

The Buch detector now has optional `output_type="molsysmt.Interactions"`,
with automatic donor/hydrogen/acceptor roles, eligible participant scope,
evaluated-empty coverage, H-A distances in nm, criterion parameters, chemical
selection rules, and observed periodic images. The donor is anchored at zero;
the hydrogen uses the D-H MIC shift, and the acceptor adds the H-A shift.
The adapter checks the H-A distance against the detector output. The D-H
unwrap supplies display geometry rather than another detection criterion.

One selection gives internal scope; two disjoint eligible universes give
between scope, with both donor/acceptor directions. Identical role selections
and repeated frames do not duplicate sparse observations. Supplied role
arrays, a second structure axis, and partially overlapping universes are
explicitly unsupported by the optional result. The detector remains eager;
chunked calculation and its trajectory-scale image-pass benchmark are open.

The existing tuple output now preserves empty evaluated frames and variable
counts under `uibcdf/molsysmt#253`: equal counts retain rectangular arrays,
while varying counts return aligned lists without padding. Synthetic tests
exercise empty and varying counts, nonconsecutive and repeated frames, scopes,
queries, both selection directions, nm units under an angstrom session, and
PBC image reconstruction in diagonal, triclinic, and rotated orthogonal boxes.
A bundled trajectory is compared with direct H-A distances. H5MSM 0.5
preserves the method, role rules, and coverage. Luzard–Chandler remains open.

Participant checks also reproduced a scientific defect in the shared donor
helper: independent column sorting could detach a hydrogen from its declared
covalent partner. The correction under `uibcdf/molsysmt#258` sorts intact
rows. An interleaved-index fixture checks exact donor-H bonds, the triples
from both existing detectors, and sparse queries for the true hydrogen.
It leaves chemical eligibility rules and geometric criteria unchanged.

## First detector result adapter (2026-09-29)

`interactions.disulfides.get_disulfide_candidates` now accepts optional
`output_type="molsysmt.Interactions"`; its default pair and distance lists
remain unchanged. The result uses original atom and structure indices,
eligible sulfur atoms as its declared internal scope, explicit evaluated
coverage including empty frames, the geometric-candidate evidence label,
nanometer distances, and the method's threshold, group filter, and PBC
parameters. Repeated requested frames are collapsed for this result. The
caller attaches the result to `MolSys.interactions` under an explicit name;
the detector does not mutate the system. A focused H5MSM 0.5 round trip
preserves method and images.

A new private Rust observed-pair pass returns both MIC distance and original-box
integer image for only the pairs emitted by a detector. The disulfide adapter
checks its distance against the neighbour result before recording images.
An independent lattice enumeration tests orthogonal, triclinic, and rotated
orthogonal boxes. The latter revealed and motivated the MIC correction under
`uibcdf/molsysmt#257`. The default neighbour-list result remains unchanged;
the extra pass is not yet benchmarked at trajectory scale. The subsequent
Buch checkpoint above adds its result route; Luzard–Chandler remains open.

## Consumer occurrence identity checkpoint (2026-09-29)

`Interactions.query(...).to_dict()` and the internal selective HDF5 reader
expose `occurrence_indices` as `int64` positions in the complete named
analysis. They distinguish parallel observations with the same structure and
relation, survive filtered views and H5MSM round trips, and require no extra
file column. Remapping or editing creates a new analysis whose positions may
change. The public native/H5MSM and selective-reader tests guard this parity.
MolSysViewer reports five passing focused tests against commit `0d1a2bf0a`
and has begun its Python adapter on the experimental result contract. Its
first real integration test remains pending.

## Public native/H5MSM consumer workflow checkpoint (2026-09-29)

`tests/interactions/test_public_molsys_h5msm_workflow.py` now exercises one
synthetic review fixture through public `Interactions`, named `MolSys`
attachment, `molsysmt.h5msm.write/read`, and selective
`molsysmt.h5msm.read_layers`. It covers hydrogen-bond triples, compound ring
participants, disulfide candidates, parallel observations, variable frame
counts, evaluated-empty and unevaluated frames, repeated and nonconsecutive
structure requests, atom-set modes, `between`, source-index maps, evidence,
nanometer distances, periodic images, extraction, and persistence of an
invalidated structure. The native and H5MSM-loaded query projections are
compared column by column. The corresponding public Cookbook example now
demonstrates an attached result surviving an H5MSM round trip.

This is contract and parity evidence for the tested public path, not
MolSysViewer acceptance or scientific validation of the synthetic records.
The public `read` and `read_layers` APIs materialize selected results; the
indexed HDF5 query reader remains internal. Detector `output_type` adapters,
bounded file-backed consumer queries, a handoff tied to an exact commit,
and the MolSysViewer smoke remain open. A public fixture generator now writes
complete and interaction-only H5MSM 0.5 files and checks representative
queries; see the [review packet](design_a_sparse_public_interactions_result_and_serialization_contract.md#runnable-molsysviewer-review-packet).
The focused interaction/native/public
H5MSM selection passed 57 tests on 2026-09-29; the pre-existing legacy
format warning was emitted in the public H5MSM test selection.
An expanded local selection later that day passed 1,347 tests across H5MSM,
native forms, interactions, `MolSys` adapters, conversion, structure append,
hydrogen bonds, and disulfides. This is checkout evidence, not a release gate
on a published candidate.
For an interaction-only H5MSM 0.5 file with named analyses, public `read`
and `convert(..., to_form="molsysmt.MolSys")` reconstruct a partial native
`MolSys`. The analyses supply the atom and structure index domains; topology,
chemical states, and structures stay absent. A present-empty interaction
layer requires `read_layers` because no analysis declares those domains.
The public H5MSM 0.5 native route now additionally round-trips a partial
`MolSys` containing structures and named interactions without chemical states,
with or without topology. Its reader requires declared identity links for the
interaction atom and structure axes; equal axis sizes alone do not establish
their correspondence. The focused guard is
`tests/form/file_h5msm/test_absent_chemical_states_v05_probe.py`.

The [H5MSM benchmark guide](../benchmarking/h5msm.md) now reports the public
`write_layers`/`read_layers` path beside the private selective reader. In its
synthetic 100,000-atom, 10,000-structure, 15,822-occurrence case, the public
interaction-only file is 235,284 bytes, a repeated `read_layers` takes 0.105 s,
and the loaded one-atom query across all frames takes 36.695 ms median. The
private file reader takes 431.042 ms median for that whole-trajectory atom
query. This is a single dirty-checkout, cache-uncontrolled measurement, not a
performance guarantee or a benchmark of a complete `MolSys` file. Public
file-backed queries, process RSS, and bounded construction remain open.

## Typed dictionary form checkpoint (2026-09-29)

The experimental `molsysmt.Interactions` and
`molsysmt.InteractionsDict` are now registered as Tier 3 forms with a
lossless `msm.convert()` round trip. The dictionary holds versioned NumPy
columns for relations, variable-arity participants, sparse occurrences,
evaluated-frame coverage, compact evidence codes, measurements, units,
method metadata, and optional periodic images. It does not expand each
occurrence into a Python record. The constructor now accepts evidence codes
with a label table so decoding also avoids building one Python string per
occurrence. `Interactions.to_dict()` remains a query projection and must not
be confused with this complete form.

The payload is not JSON-compatible because its columns are NumPy arrays.
The schema and round-trip tests establish an in-memory interchange boundary;
they do not implement the H5MSM 0.5 interaction layer, lazy file-backed
queries or incremental editing. Those remain open. A declared atom-scope
contract was added in the later checkpoint below.

A local warm-path probe with 100,000 occurrences, 1,000 structures, one
two-participant relation, and one `float64` distance column converted the
result to `InteractionsDict` in about 0.002 s. The dictionary's numeric
arrays occupied 2.81 MB; `tracemalloc` observed a 2.81 MB allocation peak
after module imports were warmed. Direct column encoding and decoding took
about 0.001 s and 0.005 s respectively. These measurements test conversion
overhead for a simple relation inventory, not query speed, HDF5 I/O, or
large variable-arity relation sets. Cold-path time was dominated by lazy
module imports and is not used as evidence of the array codec's speed. This
probe predates the source-index map columns added below; rerun it before
using the numbers for a current size claim.

## Native MolSys attachment checkpoint (2026-09-29)

`MolSys.interactions` now accepts a mapping of nonempty analysis names to
complete `Interactions` results whose atom and structure index spaces match
the native system. Copy, atom/structure extraction, and removal produce
independent results. Extraction keeps a relation only if all participant atoms
survive, remaps atom and structure indices, supports repeated selected
structures as distinct output structures, and preserves evaluated-empty
coverage. `Interactions.remap()` exposes the same sparse operation directly.

Appending structures preserves the target's existing observations and leaves
new structures unevaluated. At this checkpoint, adding atoms while either
system carried analyses was rejected; the atom-scope checkpoint below
replaces that rule. Appending a source that already contains analyses
is rejected until an analysis-merge policy is specified. The legacy H5MSM 0.4 and MolSysDict 0.1
export paths now reject a `MolSys` carrying analyses before writing, so they
cannot silently discard them. Focused native and result tests cover these
semantics. H5MSM 0.5 storage and scalable file-backed editing
remain open.

## Source-index map checkpoint (2026-09-29)

Each experimental result now records local-to-source atom and structure index
arrays and the sizes of both source axes. Constructors default to identity
maps; `remap()` composes maps under atom and structure extraction, including
repeated structures. Appended structures receive source index `-1` because
they have no counterpart in the original source. `source_id` remains attached
to that explicit mapping. `InteractionsDict` and the standalone HDF5 codec
round-trip nonidentity maps; older standalone files without map datasets read
as identity maps. Identity maps are implicit in the typed payload and file,
avoiding redundant atom and structure vectors. Contract tests cover these
cases and reject malformed maps.

These maps identify positional correspondence, not semantic equivalence after
the source itself mutates. A source fingerprint or revision check, evaluated
atom-scope semantics, and source-aware query options were open at this
checkpoint. The subsequent scope work addresses atom addition; source
fingerprints and source-aware query options remain open.

## Declared atom search scope checkpoint (2026-09-29)

An `Interactions` analysis now declares one atom search scope shared by all
its evaluated structures. `internal(A)` accepts relations entirely inside A,
`incident(A)` accepts relations touching A, and `between(A, B)` accepts
relations touching each of two disjoint sets. All relation atoms must belong
to a declared universe U. The default is `internal(all local atoms)`. The
constructor validates every relation against the declaration, but the caller
remains responsible for reporting the detector's actual search. Evaluated
and empty means no observed interactions within the declared scope; it makes
no claim about atoms outside U. This is an analysis-level contract, not a
per-structure mask. Analyses with different scopes remain separate named
results.

`remap()` projects U, A, and B alongside relations and coverage. The typed
dictionary and standalone HDF5 formats round-trip the scope, and their
readers default older payloads to full-domain `internal` scope. Adding atoms
to a target `MolSys` with analyses extends the local atom and source-map axes
but freezes each prior search universe; new atoms receive source index `-1`
and are not claimed as evaluated. Adding from a source with its own analyses
still requires a merge policy and is rejected. Focused tests exercise
incident and between scopes, grouped participants, remapping, HDF5 and typed
round trips, and native atom addition. The current representation materializes
an explicit universe atom-index array when a previously full-domain scope is frozen by
atom addition; this memory cost and a possible range encoding need measurement
before claiming large-scale efficiency.

The reproducible
[`benchmark_interactions_scope.py`](../../devtools/scripts/benchmark_interactions_scope.py)
probe used 300,000 atoms, 30,000 structures, one observed pair, and 100
new atoms on this machine. The result's numeric arrays grew from 2,640,100 B
to 7,441,748 B: 2,400,000 B for the frozen universe and approximately
2,400,800 B for the now nonidentity atom source map. The standalone file was
973,174 B. Warm single-run times were 0.092 s construction, 0.168 s atom-axis
extension, 0.072 s save, and 0.172 s full load. These figures isolate sparse
metadata overhead; they do not measure a 30,000-structure coordinate payload
or many simultaneous analyses. A prefix/range representation for the frozen
scope and a compact source-map codec remain candidates if multi-analysis
memory becomes significant.

The public `msm.append_structures` route for a coordinate-only source now
extends attached analyses with unevaluated structures, matching the native
`MolSys.append_structures` behavior. A regression test exercises that form
adapter path. Direct mutation of `molsys.structures` remains an unresolved
ownership boundary.

## Reusable HDF5 group codec checkpoint (2026-09-29)

The standalone file writer and reader now delegate to one private group
codec. It can write the same typed relation, occurrence, coverage, scope,
source-map, evidence, measurement, and periodic-image columns into an HDF5
group. A private collection codec stores named analyses in deterministic
name order under numeric group keys, so names containing `/` or Unicode do
not become HDF5 paths. A present-empty collection stays distinct from an
absent root group. Focused tests store distinct evaluated coverage,
read the analyses independently, and reject unknown per-result or collection
schema versions. The
standalone `.h5i` format still uses that codec at the file root. This is a
preparation for H5MSM 0.5, not an H5MSM integration claim: collection naming,
the four optional root domains, selective reads, migration, and crash-safe
writes remain to be designed and implemented.

The private `interactions._h5msm05` probe can write and read an
interaction-only H5MSM 0.5 file. It distinguishes absent from present-empty
interaction layers and round-trips a result with nonidentity source maps,
restricted atom scope, evaluated-empty coverage, and periodic images. The
existing 0.3/0.4 handler rejects the file as unsupported, so the probe cannot
be mistaken for the current public H5MSM conversion path. Full 0.5 support
still requires topology, chemical-state, and structure layers, MolSys
conversion, selection, and bounded I/O.

An immutable `Interactions.invalidate_structures()` operation now drops
observations in selected local frames and removes those frames from evaluated
coverage without changing the structure axis. Tests cover an observed frame,
an evaluated-empty frame, previous query-view stability, and periodic-image
alignment. This gives a truthful invalidation primitive after structural
changes, but copies the packed columns. It is not the planned local edit
overlay, cannot add new observations, and does not automatically detect an
in-place coordinate mutation through `molsys.structures`.

**Reported:** 2026-09-28, after the user requested a first version to test
the result design in [`uibcdf/molsysmt#251`](design_a_sparse_public_interactions_result_and_serialization_contract.md).
**Status:** Experimental implementation and synthetic benchmarks exist;
consumer and larger-scale validation remain open.

## What

Implement a public but experimental `molsysmt.Interactions` class that can
represent relations involving two, three, four, or more participants, including
group participants such as rings. Test selection by explicit structure lists,
atom-set `incident`/`internal`/`cross`, and interaction between two disjoint
atom sets. Measure query speed and memory on reproducible synthetic trajectories.
The independent class is the first milestone. Before 1.0, integrate the result
with the native `MolSys` lifecycle and H5MSM persistence, and verify the
MolSysViewer client path. Other client integrations may follow after 1.0.

## How

The current prototype in [`result.py`](../../molsysmt/interactions/result.py)
normalizes input records to typed arrays. Relation and participant offsets
encode variable arity and group membership. Occurrences contain structure and
relation IDs, numeric measures and unit metadata, compact evidence codes, and
optional per-participant periodic images. Evaluated structure indices are
stored independently of occurrences, preserving evaluated-empty frames.

The root lazy registry exports `molsysmt.Interactions`. `query` returns a
lightweight view. Single-frame queries use binary search over sorted occurrence
structures; atom queries use lazily constructed atom-to-relation and
relation-to-occurrence inverted indexes. `between(A, B)` requires each relation
to touch both disjoint atom sets; `exclusive=True` requires every constituent
atom to lie in their union. A standalone, versioned HDF5 round trip uses typed
datasets and JSON metadata. It does not alter H5MSM 0.4.

The [contract tests](../../tests/interactions/test_result.py) cover hydrogen
bond triples, two-ring groups, disulfide candidate pairs, a four-participant
relation, nonconsecutive and duplicate frame requests, empty evaluated versus
unevaluated frames, atom-set queries, chained views, periodic images, invalid
indices and missing units, and file round trips. These synthetic inputs check
the container semantics, not scientific detector correctness.

The four `37_Interaction_Networks.ipynb` modules were inspected. They use the
existing hydrogen-bond detector layouts, which this class does not change, so
their examples need no edit for this prototype. User Guide Foundations, Tools,
and Cookbook now describe the independent result and its current limitations.

## Why

Existing hydrogen-bond and disulfide methods return different layouts. A
generic sparse result lets consumers query chemically classified observations
without materializing atom-pair matrices or a Python object per occurrence.
MolSysViewer requested such a result in `uibcdf/molsysviewer#114`; other suite
consumers may need similar queries but have not yet accepted a shared contract.

## What is measured and what is assumed

The command `python devtools/scripts/benchmark_interactions.py` generates
1,000 evaluated structures, 1,000 atoms, 400 reusable relations, and 10,000
synthetic occurrences (ten per structure). It measures construction, the first
atom query including index construction, then 200 frame and 200 atom queries
after indexes are warm. The query numbers are medians and nearest-rank 95th
percentiles of one run, not repeated-run confidence intervals. It also reports
Python-reachable result size with `sys.getsizeof` traversal, numeric array
bytes, and HDF5 file size. It does not measure detector time or hidden
allocator fragmentation.

On 2026-09-28, Linux 7.0.0-28-generic x86_64, Intel Xeon E5-2630 v4,
Python 3.13.14, NumPy 2.4.6, and h5py 3.16.0, a run with the default command
produced:

| Measure | Result |
| --- | ---: |
| Construction | 0.092 s |
| First atom query, including indexes | 0.011 s |
| Reachable result bytes before / after indexes | 405,691 / 508,547 B |
| Numeric bytes after indexes | 492,832 B |
| Frame query median / p95 | 0.077 / 0.104 ms |
| Atom query median / p95 | 0.042 / 0.065 ms |
| Combined query median / p95, four random structures and one atom | 0.195 / 0.228 ms |
| Serialized HDF5 size | 144,672 B |
| Save / load | 0.041 / 0.0093 s |

Additional commands probe scale and relation churn:

| Command | Occurrences / relations | Reachable bytes after indexes | Frame median / atom median | HDF5 bytes |
| --- | ---: | ---: | ---: | ---: |
| `python devtools/scripts/benchmark_interactions.py --frames 10000 --per-frame 10` | 100,000 / 400 | 4,540,575 B | 0.096 / 0.067 ms | 1,026,153 B |
| `python devtools/scripts/benchmark_interactions.py --distinct-relations` | 10,000 / 9,997 | 1,658,683 B | 0.075 / 0.076 ms | 267,637 B |
| `python devtools/scripts/benchmark_interactions.py --frames 10000 --distinct-relations` | 100,000 / 99,707 | 16,470,375 B | 0.098 / 0.411 ms | 2,302,125 B |

These numbers are one local observation, not a release performance guarantee.
Results depend on relation reuse, group size, selected atom degree, file system,
hardware, and NumPy/HDF5 versions. The repository commands supply the exact
synthetic construction and measurement procedure. The distinct-relation case
models changing participant sets but does not model all coordination chemistry.
A prior encoding placed repeated labels in one JSON HDF5 attribute, producing
a 3,787,265-byte attribute for the 99,707-relation case. The current encoding
uses dictionary-coded datasets and leaves a 147-byte metadata attribute. This
reduced that case's file from 6,061,107 to 2,392,181 bytes in that comparison.
The subsequent deterministic relation ordering reduced the measured file to
2,302,125 bytes. These are separate single runs of the same generator.

Steady-state result size understates construction memory. On the same host,
the 100,000-occurrence reused-relation run began at 71.7 MB process RSS and
reached a 260.1 MB high-water mark while Python input records and intermediate
rows existed, although the resulting object was 4.54 MB by reachable-size
traversal. The 99,707-relation run reached about 333.2 MB high-water mark for
a 16.47 MB result. These measurements include the benchmark generator and
Python allocator behavior. A streaming writer is necessary before claiming
bounded peak RAM for large trajectories.

A dense Boolean 1,000-by-1,000 atom-pair matrix over 1,000 frames would
require one billion entries before representing triples or groups; this is an
array-size calculation, not an allocation or benchmark.

## Design review against the requested goals

| Goal | Current evidence | Remaining gap |
| --- | --- | --- |
| Fast queries | Single-frame, atom-across-trajectory, and four-frame-plus-atom queries are submillisecond in the synthetic runs above. The query chooses the smaller candidate side for a combined restriction. | No measured cold file-backed query, high-degree-atom case, large group case, or downstream render workload. The class does not promise a universal latency bound. |
| Low RAM | Steady-state typed arrays and sparse indexes are much smaller than a dense atom-pair representation in the tested cases. | Python record construction and intermediate rows dominate peak RSS. Base occurrence positions duplicate an integer column; adaptive integer widths and streaming construction deserve measurement. |
| Low disk use | Dictionary-coded labels, compressed numeric datasets, explicit coverage, and optional image columns yield 144,672 B for 10,000 reused-relation occurrences and 2,302,125 B for 100,000 mostly unique-relation occurrences. | The codec is standalone; no chunked append writer, lazy load, persisted inverse index, or tuned frame-oriented chunk shape. Compression/size comparisons with alternatives remain unmeasured. |
| H5MSM integration | The standalone schema is typed and versioned. Its metadata attribute stays small. | H5MSM 0.4 has no interactions layer. Its subset extraction materializes and rewrites a `MolSys`, so an added private interaction group would be lost. A format version and remap/invalidation rule must be designed first. |
| Consumer contract | Explicit coverage, source indices, roles, variable arity, ring membership, `incident`/`internal`/`cross`, nonconsecutive ordered frame lists, evidence labels, method/parameters/units, and optional periodic images are present. | No source selection maps or fingerprint, declaration scope, multi-analysis container, detector adapters, file-backed query, chunked write, full self-contained dictionary export, or tested MolSysViewer integration. Other client integrations are later work. |

The intended scale now explicitly includes hundreds of thousands of atoms
and tens of thousands of structures. The experimental `from_records` and
`load` paths materialize the whole result and are not suitable as the only
paths at that scale. The [large-index-space writer control](design_a_sparse_public_interactions_result_and_serialization_contract.md#large-atom-index-space-and-denser-observations)
shows that a blockwise typed file can be constructed with bounded observed
record memory on synthetic cases, but it is not yet a production
`ChunkedExecutor` route or a lazy public `Interactions` reader. Promotion
requires a file-backed, chunked API and sparse persisted atom indexes whose
cost scales with actual observations and participant atoms.

The atom-to-relation and relation-to-occurrence indexes are compressed sparse
relationships implemented with NumPy arrays and offsets. A SciPy CSR matrix
could expose these as an optional projection, but it would not replace the
relation/participant/occurrence schema. A fixed-rank sparse tensor loses the
meaning of variable-arity and group participants unless its axes are relation
IDs rather than atom slots. In-place changes to a CSR sparsity pattern are
expensive, so the edit-layer question remains separate from matrix selection.
The [first numeric-storage comparison](design_a_sparse_public_interactions_result_and_serialization_contract.md#sparse-library-comparison-first-numeric-storage-experiment)
includes NumPy, SciPy, PyData Sparse, PyTorch, and TensorFlow. Its pair-site
skeleton is deliberately narrower than this class's semantic payload, so its
fastest frame slice is not a choice of canonical `Interactions` backend.
The [shared-field layout comparison](design_a_sparse_public_interactions_result_and_serialization_contract.md#layout-comparison-with-shared-semantic-fields)
shows why the current two-level atom index is not universally best: mostly
unique relations make direct atom-to-occurrence postings smaller and faster
for single-atom queries. Counting selected-atom postings against a stored
participant cardinality also makes `internal` and `cross` efficient with a
direct index. The class has not adopted this algorithm or an adaptive index
policy yet.

**Assessment:** the relation/participant/occurrence split is one useful in-memory
candidate, but it is not yet the chosen architecture. Mostly changing relations
raise both dictionary cost and construction RAM. The first shared-field
comparison found an event-native encoding smaller under high relation churn
and a global dictionary smaller under high reuse. The [edit probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#local-edit-experiment)
found that a frame override is much cheaper than rebuilding the trajectory in
its synthetic case, but no production merge or atomic journal exists. A
bounded-memory writer and complete lazy reader are still required. H5MSM
embedding and `MolSys` attachment need explicit lifecycle rules. An
Arrow or Parquet backend would add a dependency and a second persistence
contract; measure it against the existing HDF5 stack before choosing it.
The [file-backed block probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#file-backed-block-experiment)
now measures complete reads through HDF5, indexed by source structure index.
It writes 10,000 structures without retaining all occurrences, but its simple
whole-block reader took 4–6 ms for one structure and 73–437 ms for one atom
across the trajectory, depending on block size. These are exploratory codec
figures, not timings for this public class. Projecting the needed HDF5 columns
improved the complete 500-structure-block query to roughly 2.7–3.0 ms in
the sampled runs. A cache holding every decoded block accelerated warm reads
but retained the trajectory's numeric payload in RAM; a four-block cache had
few hits for scattered requests. A useful bounded cache policy and an
externally built atom index remain open before choosing a disk layout.
The [multilayer graph probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#multilayer-graph-and-temporal-hypergraph-experiment)
also verifies that one graph layer per evaluated structure can preserve the
mixed-arity payload. NetworkX graph objects used far more RAM than the
columnar candidates in the sampled stable and churn trajectories, without a
complete-query speed gain. A graph remains a useful optional analysis view;
this experiment does not close the choice of compact numeric backend.
The [temporal-run probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#temporal-run-indexes-and-a-compiled-query-kernel)
adds a different candidate: relation-major intervals over evaluated structure
ordinals. For long-lived synthetic relations it compressed the incidence index
substantially; for volatile relations it was larger than frame-major CSR.
A standalone Rust kernel made its query much faster than the Python version.
MolSysMT already ships a private PyO3 Rust extension, so native acceleration
would extend the existing build architecture. The probe excludes complete
occurrence fields and parallel observations; it does not decide this class's
storage or whether its internals should be a native PyO3 object.
The [requirements-first baseline](design_a_sparse_public_interactions_result_and_serialization_contract.md#first-full-field-query-baseline)
now checks complete decoded results against an independent record oracle under
stable, churn, mixed, and persistent inputs. It exposes a large `internal` and
`cross` selection cost when relations churn, while source maps, multi-analysis,
edits, and lazy file queries remain unsupported. This is a performance and
contract diagnostic for the experimental class, not an accepted backend choice.
An optional direct atom-to-occurrence posting probe answers the same oracle
queries much faster under churn, with a measured stable-relation memory cost;
the production class still uses its original two-level index.
The [source-map and edit oracle](design_a_sparse_public_interactions_result_and_serialization_contract.md#source-maps-analysis-coverage-and-edit-semantics-probe)
also checks a two-analysis, nonidentity-map fixture after caller-side mapping.
The public class matches each single-analysis projection but still cannot
store the maps, combine method-specific coverage, or apply those edits itself.
The [transactional-row probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#transactional-indexed-row-probe)
checks the same complete single-method queries in a SQLite candidate and
confirms repeated committed local replacements. The
[indexed-file](design_a_sparse_public_interactions_result_and_serialization_contract.md#persisted-index-file-size-comparison),
[reopened-query](design_a_sparse_public_interactions_result_and_serialization_contract.md#process-isolated-file-query-probe), and
[occurrence-native](design_a_sparse_public_interactions_result_and_serialization_contract.md#complete-occurrence-native-hdf5-file)
probes compare complete HDF5 and SQLite files with persisted atom indexes.
They favor global relation descriptors under stable reuse and event-native
descriptors under churn for the measured HDF5 atom queries. OS-cold reads and
bounded writing remain unmeasured, so none selects a production codec.
The [mixed-phase block probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#mixed-phase-adaptive-block-size-probe)
selects global then occurrence-native descriptors on full-field synthetic
inputs, including a transition inside a block. Its small within-block file
savings did not offset repeated HDF5 group metadata. The
[flat-block probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#flat-adaptive-blocks-and-reopened-queries)
cuts ten-block storage to 320,205 B, close to the 313,443 B monolithic global
file, but its whole-touched-block reader trails SQLite for small queries. The
[projected-reader probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#projected-flat-file-read-probe)
reduces sparse atom-query work and passes the same full-record oracle, while
small-result requests still pay for many HDF5 column reads. A
[compact-record control](design_a_sparse_public_interactions_result_and_serialization_contract.md#compact-record-hdf5-control)
halves those calls and improves sampled frame queries, while increasing file
size slightly and leaving SQLite faster on sampled reopened small results.
In an open-reader session the projected HDF5 frame query approached SQLite
under churn, while SQLite kept the faster sampled trajectory-wide atom queries.
The [one-pass writer probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#one-pass-adaptive-block-writer-and-external-atom-posting-sort)
builds the same adaptive flat format from sorted iterators and a temporary
disk-backed atom index. On 10,000 structures it reduced measured peak RSS
growth from about 148 to 21 MiB at a roughly 4% final-file size cost, and
the checked frame and atom queries matched the independent oracle. This is a
probe, not yet the class's construction path or a `ChunkedExecutor` integration.
The [fixed-shape family codec probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#fixed-shape-family-codec-with-complete-payload)
checks complete typed files and finds a selective 10.8% file saving under
10,000-structure churn, but a 0.75% loss under stable reuse. It remains a
possible private codec, not a separate public result type.
The [edit-overlay probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#full-frame-edit-overlay-on-a-flat-snapshot)
passes pending/committed logical visibility, full-frame replacement, and
evaluated-empty oracles; group-per-edit growth and crash recovery remain open.
Cross-block relation IDs and bounded construction are still absent from the
public class.
The [structural-edit probe](design_a_sparse_public_interactions_result_and_serialization_contract.md#structural-and-occurrence-edit-semantics-probe)
checks exact deletion of one parallel observation, addition of a new relation,
physical structure deletion and renumbering, atom deletion with pruning and
renumbering, structure append, and evaluation invalidation against a
plain-record oracle. It uses prototype index maps and an in-memory append
layer; the public class has no mutation API or persisted remapping yet.

## What was refuted

- Method-specific pair matrices cannot represent hydrogen-bond triples or
  ring-group participants without a second representation.
- A Python object per occurrence is unnecessary for this first query contract;
  typed arrays and relation offsets cover the tested cases.
- Eagerly building atom indexes for every single-frame query wasted work.
  The direct frame path was added before measuring.
- Existing ArgDigest `n_atoms` digestion rejects the new classmethod caller.
  The prototype validates its inputs directly. Integrating a truthful
  function/argument contract is open; bypassing validation entirely would be
  unacceptable.

## Scope and exclusions

The current first milestone handles one source-system index space and one analysis
method per object. Input records are an ergonomic construction path, not the
long-term chunked writer. The class does not yet provide lazy file-backed
queries, streaming writes, source-index remapping, detector `output_type`
adapters, declared relationships without frame scope, cross-system joins,
symmetry operators, or H5MSM embedding. It does not infer scientific
interactions from coordinates. Existing detector outputs and `MolSys` behavior
remain unchanged. Selection and extraction of a molecular system do not
automatically transform this independent result; callers must rebuild it with
correct global indices. Inclusion of named interaction datasets in `MolSys`
and H5MSM is required before 1.0, contingent on explicit remapping,
invalidation, and persistence rules. These are subsequent milestones of this
implementation work, not capabilities of the current prototype.

There is no incremental `add` or `remove` API yet. Editing a compact array
currently requires reconstruction of that array and its indexes. Prototype
full-frame overrides and index maps demonstrate local observation edits and
atom/structure deletion without rerunning unaffected geometric detectors.
They are not persisted by this class and do not yet resolve stable handles or
chemical invalidation of surviving assignments.

## Acceptance criteria

Before closing this implementation issue:

1. The public class and file round trip pass contract tests for the scenarios
   above, and its API is classified experimental in the registry.
2. Input validation and source-index semantics are reviewed, including a
   suitable ArgDigest boundary or an explicitly documented temporary exception.
3. User Guide Foundations, Tools, Cookbook, and the relevant Four Paths
   modules are checked for accuracy; doctests and the applicable docs gate pass.
4. The benchmark command is reproducible; larger trajectories and a
   variable-membership scenario establish where memory or latency degrades.
5. Incremental replacement and deletion semantics are fixed with tests for
   one edited structure, an evaluated-empty result, removed atoms, and source
   index remapping. Append/remove/reorder structure cases and the lifetime of
   pre-edit query views are specified. The edit strategy is benchmarked
   against full rebuilding.
6. Remaining design gates and consumer requirements stay linked to #251;
   durable implemented behavior is in
   [`interactions_api.md`](../interactions_api.md), and the issue closes with a
   guard naming the contract-test module.
7. `MolSys` owns optional interaction results and preserves or explicitly
   invalidates them through copy, extract, remove, add, and structure edits.
   Tests cover stale-source prevention, atom and structure remapping, and
   evaluated-empty coverage. The implementation inventories form setters,
   direct structural append, and mutable native arrays; it either controls
   those routes or states and tests a fail-closed ownership rule.
8. A versioned H5MSM interaction layer round-trips attached results, including
   source maps, methods, units, evidence, roles, periodic images, and coverage.
   H5MSM 0.5 separates topology, chemical states, structures, and
   interactions at the root. Files without interactions and legacy 0.4 files
   remain readable; subset writes and reads obey the same remap-or-invalidate
   rule. Bounded reading and writing are measured on a large trajectory. Old
   writers reject 0.5 rather than silently discarding an unknown layer. The
   modular 0.5 handler, file-extract path, and version-specific attribute
   getters are checked together.
9. A MolSysViewer workflow verifies nonconsecutive structure and atom-set
   queries against the attached or H5MSM-loaded result before the 1.0 gate.
   TopoMT, PharmacophoreMT, and DockingMT integration is not a 1.0 condition.

## Dependencies and risks

- A view shares the parent's storage; saving a view is disallowed until a
  remapped subset serialization contract exists.
- `to_dict` returns occurrence columns and relation IDs. Callers use
  `relation(id)` to inspect participants; a fully self-contained columnar
  export is still an open API decision.
- The current HDF5 `load` reads all arrays into memory. File-backed streaming
  and H5MSM inclusion are required subsequent milestones before 1.0.
- Reusing a relation requires the same ordered roles and constituent atoms.
  Variable coordination spheres may create many relation IDs; benchmark this.

## Provenance

The reported runs used the three commands shown above in this repository on
2026-09-28. The script prints CPU model, platform, Python, NumPy and h5py
versions, dataset sizes, timing summary, numeric and reachable object bytes,
and file size.
