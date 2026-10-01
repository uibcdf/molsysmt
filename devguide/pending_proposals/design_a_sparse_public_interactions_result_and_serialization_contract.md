---
summary: Design a sparse public Interactions result and serialization contract
issue: uibcdf/molsysmt#251
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

# Design a sparse public Interactions result and serialization contract

**Reported:** 2026-09-28, after the result-contract request from
`uibcdf/molsysviewer#114` exposed a decision left open by
[`uibcdf/molsysmt#250`](organize_interaction_detection_by_family_before_1_0.md).
**Status:** The comparative evaluation selected a packed sparse implementation
baseline. The experimental public contract, named native attachment and H5MSM
0.5 persistence are implemented under `uibcdf/molsysmt#252`. Consumer
stabilization and exact-candidate release qualification remain open.

## Shared frame validity delivered — 2026-10-01

The delivered invalidation primitive now owns immutable numeric storage and
shares it across independent frame-validity snapshots. Queries exclude invalid
frames without packing all surviving occurrences; explicit full-column access
and interchange remain materialization boundaries. The experimental storage
arrays/mapping are read-only, with input-alias protection. No detector runs
automatically. Repeated invalidation reuses a single base and previously held
views retain their observations.

The measured one-frame invalidation peak is approximately 275 KiB at fixed
10,000 structures with either 100,000 or 1,000,000 observations; twenty retained
edit snapshots peak around 1.8 MiB. These allocations exclude existing shared
storage, coordinate arrays and imports. Full-column materialization remains
linear and is not a streaming writer. The exact evidence and scope belong in
[the implementation record](implement_experimental_sparse_interactions_results_and_queries.md#shared-frame-validity-implementation--2026-10-01).
The class now provides cheap reset, not same-analysis incremental replacement.
Neither the backend ranking nor the versioned persistence schemas changed.

## Local invalidation memory checkpoint — 2026-10-01

The public copying primitive was measured with up to one million observations.
Removing one frame still allocates a nearly complete surviving result: about
85 MiB of new numeric arrays with three periodic image vectors per observation,
and about 145 MiB of additional traced peak allocation in the measured fixture.
Coordinates were not allocated, and this peak is not whole-process RSS. Emptying
all frames is cheaper than retaining most observations. The reproducible
methodology, raw artifact and revised editing acceptance criteria belong in
[the implementation record](implement_experimental_sparse_interactions_results_and_queries.md#invalidation-memory-checkpoint--2026-10-01).

This confirms a limit of the delivered snapshot primitive, not a new backend
ranking. Safe shared storage with local validity and replacement data must be
qualified before claiming efficient repeated edits. Existing writable arrays,
old query snapshots and typed serialization prevent treating shallow sharing
as an already safe solution. No public editing API was added at this checkpoint.

## Controlled chemical-state edit lifecycle — 2026-10-01

Public `msm.set` atom-state and scientific bond-state assignments on native
MolSys, and owner-level `MolSys.chemical_states` replacement, now invalidate
all evaluated frames in every named analysis. This conservative rule does not
infer per-method chemical dependencies. Editing or clearing the frame-to-state
association invalidates only selected frames. Empty selections and bond IDs
preserve analyses. Earlier snapshots, source maps, units and producer metadata
survive; staged invalidation protects allocation failures and uncertain writes.

The concrete stale-evidence defect is tracked by uibcdf/molsysmt#287 and guarded
by `tests/form/molsysmt_MolSys/test_chemistry_edit_interactions.py`. The normative
contract belongs in [Interaction Analysis API](../interactions_api.md). Separate
Topology/ChemicalStates aliases, direct topology replacement, mechanics and raw
data edits require explicit owner invalidation. This extends #285's copying
primitive; it does not implement an observer protocol, scientific recalculation
or an incremental editor. Those broader gates remain open in #251 and #252.

## Current checkpoint — 2026-10-01

The [normative interaction contract](../interactions_api.md) now covers nine
implemented families, descriptive/scientific method selectors with exact profiles,
and detached optional attribution. A named result represents one producer method
and evaluation scope; `MolSys.interactions` is a mapping of names to full sparse
results. It is neither an untyped list nor automatic detector attachment.

Real local MolSysViewer qualification on clean provider commit
`e21f03d9992b87af2cc9285211adee888462be41` passed scientific geometry, index queries,
complete/analysis-only H5MSM and saved-session round trips. An additional public
client guard verifies original Baker–Hubbard bibliography and producer versions,
nonconsecutive queries and evaluated-empty frames without new Ackredit reader
tracking. See [the implementation evidence](implement_experimental_sparse_interactions_results_and_queries.md#consumer-and-attribution-checkpoint--2026-10-01).
This is source-checkout qualification, not certification of a published provider
artifact or a fresh browser/GPU run. The contract remains Experimental.

Incremental editing, bounded public file-backed queries/writing, per-frame search
scopes, arbitrary subsystem embedding and merge policy remain outside the current
supported result API. Historical comparisons and dated checkpoints below retain
their measured premises; earlier pending-contract/adapter statements are superseded
by this checkpoint and the normative guide. Halogen, hydrophobic, metal and
one-/two-water path detectors are implemented experimentally. The latest
provider and consumer qualification scope is recorded in
[the nine-family checkpoint](implement_experimental_sparse_interactions_results_and_queries.md#nine-family-provider-qualification--2026-10-01).
Public native MolSys coordinate and box setters now invalidate attached analyses
in edited structures under uibcdf/molsysmt#285. Direct edits through separate
Structures objects still require explicit owner invalidation; no generic edit
observer or incremental replacement API is implied.

## Earlier checkpoints

**Luzard-Chandler adapter checkpoint, 2026-09-29:** Both hydrogen-bond
methods and disulfide candidates now return optional sparse results. The
new angular result retains D-A distance in nm, H-D-A angle in rad, actual
scope, evaluated-empty frames, method parameters, evidence, software versions,
and donor-anchored D-H/D-A periodic images. Synthetic fixtures check image
reconstruction, nonconsecutive structures, angular rejection, a half-box tie,
and empty/variable counts. A bundled trajectory is compared with direct
distance and angle calculations. The method remains eager and has Buch's
current optional-result scope limits. Its empty/ragged-output defect is
tracked by `uibcdf/molsysmt#259`. MolSysViewer excludes this method from its
initial integration, so this provider work does not add a client blocker.
This checkpoint supersedes earlier pending-adapter statements below.

**Accepted attachment policy, 2026-09-29:** Following another request from
`uibcdf/molsysviewer#114`, the maintainer chose declared correspondence for
the pre-1.0 contract. A writer is responsible for matching the system and
analyses stored together; a caller attaching a separately loaded analysis is
responsible for selecting the correct system and explicitly aligning local
atom and structure axes when they differ. MolSysMT validates typed payloads,
indices, coverage, scope, axis sizes, and declared H5MSM associations. It does
not certify molecular identity from equal dimensions or from `source_id`,
which is an optional caller-supplied label. Existing source maps remain
provenance, not automatic cross-file matching keys. An arbitrary sparse-domain
embedding into a larger system is not provided by today's `remap` API.

Automatic source authentication and content fingerprints remain optional
future work, not release gates. This decision refines earlier fingerprint
and revision proposals below; invalidation after a known geometry or chemistry
change remains required. The current policy is recorded in
[the interaction API contract](../interactions_api.md#associating-analyses-with-a-system).
MolSysViewer accepts this policy after reviewing commit `2e79b5f29` and
reports 27 passing focused tests. It will request a user declaration when
loading an independent file, require explicit alignment when ordering differs,
and treat labels and maps as provenance. It acknowledges the current remap
limit: a subsystem analysis cannot be embedded into a larger target. Its
initial computation workflow uses Buch and disulfide candidates;
Luzard-Chandler is outside that initial client scope. Canvas and session
round trips remain the consumer integration gate.

The client plans three routes to the same named analysis collection:
opening a system with analyses, loading a separate analysis, and requesting
MolSysMT calculation followed by explicit client attachment. Its main API
and UI will own these workflows, with a gradual migration from its addon.
MolSysMT detectors continue returning results without attaching them.
The software-version requirement is implemented in the checkpoint below.
Luzard–Chandler remains MolSysMT work even though it is outside the client's
initial integration scope.

**Calculation-time software provenance, 2026-09-29:** `Interactions.software`
is an optional dictionary of nonempty software names and producer-version
strings. Buch and disulfide adapters capture the MolSysMT version during
calculation. The field survives query projections, remapping, invalidation,
copying, InteractionsDict, standalone HDF5, selective HDF5 projections, and
public H5MSM conversion. It is additive, optional analysis metadata in the
existing schema-1 codecs; it adds no per-occurrence arrays. Readers of older
payloads without the field preserve unknown provenance as `{}` and never
infer the calculation version from the reader's installed package.
`tests/interactions/test_software_provenance.py` uses different producer,
writer, and reader versions to protect that distinction, including empty
evaluated frames and old payloads. This supersedes the earlier open
software-version statements below; the result remains Experimental until
the real MolSysViewer integration gate passes.

Validation for this checkpoint: 95 focused tests passed across
`tests/interactions`, `tests/hbonds`, `tests/form/molsysmt_InteractionsDict`,
and `tests/form/file_h5msm/test_public_h5msm_v05.py`. Four doctests passed in
the result, Buch, and disulfide modules. The runs emitted expected legacy
H5MSM 0.4 deprecation warnings from bundled systems. Dependency validation
passed; no new dependency is introduced.

**Public conversion evidence, 2026-09-29:**
`tests/interactions/test_public_molsys_h5msm_workflow.py::test_public_convert_preserves_multiple_named_analyses_and_sparse_columns`
now checks `MolSys -> msm.convert(..., to_form="file:h5msm") ->
msm.convert(..., to_form="molsysmt.MolSys")` with two named analyses.
The mixed analysis retains roles, compound participants, parallel occurrence
indices, evidence, images, measurement values and units, and nonidentity
source maps. The second analysis has no occurrences and retains its method
parameters, evaluated-empty frames, and restricted atom scope. Scope is
compared through its public semantics because an internal selection equal
to its universe can use an implicit compact representation after remapping.
This is contract evidence for the public persistence route, not origin
authentication or a MolSysViewer session/export acceptance test.

The following focused run passed 29 tests; the result module's two doctests
also passed. Ruff, developer-guide validation, and queue-index checks passed.
Only markdown sources changed in the five affected course notebooks; their
code cells, outputs, and metadata were preserved.

```bash
python -m pytest --receptor=llm \
    tests/interactions/test_public_molsys_h5msm_workflow.py \
    tests/form/file_h5msm/test_public_h5msm_v05.py \
    tests/form/file_h5msm/test_associations_v05_probe.py
python -m pytest --receptor=llm --doctest-modules molsysmt/interactions/result.py
```

**Detector adapter checkpoint, 2026-09-29:** Disulfide candidates and Buch
hydrogen bonds now have optional `Interactions` outputs. The Buch adapter
declares automatic chemical role-selection rules and the actual eligible
participant universe, records evaluated-empty frames, stores H-A distances
in nm, and preserves the D-H/H-A periodic image chain. Synthetic and bundled
trajectory tests protect variable counts, scope, queries, units, and geometry;
the Buch empty-frame defect is resolved under `uibcdf/molsysmt#253`. Supplied
roles, a second structure axis, and partially overlapping participant
universes remain unsupported for its optional result. Luzard–Chandler,
chunked detector execution, and trajectory-scale image-pass measurements
remain open under `uibcdf/molsysmt#250` and `uibcdf/molsysmt#252`.

**Consumer-review preparation, 2026-09-29:**
`tests/interactions/test_public_molsys_h5msm_workflow.py` supplies a runnable
public native/H5MSM parity fixture with the requested pair, triple, compound
ring, parallel-observation, coverage, source-map, image, extraction, and
invalidation cases. The fixture generator below writes two files that a
consumer can open independently. The Cookbook contains a shorter public
H5MSM round trip. This is functional contract evidence, not a complete
large-trajectory or MolSysViewer acceptance claim. The full public file-backed
query route, bounded write/read measurements, MolSysViewer review, and its
integration smoke remain outstanding. Keep the result API Experimental.

**MolSysViewer review response, 2026-09-29:** The client generated both
synthetic H5MSM files, passed the public workflow test, and verified a
nonconsecutive `msm.convert` selection with remapped indices. It accepted the
logical relation/occurrence/query contract for starting `view.interactions`,
and requested three clarifications before freezing that adapter. First,
parallel observations need a public occurrence handle. `to_dict()` now exposes
`occurrence_indices`: `int64` row positions in the complete named analysis.
Filtered views and H5MSM round trips preserve them. A remap, invalidation, or
edit creates a new analysis version and can reassign them. The selective HDF5
reader exposes the same derived positions without a new file column. Second,
the Buch, Luzard–Chandler, and disulfide detectors still need opt-in adapters
that construct `Interactions` with actual method parameters, units, evidence,
role eligibility, evaluated atom scope, and explicit empty-frame coverage.
The existing detectors return no chosen PBC image, so an adapter must obtain
that image from the same geometry calculation before claiming a drawable
periodic observation. The current scope model may need refinement for
overlapping or asymmetric donor/acceptor selections; no adapter should declare
an all-atom search it did not perform. Third, the image convention is now
documented in `devguide/interactions_api.md`: participant vectors are integer
lattice shifts added to coordinates via `vector @ box` with box vectors as
rows, and relative placement uses the first participant as reference. One
vector shifts every atom in a compound participant; internal ring unwrapping
is outside this representation. This is a serialization and display contract,
not evidence that today's detector paths emit correct PBC images.

The client proposes an in-memory named analysis and queries of the visible
frame for MolSysViewer 1.0. Public selective H5MSM queries are not yet a
client blocker; the decision depends on joint coordinate and interaction
measurements. The requested workload matrix is 62 atoms x 5,000 structures,
10,000 x 1,000, and 100,000 x 100, each with empty frames, varying counts,
reused and changing relations, and multiple named analyses. Measure combined
resident and peak memory, first-query/index construction, visible-frame
query, one-atom trajectory query, and serialization time and size. The
100,000 x 10,000 interactions-only case remains a storage stress test, not a
normal viewer coordinate load. No numbers for this new matrix are claimed
yet. MolSysViewer's frame switching, selection, periodic drawing, scene
rebuild, and export remain the experimental integration gate. Later feedback
from TopoMT, PharmacophoreMT, and DockingMT should test the same logical
semantics without holding this client integration.

**Consumer go-ahead, 2026-09-29:** The MolSysViewer developers report that
they verified commit `0d1a2bf0a` against the earlier fixtures and passed five
focused tests. They confirm that public occurrence indices distinguish
parallel observations in the canvas and that the documented image convention
is sufficient to begin their geometry adapter. They will first consume named,
already constructed `molsysmt.Interactions` analyses through the Python API,
then test projection of the visible frame into Mol*, including parallel
observations and periodic images. An interactions-only H5MSM file must be
associated with compatible coordinates and, when relevant, box vectors before
it can be visualized. The client will report real frame switching, selection,
periodic drawing, scene rebuild, and export results before this contract is
considered stable. The reported five tests establish consumer feasibility for
the synthetic contract; they do not complete that integration gate. Public
file-backed queries remain conditional on combined coordinate and analysis
measurements for the Viewer 1.0 workload.

### Runnable MolSysViewer review packet

From a MolSysMT source checkout at the revision supplied with the review:

```bash
python devtools/scripts/create_molsysviewer_interactions_fixture.py /tmp/msm-viewer-review
python -m pytest --receptor=llm tests/interactions/test_public_molsys_h5msm_workflow.py
```

The generator refuses to overwrite either output file. It writes
`molsysviewer_full.h5msm` with topology, chemical states, structures, and a
named `review` analysis, plus `molsysviewer_interactions_only.h5msm` whose
named analysis declares the atom and structure index spaces without the other
layers. Both use H5MSM 0.5. Their observations are synthetic contract examples,
not scientific detections.

The public `molsysmt.Interactions` result contains relation types, variable
participant groups with roles, sparse per-structure occurrences, explicit
evaluated coverage, method and evidence provenance, measurement units,
periodic image vectors, and local-to-source atom and structure index maps.
`query` accepts one or several structure indices and `incident`, `internal`,
or `cross` atom-set semantics; `between` handles two atom sets. Query results
carry structure indices. An evaluated frame with zero occurrences differs
from a frame that has not been evaluated. `MolSys.interactions` owns named
analyses with matching local axes; extraction remaps them. Public
`molsysmt.h5msm.read` reconstructs a native `MolSys` from either generated
file, and `read_layers` can load only the named interaction layer.

The generator checks that a query of `[4, 1, 0, 4, 3]` yields observations in
frames `[4, 4, 0, 0]` and evaluated coverage `[4, 1, 0]`; frame 1 is
evaluated-empty and frame 3 is unevaluated. It also checks a one-atom query,
a ring-to-ring query, units, source maps, and extraction from the
interaction-only `MolSys`. The test above compares the native and H5MSM-loaded
results more fully, including periodic images and invalidation.

Current limits matter to the review: public H5MSM readers materialize the
selected analysis; the selective file reader remains internal. The result has
no incremental add/remove editor. The disulfide candidate detector has an
opt-in `Interactions` output; hydrogen-bond detectors retain only their
method-specific arrays. MolSysViewer accepted the in-memory named-result
route for its initial integration and supplied representative sizes above.

## What

Evaluate a public `molsysmt.Interactions` result interface for chemically
classified interactions across one or many structures. It should expose sparse,
typed data, efficient structure and atom queries, and a versioned serialization
boundary. The logical contract should cover hydrogen bonds, disulfide
candidates, and later interaction families; whether one physical class and
backend can serve every workload remains open. Before 1.0, `MolSys` must be
able to own interaction results and H5MSM must persist them. An individual
`MolSys` may still have no evaluated interactions.

This issue decides the logical result contract and its evidence gates. Subsequent
implementation work must deliver the class, detector adapters, and file codec.

## How

### Candidate public surface

The following is a proposal, not a published signature:

```python
result = msm.Interactions.from_arrays(...)
subset = result.query(
    structure_indices=[12, 2, 12],
    atom_indices=[4, 5, 6],
    mode="incident",  # also "internal" or "cross"
    interaction_types=["hbond"],
)
columns = subset.to_dict()
subset.save("observations.h5i")
on_disk = msm.Interactions.open("observations.h5i")
```

`query` returns an `Interactions` view by default; conversion is explicit.
`to_dict()` returns a documented columnar schema, not one Python object per
occurrence. A NumPy projection can expose fixed-width columns, but a single
ordinary ndarray cannot losslessly encode variable-arity groups, roles,
geometry, metadata, and coverage without object dtype. Detector
`output_type="molsysmt.Interactions"` should initially be opt-in, preserving
current hydrogen-bond and disulfide layouts until their compatibility work is
complete. Exact names, projections, and file-backed view lifetime need review.

### Logical data model

| Layer | Required content | Candidate compact representation |
| --- | --- | --- |
| Source | Atom and structure index spaces, source identity or fingerprint, maps from local selections to original indices. | Typed metadata and integer maps. Public queries use original indices. |
| Analysis | Interaction family, named method, parameters, units, evidence origin, schema version. | Small metadata block per method/configuration. |
| Relations | Stable IDs, kind, directionality, participants, roles, constituent atom indices. | Flat typed arrays and offsets for participants and group membership. |
| Coverage | Explicitly evaluated structures, including those with zero occurrences. | Sorted unique structure indices and aligned occurrence offsets; absence means unevaluated. |
| Occurrences | Structure index, relation ID, aligned measures, optional periodic images, provenance. | Typed columns ordered by structure, relation, then image; optional columns only when used. |

An occurrence is a frame-specific observation. A source declaration with unknown
frame scope must retain `scope=unspecified` and must not silently appear in every
frame query. A separate declaration table or analysis block may represent it;
the normative contract must choose. Inferred S–S candidates retain
`evidence=observed_geometry` and do not imply a topological bond.

Relation identity includes type, ordered roles for directional interactions,
and participant identity. Symmetric pair relations require a canonical ordering
rule. Periodic image vectors belong to the occurrence when the observed copy
or geometry depends on them. Measures declare units such as nanometers or
radians; scores are not implicitly energies.

Participant offsets permit any finite arity: two, three, four, or more
participants without a new class or an `n_atoms ** arity` array. Arity counts
semantic participants, not constituent atoms: two aromatic rings are two
participants even though each contains several atoms. Each method defines its
valid roles, arity, and aligned measures; the container does not claim that a
four-body relation is scientifically meaningful merely because it can store
one. If membership changes across frames, the first model creates a new
relation ID for each distinct participant set. The prototype must measure the
cost of that choice for variable coordination or mediation; occurrence-level
participant offsets are a possible later extension if relation proliferation
proves material.

### Query semantics

`structure_indices` is an explicit selection, including nonconsecutive or
reordered indices. Repeating one index produces one result; output follows the
order of first appearance. With no restriction, only evaluated structures are
returned. Each occurrence exposes its original structure index. Coverage stays
visible so an evaluated empty frame differs from an unevaluated one.

For an atom-index set `S`, membership uses every physical atom in the
participants, including all atoms of a group participant:

- `incident`: at least one participant atom belongs to `S`;
- `internal`: every participant atom belongs to `S`;
- `cross`: `incident` minus `internal`.

The atom set is deduplicated. A single atom follows the same rule. A hydrogen
bond uses donor, hydrogen, and acceptor atoms: selecting only the donor gives
`incident` and `cross`; selecting all three gives `internal`. For a pi–pi
relation, selecting one ring atom gives `incident` and `cross`; `internal`
requires every atom in both rings. Role filters, whole-group matching, and
drawing anchors may be added separately without changing these set rules.
Atom- and type-filtered views retain coverage even when they have no matches.

Result order is deterministic: requested structure order, then canonical
relation order, then image identity. Repeated selections never duplicate
occurrences. Empty results have stable column names, typed zero-length arrays,
and explicit coverage.

### Physical indexes and performance

Frame offsets over a sorted coverage table make one frame's occurrences
addressable without scanning other frames. Atom-to-relation and
relation-to-occurrence inverted indexes support atom queries through a long
trajectory; these may be built lazily or stored. Combined structure/atom
queries should intersect the smaller posting sets. Cold index construction
and warm query cost must be reported separately. The intended cost depends on
relevant relations and occurrences, not every possible atom pair or a full
trajectory scan for each query. No numeric bound is claimed yet.

For the intended upper scale, the target is hundreds of thousands of atoms
and tens of thousands of structures. The cost must track observed occurrences
and participant-atom postings, not the Cartesian product of atoms and
structures. For 300,000 atoms and 30,000 structures, a dense Boolean
atom-pair-by-structure array would contain 2.7 quadrillion cells, or about
2.7 PB even at one byte per cell. The coordinate array alone would be about
108 GB at float32, so an interaction analysis must never require all
coordinates in RAM. In contrast, `int64` offsets for 300,001 atoms and 30,001
structures take about 2.64 MB combined. The hard scale variable is the number
of observations and the sum of distinct participant atoms across them: at a
hypothetical 10,000 three-atom occurrences per structure over 30,000
structures, 300 million occurrences imply 900 million atom postings, about
3.6 GB at four bytes each before any other columns or indexes. These are
arithmetic estimates, not measured detector densities or file sizes.

The physical contract therefore requires chunked construction and bounded
reader caches, persisted sparse atom postings or an equivalent index,
adaptive integer widths with 64-bit global offsets where needed, and
partitioned compaction. A single unbounded in-memory relation dictionary or
one eager `load()` of every occurrence cannot be the required large-system
path. The current experimental `from_records` and `load` methods are eager;
they do not establish this scale. A frame-major logical order remains useful,
while relation descriptors may need global, block-local, or event-native
physical encoding according to churn.

### Competing physical designs

Keep the logical query contract separate from the physical backend. The current
experimental implementation is one candidate, not the reference architecture:

| Candidate | Likely strength | Risk to measure |
| --- | --- | --- |
| Global relation dictionary plus occurrence columns | Repeated atom/role tuples are stored once; a relation has an identity across frames. | If almost every occurrence has different participants, the dictionary, offsets, and inverse indexes may cost more than repeating the atoms. |
| Occurrence-native ragged columns | Simple chunked append and no global relation lookup; naturally handles changing coordination partners. | Repeats stable participant tuples and needs an atom-to-occurrence index for long trajectories. |
| Frame blocks with local dictionaries | Bounds construction and file-backed reads; can compact or replace an edited block. | Shared relation identity and cross-block atom queries need explicit indexes and stable identifiers. |
| Compact base with an edit journal | Small local changes need not rewrite the trajectory. | Query merge, tombstones, consistency, and compaction can outweigh the savings if edits are frequent. |
| Per-structure graph layers or one temporal factor graph | Natural graph-algorithm view and explicit local structure edits. | Many-body roles need incidence nodes; Python graph objects and cross-layer indexes can be expensive. |
| Relation-major temporal runs with a candidate index | Compresses long-lived relations and makes relation lifetimes explicit. | Volatile relations, parallel observations, arbitrary structure gaps, and fast structure queries need extra machinery. |
| Tagged pair, triple, and grouped-participant blocks behind one public interface | Fixed-arity cases can omit repeated ragged offsets and role codes when roles are method-defined. | Cross-family ordering, shared indexing, codec variants, and method-specific assumptions add complexity. |
| Transactional indexed rows as an edit layer | Atomic local replacements and selective disk lookup. | Row and B-tree overhead may dominate the compact scientific payload. |

The physical representation may be adaptive by analysis block or dataset size.
For example, stable hydrogen-bond relations and changing coordination partners
need not pay the same indexing costs. An atom-by-relation or
atom-by-occurrence sparse matrix is a candidate secondary index or projection;
a fixed-rank atom-pair tensor cannot by itself carry all semantic participants,
roles, evidence, and measurements. No SciPy or third-party sparse format is
selected for the canonical payload.
The dated [provisional ranking below](#provisional-ranking-and-revisit-triggers)
separates complete backend candidates from compatible indexes, native kernels,
and file codecs.

### Sparse-library comparison: first numeric-storage experiment

The [reproducible storage probe](../../devtools/scripts/benchmark_interactions_storage.py)
compares five libraries using the **same limited pair-site event skeleton**.
Each event has an integer structure, two integer sites, and a unique integer
event ID. The input has 1,000 sites, 10 events per frame, 10,000 frames, and
100,000 events. The stable case chooses pairs from a pool of 400; the churn
case chooses new pairs from the full site space on each frame. Sites are a
stand-in for atoms and are deliberately unique within each frame. The script
checks returned event IDs for the first, middle, and last frames and times 200
random, warm, single-frame queries. It reports payload array bytes, not total
process memory. The pair tensor shape is `(frames, sites, sites)` or its 2-D
flattening; the NumPy factorized variant uses relation IDs for distinct pairs.

Commands for the two input distributions are:

```bash
python devtools/scripts/benchmark_interactions_storage.py --frames 10000
python devtools/scripts/benchmark_interactions_storage.py --frames 10000 --churn
# Run optional backends when installed in an isolated environment:
python devtools/scripts/benchmark_interactions_storage.py --frames 10000 --pydata --torch
python devtools/scripts/benchmark_interactions_storage.py --frames 10000 --pydata --tensorflow
```

On 2026-09-28, Linux 7.0.0-28-generic x86_64, Intel Xeon E5-2630 v4,
Python 3.13.14, NumPy 2.4.6, SciPy 1.18.0, PyData Sparse 0.19.2, PyTorch
2.14.0+cpu, and TensorFlow CPU 2.21.0, one set of runs produced the following.
The optional backends ran from isolated `/tmp` installs; they are not MolSysMT
dependencies. Times are medians of single-frame queries in milliseconds.

| Pair-site skeleton | Stable payload bytes | Churn payload bytes | Stable native/direct frame query, ms |
| --- | ---: | ---: | ---: |
| NumPy coordinate columns, plus optional frame offsets | 1,600,000 + 80,008 | 1,600,000 + 80,008 | 0.0006 direct |
| NumPy frame offsets + flattened pair + event ID | 840,004 | 840,004 | 0.0006 direct |
| NumPy frame offsets + relation dictionary + IDs | 841,604 | 1,220,600 | 0.0007 direct |
| SciPy CSR, frame by flattened pair | 840,004 | 840,004 | 0.0006 direct buffers |
| PyData Sparse COO, 3-D | 1,600,000 | 1,600,000 | 0.0676 native |
| PyData Sparse GCXS, frame compressed | 840,004 | 840,004 | 11.47 native / 0.0007 direct buffers |
| PyTorch sparse COO, 3-D, plus optional frame offsets | 2,800,000 + 80,008 | 2,800,000 + 80,008 | 0.579 native / 0.0045 direct buffers |
| TensorFlow `SparseTensor`, 3-D | 2,800,000 | 2,800,000 | 0.897 native `sparse.slice` |

The two frame-compressed libraries and the plain NumPy layout have the same
numeric payload size because they use the same integer widths and offsets.
PyTorch and TensorFlow store the three sparse coordinate axes as int64 in this
experiment. The 2-D SciPy and 3-D tensor encodings gain no expressive power
from the million possible site pairs: only the stored events consume payload
bytes. However, all these tensor variants would collapse or otherwise need to
disambiguate two observations at the same coordinates, such as different
methods or periodic images. The test's unique-pair-per-frame input avoids that
problem; it is **not** a full `Interactions` representation. Frame queries
return event IDs only. The factorized pair dictionary saves no bytes for this
minimal two-integer relation because the repeated pair costs one int32 either
way; its potential benefit for roles, groups, and repeated provenance is not
tested by this table. The 0.0006–0.0007 ms direct-buffer numbers are close to
Python timing overhead and cannot establish a reliable ranking among them.

The public APIs matter separately from buffer layout. [SciPy CSR](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_array.html)
is 2-D, supports efficient row slicing, and documents expensive changes to its
sparsity structure. [PyData Sparse GCXS](https://sparse.pydata.org/en/stable/api/GCXS/)
extends compressed axes to higher-rank arrays. Its native `gcxs[f]` was about
11 ms in this probe, while slicing its `indptr`/`data` arrays directly was
submicrosecond; this is an observed workload-specific result, not a general
claim about GCXS indexing. [PyTorch sparse COO](https://docs.pytorch.org/docs/2.14/sparse.html)
supports higher rank and sparse `index_select`, but coalescing duplicate
coordinates sums their values. [TensorFlow `SparseTensor`](https://www.tensorflow.org/guide/sparse_tensor)
also stores coordinates and values; `tf.sparse.slice` selects a contiguous
frame range in this probe. None of these classes natively encodes the required
typed relation/participant/occurrence tables, evidence, units, explicit
evaluated-empty coverage, and source maps in one lossless tensor. They remain
valid adapters, secondary indexes, or analytical projections.

This experiment excludes participant groups, triple and four-body relations,
multiple observations at one pair/frame, atom inverse indexes, arbitrary
nonconsecutive frame lists, zero-count frames, edits, file I/O, construction
peak RAM, and dependency import cost. Those are decisive workloads, so this
table cannot select the final backend. The experimental class in
[`#252`](implement_experimental_sparse_interactions_results_and_queries.md)
tests the full logical schema and reports frame/atom query times and HDF5 size,
but uses one factorized layout and Python record construction. The next
comparison below holds the main semantic fields constant across a factorized
global dictionary, occurrence-native columns, and frame-local dictionaries.

### Layout comparison with shared semantic fields

The [second reproducible probe](../../devtools/scripts/benchmark_interactions_layouts.py)
encodes the same generated observations in three ways: one global relation
dictionary (`global`), one dictionary per 100-frame block (`block`), or one
relation descriptor per occurrence (`event`). Each encoding carries interaction
type, participant roles and grouped atom membership, occurrence evidence,
distance in nanometers, periodic image vectors, identity source maps, and explicit
evaluated-frame coverage. In the block and event encodings, a canonical
relation identity is stored or inferred so repeated relations retain a
cross-frame identity. These are optimized numeric **probes**, not
interchangeable public `Interactions` classes. The code checks sampled records,
HDF5 round trips,
and query equality across the three layouts. It includes four synthetic
families: hydrogen-bond triples, two six-atom rings, disulfide candidate
pairs, and four-body relations.

```bash
python devtools/scripts/benchmark_interactions_layouts.py --frames 10000
python devtools/scripts/benchmark_interactions_layouts.py --frames 10000 --churn
python devtools/scripts/benchmark_interactions_layouts.py --frames 1000 --duplicates
python devtools/scripts/benchmark_interactions_layouts.py --frames 1000 --churn --duplicates
python devtools/scripts/benchmark_interactions_layouts.py --frames 1000 --hot-atom
python devtools/scripts/benchmark_interactions_layouts.py --frames 1000 --churn --hot-atom
```

On the host and versions above, each 10,000-frame command generated 94,255
occurrences over 10,000 structures and 1,000 atoms, with variable frame counts and 589
evaluated empty structures. The stable input reused 400 relations. The churn
input produced 93,962 distinct global relations. The numeric core includes
the common source maps and coverage, but excludes Python container overhead
and optional inverse indexes. HDF5 files use gzip for every nonempty dataset
and exclude inverse indexes. Results are single-run observations:

| Layout | Stable core / HDF5, MB | Churn core / HDF5, MB | Stable relation index, MB | Churn relation index, MB |
| --- | ---: | ---: | ---: | ---: |
| Global dictionary | 2.895 / 1.450 | 6.615 / 2.950 | 0.391 | 2.728 |
| 100-frame dictionaries | 4.467 / 2.041 | 6.999 / 3.089 | 1.288 | 2.731 |
| Event-native descriptors | 6.626 / 2.648 | 6.247 / 2.825 | — | — |

Here `MB` means one million bytes. The global encoding derives canonical
relation IDs from dictionary order. The event-native encoding derives each
occurrence's relation slot from its ordinal and stores only exceptions where a
relation identity repeats rarely; with extensive repetition it stores a full
canonical-ID column. This removes redundant columns while preserving repeated
relation identity. Event-native direct atom-to-occurrence
postings cost 1.986 MB in the stable case and 1.977 MB with churn. The *same*
direct index can be added to the global or block core. Thus storage layout and
inverse-index choice must be evaluated separately. In the stable case, a
global core plus relation index uses about 3.286 MB of numeric arrays; a
global core plus direct atom index uses about 4.881 MB. Under churn, the
event-native core plus direct index uses about 8.224 MB, below global core
plus direct index (8.592 MB) or its two-level relation index (9.343 MB).
These counts exclude temporary builders,
the Python interpreter, metadata object overhead, and disk indexes.

The query comparison makes the index tradeoff concrete. With stable relations,
the global two-level index had median 0.008 ms for one atom across the
trajectory; the direct atom-to-occurrence index took about 0.0007 ms. Under
churn, the two-level atom path took about 0.403 ms while the direct path
remained about 0.0007 ms. Four arbitrary frames cost around 0.006 ms from
memory in all layouts. The 0.0006–0.0007 ms measurements are near timing
overhead; repeated trials and high-degree atoms are needed before treating
their ratio as precise.

An additional **posting-count algorithm** changed the set-query conclusion.
For each selected atom, concatenate its atom-to-relation or atom-to-occurrence
postings; count how many distinct selected atoms contribute to each candidate.
`internal` holds exactly when this count equals that relation's number of
distinct participating atoms; `cross` holds when the count is smaller. The
benchmark compares this with checking every candidate's participant atoms,
and verifies equal `incident`, `internal`, and `cross` results. It stores one
int32 cardinality per relation, costing 1,600 B for the 400-relation stable
global layout or 377,020 B for the 94,255-event churn layout.

With stable relations, a complete-relation `internal` query had median
0.042 ms through the global relation index, and 0.103 ms through the global
core plus direct atom index and counting. The old per-occurrence check on
that direct index took about 3.5 ms. With churn, the event-native direct
index plus counting took about 0.065 ms, versus about 2.4 ms with
per-occurrence checks and about 0.077 ms with a two-level global relation
index plus counting. Thus a relation-level index is **not required** merely
to support efficient set semantics. The direct index plus cardinalities costs
about 8.601 MB with event-native churn data; a global core plus the
two-level relation index and cardinalities costs about 9.718 MB. An adaptive
integer width for cardinalities may lower these figures further, subject to
large-group correctness.
The two additional duplicate runs each included 42 pairs of observations
with the same relation and frame but different image vectors and distances;
their cross-layout queries and HDF5 round trips passed. These storage probes
still use one analysis method, identity source maps, and synthetic geometry.
In the 1,000-frame hot-atom runs, atom 0 belonged to 4,627 stable-case or
4,765 churn-case occurrences. Its two-level global-index query took median
0.171 or 2.568 ms, respectively, while the direct index returned its posting
slice in about 0.0006 ms. The latter measures locating the result, not
processing thousands of returned occurrences. The counted set algorithm
remained below about 0.11 ms median for sampled complete-relation sets in
the churn case. More varied high-degree scenarios and end-to-end result
materialization remain unmeasured.

A warm HDF5 read of the *event-ID slice only* for one selected frame took
roughly 0.009 ms median; the first slice after opening was about 0.13 ms.
The file handle stayed open and the operating-system cache was uncontrolled.
This does not measure a complete lazy result reconstruction, atom queries from
disk, cold physical I/O, or sustained chunked writing. A relation dictionary
per block was more expensive in the stable input, but this flat-file probe
does not yet test replacing a block on disk, so the potential edit advantage
remains open.

**Interim inference:** a global relation dictionary is a good base when
relations repeat; an event-native layout is smaller when almost every
occurrence has a distinct participant set. A direct atom-to-occurrence index
with posting counts is a strong candidate for the general atom and set query
path. A two-level relation index remains attractive when the dictionary is
small and memory matters more than the fastest single-atom lookup. Layout and
index policies can be chosen separately, possibly per analysis block. The
crossing point depends on participant size, reuse, and queried operations,
not one fixed percentage from this generator. This is a direction for the
next prototype, not a settled API or file layout. The atom-remapping,
bounded-memory construction, broader high-degree, and complete file-backed query
gates remain open.

### Local edit experiment

The [edit probe](../../devtools/scripts/benchmark_interactions_edits.py)
starts from the same stable 10,000-frame input. In structure 10 it removes one
observation involving a selected atom and adds a new hydrogen-bond relation.
The tested alternatives are rebuilding the global payload and atom index,
encoding a replacement for that one frame, or encoding its 100-frame block.
The original base remains immutable. A second probe writes each replacement
as an HDF5 journal group, and a 20-version sequence changes one distance value
in each version. It checks selected atom counts against the full rebuild and
checks that an empty replacement frame still has explicit evaluated coverage.

```bash
python devtools/scripts/benchmark_interactions_edits.py --frames 10000
python devtools/scripts/benchmark_interactions_edits.py --frames 10000 --churn
```

On the same host, one stable-input run on 2026-09-28 gave these single-run
figures. Encoding times include the relevant inverse index but exclude the
scientific detection and construction of the edited input record list.

| Operation | In-memory numeric payload + index | Encode time | HDF5 write and growth |
| --- | ---: | ---: | ---: |
| Rebuild all 94,255 occurrences | 2.895 MB core + 1.986 MB direct index | 1.05 s | Rewrite: 0.100 s; final file 1.450 MB |
| Replace structure 10 | 4,464 B core + 4,116 B direct index | 0.0003 s | Append: 0.0052 s; +48,344 B |
| Replace its 100-frame block | 48,808 B core + 24,084 B direct index | 0.0117 s | Append: 0.0070 s; +69,569 B |

The high fixed HDF5 overhead of a one-frame journal entry is visible: a
4.5 KB numeric delta increased the file by about 48 KB. Twenty append-only
versions increased the original file by 941,920 B, while a full rewritten
snapshot of the single edited state was about 1.450 MB. The benchmark did
**not** perform compaction; the snapshot size suggests the potential recovery.
The HDF5 journal entries do not contain the optional atom indexes. A direct
atom-count lookup over the rebuilt object had a median of about 0.0008 ms;
merging the base and one frame override took about 0.0052 ms. The query returns
counts only, not a complete public result view.

This experiment supports a local replacement layer in principle: a new
relation in one frame need not force scientific recalculation of other frames.
It does **not** establish a production mutation design. The HDF5 groups lack
atomic commit and recovery rules, versioned decoding, journal compaction, and
full `incident`/`internal`/`cross` merge semantics. Repeated edits should
replace the current in-memory frame override; an append-only disk history
needs an explicit compaction threshold or bounded reusable slots. Removal of
atoms from the molecular system still requires pruning affected relations and
remapping surviving indices (or invalidating the result) across the base and
every live delta. These operations need contract tests and performance data
before an edit API can be accepted.

### File-backed block experiment

The [file-backed probe](../../devtools/scripts/benchmark_interactions_file_backed.py)
generates evaluated structures one at a time, including zero-observation
structures, and writes groups of 100, 500, or 1,000 structures. It chooses a
global-within-block relation dictionary or an event-native layout from the
numeric payload byte count for that block. Each group stores complete roles,
participant atoms, evidence, distance, periodic images, evaluated coverage,
source **structure indices**, and a local atom index. A root atom-to-block
index narrows atom queries to relevant blocks. Internal occurrence ordinals
are not structure IDs. Relation numbers are local to a block; logical relation
identity across blocks is the complete type/participant/role key, not a global
number. The check compares complete returned records against an independently
regenerated stream, including duplicate observations and nonconsecutive,
repeated structure-index selections.

```bash
python devtools/scripts/benchmark_interactions_file_backed.py --frames 10000 --block-size 100
python devtools/scripts/benchmark_interactions_file_backed.py --frames 10000 --block-size 500
python devtools/scripts/benchmark_interactions_file_backed.py --frames 10000 --block-size 1000
python devtools/scripts/benchmark_interactions_file_backed.py --frames 10000 --block-size 500 --churn
python devtools/scripts/benchmark_interactions_file_backed.py --frames 50000 --block-size 500 --write-only
```

On the same host, one set of runs on 2026-09-28 produced the following
single-run figures for 1,000 atoms. Timed reads keep the file open and use
the operating-system cache; a full frame query reconstructs all semantic
fields, while a full atom query reconstructs every occurrence of that atom
through the trajectory. Each requested block is read in full, without a
decoded-block cache.

| Input and block size | File | Complete structure query, median | Complete atom query, median | Peak RSS during writing |
| --- | ---: | ---: | ---: | ---: |
| Stable, 10,000 structures, 100 | 7.62 MB | 4.47 ms | 437 ms | 96.6 MB |
| Stable, 10,000 structures, 500 | 2.86 MB | 5.25 ms | 115 ms | 84.2 MB |
| Stable, 10,000 structures, 1,000 | 2.26 MB | 6.27 ms | 73 ms | 86.3 MB |
| Churn, 10,000 structures, 500 | 4.82 MB | 6.39 ms | 131 ms | 86.4 MB |

A second read path projects the columns and participant spans needed for one
structure, rather than loading its whole block. On repeated 500-structure
block runs, its complete-structure median was 2.99 ms for stable relations
and 2.69 ms for churn, versus 5.52 and 6.37 ms respectively for the whole-block
reader in those same runs. It still makes several HDF5 dataset calls per
query; the observed improvement is not enough to claim an interactive reader.
The projected path was checked against complete source records, including
empty structures and periodic images. Atom queries still use whole-block reads.

A cache experiment distinguishes repeated HDF5 calls from result assembly.
For the stable 10,000-structure, 500-structure-block input, retaining all 20
decoded blocks required 3.85 MB of numeric arrays plus unmeasured Python
overhead. Warm complete structure queries fell to 0.263 ms and full-trajectory
atom queries to 14.6 ms in one run. A four-block LRU cache gave 5.24 and
108 ms under the same scattered request pattern, with only 6 hits and 94
misses. The full cache is effectively rehydrating the complete result; its
memory grows with the trajectory. A small cache may still help temporally
local viewer requests, but this random-access probe does not establish that.

For a stable 50,000-structure write-only run with 500-structure blocks, the
file was 14.22 MB, the largest block's numeric payload plus index was
198 KB, and process peak RSS was 100.1 MB. The corresponding 10,000-structure
run's largest block was 197 KB. This shows that the encoder does not hold all
occurrence rows in memory, but **does not prove a fixed memory bound**: the
Python atom-to-block accumulator and the synthetic per-structure count array
grow with trajectory length. Writing also builds both candidate encodings
for each block, then discards one. The block choice minimizes numeric core
bytes, not compressed disk bytes or total query cost.

These complete reads are orders of magnitude slower than the previous
0.009 ms partial read of internal occurrence ordinals. Smaller blocks reduce
one-structure latency slightly but repeat HDF5 group/dataset metadata and
increase atom-query time. The simple reader loads every column and descriptor
in each block, even for one result. These timings reject **these uncached
readers** as the final interactive design; they do not reject block-local
storage itself. The next comparison must test bounded decoded-block caches,
flat chunked/extendible datasets, and a more compact indexed read path against
the same complete query contract. The [h5py dataset guide](https://docs.h5py.org/en/stable/high/dataset.html)
documents chunking and resizing; its [SWMR guide](https://docs.h5py.org/en/stable/swmr.html)
also says new groups and datasets cannot be created after switching a writer
into SWMR mode. Thus the group-per-block probe must not be presented as an
already concurrent appendable H5MSM design. No H5MSM integration, atomic
commit, process-independent cold-I/O measurement, nonidentity atom mapping,
or `ChunkedExecutor` integration was tested here.

### Multilayer graph and temporal hypergraph experiment

A graph with one layer per evaluated structure is a useful *logical* reading
of the data. For atom-pair interactions, an atom-to-atom multiedge can identify
parallel observations. Hydrogen bonds, ring-to-ring interactions, and
four-participant examples are hyperedges: flattening them to ordinary
atom-pair edges loses participant grouping and ordered roles. A lossless
graph encoding therefore uses one occurrence node, ordered participant
nodes, and atom nodes in each layer. Node attributes retain interaction type,
evidence, measure, and periodic image; an empty evaluated structure has an
empty layer. Distinct occurrence nodes preserve two observations of the same
participants in one structure. A global factor graph can instead share atom
and relation nodes across structures and connect each occurrence to a
structure node. This factors stable relations but needs explicit source
structure indices, relation identity, and occurrence identity.

The existing compact arrays already encode this factor graph as adjacency
lists with offsets:

| Logical graph traversal | Compact array route |
| --- | --- |
| Structure → occurrences | Evaluated structure indices and `frame_offsets` |
| Occurrence → relation | `occurrence_relations`, or implicit event-native identity |
| Relation → ordered participants | `relation_participant_offsets`, roles |
| Participant → constituent atoms | `participant_atom_offsets`, atom indices |
| Atom → relations/occurrences | Optional inverse postings |

The [graph probe](../../devtools/scripts/benchmark_interactions_graph.py)
compares that encoding with NetworkX 3.6.1 `MultiGraph` instances, one per
structure, and with one shared factor graph. It uses the same mixed-arity
source events and checks complete returned records, including evaluated empty
structures, grouped ring atoms, four-body examples, image vectors, and
parallel observations. Each mode runs in a fresh process and retains the
same generated Python source list. RSS increase above that shared baseline
is approximate allocator-sensitive representation cost, while numeric bytes
include only the columnar payload and direct atom index. Query timings include
reconstructing complete Python tuples and use warm process memory. All values
below are single sequential runs on 2026-09-28 with 1,000 atoms and 1,000
structures; the stable case had 9,361 occurrences and the churn-plus-duplicate
case had 9,403.

```bash
python devtools/scripts/benchmark_interactions_graph.py --mode layers
python devtools/scripts/benchmark_interactions_graph.py --mode shared
python devtools/scripts/benchmark_interactions_graph.py --mode columnar_global
python devtools/scripts/benchmark_interactions_graph.py --mode columnar_event
# Repeat each command with --churn --duplicates for the second distribution.
```

| Input | Representation | RSS increase | Numeric payload + atom index | Build | Complete structure query | Complete atom query |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Stable | Columnar global | 4.63 MB | 0.508 MB | 0.103 s | 0.101 ms | 0.847 ms |
| Stable | Columnar event-native | 6.33 MB | 0.865 MB | 0.109 s | 0.104 ms | 0.835 ms |
| Stable | Shared factor graph | 18.55 MB | — | 0.110 s | 0.142 ms | 1.058 ms |
| Stable | Per-structure graph layers | 72.89 MB | — | 0.381 s | 0.113 ms | 0.927 ms |
| Churn + duplicates | Columnar global | 7.00 MB | 0.861 MB | 0.115 s | 0.105 ms | 0.700 ms |
| Churn + duplicates | Columnar event-native | 6.97 MB | 0.826 MB | 0.109 s | 0.107 ms | 0.690 ms |
| Churn + duplicates | Shared factor graph | 67.18 MB | — | 0.381 s | 0.118 ms | 0.929 ms |
| Churn + duplicates | Per-structure graph layers | 72.35 MB | — | 0.368 s | 0.107 ms | 0.811 ms |

The graph model is expressively adequate and local layer replacement is
conceptually simple, but the Python graph objects did not yield a memory or
query advantage for these workloads. Replacing one layer still requires
updating the atom inverse index; removing atoms must cascade to affected
hyperedges or explicitly invalidate them. A shared graph must remove unused
relation/participant nodes after occurrence edits. Treating a many-body
hyperedge as several pair edges would silently change `incident`, `internal`,
and `cross` semantics. The best current use of a graph is an optional,
explicitly defined view or analysis projection for graph algorithms, with
the compact typed arrays retaining canonical identity and storage. This is
an inference from the measured NetworkX implementation, not a theorem that
all graph backends are slower. A compact numeric graph backend would be very
close to the current offset arrays and should be judged by its additional
algorithms and indexes, not by a different name for the same incidence data.
The probe did not compare disk codecs, `incident`/`internal`/`cross` query
latency, graph algorithms, or update latency; those remain separate gates.
It also uses one synthetic analysis method and identity source-atom mapping.

### Temporal-run indexes and a compiled query kernel

The current random frame generator under-tests persistence of a relation
through adjacent structures. A fourth physical candidate stores, for each
relation, intervals over the **evaluated-structure ordinal** where it is
present, plus a block-level candidate index. Each interval maps its structures
to aligned occurrence measurements; distance, evidence, image, and other
per-occurrence values remain distinct rows. An interval over coverage
ordinals must not imply that source structure indices between two evaluated
indices were examined. If intervals are exposed scientifically as durations,
gaps in source structure indices must split them or have an explicit unknown
state. Multiple observations of one relation in one structure need a separate
multiplicity/exception route; the first probe does not encode them.

The [temporal index probe](../../devtools/scripts/benchmark_interactions_temporal.py)
compares frame-major CSR incidence with relation-major runs. It generates
10,000 evaluated structures, 400 possible relations, approximately 10 active
relations per nonempty structure, and 99,980 occurrences. The first and last
structures are evaluated empty. A survival probability controls temporal
autocorrelation, with new relations filling vacancies. Both formats would
store the same per-occurrence measure arrays, which are excluded from the
figures below. Run start, exclusive end, relation offsets, measure-row starts,
and a packed 100-structure-block candidate bitmap are included in run bytes.
Every frame's relation set and every measure-row permutation were checked.

```bash
python devtools/scripts/benchmark_interactions_temporal.py --survival 0.0 --rust
python devtools/scripts/benchmark_interactions_temporal.py --survival 0.5 --rust
python devtools/scripts/benchmark_interactions_temporal.py --survival 0.95 --rust
python devtools/scripts/benchmark_interactions_temporal.py --survival 0.995 --rust
```

The optional `--rust` command compiles a standalone
[Rust query kernel](../../devtools/scripts/interactions_temporal_kernel.rs)
using the existing toolchain and calls it through `ctypes`. It does not modify
the production extension and is not a PyO3 or H5MSM performance claim. The
measurements below are single warm runs on 2026-09-28; structure queries
return relation indices and aligned measure-row indices, not fully decoded
public results.

| Survival | Runs | Frame-major index | Run index | CSR structure slice | Rust via `ctypes` |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.000 | 97,472 | 440 KB | 1,176 KB | 0.0006 ms | 0.0229 ms |
| 0.500 | 49,295 | 440 KB | 598 KB | 0.0006 ms | 0.0171 ms |
| 0.950 | 4,869 | 440 KB | 65 KB | 0.0006 ms | 0.0072 ms |
| 0.995 | 459 | 440 KB | 12 KB | 0.0007 ms | 0.0056 ms |

For a 100-index nonconsecutive structure request at survival 0.95, a later
run gave median 0.061 ms for 100 Python CSR slices, 0.683 ms for 100 separate
Rust/`ctypes` calls, and 0.207 ms for one Rust batch call. The batch preserves
first-appearance order and removes repeated requested indices; its returned
offsets delimit each structure's relation and measure-row arrays. This
demonstrates why a compiled design needs batch APIs and why compiling the
run lookup alone does not automatically beat a simple CSR slice.

The probe also writes both indexes as versioned, typed HDF5 datasets with
explicit evaluated structure indices and checks round trips. With gzip and
shuffle, the **index-only** files at survival 0.95 were 40.1 KB (frame-major)
and 49.4 KB (runs); at survival 0.995 they were 21.0 and 28.1 KB. Adding
the same random distance and evidence arrays in each layout gave 761/771 KB
and 742/750 KB respectively. The repeated frame-major relation sequence
compressed so well that the smaller uncompressed run index did **not** yield
a smaller file in these two cases. Dataset metadata and measure order also
matter. This HDF5 probe remains an index-and-two-measure skeleton, not a
complete Interactions codec or a change to H5MSM.

This is a genuine memory/speed tradeoff. Long-lived relations make temporal
runs 7–36 times smaller than the frame-major incidence index, while rapidly
changing relations make runs about 2.7 times larger. The compiled run query is
much faster than Python/NumPy run search in this probe, yet a direct CSR slice
remains faster for one structure. A relation-major atom query, full semantic
materialization, multiplicity,
mixed stable/churn phases, and disk access still need tests. A two-axis
adaptive layout is therefore a candidate: use runs for persistent relations,
frame-major postings for volatile relations, and an explicit merge order. Its
extra index and branch complexity must be counted before acceptance.

Native acceleration is particularly plausible here because MolSysMT already
ships the private Rust `molsysmt._rust` extension through PyO3,
`setuptools-rust`, and `cp311-abi3` wheels; its maintained policy has no JIT
or Python kernel fallback. The public `molsysmt.Interactions` could remain a
Python facade over typed NumPy arrays with private Rust query functions, or a
private PyO3 class could own compiled indexes and expose batch methods. Both
choices must test ownership, copying, validation, packaging, and public-result
materialization. A C backend would add a second native implementation stack
without a demonstrated advantage. Compilation should accelerate a selected
algorithm; it does not determine the logical schema or the serialized form.

### Complete-payload temporal-run control

The [complete temporal control](../../devtools/scripts/benchmark_interactions_temporal_complete.py)
retests runs on the full-field synthetic contract fixture. It encodes runs over
evaluated-structure ordinals, records exceptions for parallel observations,
and keeps relation-major occurrence payload rows. The comparison includes
500 atoms; hydrogen-bond triples, two-ring groups, disulfide candidates, and
four-body relations; evidence, distance and angle measures, periodic image
vectors, explicit evaluated-empty frames, and atom postings. Both HDF5 files
hold the same labels, method/source metadata, coverage, relation descriptors,
and complete observations. The frame-major file stores frame offsets plus
per-occurrence structure and relation IDs; the temporal file replaces those
with run offsets, bounds, payload offsets, multiplicity exceptions, and a
packed relation candidate bitmap per 100 evaluated structures. Occurrence
payload and atom postings are permuted into relation-major order. Readback
checks every stored typed array; the permutation is checked for all aligned
occurrence fields, images, and atom postings. A plain-record oracle checks
204 sampled structure queries including empty and unevaluated frames.

```bash
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 1000 --distribution persistent --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 1000 --distribution stable --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 1000 --distribution mixed --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 1000 --distribution churn --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 10000 --distribution persistent --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 10000 --distribution stable --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 10000 --distribution mixed --file-probe
python devtools/scripts/benchmark_interactions_temporal_complete.py --frames 10000 --distribution churn --file-probe
```

**Benchmarked, 2026-09-28:** Linux, Intel Xeon E5-2630 v4 at 2.20 GHz,
Python 3.13.14, NumPy 2.4.6, h5py 3.16.0. Files use gzip without shuffle;
the two candidates use the same HDF5 settings. Each row is one process run;
timings are medians of 204 seeded queries in a warm process, without a separate
warm-up or confidence interval. All rows have eight nominal observations per
evaluated frame; evaluated frames are about 96.5% of all frames. `stable`
reuses a 120-relation pool without sustained presence; `persistent` retains
active relations with probability 0.95; `mixed` switches from stable to churn
halfway through; `churn` generates mostly new relations.

| Structures / distribution | Relations / runs | Raw frame / temporal index | Complete HDF5 frame / temporal | Median complete frame query, frame / temporal |
| --- | ---: | ---: | ---: | ---: |
| 1,000 / persistent | 120 / 1,224 | 124,712 / 30,742 B | 243,085 / 246,869 B | 0.229 / 0.594 ms |
| 1,000 / stable | 120 / 6,827 | 124,712 / 165,214 B | 257,137 / 283,310 B | 0.223 / 0.787 ms |
| 1,000 / mixed | 3,655 / 7,045 | 124,712 / 203,146 B | 321,015 / 365,994 B | 0.208 / 1.162 ms |
| 1,000 / churn | 6,946 / 7,262 | 124,712 / 238,810 B | 378,104 / 435,581 B | 0.197 / 2.456 ms |
| 10,000 / persistent | 120 / 12,296 | 1,247,704 / 299,887 B | 1,884,659 / 1,802,661 B | 0.211 / 0.604 ms |
| 10,000 / stable | 120 / 68,122 | 1,247,704 / 1,639,711 B | 2,043,547 / 2,135,067 B | 0.204 / 0.795 ms |
| 10,000 / mixed | 33,469 / 70,419 | 1,247,704 / 2,366,032 B | 2,634,035 / 3,042,266 B | 0.196 / 0.959 ms |
| 10,000 / churn | 66,053 / 72,667 | 1,247,704 / 3,075,801 B | 3,215,951 / 3,904,293 B | 0.200 / 2.733 ms |

The raw index comparison excludes common payload, relation descriptors,
coverage, atom postings, HDF5 metadata, and the probe-only row-permutation
map. A real temporal file does not need that map because it physically
reorders payload rows, as the file-size control does. At 10,000 persistent
structures, the run index is about 76% smaller in raw numeric bytes, but the
complete compressed file saves only 4.35%. At 1,000 persistent structures it
is 1.56% larger. Mixed and churn inputs enlarge the complete file by 15.5%
and 21.4% respectively at 10,000 structures. Reusing relation identities
without temporal persistence is insufficient for interval compression.

The timed temporal lookup is a Python per-candidate-relation reference
implementation. Both timed complete-result paths materialize from the same
in-memory frame-major `Interactions` arrays after selecting positions; they
are **not** HDF5 read timings or a compiled relation-major reader benchmark.
The temporal path pays for candidate lookup and permutation, but does not
measure scattered reads from a relation-major file. These timings cannot set
a lower bound on an optimized native run kernel. They do show that the tested
implementation does not win frame requests, even in the persistent case.
An atom query through a persisted temporal file, long-run relation-history
queries, local edits to runs, and a mixed frame/run adaptive file remain
unmeasured. On present complete-file evidence, temporal runs are justified as
an optional codec/index for demonstrated persistence, not the universal
canonical incidence layout.

### Warm file-backed temporal queries and a bundled trajectory

The [file-query control](../../devtools/scripts/benchmark_interactions_temporal_file_queries.py)
reopens both complete HDF5 files and decodes every field needed to reconstruct
the requested observations. It checks 44 sampled frame requests and ten atom
requests against independent plain records, including empty/unevaluated
frames, roles, measures, evidence, and periodic image vectors. Each reader
loads the common relation descriptors and labels on opening. The frame-major
reader loads frame and atom offsets; the temporal reader loads its run arrays
and atom offsets. Both read selected occurrence payload from HDF5. Neither
loads the whole occurrence payload. The raw cache figures below omit Python
relation objects and HDF5 library caches, so they are not RSS comparisons.

```bash
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 1000 --distribution persistent
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 1000 --distribution stable
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 1000 --distribution mixed
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 1000 --distribution churn
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 10000 --distribution persistent
python devtools/scripts/benchmark_interactions_temporal_file_queries.py --frames 10000 --distribution mixed
```

**Benchmarked, 2026-09-29:** same Linux/Xeon/Python/NumPy/h5py environment as
the preceding control. One warm-process sample per case, no independent OS
cold start or repeated-run confidence interval. The table gives medians in
milliseconds for complete decoded queries, frame-major / temporal, with the
reader already open and its index cache built.

| Structures / distribution | One frame | One atom across trajectory | Raw index + coverage cache, frame / temporal |
| --- | ---: | ---: | ---: |
| 1,000 / persistent | 1.86 / 3.27 | 5.13 / 2.43 | 19,736 / 42,470 B |
| 1,000 / stable | 2.05 / 3.76 | 7.16 / 3.11 | 19,736 / 176,942 B |
| 1,000 / mixed | 2.03 / 4.53 | 7.67 / 5.67 | 19,736 / 214,874 B |
| 1,000 / churn | 2.07 / 5.51 | 7.14 / 5.88 | 19,736 / 250,538 B |
| 10,000 / persistent | 2.19 / 5.43 | 38.10 / 12.86 | 161,256 / 381,135 B |
| 10,000 / mixed | 2.14 / 6.46 | 40.98 / 34.48 | 161,256 / 2,447,280 B |

The temporal reader wins these atom-history requests, especially when
relations persist, because relation-major payload rows cluster observations
for an atom. Its frame lookup loses in every measured synthetic case. The
sampled atom set includes the two highest-degree atoms and eight seeded
random atoms. This is a **reader-strategy result**, not proof of an intrinsic
temporal advantage: a projected frame-major reader can use different gather,
span, block, and cache strategies. The temporal reader eagerly loads all run
arrays and all relation descriptors; the mixed 10,000-frame raw run/coverage
cache is about 15 times the frame-major cache before Python objects. This
study does not measure independent-process cold reads, bounded relation
descriptor caches, compiled batch lookup, or edit cost in either file.

The [bundled-trajectory control](../../devtools/scripts/benchmark_interactions_real_hbonds.py)
uses the 5,000-structure, 62-atom pentalanine H5MSM file. It applies the Buch
donor/acceptor helper and 0.23 nm hydrogen-to-acceptor neighbor criterion in
100-structure blocks with `pbc=False`, excluding the same donor/acceptor atom.
This is an adapter around the geometric core because the public Buch detector
currently raises on evaluated-empty structures; see `uibcdf/molsysmt#253`.
It creates full typed records with source indices, explicit coverage, roles,
distance units, evidence, and zero periodic image vectors. It verifies 198
sampled frames against the records, a nonconsecutive duplicate frame request,
and real atom-set `incident`/`internal`/`cross` counts. The HDF5 files and
file-backed frame/atom queries pass the same full-field checks as the
synthetic control.

```bash
python devtools/scripts/benchmark_interactions_real_hbonds.py --frames 5000 --block-size 100
```

**Benchmarked, 2026-09-29:** the same host and dependency versions. The run
found 2,241 occurrences, 33 relations, 1,903 temporal runs, and 3,260
evaluated-empty frames. The raw index was 75,864 B frame-major versus
46,202 B temporal, yet the complete compressed HDF5 file was 97,444 B
frame-major versus 109,216 B temporal (**12.08% larger**). Warm complete
file-backed frame medians were 0.737 / 0.762 ms and atom medians 5.527 /
3.182 ms, frame-major / temporal. The raw index-and-coverage caches were
80,512 / 86,706 B, excluding shared relation descriptors and Python objects.
The first 100 frames alone have 61 evaluated-empty frames; this is a genuine
sparse detector distribution, unlike a fixed-count synthetic fixture. It is
only one small molecule and one method, so it cannot establish the prevalence
of temporal persistence in larger proteins or other interaction families.

The stronger atom-history result keeps relation-major projections in scope.
The combination of slower structure requests, greater complete-file size on
this trajectory, and a more expensive run cache still favors frame-major
occurrences as the common snapshot. An optional relation-major secondary
index or selected persistent block may capture the atom-history benefit, but
its additional bytes and edit maintenance must be measured before adoption.

### Multiple analyses: result collection and grouped storage

The [multi-analysis control](../../devtools/scripts/benchmark_interactions_multi_analysis.py)
splits one full-field mixed fixture into four method-specific results:
hydrogen bonds, ring pairs, disulfide candidates, and four-body relations.
The disulfide method evaluates only even covered structures, while the other
methods evaluate every covered structure. Each result retains its own method,
parameters, evidence, units, and evaluated coverage. Structure and atom
queries of the four-result collection match independent records; standalone
save/load round trips also pass. The file probe adds explicit identity source
atom and structure maps to each separate file, then copies the four typed
analysis groups into one HDF5 container with the source maps stored once.
Every copied dataset and shared map is checked on readback.

```bash
python devtools/scripts/benchmark_interactions_multi_analysis.py --frames 1000
python devtools/scripts/benchmark_interactions_multi_analysis.py --frames 10000
```

**Benchmarked, 2026-09-29:** same Linux/Xeon/Python/NumPy/h5py host, one
synthetic mixed fixture and one run per size. Four separate files totaled
407,211 B at 1,000 structures and 1,951,322 B at 10,000; the grouped file
used 355,341 B (**12.74% less**) and 1,861,009 B (**4.63% less**),
respectively. A warm in-memory query across all four result objects took
about 0.51/0.54 ms for one sampled frame and 0.51/1.62 ms for one sampled
atom at 1,000/10,000 structures. Those query timings do not compare a
combined public object; no such object or grouped-file loader exists.

The shared file offers a real but modest storage benefit, especially for
small analyses with repeated source maps and file metadata. It does not
require merging methods into one `Interactions` object. A collection of
single-method results already preserves distinct coverage and provenance,
and a future H5MSM or standalone container can group their files while
sharing source maps. A public multi-analysis object needs a client operation
that this collection cannot express efficiently, plus a tested cross-method
query and edit contract. This probe does not establish that need.

An illustrative **versioned, typed** persistence boundary for run-coded
analysis would contain source atom and structure index maps, explicit coverage,
relation participant/role arrays, relation-to-run offsets, run start/length and
measure-row offsets, occurrence measure/evidence/image columns, and optional
atom/block indexes and multiplicity exceptions. Integer widths, units,
method parameters, provenance, periodic images, and schema version belong in
the contract. HDF5 datasets can hold those arrays; no Rust `Vec` memory image,
Python pickle, or native pointer is a file format. Normative H5MSM 0.4 has
no interactions layer. H5MSM 0.5 is now the accepted pre-1.0 container target:
the standalone typed codec tests round trips first, then its payload must be
integrated with the modular 0.5 reader and writer before 1.0.

Two other candidates deserve bounded experiments rather than adoption by
analogy. SQLite's indexed tables and transaction log may suit a mutable edit
layer, at a likely row/index-space cost that must be measured; see its
[WAL contract](https://www.sqlite.org/wal.html). Arrow IPC offers typed,
memory-mappable columnar batches and nested arrays, but would add a sizeable
dependency and a second file contract; see its
[Python IO guide](https://arrow.apache.org/cookbook/py/io.html). Compressed
bitmaps such as [Roaring](https://github.com/RoaringBitmap/RoaringFormatSpec)
could index relation presence or atom postings, with the same need to preserve
roles and per-occurrence values elsewhere. These have not been benchmarked
against the complete interaction payload.

### Provisional ranking and revisit triggers

**Dated assessment, 2026-09-28.** This ranking selects a baseline for the next
implementation, not a claim that the final public contract or every optional
codec is settled. Eligibility requires lossless
mixed-arity participants and roles, parallel observations, evidence and
measure columns, original atom and structure **indices**, evaluated-empty
coverage, and a typed versioned serialization boundary. Among eligible
designs, judge complete structure and atom/set query latency, steady and peak
RAM, disk bytes, local edit and compaction cost, then implementation and
dependency cost. A fast pair-only index cannot win by omitting the rest of the
contract. Ranks 1 and 2 have the most comparable full-field storage evidence.
Ranks 3 and 4 are now selective codec/index candidates; rank 5 is a possible
transactional edit or query sidecar. Rank 6 may use any suitable snapshot
layout rather than compete as an exclusive codec. The exact order of these
less-measured candidates is tentative. "Park" means remove from the
**canonical-core shortlist now**, not prohibit it as a view or index.

| Rank | Design or experiment | Provisional disposition and evidence | What would change the ranking |
| ---: | --- | --- | --- |
| 1 | Global relation dictionary, frame-major occurrence columns, direct atom postings, and bounded local frame overrides | **Finalist; measured baseline.** Best tested core for recurring relations: 2.895 MB RAM arrays / 1.450 MB HDF5 on the 10,000-frame stable input. Structure slices and atom postings are direct. A single-frame override encoded in about 0.0003 s. Churn increases core to 6.615 MB; the edit journal lacks production recovery. | A complete mixed-workload comparison shows adaptive or native storage wins enough to justify extra complexity, or global relation churn becomes routine. |
| 2 | Adaptive frame-major columnar blocks: choose global, local, or occurrence-native descriptors per analysis block, with direct postings and bounded edit overlays | **Finalist; partial prototype.** Event-native core is 6.247 MB versus global 6.615 MB under near-total churn, while global is 2.895 MB versus event-native 6.626 MB with stable relations. A complete indexed HDF5 occurrence-native file was 359,555 B versus 372,147 B for global descriptors under churn and improved high-degree atom reads; under stable reuse it was 325,375 B versus 251,076 B and slower. A full-field mixed-phase block probe selected global then event descriptors correctly. Flattening ten blocks cut its file from 655,041 to 320,205 B, near the 313,443 B monolithic global file. A projected reader passes the record oracle and speeds sparse atom queries, but still makes 11–13 HDF5 column reads per touched block. A compact-record HDF5 variant halves those calls and improves small queries at a 6% mixed-file cost, yet SQLite remains about four times faster for sampled reopened nonempty frames. A one-pass block writer with disk-backed atom-posting sort cut 10,000-frame peak RSS growth from about 148 to 21 MiB at a 4% final-file cost, with similar build time in one run. Full-frame overrides pass a local edit oracle, yet per-edit HDF5 groups grow quickly and the marker is not crash recovery. Cross-block numeric relation identity is absent. | Generalize the bounded writer through `ChunkedExecutor`, preserve cross-block relation identity, and demonstrate client-fast queries plus a recoverable compact edit journal; otherwise the extra format branches lose their case. |
| 3 | Specialized fixed-arity pair/triple/group descriptor columns behind one logical interface | **Exploratory finalist as a selective codec.** A complete single-block HDF5 file with all occurrence fields, coverage, atom postings, family role schema, and relation maps passed readback checks. At 10,000 structures the specialized file saved 10.8% under churn and 6.2% on mixed input, but was 0.75% larger under stable reuse. Full-load times were similar. This synthetic fixture has only four fixed-shape families; variable-length groups, mixed-family query latency, and a bounded writer are untested. | A client-relevant workload retains the file/RAM gain after variable groups, query dispatch, and streaming construction, without making the common stable case worse. |
| 4 | Frame-major incidence for volatile relations and relation-major temporal runs for persistent relations, with a structure candidate index, direct atom postings, and edit overlays | **Selective codec/index candidate, no universal-core case.** The full-field temporal control preserves parallel observations. On the real pentalanine trajectory the temporal file is 12.08% larger and warm frame reads are similar, but atom-history reads are 3.18 versus 5.53 ms; synthetic persistent atom reads also favor temporal. Synthetic mixed/churn files grow 15.5%/21.4% at 10,000 frames and frame queries lose. The temporal run cache can be much larger. Mixed frame/run dispatch, cold reads, and edits remain untested. | Multiple real detector workloads and a bounded-cache hybrid win complete frame and atom requests, RAM, disk, and edits after merge costs. |
| 5 | Indexed transactional rows, for example SQLite, as the whole canonical object | **Exploratory finalist; partial full-field probe.** A single-method SQLite schema passed the record oracle and repeated local edits. With atom and structure indexes persisted in both candidates, SQLite used 1.86–2.20 MB versus 0.25–0.37 MB for the indexed HDF5 snapshot on these fixtures. SQLite wins the tested small-result file queries and keeps repeated full-frame edits near constant file size; HDF5 block batching approaches or beats its high-degree atom query while retaining a smaller snapshot. Block-local descriptors, bounded construction, source maps, and multiple analyses remain untested. | A complete indexed-row prototype wins repeated edits and file-backed queries within the same RAM/disk and schema limits. |
| 6 | Mutable indexed native store or builder, with typed columnar snapshots and the same logical query/codec contract | **Cross-cutting editing/runtime branch; unmeasured as a complete backend.** The local-delta probe shows why updates matter, and a Rust kernel shows compiled lookup is feasible, but neither establishes a PyO3 object with compact ownership, fast batch queries, bounded disk writes, or safe mutation views. It may use rank 1 or 2 as its snapshot layout. | A complete PyO3 prototype beats their edit layer on repeated edits without losing frame/atom query speed, RAM, serialization fidelity, or wheel compatibility. |
| 7 | Occurrence-native descriptors everywhere | **Park as universal layout; retain inside rank 2.** It wins the near-total-churn numeric core (6.247 MB) but repeats stable descriptors (6.626 MB versus global 2.895 MB). The complete indexed file is about 3% smaller under churn but about 30% larger under stable reuse; its best tested page size improved churn atom queries but lost stable ones. | Representative detector output has predominantly unique relations, including grouped roles and all metadata, with no large stable phase. |
| 8 | Fixed-size frame-local dictionaries everywhere | **Park as universal layout; retain inside rank 2.** The 100-frame stable core was 4.467 MB versus global 2.895 MB. HDF5 block size changes file size and atom-query time substantially; local edits remain a possible strength. | Complete local edits and bounded file-backed queries offset dictionary repetition and block metadata on realistic trajectories. |
| 9 | Relation-major temporal runs as the only incidence index | **Park; retain the selective version at rank 4.** The complete temporal file saves 4.35% only on the tested 10,000-frame persistent synthetic input. It costs 12.08% more on the bundled sparse trajectory and 4.5–21.4% more on other 10,000-frame synthetic inputs. Warm atom-history reads can improve, but frame reads lose and the run cache grows. | Strong, sustained persistence and relation-history requests dominate real client work; a bounded compiled reader and editor win the complete cost. |
| 10 | SciPy CSR as the sole domain object | **Park as canonical; retain as an index/projection.** The frame-compressed pair skeleton used 840,004 bytes, essentially the same as direct NumPy buffers. Its two axes and data values do not alone encode hyperedges, parallel observations, provenance, and coverage. | Sparse algebra becomes a dominant client operation and a full-contract wrapper beats the same buffers end to end. |
| 11 | PyData Sparse GCXS as the sole domain object | **Park as canonical; retain as a possible index/projection.** The compressed pair skeleton also used 840,004 bytes; native frame selection took 11.47 ms versus about 0.0007 ms for direct buffer slicing in this probe. | Its native higher-rank operations save enough client work to offset wrapping the complete interaction schema and the dependency. |
| 12 | PyData Sparse COO as the sole domain object | **Park as canonical; retain explicit tensor projections.** The pair skeleton used 1.6 MB and native single-frame selection took 0.0676 ms. Pair coordinates still need a separate occurrence/role schema. | A complete typed schema with duplicate-coordinate support shows an end-to-end advantage over compressed columns. |
| 13 | PyTorch sparse COO as the sole domain object | **Park as canonical; retain explicit tensor projections.** The pair skeleton used 2.8 MB; native frame selection took 0.579 ms. Coalescing duplicate coordinates changes their values, so occurrence identity requires another layer. | Tensor-native client computation dominates and a lossless full-contract adapter justifies the dependency. |
| 14 | TensorFlow `SparseTensor` as the sole domain object | **Park as canonical; retain explicit tensor projections.** The pair skeleton used 2.8 MB; native `sparse.slice` took 0.897 ms. Roles, grouped participants, and duplicate observations require a separate schema. | Tensor-native client computation dominates and a lossless full-contract adapter justifies the dependency. |
| 15 | One shared NetworkX factor graph | **Park as canonical; retain graph-algorithm views.** For 1,000 stable frames, it added about 18.55 MB RSS versus 4.63 MB for columnar global storage, without a query-speed win. | Graph algorithms or edits dominate, and a compact graph implementation wins on the complete contract. |
| 16 | One NetworkX graph layer per structure | **Park as canonical; retain graph-algorithm views.** The same stable probe added about 72.89 MB RSS. Per-layer replacement still needs atom inverse-index maintenance. | Layer-local graph operations dominate and a compact implementation beats columnar storage including disk and atom queries. |
| 17 | Python records/lists per occurrence | **Park as canonical.** Each record brings object and serialization overhead; typed columns preserve the same fields. No full-record memory comparison was run, so this is a structural concern, not a numeric benchmark. | A measured small editable working set or builder mode wins total cost, followed by typed snapshotting. |
| 18 | Dense atom-pair tensor | **Park as canonical.** A `(frames, atoms, atoms)` array scales with possible pairs and cannot directly encode grouped or higher-arity participants. | Use only as an explicitly pair-only derived analytical view; it cannot satisfy the general result contract. |

The numbered ranking records relative evidence on the earlier small/medium
fixtures. At the stated 300,000-atom and 30,000-structure target, the
preferred **implementation path** is the chunked frame-major architecture in
rank 2, using rank 1's global descriptor encoding where relation reuse makes
it economical. The large-scale writer probe removes an accidental full-atom
scan and demonstrates bounded observed record memory on a synthetic input;
it does not settle cross-block identity, high-churn descriptor memory, or
client query latency. Those gates prevent promotion of the adaptive prototype
to a stable backend today.

### Best-supported implementation baseline

**Design recommendation, updated 2026-09-29; pending consumer review and
production verification.** Keep one logical `Interactions` result contract
independent of the storage backend. The required large-system snapshot should
partition frame-major typed occurrence columns by structure blocks, with
explicit evaluated coverage and source-index maps. Relations retain a stable
logical identity across blocks. Their physical descriptors may use global,
block-local, or occurrence-native encoding according to reuse and churn; no
single giant Python dictionary is required in RAM. Build or persist sparse
atom-to-occurrence postings when atom queries warrant them, and support a
bounded cache rather than loading the whole trajectory. This baseline handles
arbitrary participant groups and parallel observations while preserving
direct structure slices. The global dictionary is the preferred descriptor
encoding when relations recur; the adaptive block route is the implementation
target at the stated upper scale.

Treat descriptor encodings, query indexes, and edit storage as independent
choices behind that contract. An adaptive block codec may encode high-churn
descriptors by occurrence or family, provided every block preserves a
traceable cross-block relation identity and the same frame-major query order. A temporal
run projection may serve long-lived relations or relation-history analysis;
the complete-file probe does not justify it as the sole canonical layout.
A per-structure replacement overlay plus current-to-storage atom/structure
maps is the leading local-edit design. Exact occurrence handles, view lifetime,
atomic persistence, recovery, and compaction remain required before exposing
mutation publicly. SQLite can serve a temporary posting sort or a measured
transactional edit sidecar; its tested file size does not justify making it
the sole canonical serialized result. Develop the typed payload independently
of its container, then embed it in a versioned H5MSM layer before 1.0.

This is an architecture decision for what to implement and compare next, not
a universal performance guarantee. Before freezing the public interface or
claiming a best codec, obtain client examples and thresholds, run real detector
trajectories including variable-size groups and multiple analyses, and test
the production streaming reader/writer, cold and warm queries, RAM and file
size, edit recovery, and H5MSM boundary. The optional codecs only graduate
when they beat this baseline on complete client workloads without losing the
logical contract.

Several choices are **orthogonal to this ranking**. Direct atom-to-occurrence
postings with distinct-atom cardinalities are the strongest measured general
atom/set index, but may be built lazily or compacted. A two-level
atom-to-relation-to-occurrence index used only 0.391 MB with 400 stable
relations versus roughly 1.986 MB for direct postings, while its hot-atom and
churn lookups were slower; keep it as a selectable index, not a mandatory
backend. Roaring bitmaps could compress presence or postings if those indexes
dominate total bytes; their full-contract performance is unmeasured. A compact
numeric incidence graph is already expressible as offset arrays; any new
graph core needs a measured algorithmic benefit beyond that relabeling.

Likewise, Rust via the maintained private PyO3 extension, or Python/NumPy
kernels, is an execution choice. The standalone Rust temporal probe supports
batch-kernel experiments but does not rank a native object ahead of the
measured columnar layouts; C adds another native stack without evidence of a
need. HDF5 is a viable typed standalone codec boundary, yet the tested group
reader and append-only journal are not production designs and H5MSM 0.4 has no
interaction layer. Arrow IPC/Parquet and SQLite remain bounded codec or edit
layer experiments if HDF5 cannot meet cold-read or transactional requirements;
they have not been discarded by a comparative file benchmark. No `pickle`,
native memory image, or library-specific tensor file is the versioned public
contract. Revisit a parked alternative against the **same complete fixtures**
and costs, not the pair-only skeleton that initially made it attractive.

### Requirements-first comparison protocol

The requirements below come from the design discussion and the consumer
request in `uibcdf/molsysviewer#114`. They define the problem to solve; the
ranking above does not define the requirements. The small
[experimental-class tests](../../tests/interactions/test_result.py) passed
locally on 2026-09-28 (`python -m pytest --receptor=llm
tests/interactions/test_result.py`: 9 passed). Later file probes below use
complete-record oracles, but remain experimental and do not establish a
complete public operation.

| ID | Required behavior or outcome | Evidence today | Remaining production or client check |
| --- | --- | --- | --- |
| R01 | Use explicit local atom and structure indices, with local-to-source maps when a selection changes either index space; never substitute IDs. | The public result now stores nonidentity atom and structure maps, composes them on extraction, and round-trips them through `InteractionsDict` and standalone HDF5. | Source revision/fingerprint checks, source-index query modes, and the H5MSM layer. |
| R02 | Preserve ordered, nonconsecutive structure requests without duplicated results; distinguish evaluated empty from unevaluated. | The packed file reader passed explicit repeated/nonconsecutive requests and both empty states, including an oracle-checked large selected-frame query. | Public file-backed behavior after source remaps and large sparse selections. |
| R03 | Preserve any finite participant arity, ordered roles, and compound participants containing multiple atoms. | Class tests cover pairs, a hydrogen-bond triple, a four-participant relation, and two rings; the file-reader edge fixture includes a repeated atom across participants. | Larger or changing groups and identity across methods. |
| R04 | Query one atom or atom set across selected structures as `incident`, `internal`, or `cross`, counting every atom in every participant. | The packed file reader passed all three modes on stable, mixed, churn, and repeated-atom fixtures; a high-degree atom and a narrow large-file selection were measured. | Public reader, wider atom sets, bounded results, and client latency budgets. |
| R05 | Query two atom sets against each other, with a documented rule for outside atoms. | Disjoint, overlapping, and exclusive two-set queries passed the file-reader oracle. | Client agreement on overlap semantics and large-set performance. |
| R06 | Preserve parallel observations of a relation in one structure, deterministic order, and unambiguous occurrence identity for edits. | File-reader edge checks retain two observations with different images and measures; class tests cover deterministic order. | Exact public occurrence handles, removal, and edit round trip. |
| R07 | Keep type, method, parameters, evidence, measures with units, and relevant periodic images; never equate inferred proximity with declared connectivity. | Basic fields and standalone round trips are tested; the class holds one method and declares an atom search scope. Mixed explicit and absent periodic images now fail instead of receiving fabricated zero vectors. A logical probe keeps coverage separately when methods are combined. | Per-frame or mixed analysis scope, source evidence, and scientific detector adapters. |
| R08 | Return typed, shaped empty results and useful columnar projections without requiring one Python object per occurrence. | The packed file reader returns full typed ragged observations and stable empty shapes; the public `InteractionsDict` carries labels, method metadata, and source maps. | Bounded public file-backed projection and current-scale memory measurements. |
| R09 | Add, remove, or replace observations in one structure without recomputing unaffected structures; preserve evaluated-empty coverage. | A numeric frame-override probe showed low local encoding cost; a plain-record oracle checks replacement semantics. Public `invalidate_structures()` produces an independent snapshot that marks stale frames unevaluated and preserves earlier query views. | Local add/replace editor, atomic query merge, repeated edits, compaction, and scalable view lifetime. |
| R10 | Remove atoms or structures, append or reorder structures, and remap every surviving reference or explicitly invalidate the result. | Native copy/extract/remove and structure append have public tests. Target atom addition preserves the previous evaluated atom scope; source-analysis merging fails before mutation. | Source analysis merge, direct mutation ownership, and repeated-edit implementation. |
| R11 | Serialize compact, typed, versioned data both standalone and inside H5MSM before 1.0. | Experimental standalone HDF5 and `InteractionsDict` round trips preserve source maps; a bounded one-pass synthetic writer has oracle-checked file queries. | Production multi-analysis codec, atomic writes, lazy public reads, and a versioned H5MSM interaction layer. |
| R12 | Keep memory and disk proportional to sparse observations and descriptors, and support fast frame and atom queries over long trajectories. | Synthetic 300,000-atom/30,000-structure write, read, packed projection, and frame-first controls give partial complete-result numbers. A public-result scope probe measured about 4.8 MB of extra atom-map and frozen-universe arrays after adding 100 atoms to a 300,000-atom analysis. | Larger output density, many-analysis scope memory, cache-cold reads, bounded iteration, and client latency budgets. |
| R13 | Let clients consume the logical result without depending on the physical backend. | MolSysViewer request is recorded; other client needs are inferred. | Verify a concrete MolSysViewer integration before 1.0. Gather other clients' requirements when their integrations are scheduled. |
| R14 | Offer one general public result interface across interaction families, with explicit columnar/dictionary projections and optional detector `output_type` adapters. | The experimental class represents several kinds and offers `to_dict`; existing detectors keep their method-specific outputs. | Multi-method containers, lossless projections, and opt-in detector adapters without changing legacy defaults. |
| R15 | Make `Interactions` an optional native `MolSys` domain with coherent copy, selection, editing, and H5MSM lifecycle. | `MolSys.interactions` holds named full analyses; native copy, extraction, removal, atom addition, and structure append have focused tests. The public coordinate-only append route preserves unevaluated coverage. | Control direct mutation and remaining form-operation routes, and round-trip attached results through H5MSM. |

R01–R11 and R14–R15 are correctness or lifecycle gates: a candidate cannot compensate for
losing one by being faster on R12. R12 is a multi-objective performance gate,
not one score: report resident and peak RAM, serialized bytes, construction,
save/load, cold and warm complete query latency, and edit/compaction cost.
R13 checks whether the exposed contract is actually usable by clients.
The independent result can be tested first. `MolSys` attachment, H5MSM
embedding, and MolSysViewer integration are pre-1.0 release conditions.

Use the same deterministic, full-field oracle and source-index space for all
five storage architectures. Every candidate must first reproduce these cases:

1. A small semantic fixture with hydrogen bonds, disulfide candidates, two
   ring participants, a four-participant relation, multiple methods, periodic
   images, parallel occurrences, evaluated empty and unevaluated structures,
   nonconsecutive requests, and nonidentity source maps.
2. Stable, high-churn, mixed-phase, and strongly persistent trajectories with
   identical occurrence counts where comparison requires them. Include
   group-heavy and high-degree-atom variants; retain all measure and evidence
   fields rather than benchmark only integer pairs.
3. An edit sequence that adds and removes exact observations, replaces those
   incident to a moved ligand in one structure, makes one evaluated structure
   empty, deletes atoms, and appends, removes, and reorders structures. Compare
   every visible result with an independently rebuilt oracle after each step.
4. A large streamed trajectory that exceeds an agreed RAM budget, with
   bounded construction, standalone round trip, scattered file-backed frame
   and atom queries, and recovery or explicit failure after interrupted edits.

Report median and 95th-percentile complete query times over repeated runs,
including the first query/index-build cost, plus independent-process cold
reads. State host, dependency versions, input distribution, warm-up, sample
count, process RSS baseline and peak, numeric payload bytes, and file bytes.
Measure atom queries across the trajectory and combined nonconsecutive-frame
queries separately. Compare a native editing branch with the same snapshot
layout and oracle; compiling a different algorithm must not silently change
the semantic workload. Use the maintained `ChunkedExecutor` when evaluating
large-trajectory detection or construction through MolSysMT forms.

The questions left open by the requirements have explicit decision tests:

| Open choice | Decision evidence to obtain |
| --- | --- |
| Direct mutation versus immutable snapshot plus edits | Run the same one-frame and repeated-edit sequence; compare query merge, stale-view behavior, peak RAM, atomic recovery, and compaction. Require either stable snapshots or explicit invalidation of pre-edit views. |
| Numerical latency and memory budgets | Ask clients for frame-update, atom-highlight, and trajectory-query workloads and budgets. Until then, report absolute distributions and Pareto tradeoffs without declaring an arbitrary pass time. |
| Lazy disk-backed queries | Test complete cold and warm frame, nonconsecutive-frame, and atom queries with a bounded decoded cache and a trajectory larger than RAM. If clients need only eager small results, record that narrower scope explicitly. |
| Operations required by clients before 1.0 | Exercise one concrete MolSysViewer read/query/display workflow. Record other client requests for later integration without making them a 1.0 gate. |
| Identity after edits and compaction | Test duplicate occurrences, deletion/reinsertion, relation reuse, reordering, and save/load. Distinguish stable public handles from internal row positions, or explicitly limit handle lifetime. |

Until clients supply numerical latency and memory budgets, no invented cutoff
will decide the winner. First reject any candidate that fails a correctness
gate; then compare the remaining designs by workload and identify dominated
choices. Retain a slower or larger design only if it delivers a measured
required capability, such as atomic local edits or bounded file-backed reads,
that the apparent winner lacks. The first benchmark below establishes a
supported-subset semantic oracle and measures the present experimental class;
extend it to source maps, multiple analyses, and edits before using it to
select a backend. The existing pair-only probes remain useful diagnostics,
not final votes.

### First full-field query baseline

The [contract benchmark](../../devtools/scripts/benchmark_interactions_contract.py)
is the first executable step of this protocol. It constructs the same number
of observations under stable, churn, mixed-phase, and persistent relation
distributions. A plain-record oracle independently selects interactions by
source structure and atom indices, `incident`/`internal`/`cross`, and two
disjoint atom sets; it compares complete decoded type, ordered roles, grouped
atoms, evidence, distance, angle, and periodic-image fields. It also checks
evaluated-empty and unevaluated coverage, repeated nonconsecutive structure
requests, parallel observations, and a complete standalone HDF5 round trip.
Some sampled sets contain all atoms of a known relation, so an `internal`
query must sometimes return actual observations. The benchmark reports both
selection-only and complete materialization times and the number of returned
rows; locating an index is not mistaken for delivering the result.

```bash
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution stable
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution churn
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution mixed
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution persistent
```

**Benchmarked, 2026-09-28:** Linux 7.0.0-28-generic x86_64, Intel Xeon
E5-2630 v4, Python 3.13.14, NumPy 2.4.6, h5py 3.16.0. One warm process run
per distribution, 20 sampled requests per query category plus two fixed edge
requests; all 182 requests per run agreed with the oracle. Each input has 500
atoms, 1,000 structures, 965 evaluated structures, and 7,294 observations.
The medians below are milliseconds; the file is the class's standalone HDF5
format, not H5MSM. Numeric bytes include the lazy inverse indexes after the
first atom query. Query time includes neither detector science nor rendering.

| Distribution | Relations | Numeric bytes / file bytes | Complete frame | Complete atom | `internal` select / complete | `cross` select / complete |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Stable | 120 | 706,440 / 175,269 | 0.309 | 2.380 | 1.348 / 1.609 | 1.783 / 21.827 |
| Churn | 6,946 | 1,555,852 / 288,719 | 0.302 | 1.410 | 64.963 / 64.865 | 66.284 / 83.806 |
| Mixed | 3,655 | 1,147,520 / 233,303 | 0.293 | 1.562 | 33.248 / 33.347 | 33.848 / 51.247 |
| Persistent | 120 | 707,412 / 166,440 | 0.302 | 1.481 | 0.947 / 1.524 | 1.119 / 13.602 |

In the stable and churn samples, `internal` returned median 22 and 1 rows
respectively, yet its selection-only median rose from 1.348 to 64.963 ms.
Inspection of the experimental [`query` implementation](../../molsysmt/interactions/result.py)
shows a Python loop over candidate relations that checks each relation's atoms
for `internal` and `cross`; the near-unique-relation input exercises many more
such checks. This is a plausible cause, not a profile attributing every
millisecond. `cross` also materialized roughly 1,000 observations per sampled
set, explaining why complete delivery costs more than selection. Atom-query
tail times depend strongly on the hot atom: the stable complete atom-query
95th percentile was 44.986 ms while its median was 2.380 ms. The output row
counts must accompany latency comparisons.

The process RSS started near 70 MB; after construction it was about 90 MB for
stable relations and 101 MB for churn. The run-wide high-water marks were
about 112 and 121 MB, respectively, including Python input records, oracle
checks, serialization, and allocator behavior. They are not isolated object
sizes. These single runs are diagnostic, not confidence intervals or client
latency guarantees. The present class cannot pass the source-map,
multi-analysis, incremental-edit, remapping, bounded-writer, or lazy-file-read
gates; those are reported as unsupported rather than dropped from the input
contract. A future candidate comparison must use the same oracle and add
those missing cases before it can claim overall superiority.

The same benchmark has an optional `--direct-index-probe` that builds
atom-to-occurrence postings and one distinct-atom cardinality per occurrence,
then reuses the experimental class's result view and complete decoder. It
compares 100 atom/set/combined queries per distribution with the same record
oracle. This is a query-index experiment, **not** a change to the public class:

```bash
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution stable --direct-index-probe
python devtools/scripts/benchmark_interactions_contract.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution churn --direct-index-probe
```

| Input | Existing two-level index bytes | Direct index bytes | Existing / direct `internal` selection median | Existing / direct `cross` selection median |
| --- | ---: | ---: | ---: | ---: |
| Stable | 68,368 | 363,480 | 1.348 / 0.163 ms | 1.783 / 0.172 ms |
| Churn | 418,264 | 368,688 | 64.963 / 0.158 ms | 66.284 / 0.171 ms |

The direct index built in about 0.05 s in each single run. Complete `internal`
delivery through it took median 0.588 ms (stable) and 0.244 ms (churn); when
`cross` returned about a thousand rows, complete delivery still took roughly
16–20 ms. Thus the direct index fixes the measured relation-scan bottleneck,
while bulk Python result decoding remains a separate cost. With stable
relations it uses about 5.3 times the current index bytes; with churn it is
slightly smaller. The experiment does not measure its peak construction RAM,
on-disk index, concurrent access, edits, or nonidentity source maps. These
are index policy tradeoffs within a storage architecture, not evidence that
the entire class or one of the five backends has won.

### Source maps, analysis coverage, and edit semantics probe

The [plain-record logical probe](../../devtools/scripts/probe_interactions_semantics.py)
exercises R01, R07, R09, and R10 without choosing an array layout or editing
backend:

```bash
python devtools/scripts/probe_interactions_semantics.py
```

It starts with two named analyses whose **local** atom and structure indices
map to nonidentity positions in one 12-atom, six-structure source system.
Their observations include duplicate hydrogen bonds with different images,
a two-ring relation, a four-participant relation, and a source-declared
disulfide with a type distinct from an inferred S–S candidate. Their
evaluated coverage differs: the first analysis
evaluates source structures `[4, 1, 5]`, the second `[4, 5]`. For a request
`[5, 4, 5, 1]`, the oracle returns coverage `[5, 4, 1]` and `[5, 4]`
respectively. A single union coverage would falsely imply that both methods
evaluated structure 1. **If** one `Interactions` object combines analyses, it
must preserve coverage per analysis; separate single-analysis results already
provide that separation. This is a logical requirement, not a decision to
make a multi-analysis container mandatory. The oracle also checks occurrence
order for the requested source structure sequence before applying a stable
analysis and relation order within each structure.

Eight projections from the oracle's source-index rows into the current
single-method `Interactions` class agreed on full decoded records and coverage
after caller-side index mapping. The class itself does not retain the maps or
combine the analyses. The oracle then replaced observations incident to a
moved source atom in structure 4 for both analyses, leaving other structures
untouched; the atom lost its old hydrogen bonds and gained two new ones with
a different partner. Removing source atom 6 pruned the ring, four-body, and
disulfide observations touching it, remapped surviving atom indices, and kept
evaluated-empty structures explicit. A later structure subset/reorder and
append similarly remapped positional structure indices and marked the new
structure evaluated for only one analysis. The original snapshot remained
unchanged. The probe passed locally on 2026-09-28.

This verifies the *reference semantics* of one synthetic edit sequence, not
an editing API, transaction, scientific reassignment rule, or performance
result. Its local-to-source maps use `None` for removed entries after pruning;
a physical result may instead invalidate the map or rebuild it, but must not
silently point it at a different atom or structure. Stable occurrence handles,
partial-method evaluation, source declarations without a frame, and changes
that require wider chemical recomputation still need explicit decisions.

### Transactional indexed-row probe

The [SQLite candidate probe](../../devtools/scripts/benchmark_interactions_sqlite.py)
uses the same deterministic full-field records and 182 oracle-checked query
requests per distribution as the experimental-class baseline. It stores one
method, explicit coverage, typed relation-role/atom and periodic-image BLOBs,
numeric measures, evidence codes, occurrence rows, and indexes by structure
and atom. Each parallel observation has its own row ID. The open reader caches
decoded relations as it encounters them. It then transactionally replaces
observations incident to one atom in one structure, checks frame and atom
queries against a rebuilt record oracle, performs 20 further replacements,
removes orphan relation rows, compacts, and reopens the committed file.

```bash
python devtools/scripts/benchmark_interactions_sqlite.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution stable
python devtools/scripts/benchmark_interactions_sqlite.py --frames 1000 --atoms 500 --per-frame 8 --samples 20 --distribution churn
```

**Benchmarked, 2026-09-28:** the same Linux/Xeon/Python/NumPy host as above,
SQLite 3.53.4, one warm process run per distribution. Each input has 965
evaluated structures and 7,294 observations. Medians include complete record
decoding for frame and atom queries; the set-query column measures only SQL
selection and result ID ordering. File bytes are measured after the build
transaction and include SQLite's structure and atom indexes.

| Input | SQLite file / experimental HDF5 file | Build | Complete frame / atom query | SQLite `internal` selection | Median repeated local transaction |
| --- | ---: | ---: | ---: | ---: | ---: |
| Stable | 1,859,584 / 175,269 B | 0.171 s | 0.197 / 2.087 ms | 0.717 ms | 2.881 ms |
| Churn | 2,199,552 / 288,719 B | 0.195 s | 0.201 / 1.226 ms | 0.774 ms | 3.106 ms |

The 20 replacements did not enlarge either SQLite file in this run; the
database reused pages. Cleaning orphan relation rows and running `VACUUM`
reduced them to 1,748,992 and 2,080,768 B, at about 0.028 and 0.039 s.
The original and final edited states agreed with the oracle after reopening.
This demonstrates local committed updates and selective warm reads for this
schema, not crash recovery or an upper bound on growth after arbitrary edit
histories. The probe begins near 71 MB process RSS, reaches about 83 MB after
stable construction or 93 MB after churn construction, and peaks at about 107
or 129 MB across the complete query/edit run. Python source records and the
growing decoded-relation cache are included, so these are not isolated backend
payload sizes.

The original disk comparison was **not index-equivalent**: the HDF5
experimental class did not persist its atom inverse index, while SQLite did.
The index-equivalent file-size probe below narrows that specific gap. SQLite
is a row store with no compression, and its open connection uses the
operating-system page cache. Its warm complete-frame median being slightly
lower than the current in-memory class's Python decoder does not establish
faster file-backed storage. The probe has no nonidentity source maps,
multi-analysis coverage, bounded streaming builder, H5MSM path, independently
cold reads, or interrupted-write recovery test. Its structure-index SQL and
relation cache need further scaling tests. SQLite remains a live candidate for
an edit layer or a full backend, with a clear file-size cost and a measured
local-edit advantage in this narrow scenario.

### Persisted-index file-size comparison

The [indexed-file probe](../../devtools/scripts/benchmark_interactions_indexed_files.py)
uses the same full-field records and writes both candidate files. It appends
four compressed, typed HDF5 sidecar datasets: structure offsets, atom posting
offsets, atom-to-occurrence postings, and distinct-atom counts per occurrence.
SQLite already persists equivalent logical lookup information through its
structure and atom indexes and the `atom_count` occurrence column. The probe
checks every HDF5 atom posting for false positives, sorted uniqueness and
complete cardinality, verifies structure offsets, and compares both decoded
payloads with the independent record oracle. The HDF5 sidecar is experimental;
the public loader ignores it and does not yet perform lazy file queries.

```bash
python devtools/scripts/benchmark_interactions_indexed_files.py --distribution stable
python devtools/scripts/benchmark_interactions_indexed_files.py --distribution churn
```

**Benchmarked, 2026-09-28:** Linux 7.0.0-28-generic x86-64, h5py 3.16.0,
SQLite 3.53.4, 1,000 structures, 500 atoms, 965 evaluated structures and
7,294 observations per fixture; one deterministic file write per distribution.
The HDF5 delta includes dataset and group metadata, whereas its dataset-storage
column reports only compressed dataset payload.

| Distribution | HDF5 before / after sidecar | Sidecar dataset storage | SQLite indexed file | SQLite / indexed HDF5 |
| --- | ---: | ---: | ---: | ---: |
| Stable relations | 175,269 / 251,076 B | 63,647 B | 1,859,584 B | 7.41 |
| Changing relations | 288,719 / 372,147 B | 71,467 B | 2,199,552 B | 5.91 |

Persisting a direct atom index costs about 76–83 KB more HDF5 file space here;
the indexed HDF5 file remains materially smaller. The candidates now carry
comparable **logical** indexes, not equivalent physical layouts or query
implementations. This probe measures no file-backed query latency, bounded
writer memory, or update cost for the HDF5 sidecar. Rebuild it after edits
before treating it as a canonical persisted index. The following comparison
uses complete projected reads in independent processes and reports whether
the operating-system cache is warm; calling an in-memory `Interactions.load`
a file-backed query would conceal its full-file load cost.

### Process-isolated file query probe

The [reopened-query probe](../../devtools/scripts/benchmark_interactions_reopened_queries.py)
opens the same indexed files in a fresh Python process for each request. Both
readers return complete relation participants and roles, evidence, measures,
periodic images, and the relevant evaluated coverage; each result is checked
against the record oracle. The timer begins just before opening the file and
ends after reconstructing the result. It excludes Python interpreter startup.
The HDF5 reader selects atom postings and occurrence columns, then reads each
needed relation and image span through h5py; it caches decoded relations within
one query. SQLite uses the indexed-row probe's queries and relation cache. Both
processes are fresh, but the **operating-system page cache is likely warm**
because the files were just written and reopened repeatedly. No OS-cold claim
follows from these measurements.

```bash
python devtools/scripts/benchmark_interactions_reopened_queries.py --distribution stable --repeats 3
python devtools/scripts/benchmark_interactions_reopened_queries.py --distribution churn --repeats 3
```

**Benchmarked, 2026-09-28:** the same Linux host and 1,000-structure,
500-atom, 7,294-observation fixtures as above; h5py 3.16.0 and SQLite 3.53.4.
Each number is the median of three independent-process opens and complete
queries, in milliseconds. The checked frame 1 is evaluated but empty.

| Distribution | Request (rows) | Projected HDF5 open + query | SQLite open + query |
| --- | --- | ---: | ---: |
| Stable | Frame 2 (10) | 17.30 | 1.53 |
| Stable | Frame 1 (0) | 1.42 | 0.91 |
| Stable | Atom 0 (2,511) | 875.58 | 40.87 |
| Stable | Atom 42 (224) | 84.15 | 4.73 |
| Churn | Frame 2 (10) | 18.17 | 1.56 |
| Churn | Frame 1 (0) | 1.48 | 0.94 |
| Churn | Atom 0 (2,801) | 3,539.91 | 111.07 |
| Churn | Atom 42 (78) | 117.59 | 4.52 |

This is evidence against **this simple HDF5 reader and the present global
descriptor layout** for interactive file-backed queries, especially when many
different relations are requested. It is not evidence that HDF5 as a container
has these intrinsic latencies: the prototype issues several small dataset
reads per relation and image span, whereas SQLite stores a relation in one row
and fetches occurrence rows in a batch. The next probe tests contiguous page
reads without changing the stored payload. The result also does not erase
SQLite's measured 5.91–7.41 times disk cost on these fixtures.

### Batched projected HDF5 reader

The same [reopened-query probe](../../devtools/scripts/benchmark_interactions_reopened_queries.py)
also tests `hdf_batch` against the same files, requests, and oracle. This reader
loads only touched 256-occurrence pages and 128-relation descriptor pages.
Images are decoded from one contiguous span per touched occurrence page.
Temporary page arrays are bounded by those sizes; decoded relation and image
results grow with the requested output. The file bytes and persisted indexes
are unchanged. It is a read-plan experiment, not a public implementation.

**Benchmarked, 2026-09-28:** same host, files, three independent-process
repeats, and likely warm operating-system page cache as the preceding table.
Values are median opening plus complete-query times in milliseconds.

| Distribution | Request (rows) | Scalar HDF5 | Batched HDF5 | SQLite |
| --- | --- | ---: | ---: | ---: |
| Stable | Frame 2 (10) | 17.54 | 13.30 | 1.53 |
| Stable | Frame 1 (0) | 1.42 | 1.46 | 1.01 |
| Stable | Atom 0 (2,511) | 878.23 | 64.56 | 40.67 |
| Stable | Atom 42 (224) | 84.05 | 36.89 | 4.72 |
| Churn | Frame 2 (10) | 17.96 | 23.07 | 1.56 |
| Churn | Frame 1 (0) | 1.47 | 1.44 | 0.95 |
| Churn | Atom 0 (2,801) | 3,503.41 | 121.13 | 106.05 |
| Churn | Atom 42 (78) | 114.41 | 69.90 | 4.64 |

Page batching reduces the high-degree atom query by about 14-fold in the
stable input and 29-fold in churn; the batched reader is within 1.59 and
1.14 times SQLite for those requests. It makes the churn frame slower by
overreading descriptor pages for only ten results, and low-degree atom reads
still pay for many scattered descriptor pages. Thus reader layout and an
adaptive read plan can change the ranking materially. This is still not a
final comparison: block-local descriptors, OS-cold reads, larger trajectories,
edits, and end-to-end write memory remain untested. The next probe tests a
complete occurrence-native descriptor file.

### Complete occurrence-native HDF5 file

The [occurrence-native codec probe](../../devtools/scripts/benchmark_interactions_event_native.py)
stores the same evaluated coverage, method metadata, participants and roles,
evidence, measures and units, periodic images, and atom/structure indexes as
the global-relation HDF5 file. It repeats type and participant descriptors
beside each occurrence instead of storing a global relation dictionary. The
common numeric fields use the same types as the experimental class snapshot;
the two files are independently complete. The reader touches fixed-size event
pages and reconstructs each requested result without loading all frames.
The [reopened-query harness](../../devtools/scripts/benchmark_interactions_reopened_queries.py)
checks every answer against the independent record oracle in fresh processes.

```bash
python devtools/scripts/benchmark_interactions_reopened_queries.py --distribution stable --repeats 3 --backends hdf_batch,hdf_event,sqlite --event-page-size 512
python devtools/scripts/benchmark_interactions_reopened_queries.py --distribution churn --repeats 3 --backends hdf_batch,hdf_event,sqlite --event-page-size 512
```

**Benchmarked, 2026-09-28:** same Linux host, h5py 3.16.0, SQLite 3.53.4,
1,000 structures, 500 atoms, 965 evaluated structures, and 7,294 observations;
medians of three independent-process opening-plus-query runs with likely warm
OS page cache. A one-run exploratory sweep of 32, 128, and 512-event read
pages selected 512 on these **same** fixtures, so the reader choice is tuned
to the benchmark data and needs a held-out workload before adoption.

| Distribution | Indexed global HDF5 | Indexed event-native HDF5 | Indexed SQLite |
| --- | ---: | ---: | ---: |
| Stable file bytes | 251,076 | 325,375 | 1,859,584 |
| Churn file bytes | 372,147 | 359,555 | 2,199,552 |

| Distribution | Request (rows) | Global HDF5 batched | Event-native HDF5 | SQLite |
| --- | --- | ---: | ---: | ---: |
| Stable | Frame 2 (10) | 13.60 ms | 13.05 ms | 1.54 ms |
| Stable | Frame 1 (0) | 1.48 ms | 1.81 ms | 0.93 ms |
| Stable | Atom 0 (2,511) | 64.58 ms | 87.37 ms | 40.50 ms |
| Stable | Atom 42 (224) | 36.72 ms | 55.37 ms | 4.79 ms |
| Churn | Frame 2 (10) | 22.94 ms | 13.35 ms | 1.55 ms |
| Churn | Frame 1 (0) | 1.44 ms | 1.80 ms | 0.91 ms |
| Churn | Atom 0 (2,801) | 121.98 ms | 92.60 ms | 105.74 ms |
| Churn | Atom 42 (78) | 69.59 ms | 54.05 ms | 4.71 ms |

The complete event-native file is about 30% larger under stable reuse, but
about 3% smaller under churn. For the measured nonempty churn frame and both
churn atom requests it beats the tested global HDF5 reader; the high-degree
atom query also beats SQLite narrowly. Stable atom queries favor the global
dictionary, and SQLite remains much faster for small result sets. This supports
**selective** event-native blocks inside the adaptive candidate, while leaving
occurrence-native descriptors parked as a universal layout. The codec writer
still builds from a fully materialized result and its atom index in memory;
its peak memory and local edit cost are not established. The page-size sweep
is exploratory, and a different mixed-phase detector workload could reverse
these measured preferences.

### Mixed-phase adaptive block-size probe

The [adaptive-block probe](../../devtools/scripts/benchmark_interactions_adaptive_blocks.py)
writes three HDF5 files from the same full-field records: every block uses a
relation dictionary, every block uses occurrence-native descriptors, or each
block selects the smaller **uncompressed numeric descriptor projection**.
Method metadata, explicit evaluated coverage, labels, evidence, distances,
angles, periodic images, and a compressed global atom-to-occurrence posting
index are present in every file. The index uses global occurrence positions
plus block offsets, avoiding a redundant `(block, local occurrence)` pair per
posting. Every decoded occurrence and every atom posting is checked against
the independent oracle. The mixed input has 500 stable-relation structures
followed by 500 changing-relation structures; a second input moves the switch
to structure 430, inside a candidate block.

```bash
python devtools/scripts/benchmark_interactions_adaptive_blocks.py --distribution mixed --block-size 100
python devtools/scripts/benchmark_interactions_adaptive_blocks.py --distribution mixed --block-size 250
python devtools/scripts/benchmark_interactions_adaptive_blocks.py --distribution mixed --block-size 500
python devtools/scripts/benchmark_interactions_adaptive_blocks.py --distribution mixed --block-size 100 --switch-frame 430
python devtools/scripts/benchmark_interactions_adaptive_blocks.py --distribution mixed --block-size 250 --switch-frame 430
```

**Benchmarked, 2026-09-28:** same Linux host, h5py 3.16.0, 1,000 structures,
500 atoms, 965 evaluated structures and 7,294 observations; deterministic
single file writes with no timing claim. The table reports complete file bytes
after all indexes are persisted. The adaptive choice was global in early
blocks and occurrence-native in late blocks. With the switch at 430, the
straddling block stayed global and the choice changed at the next boundary.

| Switch / block size | Fixed global | Fixed occurrence-native | Adaptive | Adaptive HDF5 metadata and padding |
| --- | ---: | ---: | ---: | ---: |
| 500 / 100 | 677,709 B | 673,776 B | 655,041 B | 389,537 B |
| 500 / 250 | 431,564 B | 460,194 B | 426,005 B | 167,403 B |
| 500 / 500 | 351,327 B | 386,930 B | 348,820 B | 94,684 B |
| 430 / 100 | 687,320 B | 676,332 B | 664,718 B | 391,240 B |
| 430 / 250 | 441,374 B | 462,249 B | 433,803 B | 166,555 B |

For the aligned input, adaptive storage saves about 2.8%, 1.3%, and 0.7%
against the smaller fixed **block** file at block sizes 100, 250, and 500.
On all-stable 100-structure blocks, it selected global for every block and
matched that fixed file exactly (620,560 B); on all-churn blocks, it selected
occurrence-native throughout and matched that fixed file (689,372 B). The
unaligned transition still selected the expected scopes, but did not remove
the block overhead.

For context, the [single-block indexed global file](../../devtools/scripts/benchmark_interactions_indexed_files.py)
for the aligned mixed input is 313,443 B. The 500-structure adaptive file is
about 11% larger, and the 100-structure adaptive file is about 109% larger.
This is not a proof that adaptive blocks are inferior: the current encoding
creates many HDF5 groups and datasets, and the latter file spends 389,537 B
on HDF5 metadata and padding versus 265,504 B on stored dataset payload.
Fewer or flat datasets, actual lazy query times, and local replacement cost
must be compared before selecting block granularity. The selector uses raw
numeric bytes, which do not predict compressed file bytes exactly.

The writer currently holds all source records and both descriptor candidates
for each block in memory. Numeric relation IDs are local to a block; the
semantic descriptor can be reconstructed, but stable cross-block relation IDs
and edit handles are not persisted. Thus the oracle establishes full
observation fidelity and atom-posting correctness for this fixture, not the
complete proposed identity, streaming, or lifecycle contract. A production
adaptive design must close these gaps before its file-size savings can count
as a backend win.

### Flat adaptive blocks and reopened queries

The [flat-block probe](../../devtools/scripts/benchmark_interactions_flat_blocks.py)
places each typed field in one HDF5 dataset, uses one block-offset matrix, and
persists the same global atom postings as the grouped block probe. It selects
global relation descriptors for the stable half and occurrence-native
descriptors for the changing half. A reader retains at most four decoded
blocks, skips an evaluated-empty frame without decoding its block, and checks
complete returned records and coverage against the independent oracle. A
"flat" file here still has a small fixed number of HDF5 datasets; it is not a
dense atom-pair matrix or a proposed H5MSM schema.

```bash
python devtools/scripts/benchmark_interactions_flat_blocks.py --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_flat_blocks.py --block-size 500 --repeats 5
```

**Benchmarked, 2026-09-28:** Linux 7.0.0-28-generic x86_64, Intel Xeon
E5-2630 v4, Python 3.13.14, NumPy 2.4.6, h5py 3.16.0, SQLite 3.53.4;
1,000 structures, 500 atoms, 965 evaluated structures, 7,294 full-field
observations. Each latency is the median of five same-process file reopens
and complete queries, with the operating-system page cache likely warm. The
compared SQLite file includes its atom and frame indexes. The grouped and
flat HDF5 readers load each touched block's columns before decoding selected
rows, so these results measure this read plan, not optimized projected reads.

| Block size | Grouped HDF5 | Flat HDF5 | SQLite indexed |
| ---: | ---: | ---: | ---: |
| 100 | 655,041 B | 320,205 B | 2,027,520 B |
| 500 | 348,820 B | 317,990 B | 2,027,520 B |

| Block size | Request (rows) | Grouped open + query | Flat open + query | SQLite open + query |
| ---: | --- | ---: | ---: | ---: |
| 100 | Frame 2 (10) | 5.32 ms | 6.19 ms | 1.29 ms |
| 100 | Evaluated-empty frame 1 (0) | 1.76 ms | 2.53 ms | 0.69 ms |
| 100 | Frame 750 (7) | 5.50 ms | 6.73 ms | 1.14 ms |
| 100 | Atom 0 (2,654) | 76.87 ms | 78.26 ms | 71.34 ms |
| 100 | Atom 42 (154) | 39.65 ms | 40.90 ms | 3.90 ms |
| 500 | Frame 2 (10) | 6.49 ms | 7.31 ms | 1.26 ms |
| 500 | Evaluated-empty frame 1 (0) | 1.75 ms | 2.56 ms | 0.72 ms |
| 500 | Frame 750 (7) | 7.63 ms | 8.15 ms | 1.15 ms |
| 500 | Atom 0 (2,654) | 50.53 ms | 50.92 ms | 76.54 ms |
| 500 | Atom 42 (154) | 14.56 ms | 15.38 ms | 4.31 ms |

Flattening removes most per-block HDF5 metadata cost: ten adaptive blocks are
about 2.2% larger than the 313,443 B monolithic indexed global file on this
input, against 109% for the grouped ten-block file. It does not itself speed
queries. Atom 42 appears across blocks; reading whole touched blocks dominates
its relatively small result. Increasing block size improves the high-degree
atom 0 query by reducing block overhead but slows small frame requests.
These are cache-warm, single-host samples; no independent-process or OS-cold
latency claim follows. The four-block decoded cache is bounded in block count,
but block size and query output still determine memory. The writer retains
all records, descriptor candidates, and atom postings in Python memory.

### Full-frame edit overlay on a flat snapshot

The [flat-edit probe](../../devtools/scripts/benchmark_interactions_flat_edits.py)
appends typed full-frame replacements to the flat HDF5 snapshot. The latest
committed replacement takes precedence; a pending replacement remains
invisible. The oracle checks a molecule-atom change in frame 10, a committed
evaluated-empty frame, an unaffected frame, an unevaluated frame, and atom
queries after each of 20 further replacements. The comparison uses SQLite
full-frame replacement over the same records, then compacts both stores.

```bash
python devtools/scripts/benchmark_interactions_flat_edits.py
```

**Benchmarked, 2026-09-28:** the same host and package versions as above,
100-structure flat blocks, one 1,000-structure mixed fixture, one sequential
edit run. Append medians cover 20 repeated edits; query medians cover five
same-process file reopens with a likely warm operating-system cache. Times
include complete result reconstruction and are exploratory, not a generalized
throughput guarantee.

| Checkpoint | HDF5 overlay | SQLite indexed rows |
| --- | ---: | ---: |
| Initial file | 320,205 B | 2,027,520 B |
| After 20 further replacements | 1,121,149 B | 2,031,616 B |
| Compacted file | 320,236 B | 1,916,928 B |
| Median repeated replacement | 6.23 ms | 9.05 ms |
| Compaction of this fixture | 0.288 s | 0.040 s |

The pending HDF5 edit raised the file to 358,405 B; a committed evaluated-empty
edit raised it to 376,189 B. A pending marker proves only the tested logical
visibility rule. It is **not** evidence of atomicity, durability, or recovery
from an interrupted HDF5 write. Group-per-edit metadata causes roughly linear
growth until snapshot compaction; SQLite reused pages in this sequence.

| Reopened request | HDF5 overlay after edits | SQLite after edits | HDF5 after compaction | SQLite after compaction |
| --- | ---: | ---: | ---: | ---: |
| Frame 10 | 9.24 ms | 1.16 ms | 6.28 ms | 1.16 ms |
| Atom 41 | 47.66 ms | 3.34 ms | 41.12 ms | 3.33 ms |
| Atom 0 | 85.68 ms | 73.34 ms | 78.51 ms | 73.48 ms |

The current overlay reader scans committed edits and decodes base matches
before removing overridden-frame records. A compact journal index and a
reader that skips those base matches could change the result. Conversely,
SQLite's transaction and page-reuse behavior here is evidence for an edit
layer, not proof that row storage should own the whole public object. A
streaming snapshot writer, cross-block relation identity, true crash recovery,
and source-index remapping remain open before either backend can be selected.

### Projected flat-file read probe

The [projected-reader probe](../../devtools/scripts/benchmark_interactions_projected_reader.py)
uses the same flat HDF5 file as above and fetches only the requested event,
relation, participant, atom, and image positions. For sparse positions it
compares an h5py indexed gather with one continuous span; the default chooses
a span when it covers no more than four times the requested row count. It
returns complete records and coverage checked against the independent oracle.
The result is compared with the bounded-cache whole-block reader and the same
indexed SQLite file. No file schema or public class behavior changes.

```bash
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution mixed --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution mixed --block-size 500 --repeats 5
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution stable --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution churn --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution mixed --block-size 100 --strategy gather --repeats 5
python devtools/scripts/benchmark_interactions_projected_reader.py --distribution mixed --block-size 100 --strategy span --repeats 5
```

**Benchmarked, 2026-09-28:** Linux 7.0.0-28-generic x86_64, Intel Xeon
E5-2630 v4, Python 3.13.14, NumPy 2.4.6, h5py 3.16.0, SQLite 3.53.4;
1,000 structures, 500 atoms, 965 evaluated structures, 7,294 full-field
observations per distribution. Each time is the median of five same-process
file reopens and complete queries, with the operating-system page cache likely
warm. The HDF5 projection's read counts below include only `data/` column
accesses, excluding index, metadata, labels, and the decompression of gzip
chunks. They are not physical bytes read from disk.

| Distribution / block size | Request (rows) | Whole block | Projected adaptive | SQLite | Projected column reads |
| --- | --- | ---: | ---: | ---: | ---: |
| Mixed / 100 | Frame 2 (10) | 6.25 ms | 6.24 ms | 1.29 ms | 13 |
| Mixed / 100 | Evaluated-empty frame 1 (0) | 2.54 ms | 2.55 ms | 0.71 ms | 1 |
| Mixed / 100 | Frame 750 (7) | 6.56 ms | 5.65 ms | 1.17 ms | 12 |
| Mixed / 100 | Atom 0 (2,654) | 78.48 ms | 62.69 ms | 75.26 ms | 115 |
| Mixed / 100 | Atom 42 (154) | 41.39 ms | 25.09 ms | 4.32 ms | 115 |
| Mixed / 500 | Frame 2 (10) | 7.45 ms | 6.41 ms | 1.25 ms | 13 |
| Mixed / 500 | Atom 0 (2,654) | 50.01 ms | 59.02 ms | 73.75 ms | 23 |
| Mixed / 500 | Atom 42 (154) | 15.21 ms | 17.53 ms | 3.97 ms | 23 |
| Stable / 100 | Atom 0 (2,511) | 74.68 ms | 51.43 ms | 38.10 ms | 120 |
| Stable / 100 | Atom 42 (224) | 42.31 ms | 25.96 ms | 3.99 ms | 120 |
| Churn / 100 | Atom 0 (2,801) | 84.00 ms | 76.94 ms | 104.07 ms | 110 |
| Churn / 100 | Atom 42 (78) | 40.16 ms | 23.17 ms | 4.16 ms | 110 |

Projection helps a sparse atom request but does not remove the cost of
touching ten blocks and 110–120 separate column reads. The evaluated-empty
frame still needs only two frame-offset values. Stable relations favor SQLite
for the high-degree atom query here; changing relations make the projected
HDF5 query faster. SQLite remains about five to six times faster for the
sampled nonempty frame requests and about five to six times faster for a
low-degree atom query, despite its larger file. These are results for the
tested readers and fixtures, not intrinsic format limits.

The gather-versus-span check also rejects a naive "read the fewest logical
rows" rule. On mixed 100-structure blocks, gathering only selected positions
for atom 0 read 45,946 logical `data/` rows but took 128.75 ms; reading spans
read 112,643 rows and took 63.34 ms. For atom 42, gathering 2,355 rows took
25.02 ms, while spans read 92,758 rows and took 15.22 ms. Compression chunks,
fancy-index overhead, and call count all matter. A next reader experiment
should reduce column calls through a compact event/participant record layout
or batch API, and measure independent-process and OS-cold latency before
promising client query speed.

### Compact-record HDF5 control

The [compound-record probe](../../devtools/scripts/benchmark_interactions_compound_hdf5.py)
repacks the same flat adaptive file into six datasets: fixed-width event,
relation, and participant records, plus atom indices, image vectors, and frame
offsets. It retains the source atom postings, coverage, labels, both geometry
measures, evidence, and images. The event and descriptor tables still select
global relations for stable blocks and occurrence-native descriptors for churn
blocks. Its reader checks complete results against the same independent
oracle. This is a test of fewer HDF5 calls, not a proposed general schema:
the probe currently uses `uint32` indices and an eager repacker.

```bash
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution mixed --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution mixed --block-size 500 --repeats 5
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution stable --block-size 100 --repeats 5
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution churn --block-size 100 --repeats 5
```

**Benchmarked, 2026-09-28:** same Linux/Xeon/Python/NumPy/h5py/SQLite
environment, fixture and warm-cache, five-reopen median method as the
projected probe. Both HDF5 files include the same global atom postings.

| Distribution / block size | Flat column file | Compact-record file | Indexed SQLite file |
| --- | ---: | ---: | ---: |
| Mixed / 100 | 320,205 B | 339,003 B | 2,027,520 B |
| Mixed / 500 | 317,990 B | 336,021 B | 2,027,520 B |
| Stable / 100 | 263,334 B | 264,889 B | 1,859,584 B |
| Churn / 100 | 369,373 B | 410,375 B | 2,199,552 B |

| Distribution / block size | Request (rows) | Whole flat block | Compact record | SQLite | Compact `data/` reads |
| --- | --- | ---: | ---: | ---: | ---: |
| Mixed / 100 | Frame 2 (10) | 6.08 ms | 4.97 ms | 1.33 ms | 6 |
| Mixed / 100 | Frame 750 (7) | 6.60 ms | 4.50 ms | 1.17 ms | 6 |
| Mixed / 100 | Atom 0 (2,654) | 76.23 ms | 88.26 ms | 73.76 ms | 50 |
| Mixed / 100 | Atom 42 (154) | 40.65 ms | 22.25 ms | 4.27 ms | 50 |
| Mixed / 500 | Frame 2 (10) | 7.61 ms | 4.96 ms | 1.22 ms | 6 |
| Mixed / 500 | Atom 0 (2,654) | 54.70 ms | 81.52 ms | 74.78 ms | 10 |
| Mixed / 500 | Atom 42 (154) | 15.15 ms | 14.62 ms | 4.11 ms | 10 |
| Stable / 100 | Atom 0 (2,511) | 74.09 ms | 75.76 ms | 39.21 ms | 50 |
| Churn / 100 | Atom 0 (2,801) | 79.69 ms | 102.75 ms | 102.96 ms | 50 |

The compact file trades about 6% more bytes on the mixed 100-block fixture
for half as many small HDF5 `data/` accesses per block. It improves sampled
frame and low-degree atom requests, but loses on high-output atom requests
against the best projected column reader. SQLite still wins sampled small
requests by roughly four to five times. Thus neither "HDF5 is intrinsically
slow" nor "one record table solves the latency gap" follows. A final
implementation could select an in-memory query object, an HDF5 snapshot, and
a transactional edit store separately; the public semantic contract need not
inherit any one physical codec. Larger fixtures, OS-cold reads, peak RAM, and
multiple analyses remain untested for this compound control.

The same command with `--session-probe` opens each reader once and issues 200
distinct, seeded, nonconsecutive structure requests followed by 20 atom
requests, including atoms 0 and 42. Each complete result is checked against
the oracle outside its timed interval. The flat reader retains at most four
decoded blocks, the projected and compact readers cache HDF5 dataset handles,
and SQLite caches decoded relations. This is a single warm-process session on
the same host, not an OS-cold or multi-user throughput test.

```bash
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution mixed --block-size 100 --repeats 5 --session-probe
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution stable --block-size 100 --repeats 5 --session-probe
python devtools/scripts/benchmark_interactions_compound_hdf5.py --distribution churn --block-size 100 --repeats 5 --session-probe
```

| Distribution | Query set | Whole flat median / p95 | Projected flat median / p95 | Compact record median / p95 | SQLite median / p95 |
| --- | --- | ---: | ---: | ---: | ---: |
| Mixed | 200 frames | 3.58 / 4.13 ms | 0.74 / 0.95 ms | 1.01 / 1.22 ms | 0.33 / 0.46 ms |
| Mixed | 20 atoms | 36.93 / 40.61 ms | 11.03 / 18.27 ms | 11.70 / 20.05 ms | 1.89 / 6.58 ms |
| Stable | 200 frames | 3.54 / 4.02 ms | 0.79 / 0.95 ms | 1.06 / 1.24 ms | 0.21 / 0.31 ms |
| Stable | 20 atoms | 37.13 / 41.00 ms | 8.67 / 18.27 ms | 10.04 / 21.10 ms | 1.30 / 5.52 ms |
| Churn | 200 frames | 3.67 / 4.17 ms | 0.38 / 0.52 ms | 0.76 / 0.99 ms | 0.38 / 0.49 ms |
| Churn | 20 atoms | 37.70 / 40.88 ms | 12.25 / 16.21 ms | 12.80 / 17.73 ms | 2.04 / 7.12 ms |

Keeping the projected HDF5 reader open changes the frame comparison
materially. On this churn session its frame median matched SQLite to the
reported two decimals; stable and mixed sessions still favored SQLite. Atom
requests across the trajectory favored SQLite in all three distributions.
The fixed-record variant did not beat the projected column reader in these
persistent sessions, despite fewer data calls, so reducing call count alone
is an insufficient optimization criterion. This supports evaluating a live
in-memory index separately from serialized file access and measuring client
workloads before specifying universal latency guarantees. The sampled atom
set is small and the file/page caches are warm; neither a universal backend
ranking nor an H5MSM integration claim follows.

### One-pass adaptive block writer and external atom-posting sort

The [streaming-writer probe](../../devtools/scripts/benchmark_interactions_streaming_writer.py)
consumes sorted records and evaluated structure indices as iterators. It holds
one analysis block and both descriptor candidates for that block, appends
typed columns to extendible HDF5 datasets, and stores atom-to-occurrence
postings in a temporary on-disk SQLite table. At the end, it creates the
sorted compressed posting arrays from that table. SQLite here is a scratch
sorter, not the result container. Metadata and offset arrays still scale with
the number of blocks and atoms; the writer is bounded in the number of
interaction **records** retained, not in total output bytes or all metadata.
The synthetic fixture generator was refactored to provide the same records
incrementally; its 1,000-structure record-and-coverage digest remained
unchanged (`9d3318e8eb3483387642c02de8e0e366884d21040f500002e0ff2ac8414075c7`).

```bash
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 1000 --block-size 100 --verify
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode eager --frames 1000 --block-size 100 --verify
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 10000 --block-size 100 --verify
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode eager --frames 10000 --block-size 100
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 30000 --block-size 100
```

**Benchmarked, 2026-09-28:** same Linux/Xeon/Python/NumPy/h5py/SQLite host
as above, mixed stable/changing relation fixture, 500 atoms and eight nominal
observations per evaluated structure. Each command is a separate process and
one build run. `resource.getrusage().ru_maxrss` is read immediately after
generation and writing, before optional oracle verification. The baseline
after imports is about 79 MiB in these runs. Time includes fixture generation,
HDF5 write, and the streaming writer's temporary SQLite sort. There is no
warm-up or multi-run confidence interval for build time.
These rows predate the 2026-09-29 removal of a per-block full-atom scan;
their build times are historical checkpoint measurements. The current script
keeps the same fixture and output schema but has a different construction
path. The scale measurements below describe that updated path.

| Structures / writer | Build | Peak RSS growth after imports | Final HDF5 | Temporary posting SQLite |
| --- | ---: | ---: | ---: | ---: |
| 1,000 / eager | 0.553 s | 20,636 KiB | 320,205 B | — |
| 1,000 / streaming | 0.658 s | 13,456 KiB | 318,488 B | 962,560 B |
| 10,000 / eager | 6.475 s | 148,316 KiB | 2,620,118 B | — |
| 10,000 / streaming | 6.592 s | 21,136 KiB | 2,736,202 B | 10,477,568 B |
| 30,000 / streaming | 19.710 s | 22,600 KiB | 8,160,333 B | 32,288,768 B |

The 10,000-structure streaming file is about 4.4% larger than the eager
file, while the observed additional process peak is about one seventh as
large. From 10,000 to 30,000 structures, its peak growth rises only about
1.4 MiB while the temporary disk sort grows by about 21.8 MB. The 1,000-
and 10,000-structure streaming files pass independent full-record oracles for
selected unevaluated, evaluated-empty, nonempty, middle, and last frames,
and for atoms 0, 42, and 499 across the trajectory. All-stable and all-churn
1,000-structure files pass the same checks and select global and event-native
descriptors respectively. An empty file and labels first appearing in a
later block also passed focused readback checks. These results establish
feasibility of bounded-record construction for this fixture, not a proven
memory bound for arbitrary detector output or a larger-than-RAM trajectory.
The same blockwise construction and external posting sort can serve a
fixed-global writer; this experiment does not rank adaptive descriptors ahead
of the simpler global candidate by itself.

The writer requires sorted input and uses probe-specific fixed method,
measure fields, and source metadata. It has not been wired through the
required `ChunkedExecutor`, and it does not persist stable relation identity
between blocks or support parallel analyses and source-index maps. The
temporary SQLite sorter is safe to delete after a complete snapshot, but a
production writer needs failure cleanup, resumability rules, and a decision
on whether that scratch-disk cost is acceptable.

#### Large atom-index space and denser observations

The first 300,000-atom, 30,000-structure stable run exposed an avoidable
`O(n_atoms * n_blocks)` loop in the probe writer: for each block it built
full-length atom postings and scanned every atom to insert mostly empty
lists into the temporary sorter. It took 105.417 s despite only 218,969
observations. The writer now computes per-occurrence participant cardinality
directly and inserts postings only for atoms actually present in the block.
The identical input then took 18.010 s and produced the same 6,737,827-byte
HDF5 file and 1,149,343 postings. These are one run before and one run after,
not a controlled confidence interval. The algorithmic removal of the full
atom scan is the supported conclusion; the exact speed ratio is host-specific.
Small 100-structure/100-observation and 1,000-structure/eight-observation
fixtures pass independent record-oracle readback after the change.

```bash
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 30000 --atoms 300000 --per-frame 8 --distribution stable --block-size 100
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 10000 --atoms 300000 --per-frame 100 --distribution stable --block-size 100
```

**Benchmarked, 2026-09-29:** Linux, Intel Xeon E5-2630 v4, Python 3.13.14,
NumPy 2.4.6, h5py 3.16.0, SQLite scratch sorter; separate process and one
run per row. Peak RSS growth is after imports and before optional verification.
The stable fixture reuses a bounded relation pool. The second row uses
approximately 100 observations per nonempty structure and therefore tests
output density as well as the index-space dimensions.

| Atoms / structures / nominal observations per frame | Actual observations | Postings | Build | Peak RSS growth | HDF5 | Scratch SQLite |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 300,000 / 30,000 / 8 | 218,969 | 1,149,343 | 18.010 s | 21,412 KiB | 6,737,827 B | 34,734,080 B |
| 300,000 / 10,000 / 100 | 908,893 | 4,770,845 | 57.566 s | 44,268 KiB | 25,673,987 B | 148,217,856 B |

The higher-density file is still small relative to its event count because
this fixture has strong relation reuse, simple measures, and compressible
images. It is not representative of high-churn coordination or a detector
with thousands of observations per structure. These large runs did not use
an independent full-record oracle; only smaller fixtures with the same writer
path did. The temporary posting database grows faster than the final HDF5
file and must be budgeted, cleaned after failure, or replaced by a bounded
external merge/partition strategy. The prototype also builds per-block
`Interactions` objects eagerly and does not use `ChunkedExecutor`; its
observed peak does not establish a worst-case bound for arbitrary detectors.

The same one-pass writer was subsequently run with relation descriptors
generated afresh in every nonempty structure. Every block selected
occurrence-native descriptor encoding. A separate
1,000-structure/500-atom/eight-observation churn fixture
passed the independent full-record frame and atom query oracle after writing
and reopening its 367,076-byte file. The larger runs below did not retain a
full-record oracle; they test write cost, peak RSS, file size, and index output
under high churn, not complete public readback.

```bash
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 1000 --atoms 500 --per-frame 8 --distribution churn --block-size 100 --verify
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 30000 --atoms 300000 --per-frame 8 --distribution churn --block-size 100
python devtools/scripts/benchmark_interactions_streaming_writer.py --mode streaming --frames 3000 --atoms 300000 --per-frame 100 --distribution churn --block-size 100
```

**Benchmarked, 2026-09-29:** the same Linux/Xeon/Python/NumPy/h5py host and
one process per run; no repeated timing statistic. Initial RSS was about
79,100 KiB in each process. Observation counts follow the deterministic
fixture, including parallel observations. The high-density row has fewer
structures and must not be compared directly with the stable 10,000-structure
row above.

| Atoms / structures / nominal observations per frame | Actual observations | Postings | Build | Peak RSS growth | HDF5 | Scratch SQLite |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 300,000 / 30,000 / 8 | 218,969 | 1,149,274 | 25.319 s | 23,100 KiB | 12,660,097 B | 34,705,408 B |
| 300,000 / 3,000 / 100 | 272,589 | 1,429,736 | 30.312 s | 58,956 KiB | 14,606,834 B | 43,339,776 B |

The first churn file is 1.88 times the stable file for the same number of
observations and structures. This supports adaptive occurrence-native
descriptors as a bounded-memory route when relation reuse disappears; it does
not establish an optimal codec or a bound for hundreds of millions of
observations. Descriptor labels remain small in this fixture, and the scratch
sorter still scales with the number of atom postings.

#### Fresh-process readback of a streamed large file

The [streamed-read probe](../../devtools/scripts/benchmark_interactions_streamed_reads.py)
writes the churn fixture through the one-pass writer, replays the deterministic
fixture into an independent oracle retaining only requested frame and atom
signatures, and opens the finished HDF5 file in a new process for each query.
It compares complete roles, grouped participants, evidence, measures, images,
structure indices, duplicate occurrences, and evaluated coverage. Nine
sampled queries passed at both 1,000 structures/500 atoms and 30,000
structures/300,000 atoms, including unevaluated frame 0, evaluated-empty frame
1, nonempty frames near the beginning and end, one high-degree atom, and two
rare atoms. This extends semantic readback to the large streamed file without
retaining all 218,969 fixture records in the parent oracle.

```bash
python devtools/scripts/benchmark_interactions_streamed_reads.py --frames 1000 --atoms 500 --per-frame 8 --distribution churn
python devtools/scripts/benchmark_interactions_streamed_reads.py --frames 30000 --atoms 300000 --per-frame 8 --distribution churn --block-size 100
```

**Benchmarked and oracle-checked, 2026-09-29:** Linux/Xeon E5-2630 v4,
Python 3.13.14, NumPy 2.4.6, h5py 3.16.0; one run of each command, with no
timing statistic or deliberate page-cache eviction. `query_ms` includes HDF5
open, indexed selection, complete Python record decoding, and close, but
excludes Python process startup and digest construction. The HDF5 file was
12,660,097 B. The memory column is the new reader process's `VmHWM` increase
over its post-import baseline, read from `/proc/self/status`; an inherited
`ru_maxrss` high-water mark was unsuitable for this measurement.

| Request on 30,000-structure file | Returned observations | Query | Reader peak growth |
| --- | ---: | ---: | ---: |
| Unevaluated frame 0 | 0 | 7.3 ms | 5.4 MiB |
| Evaluated-empty frame 1 | 0 | 7.0 ms | 5.4 MiB |
| Nonempty frame 2 | 10 | 11.0 ms | 5.5 MiB |
| Nonempty frame 15,000 | 7 | 11.4 ms | 5.5 MiB |
| Nonempty frame 29,999 | 9 | 11.6 ms | 5.5 MiB |
| High-degree atom 0 | 82,665 | 2,576 ms | 108.0 MiB |
| Rare atom 42 | 5 | 35.7 ms | 7.8 MiB |
| Rare atom 299,999 | 3 | 27.3 ms | 7.4 MiB |

These are fresh-process reads, **not cold-disk reads**: the operating-system
page cache may be warm. The roughly 0.52-second process wall time for a small
query is mostly Python startup and imports, not the indexed file query. The
baseline high-degree query's time and memory include building a Python
`Counter` of 82,665 fully decoded signatures. The probe does not establish
worst-case RAM, cache-cold latency, or complete readback of every occurrence
in the file.

#### Typed ragged projection control

The [packed-reader probe](../../devtools/scripts/benchmark_interactions_packed_reader.py)
reads the **same file and atom index** into typed occurrence columns, ragged
participant and atom offsets, aligned image vectors, and the file's label
codes. It assembles one full query result without constructing a Python record
for each occurrence. After recording query time and peak memory, a separate
oracle adapter decodes those columns into complete signatures and compares
them with the plain-record fixture. The adapter's cost is excluded from the
typed query measurements. This tests a physical projection, not a standalone
public result class: labels and analysis metadata are still held by the
reader, and the output is eager.

The stable and churn fixtures each passed nine complete queries with both
readers at 1,000 structures. A mixed fixture passed the nine packed-reader
queries across a file with five global and five occurrence-native blocks.
The 30,000-structure churn file passed the same nine queries with each
reader. Each comparison below is one fresh-process run on the host and
dependency versions above; page cache may be warm. `VmHWM` growth is relative to
each reader's post-import baseline. `query_ms` includes file open, typed
selection or Python materialization, and close, but excludes process startup,
semantic oracle decoding, and digest creation.

| Request on 30,000-structure file | Observations | Python record reader | Typed projection | Typed payload |
| --- | ---: | ---: | ---: | ---: |
| Frame 2 | 10 | 10.8 ms, 5.5 MiB | 10.5 ms, 5.3 MiB | 1,552 B |
| High-degree atom 0 | 82,665 | 2,455 ms, 108.1 MiB | 1,207 ms, 36.4 MiB | 12,223,512 B |
| Rare atom 42 | 5 | 35.0 ms, 8.1 MiB | 35.2 ms, 8.0 MiB | 920 B |
| Rare atom 299,999 | 3 | 27.2 ms, 7.4 MiB | 27.4 ms, 7.6 MiB | 520 B |

For the high-degree atom, the typed projection reduced the measured query
time by about half and reader peak growth by roughly two thirds while
preserving the complete result. The process wall times were similar once the
typed result was **also decoded into Python records for verification**; clients
that request Python records still pay that cost. The 12.2 MB numeric payload
does not include NumPy array objects, HDF5 caches, or metadata. Low-result
queries are dominated by opening the file and touching blocks, so the new
projection brings no measured speed benefit there. The next implementation
gate is a persistent public reader with self-contained typed views, bounded
batch iteration for results larger than RAM, and cache-cold measurements
against client latency budgets.

#### Structure selections and atom-set queries on the typed reader

The packed-reader probe now also selects an explicit list of **source
structure indices** in first-appearance order, dropping duplicate requests
without losing evaluated-empty coverage. It queries an atom set by unioning
its direct atom-to-occurrence postings. Counts of distinct selected atoms are
compared with the stored distinct participant-atom cardinality to distinguish
`incident`, `internal`, and `cross`; every atom of a compound ring participant
is included. Two-set queries intersect the two posting unions and can require
that all participant atoms belong to their union. The result is reordered by
the requested structure sequence without expanding observations into Python
records. These are source indices, not atom or structure IDs.

The [selection oracle](../../devtools/scripts/benchmark_interactions_packed_selection.py)
compares complete decoded records, coverage, structure order, and empty array
shapes/types for 15 queries on each of three 1,000-structure/500-atom
fixtures. The queries include one frame, repeated and nonconsecutive frames,
an unevaluated frame, an evaluated-empty frame, one atom, ring-atom subsets,
all three set modes, two disjoint sets with and without exclusivity, two
overlapping sets, and an unrestricted control. All 45 comparisons passed on
2026-09-29; each fixture has 7,294 observations. The stable file selected 10
global descriptor blocks, the mixed file five global and five
occurrence-native blocks, and the churn file 10 occurrence-native blocks. The
three query planners described below produced 31 matching checks per
distribution, 93 in total. A separate 40-structure fixture passed 22 checks
with one atom repeated in two participants, overlapping compound groups, two
parallel observations of the same relation in one structure, and an
evaluated-empty structure. These are storage and query edge cases, not claims
that the synthetic relations are chemically valid.

```bash
python devtools/scripts/benchmark_interactions_packed_selection.py --distribution stable
python devtools/scripts/benchmark_interactions_packed_selection.py --distribution mixed
python devtools/scripts/benchmark_interactions_packed_selection.py --distribution churn
```

This is **oracle-checked prototype behavior**, not an accepted public query
contract or a large-set latency measurement. The probe treats an atom in the
intersection of two query sets as touching both sets; whether that overlapping
set rule is useful to clients remains open. For a narrow frame request with a
high-degree atom, an atom-first plan still reads that atom's full trajectory
posting list before filtering frames. The reader now also offers a frame-first
plan and a provisional automatic choice; their cost is measured below. A
production reader must provide an iterator or lazy view for results that exceed
memory and preserve the same source-index and coverage semantics.

#### Choosing the first index for a combined query

The [query-planner probe](../../devtools/scripts/benchmark_interactions_frame_first.py)
requests source structures in the order `[last, 2, middle, 10, 2, 1, 0]` and
restricts results to atom 0. The repeated frame is returned once; frame 1 is
evaluated with zero observations, and frame 0 is unevaluated. A frame-first
plan reads those frames' occurrence slices and counts distinct participant
atoms within them. An atom-first plan reads atom 0's postings across the
trajectory and then applies the frame restriction. Both return identical
complete typed results, checked against a streaming plain-record oracle. The
automatic plan compares the number of candidate frame occurrences with the
atom-posting count; this is a provisional cost rule, not a client latency
guarantee.

```bash
python devtools/scripts/benchmark_interactions_frame_first.py --frames 1000 --atoms 500 --distribution mixed --repeats 3
python devtools/scripts/benchmark_interactions_frame_first.py --frames 30000 --atoms 300000 --distribution churn --repeats 3
```

**Benchmarked and oracle-checked, 2026-09-29:** same Linux/Xeon E5-2630 v4,
Python 3.13.14, NumPy 2.4.6, and h5py 3.16.0 host; three fresh processes per
plan, with no page-cache eviction. Times are medians of file open plus complete
typed selection, excluding Python startup, file close, and oracle decoding.
Peak growth is the median increase in the child process's `VmHWM` before
oracle decoding. The 1,000-structure mixed file returned 14 observations and
the 30,000-structure churn file returned 13.

| Fixture | Frame-first | Atom-first | Automatic | Typed payload |
| --- | ---: | ---: | ---: | ---: |
| 500 atoms / 1,000 structures | 22.9 ms | 48.5 ms | 23.3 ms | 2,112 B |
| 300,000 atoms / 30,000 structures | 28.8 ms, 8.0 MiB | 1,233 ms, 12.1 MiB | 29.3 ms, 7.8 MiB | 1,864 B |

On the large fixture the frame-first plan was about 43 times faster for this
narrow selection because it avoided decoding the high-degree atom's history
across unrelated structures. This does not imply frame-first wins when many
structures are requested or an atom has few postings; the automatic rule is
only a first control. The reader still constructs one eager result and has no
measured cache-cold behavior. A production query planner should compare both
candidate sizes without scanning the trajectory, retain bounded caches, and
be tested with wider frame and atom selections from clients.

### Fixed-shape family codec with complete payload

The [specialized-family probe](../../devtools/scripts/benchmark_interactions_specialized_bound.py)
compares a global relation descriptor dictionary with a second complete HDF5
file in which relations are grouped by interaction kind, participant roles,
and participant atom counts. It stores one fixed atom matrix per family plus
the family schema and relation-to-family/local maps. Both files contain the
same frame-major occurrences, evaluated coverage, evidence, measures, image
vectors, source metadata, and atom postings. Readback checks compare every
typed common/index array, the stored family schema, every relation's kind,
roles, and atom indices, and occurrence-to-relation IDs. Thus the file-size
comparison includes the full payload used by this synthetic fixture, while
the optimistic numeric bound excludes schema and HDF5 metadata.

```bash
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 1000 --distribution stable --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 1000 --distribution mixed --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 1000 --distribution churn --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution stable --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution mixed --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution churn --file-probe
```

**Benchmarked, 2026-09-28:** same Linux/Xeon/Python/NumPy/h5py host as
above, 500 atoms, eight nominal observations per evaluated structure, four
fixed-shape synthetic families. One file write per row; full-load time is the
median of five same-process reopened reads of all common, index, and
descriptor datasets with a likely warm operating-system cache. This is a
codec/load probe, not a file-backed selection benchmark.

| Structures / distribution | Relations | Global file | Family file | Family saving | Optimistic full numeric saving | Global / family full load |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1,000 / stable | 120 | 257,137 B | 272,474 B | −5.96% | 0.51% | 7.82 / 8.94 ms |
| 1,000 / mixed | 3,655 | 321,015 B | 318,567 B | 0.76% | 11.71% | 9.39 / 9.99 ms |
| 1,000 / churn | 6,946 | 378,104 B | 361,005 B | 4.52% | 18.04% | 10.30 / 10.74 ms |
| 10,000 / stable | 120 | 2,043,547 B | 2,058,884 B | −0.75% | 0.05% | 35.69 / 36.79 ms |
| 10,000 / mixed | 33,469 | 2,634,035 B | 2,469,749 B | 6.24% | 11.06% | 45.69 / 44.63 ms |
| 10,000 / churn | 66,053 | 3,215,951 B | 2,868,732 B | 10.80% | 17.62% | 54.05 / 50.94 ms |

The actual file benefit is smaller than the numeric upper bound because
compression already removes some redundant global descriptor bytes and the
specialized file adds family datasets and maps. This rules out fixed-shape
families as an unconditional codec: stable reuse loses disk space. It keeps
family coding alive as a selective physical optimization for relations with
high churn. The logical interface and general ragged fallback remain needed
for variable ring size, coordination groups, and other many-body roles.
Mixed-family frame/atom query speed, edits, bounded construction, and a
real detector distribution have not been established. The result does not
replace the global relation identity or promote one fixed-arity class per
interaction type into the public API.

A later [variable-group control](../../devtools/scripts/benchmark_interactions_specialized_bound.py)
changes each ring group deterministically to five, six, or seven atoms while
preserving relation reuse. The four original family shapes become twelve
method/role/size families. It checks all reconstructed relation participants,
the complete typed common/index arrays, and HDF5 readback against the global
descriptor file. Both files retain all occurrence fields and atom postings.

```bash
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution stable --variable-groups --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution mixed --variable-groups --file-probe
python devtools/scripts/benchmark_interactions_specialized_bound.py --frames 10000 --distribution churn --variable-groups --file-probe
```

**Benchmarked, 2026-09-29:** same Linux/Xeon/Python/NumPy/h5py host; one
fixture and file write per row. Full-load medians are five same-process warm
reopens, not selected-query timings. At 10,000 structures the specialized
file was 2.02% larger than global under stable reuse, 4.55% smaller on mixed
input, and 9.11% smaller under churn. Global/specialized full-load medians
were 41.22/43.61, 48.64/50.25, and 55.28/56.34 ms respectively. More
group-size families narrow the mixed/churn file saving compared with the
fixed-six-ring fixture and make the stable case worse. This retains family
coding as a selective physical codec, not an unconditional result schema.
Method-specific mixed-family frame/atom query latency and a bounded writer
still need measurement before promoting this optimization.

### Structural and occurrence-edit semantics probe

The [structural-edit probe](../../devtools/scripts/benchmark_interactions_structural_edits.py)
uses the flat HDF5 snapshot and committed full-frame overrides as a base. A
separate prototype view keeps current-to-storage structure and atom index
maps, plus appended structures. It checks every stage against independently
transformed plain records and evaluated coverage, including nonconsecutive
structure requests, individual structures, and atom queries across the
trajectory. It deliberately distinguishes **dropping a structure**, which
renumbers subsequent structure indices, from **invalidating an evaluation**,
which leaves the structure index space in place but removes its evaluated
coverage and observations.

```bash
python devtools/scripts/benchmark_interactions_structural_edits.py
```

**Oracle-checked prototype, 2026-09-28:** the 1,000-structure,
500-atom, 7,294-observation mixed full-field fixture. The probe performs:

1. Removal of exactly one of two distinguishable parallel observations in
   structure 2, retaining the other via a complete-frame replacement.
2. Addition of a previously absent hydrogen-bond relation and observation in
   that same structure, again via replacement.
3. Deletion of structure 2 from the molecular-system index space, dropping its
   observations and mapping every later current structure index to the prior
   storage index without rewriting the base occurrence table.
4. Deletion of atom 41, pruning every interaction containing it and mapping
   surviving atom indices to the smaller current atom space.
5. Appending a new evaluated structure with one interaction of a type not in
   the base snapshot, held in the prototype's in-memory append layer.
6. Invalidating structure 10's evaluation without deleting that structure.

After each operation, frame and atom queries match the plain-record oracle.
The final result has 7,180 observations and 964 evaluated structures; an
independent `Interactions.from_records` reconstruction also accepts the
resulting 499-atom, 1,000-structure index space. The maps are small in
principle: two `int64` current-to-storage arrays at this size have a 11,992 B
raw lower bound. The prototype actually uses Python lists and dictionaries,
so this number is **not** its resident memory measurement. Single-run Python
map updates were about 0.12 ms each; no latency or complexity guarantee
follows from that sample.

This demonstrates that physical structure and atom deletion can be expressed
without recomputing unaffected interaction geometry or immediately rewriting
every occurrence. It does **not** implement public `add`/`remove` methods,
persist the index maps or appended structure, maintain stable external
occurrence handles, or recover interrupted writes. The HDF5 override uses an
existing interaction type/role/evidence label table; introducing a new type
into an existing stored structure still needs an extensible label schema.
Atom deletion also cannot guarantee that chemical assignments on surviving
atoms remain scientifically valid; detector-specific invalidation is a
separate rule. Further tests must cover repeated deletions and insertions,
reordering, source-system extraction, compaction, and round-trip remapping.

The [repeated-remap control](../../devtools/scripts/benchmark_interactions_remap_roundtrip.py)
extends that experiment with two atom deletions, two structure deletions,
structure reordering, atom reordering, insertion of an evaluated-empty and an
unevaluated structure, typed HDF5 map save/load, and a compacted standalone
`Interactions` save/load. It keeps two distinct parallel observations of the
same relation and checks every stage against independently transformed plain
records. After the edits the current index space has 498 atoms, 1,000
structures, 964 evaluated structures, and 4,547 surviving observations.
The original flat file used 320,205 B; adding typed current-to-storage maps,
appended-empty and invalidated-frame arrays made it 336,309 B. Compaction to
a new standalone result used 164,147 B after the atom deletions pruned many
observations. These sizes compare different logical contents after edits, so
the compaction number is **not** a compression advantage for one unchanged
dataset.

```bash
python devtools/scripts/benchmark_interactions_remap_roundtrip.py
```

**Oracle-checked prototype, 2026-09-29:** same Linux/Xeon/Python/NumPy/h5py
host. The typed map round trip covers evaluated-empty and unevaluated inserted
structures, original-index remapping, and repeated deletion/reordering without
redetecting unaffected geometry. It does not persist a newly appended
nonempty structure or exact external occurrence handles, implement an atomic
edit transaction, or define view lifetime after mutation. The compacted file
is rebuilt from transformed records to test semantics, not by a streaming
in-place compactor. Those remain explicit production gates.

### Evaluation outcome and decision boundary

**Comparative evaluation concluded, 2026-09-29; implementation remains open.**
Select a single logical `Interactions` contract with typed relation
participants and roles, sparse structure-indexed occurrences, explicit
evaluated coverage, source-index maps, measurements, evidence, and periodic
images. For the general large-system snapshot, implement bounded frame-major
blocks and direct atom-to-occurrence postings. Encode relation descriptors
globally when reuse is high, or block-locally/occurrence-native when churn
makes a global dictionary wasteful. Build and read those indexes without
holding the trajectory in Python objects. This is a choice of architecture,
not a claim that the current eager class or benchmark writer meets it.

The choice follows the complete-field semantic oracle, sparse index and file
query probes, editing probes, and the stable and churn streaming controls
above. A frame-major layout gives direct structure slices; a sparse inverse
index gives atom queries without scanning all structures. The adaptive block
probe kept its observed record working set bounded on 300,000 atom inputs and
selected different descriptor encodings according to relation reuse. The
typed HDF5 experiments demonstrate a standalone, versioned route compatible
in principle with later H5MSM inclusion. They do not establish production
atomicity, a stable H5MSM schema, or cold-read latency at client scale.

Dense tensors and pair-matrix formats are excluded as the general result:
their size follows possible pairs and they cannot represent arbitrary grouped
participants without a second schema. Python object graphs, ordinary
dictionary-of-occurrence stores, SciPy/PyData sparse pair arrays, PyTorch and
TensorFlow sparse tensors, and NetworkX graphs remain useful views or
specialized computations, but the measured or structural evidence does not
support any as the canonical general store. The winning design uses small
dictionaries for metadata and transient lookup, not one dictionary or object
per stored observation. A temporal run codec, fixed-family codecs, SQLite
editing sidecar, and compiled query kernels stay optional candidates behind
the same logical contract; the probes identify workloads where each may win.

Reopen the storage choice if a complete client workload, with the same roles,
groups, provenance, coverage, source maps, duplicate observations, and query
semantics, shows that another design materially improves both relevant
resource costs or delivers a required operation this baseline cannot. Compare
resident and construction RAM, file and scratch bytes, cold and warm complete
queries, local edits, and compaction; no isolated pair-only or raw-array
microbenchmark can overturn the full-result decision by itself. At 300
million observations, even four-byte atom postings alone would require
multiple gigabytes, so the present sub-million synthetic controls do not
establish performance at the stated upper output scale.

The **evaluation phase** of `uibcdf/molsysmt#251` is complete. The proposal
remains `partial` until client review settles the public logical contract and
durable rules move into a normative document. `uibcdf/molsysmt#252` tracks
the experimental implementation; the observed evaluated-empty Buch detector
failure is tracked independently as `uibcdf/molsysmt#253`. The gates below
belong to production implementation and possible targeted revisions of the
physical design; they are not a reason to restart the broad candidate survey.

### Next discriminating gates

1. Generalize the one-pass adaptive writer to detector output and the
   maintained `ChunkedExecutor` path. Its scratch posting index scales with
   output size on disk, while its record memory is block-bounded on the
   measured fixture. Persist cross-block relation identity and
   compare projected raw bytes with compressed file bytes. Test high-reuse, high-churn,
   mixed-phase, group-heavy, and duplicate-observation inputs, including held-out
   phase boundaries. Keep a stable logical result interface across layouts.
2. Add direct atom-to-occurrence postings and distinct-atom cardinalities as
   optional, lazily built indexes in the public reader. The file probes now
   check `incident`, `internal`, `cross`, two-set queries, high-degree atoms,
   ring groups, repeated atoms in participants, nonconsecutive frame requests,
   and empty coverage. Extend these checks to wider atom sets, source remaps,
   and bounded result construction.
3. Use the tested temporary external sorter or another bounded index builder
   in a production chunked route. Measure peak process RSS separately from
   steady-state numeric bytes. Verify a trajectory larger than available RAM,
   including hundreds of thousands of atoms, tens of thousands of structures, and a
   high-output detector case. The synthetic 300,000-atom controls cover only
   about 0.22 and 0.91 million occurrences, not hundreds of millions. Compare
   projected HDF5 reads, bounded caches,
   and flat extendible datasets for complete structure-index and atom queries,
   including independent-process cold reads. The first selective field/row
   reader passed the oracle but remains slow for small results because it makes
   many per-block HDF5 calls. A fixed-width compact-record control halved
   those calls but still trails SQLite on sampled small queries. A separate
   large streamed file passed nine sampled fresh-process oracle queries per
   reader. A complete typed projection cut high-degree atom peak growth from
   108 to 36 MiB and query time from 2.45 to 1.21 s, but remains eager and
   probe-only. Fifteen complete selection queries passed each of stable,
   mixed, and churn files, including nonconsecutive frames and atom sets.
   A frame-first probe reduced one narrow high-degree query from 1,233 to
   28.8 ms; its automatic choice needs broader workloads. Test persistent
   typed views, bounded batch iteration, alternative query plans, and
   cache-cold reads without loading all relations or occurrences.
4. Specify and test an atomic frame-replacement journal: version marker,
   recovery after interrupted writes, live override selection, repeated-edit
   compaction, and HDF5/H5MSM compatibility boundary. Compare frame and block
   replacement over many edits, including an evaluated frame becoming empty.
   The prototype demonstrates pending/committed logical visibility and
   repeated full-frame replacements, but not crash recovery or compact journal
   metadata. Compare native mutable maps and a transactional indexed row store
   under the same edit sequence; define the lifetime of pre-edit query views.
5. The typed map probe now checks repeated atom/structure deletions,
   reordering, evaluated-empty and unevaluated insertions, save/load, and
   semantic compaction while retaining parallel observations. Turn that into
   a public edit contract with exact external occurrence handles, persisted
   nonempty appends, atomic recovery, view lifetime, and source-system
   extraction. Define which chemical assignments require recomputation after
   an atom edit, and obtain consumer feedback before fixing the public class.
6. Ask graph-analysis clients whether they need an explicit per-structure
   graph or hypergraph projection, and define what a pairwise projection means
   for many-body interactions before exposing one as a public convenience.
7. The full-field temporal file now covers mixed persistence, parallel
   observations, sparse evaluated coverage, and the complete payload. Warm
   file-backed frame and atom queries have independent record oracles on
   synthetic and one bundled detector trajectory. Next compare compiled
   batch frame queries, cold reads, bounded relation caches, edits, and a
   selective frame/run hybrid. A native kernel must pass through the existing
   PyO3 extension boundary before deciding whether the public object itself
   should be native.
8. Test whether specialized pair/triple/group blocks save enough total RAM and
   disk bytes to justify their codec and query-merge complexity, including
   method-defined roles and a mixed-family request.
9. A four-method collection and grouped HDF5 storage probe now preserve
   per-analysis coverage, provenance, and source-index queries, and quantify
   shared-map/file-metadata savings. Next test cross-method queries, edits,
   and actual H5MSM or standalone grouped-file loading with a client use case.
   The observed storage saving alone does not require a combined public
   `Interactions` object.

The numeric probes support these gates; they are not a substitute for them.

Compare candidates on the same contract fixtures and representative workloads:
one frame, arbitrary nonconsecutive frames, one atom across a trajectory, two
atom sets, ring groups, mostly stable and mostly changing relations, empty
evaluated frames, local replacement after a coordinate edit, atom deletion and
remapping, and file-backed reading. Record construction peak RAM, steady-state
RAM, disk bytes, cold/warm query latency, edit latency, and compaction cost.
Include source maps, multiple methods, and periodic images in the comparison;
an apparent speedup that drops those fields does not satisfy the contract.

Streaming writes accept sorted, unique evaluated structure indices in bounded
chunks, including frames with zero observations. Relation IDs must stay stable
across chunks. Large analyses should use the maintained `ChunkedExecutor` path.
File-backed `open` must read frame slices lazily rather than loading the full
trajectory into memory.

### Serialization and molecular-system lifecycle

Define a versioned, typed payload independent of its container. Prototype a
standalone file with flat numeric arrays, offsets, metadata, explicit unit
strings, coverage, and optional indexes. Ragged HDF5 object or variable-length
arrays are not the default. Round trips must preserve roles, source maps,
evidence, measures, images, and empty evaluated frames. Incompatible versions
must fail clearly.

H5MSM 0.4 has no interactions layer. H5MSM 0.5 must add the explicitly
versioned interaction layer and separate topology, chemical states, and
structures at the root without silently reinterpreting 0.4 files. A `MolSys`
read from H5MSM must recover its attached interactions; writing or extracting
a subset must preserve and remap compatible observations or explicitly
invalidate them.

### Native and H5MSM integration checkpoint (2026-09-29)

Source inspection identifies four paths that must agree before an attachment
can be called implemented:

| Path | Current behavior | Required decision and check |
| --- | --- | --- |
| Native `MolSys` | `native/molsys.py` owns topology, structures, mechanics, and the structure-to-state map. `copy`, `extract`, `remove`, `add`, and `append_structures` have no interaction hook. | Define a named collection of zero or more method-specific results, ownership and view lifetime, axis checks at attach time, and propagation or explicit invalidation for each operation. A single monolithic multi-method result is not required. |
| Native and form mutation | `form/molsysmt_MolSys/append_structures.py` can append directly to `to_item.structures`; form setters and direct access to `molsys.structures` can modify data without entering a `MolSys` edit method. | Inventory every public mutation route. An attached observation must not silently survive a change that can invalidate its scientific evidence. Define frame-local invalidation where the changed scope is known and an explicit fail-closed rule otherwise. Direct mutable-array access needs a documented and tested ownership rule; a generation counter alone cannot detect an in-place NumPy write. |
| H5MSM write/read | `form/molsysmt_MolSys/to_file_h5msm.py` writes topology and structures; `form/molsysmt_H5MSMFileHandler/to_molsysmt_MolSys.py` reconstructs only those domains. The handler writes version 0.4 and accepts 0.3/0.4. | Give the interaction layer an explicit format feature/version, encode named analyses as typed datasets, and round-trip coverage, source maps, roles, measures, units, evidence, and images. A file without the layer stays valid. Unknown interaction schema versions fail visibly. |
| H5MSM subset | The 0.4 `file_h5msm.extract` path materializes a full `MolSys`, extracts it, and rewrites it. | Preserve or remap interactions during file selection. For large trajectories, select interaction blocks directly without loading the whole trajectory or every interaction into RAM. An old writer must not rewrite a file carrying an unknown interaction layer and silently discard it. |

The version choice is now H5MSM 0.5 with four optional root layers. The
0.4.1 extension candidate is withdrawn because it would postpone the agreed
independent chemical-state layer. New readers must accept legacy 0.3/0.4 and
the new 0.5; old readers reject 0.5 explicitly. The interaction payload keeps
its own schema version within 0.5. This is an accepted target, not an
implemented format. Conversion and subset/append paths must handle the
modular root, including chemical-state-only and interaction-only files.

`MolSys` should hold optional named results, including file-backed results,
without forcing all observations into memory. Copying a system should share
immutable result storage or make an explicitly bounded copy. Extracting atoms
or structures must preserve a local-to-origin index map and evaluated-empty
coverage; removing atoms prunes affected relations and remaps surviving ones
without rerunning unrelated detectors. Appending structures leaves new frames
unevaluated unless corresponding results are supplied. Adding atoms or changing
chemistry/coordinates needs a scoped invalidation rule before the result can
be queried or serialized as current evidence. These are target semantics, not
claims about the experimental class.

The current `file:h5msm -> MolSys` converter closes its handler before
returning. A file-backed interaction result cannot borrow that closed handle;
it must own a reopenable source or an independently managed handle with an
explicit close/lifetime contract. Query views must remain valid under that
contract, or fail clearly after close. A default `MolSys` read may materialize
small results, but the required large-trajectory path must load only metadata
and selected interaction blocks.

The integration test matrix must include: no interaction layer; an attached
analysis with zero observed interactions but evaluated frames; two analyses
with different coverage and method parameters; triples and grouped
participants; nonconsecutive and repeated structure requests; atom deletion
and index remapping; local geometry and chemistry edits; periodic images and
unit-bearing measures; an old reader rejecting the new root version; an
unknown interaction payload version; direct H5MSM subset round trips; and
file-backed queries over a trajectory too large to load eagerly. The tests
must compare the same source indices and values through standalone result,
native `MolSys`, H5MSM, and MolSysViewer paths where applicable. A separate
performance run records peak resident memory, disk size, write throughput,
and cold and warm query latency at the intended atom/structure scale.
Extraction, atom reorder, and structure subset must remap every reference and
coverage index or explicitly invalidate the result. A source fingerprint may
detect stale results, but its algorithm needs its own tests. Cross-system
interactions, symmetry mates, and structure intervals require explicit
identities before entering a first codec version.

### Incremental edits and source changes

A result must eventually support adding and removing occurrences without
rerunning analysis over unaffected structures. Moving a small molecule in
structure 10 requires an atomic replacement of the observations involving its
atoms in structure 10: remove old observations in that scope, add newly
classified ones, and keep coverage for structure 10 explicit. A new participant
set creates a relation; an occurrence involving an existing set reuses its
relation. Deleting the last occurrence of a relation may leave an orphan until
compaction, but queries must never expose it as an observation.

Compiling the container does not change the insertion cost of a packed
`Vec`/NumPy array or a temporal run array: inserting near the beginning still
moves later entries, and deleting an interior occurrence can split a run.
Native code can make the *query and update algorithms* efficient, but it
cannot make a read-optimized frozen representation intrinsically mutable.
These physical choices must be compared behind the same public semantics:

| Candidate editing state | Local update strength | Cost to measure |
| --- | --- | --- |
| Native mutable maps and adjacency/posting sets | Direct add/remove by structure and atom; convenient for many edits. | Per-entry allocator and hash/tree overhead; typed HDF snapshot still needs packing. |
| Immutable compact base plus mutable per-structure overlay | Small edits touch affected structures and preserve compact base. | Queries merge layers; long edit histories need compaction and atomic persistence. |
| Replaceable immutable structure blocks | Edits rewrite one bounded block; simple reader snapshot. | Repeated relation definitions, block metadata, and cross-block indexes. |
| Relation-major temporal runs plus exceptions | Persistent relations compress well; add/remove may extend, shorten, split, or merge one run. | Packed run arrays still need shifting or an overlay; duplicates need an exception route. |
| Transactional indexed row store | Local disk edits and rollback are built into the store. | Disk and RAM index overhead, H5MSM export, and query latency. |

The user-facing editor should distinguish five operations rather than expose
only a generic mutation:

1. Add or remove exact occurrences in an evaluated structure. Parallel
   observations of one relation and structure require an unambiguous
   occurrence handle or an exact selection rule; `(structure_index,
   relation_index)` alone is insufficient.
2. Atom-scoped replacement for a changed ligand: delete only observations
   incident to the chosen atom set in one structure, insert newly detected
   observations, and commit the change as one transaction. Unaffected
   structures must not be scientifically recomputed.
3. Append source structures, marking each new structure explicitly as
   unevaluated or evaluated with zero or more observations. Appending to an
   ordered source index space can extend coverage and occurrence columns.
4. Remove or reorder structures: delete their observations and coverage, then
   remap surviving positional structure indices against the transformed
   molecular system. Internal stable handles can defer array relocation but
   cannot silently change the public source-index meaning.
5. Remove atoms: use an atom-to-relation/occurrence index to prune every
   affected observation, including a whole grouped participant such as a
   ring, then remap surviving positional atom indices or invalidate the
   result. Adding an atom does not create scientifically classified
   interactions until the relevant detector runs.

The existing experimental `Interactions` implementation has no incremental
mutation API; its query views share parent arrays. A mutable version must
define whether existing views are immutable snapshots, live views, or become
invalid after a commit. An epoch/generation check or copy-on-write snapshots
could prevent stale views. The same rule applies to native PyO3 ownership:
storing `Vec` inside a Rust class may simplify internal edits, but does not
decide external view lifetime or persistence.

Contiguous sorted occurrence arrays cannot support arbitrary insertion or
deletion in constant time. The candidate design is a compact immutable base
plus a small per-structure edit layer, followed by explicit compaction or a
new snapshot. The edit layer needs atom and frame indexes of its own and must
honor the same query order and `incident`/`internal`/`cross` semantics. Its
memory and query overhead must be measured against full reconstruction. This
is a design candidate, not an implemented mutation API.

Removing atoms from the source system has two distinct effects. Relations
touching removed atoms can be dropped without scientific recalculation of
unaffected observations. Surviving participants must then be mapped from old
to new positional atom indices with an explicit map; otherwise the result must
be invalidated. An algorithm whose assignments depend on the removed chemical
environment may need a wider recomputation scope, which the method provenance
must state. The required `MolSys` attachment cannot silently keep stale results.

The editor contract must decide stable identity for individual occurrences,
duplicate handling, relation-ID changes after compaction, atomic failure and
rollback, and whether adding a new method/family creates a separate analysis
block. It must distinguish an evaluated structure with all observations
removed from a structure whose analysis is now invalid.

### MolSysViewer review gate before client implementation

MolSysMT must present a runnable candidate to the developers of
`uibcdf/molsysviewer#114` before they start the MolSysViewer interaction
module and before this result API is stabilized. The review packet will name
the exact MolSysMT commit and provide:

1. a small fixture with hydrogen-bond triples, two compound ring
   participants, a disulfide candidate, parallel observations, variable
   per-structure counts, an evaluated-empty structure, and an unevaluated
   structure;
2. public calls for one structure, repeated and nonconsecutive structure
   indices, one atom across a trajectory, `incident`/`internal`/`cross`,
   `between(A, B)`, and named analyses attached to `MolSys`;
3. expected typed outputs, local-to-source index maps, atom search scope,
   method and evidence provenance, measurement units, and periodic images;
4. a native versus H5MSM-loaded result comparison, including extraction and
   an edited or invalidated structure;
5. measured memory, disk size, frame-query latency, atom-history latency,
   and bounded read/write behavior on a large trajectory.

Ask the MolSysViewer developers whether the public result and query views
provide everything their `view.interactions` module needs, whether the
compound-participant and three-role hydrogen-bond semantics are usable, and
whether their intended interaction lifecycles expose a missing query or
provenance field. In the same review, ask how they would consume the H5MSM 0.5
representation of those results:

- whether loading named analyses through `molsysmt.h5msm.read_layers` meets
  their expected memory and latency budget, or whether they need a public
  file-backed query for one frame, nonconsecutive frames, or an atom across a
  trajectory;
- whether they prefer `read_layers` for a named analysis or
  `read` to reconstruct an interaction-only file as a partial native `MolSys`;
- whether the file-loaded result preserves every index map, role, unit,
  periodic image, provenance field, and evaluated-empty versus unevaluated
  distinction needed for display and selection;
- what should happen in their workflow when a file lacks an interaction layer,
  contains an empty layer, carries an unsupported interaction schema, or the
  molecular system is extracted or edited;
- which realistic trajectory sizes and access patterns should set the
  acceptance measurements for public H5MSM reads, file size, and resident
  memory.

This is one consumer review of the result and its persistence boundary, not
two independent approvals. MolSysMT retains ownership of the H5MSM schema;
MolSysViewer's concrete usage determines whether the pre-1.0 public access
route is sufficient. Record their concrete examples, measured objections, and
any agreed contract changes in the linked issues. Do not treat silence or a
passing MolSysMT-only test as client acceptance. Keep the API Experimental
until the feedback has been reconciled and a MolSysViewer integration smoke
passes. Other clients can review the same logical contract later; their
integration is not a MolSysMT 1.0 gate.

### Decision sequence

1. Complete a runnable MolSysMT candidate with the query, edit, MolSys, and
   H5MSM paths needed for the review packet above. Add the selected lazy
   indexes and bounded file reader/writer, measure cold and warm queries,
   memory, and serialized size on representative trajectories. Keep
   provisional choices visibly Experimental.
2. Review that candidate with `uibcdf/molsysviewer#114` before their module
   implementation and before stabilizing MolSysMT's result API. Consult
   TopoMT, PharmacophoreMT, and DockingMT when their integrations are
   scheduled; they do not gate MolSysMT 1.0. If the contract becomes
   suite-wide policy, open a linked MolSysSuite coordination issue under its
   ownership rules.
3. Settle the open choices and write the accepted contract in a normative
   `devguide/` document. Close this design issue only then.
4. Recheck pair, triple, group, parallel-observation, source-map, and
   coverage cases against the accepted contract. Add detector `output_type`
   adapters without silently changing existing defaults; stabilize the API
   only after resolving review feedback.
5. Verify MolSysViewer's concrete structure and atom queries against the
   public result and integration path before 1.0.

Steps 1, 4, and 5 require tracked implementation work under #252 and the MolSysViewer
consumer issue. They are pre-1.0 gates, subject to the accepted contract and
measured performance targets.

## Why

[`interactions_api.md`](../interactions_api.md) records method-specific
hydrogen-bond and disulfide outputs; the generic result class remains
experimental. The
[`#250 proposal`](organize_interaction_detection_by_family_before_1_0.md)
requires a minimum shared result contract but leaves its schema open.
`uibcdf/molsysviewer#114` requests fast nonconsecutive frame and atom queries,
sparse storage, evaluated-empty state, provenance, and typed serialization.
The [attribute-centric proposal](attribute_centric_molecular_system_model.md)
sketches definitions, participants, and occurrences; its broader architectural
changes remain separate. Native attachment is required before 1.0, while instances
without evaluated interactions remain valid.

## What is measured and what is assumed

- **Inspected:** current interaction methods have method-specific outputs and
  H5MSM 0.4 has no interactions layer.
- **Measured:** the pair-site storage, shared-field layout, local edit,
  file-backed block, graph, temporal-index, complete-query, and SQLite
  transactional-row probes, plus the experimental class benchmark in #252.
  Plain-record probes check source mapping and edit semantics; a bundled
  pentalanine hydrogen-bond trajectory probes a real geometry distribution.
  The benchmarks ran on one host and do not establish production behavior at
  the upper output scale.
- **Consumer request:** `uibcdf/molsysviewer#114` describes the query,
  sparsity, provenance, and serialization needs above. Equivalent needs of
  other consumer teams are plausible but unconfirmed.
- **Selected implementation target:** frame-major typed blocks, adaptive
  descriptors, and sparse atom postings. The public reader, writer, and edit
  implementation still require complete-workload measurements.
- **Estimate:** an independent in-memory result can precede H5MSM integration.
  This is an architectural ordering, not a delivery-date claim.

## What was refuted

- One global relation dictionary is not uniformly smallest: the event-native
  encoding used fewer bytes with 93,962 distinct relations among 94,255
  observations in the shared-field probe. Conversely, event-native descriptors
  repeated too much information when the same 400 relations recurred.
- A direct atom index does not require a slow per-occurrence membership loop
  for `internal` and `cross`: counting selected-atom postings against stored
  participant cardinalities gave equivalent answers at much lower latency.
  This refutes the initial reason for requiring two indexes in every result.
- An unbounded append-only HDF5 edit journal is not space efficient for
  repeated local changes; 20 tiny versions added about 0.94 MB in the edit
  probe. Compaction and transaction semantics are design requirements.
- One subclass per family would multiply query and codec contracts. Revisit it
  if different family lifecycles or specialized storage prove valuable; the
  shared logical interface should still be tested across families.
- A dense atom-pair matrix per frame scales with possible pairs and cannot
  represent triples or groups directly.
- A sparse pair matrix or fixed-rank tensor does not by itself preserve
  variable-arity participants, roles, multiple methods or images for the same
  atom pair, evidence, and evaluated-empty coverage. An atom-by-relation or
  structure-by-relation sparse matrix is a useful secondary index or explicit
  projection, not the sole domain object. The current NumPy offset arrays
  already implement the relevant compressed sparse relationships without a
  new hard dependency. A SciPy or multidimensional sparse adapter should be
  considered only for a measured client operation with defined collapse rules.
- Lists of Python objects per occurrence inflate storage and serialization;
  typed columns with offsets retain variable arity.
- One generic NumPy ndarray cannot represent the full mixed schema losslessly;
  explicit projections can still serve array callers.
- An observed S–S candidate is not a declared disulfide bond.
- The broader H5MSM 0.5 modular layout is not required merely to add a
  versioned interaction layer. Native `MolSys` attachment is required, but it
  does not imply that every system has evaluated interactions.

## Scope and exclusions

This issue covers one-system result semantics, the public query contract,
sparse logical schema, versioned serialization boundary, and implementation
gates. It does not implement the class, detectors, indexes, file writer, H5MSM
integration, future interaction families, scientific validation of methods,
cross-system alignment, symmetry expansion, or automatic `MolSys` attachment.
Detector science and API migration remain with #250 or family-specific issues.

## Acceptance criteria

Close this design issue only when:

1. A normative result contract fixes index spaces, source mapping,
   relation/participant/occurrence identity, roles, coverage, evidence,
   measures and units, periodic images, query order, and empty result types.
2. It contains checkable examples for one frame, nonconsecutive and duplicate
   frame requests, variable and zero counts, one atom, atom-set
   `incident`/`internal`/`cross`, a hydrogen-bond triple, a four-participant
   relation, and a two-ring group relation.
3. It specifies a typed versioned payload, file-backed query expectations,
   the H5MSM boundary, and a remap-or-invalidate rule.
4. The MolSysViewer query and lifecycle requirements have been checked with
   `uibcdf/molsysviewer#114`; decisions and unanswered dependencies are
   recorded. Other client integrations are deferred. Any suite-wide ownership
   issue is linked.
5. It defines measurable prototype gates: resident memory, cold and warm frame
   and atom queries over hundreds or thousands of frames, serialized size,
   chunked-writing peak memory, and round-trip fidelity. Claims of passing a
   gate require a measurement command and data.
6. It defines an edit contract for adding and removing occurrences in a
   selected structure, replacing interactions affected by moved atoms,
   dropping interactions involving removed atoms, atom-index remapping,
   coverage, and compaction. The contract includes benchmarks for repeated
   small edits against full reconstruction.
7. The issue records the decision and implementation follow-ups. This proposal
   is archived with `normative` pointing to the accepted document.
8. The normative contract specifies optional `MolSys` ownership and the
   versioned H5MSM interaction layer, including read, write, subset, remap,
   invalidation, and compatibility with files without interactions.

## Dependencies and risks

- The contract must work with the migration in
  [`uibcdf/molsysmt#250`](organize_interaction_detection_by_family_before_1_0.md),
  but is not blocked on every detector gate there.
- `uibcdf/molsysviewer#114` needs a provider contract before fixing its view
  API. The MolSys and H5MSM integrations are additional MolSysMT 1.0 gates.
- Ring display anchors must remain separate from atom-set membership rules.
- Views over an open file need explicit lifetime, close, and ownership rules.
