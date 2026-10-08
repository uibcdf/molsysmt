# Reviewing Interactions with MolSysViewer

This operational packet belongs to `uibcdf/molsysmt#251` and
`uibcdf/molsysmt#252`, in coordination with `uibcdf/molsysviewer#114`.
The [Interaction Analysis API](interactions_api.md) defines the current contract;
this page provides a reproducible review checkpoint and requested feedback.

## Published consumer acceptance — 2026-10-07

MolSysViewer has closed uibcdf/molsysviewer#114 with explicit acceptance of
named analysis discovery, declared attachment, H5MSM import, all nine family
projections, sparse structure/atom queries, parallel occurrence identity,
periodic images, Studio, scene replay/export and session fidelity. Its closure
retains 207 installed interaction/loading tests with zero failures, errors or
skips, executable user-guide examples and separate browser evidence. This is
owner-reported evidence, not a new browser execution by MolSysMT.

The exact delivered pair is MolSysMT 0.23.0 build 0 at
`46ef28eb60a258aa77d82ff1bc39ee0d1591e3c9` and MolSysViewer 0.24.0 build 1 at
`1a4c97a58b68b69f3a836546c9e4ac6187c3efa2`. The provider's 8/8 final source
matrix and 16/16 public installed-pair matrix are retained in the
[publication receipt](../devtools/data/stabilization_023_staging_handoff_20261006.json).
Their terminal conclusions were independently rechecked with GH Run Receptor.

This supersedes the unreceived-feedback state in the dated S2 table below.
The design and experimental result implementation have their delivered
consumer evidence; experimental classification, measured workload limits and
the deferred #335/#336 capabilities are unchanged. Repeating the agreed
workflow on the exact future 1.0 candidate remains mandatory under #334 and
uibcdf/molsysviewer#114's retained final-candidate obligation. No 1.0 candidate
is selected or certified by this reconciliation.

## Public validation completion — 2026-10-05

Provider **`0959a0f7cf3ecf6352d0ed714afacf441563c8b6`** completes the public
ArgDigest boundary that the S2 baseline below identified. Original positional
calls and detector defaults are preserved. Keyword-only `skip_digestion=False`
is now explicit on original result methods; invalid fractional/boolean indices
and overflow fail before encoding, including typed dictionary reads and
queries on invalidated or recalculated results. Stored/file invariants remain
checked on trusted delegation. The
[validation artifact](../devtools/data/interactions_argument_validation_20261005.json)
records the 1,520-test regression and final 116-test delegation check, their
overlap/source phases and documentation limits. Criterion 2 has its guard in
`tests/interactions/test_argument_validation.py`; the native/result/scientific
and persistence contracts remain experimental pending the other gates.

## S2 stabilization review — 2026-10-05

The earlier S2 baseline is clean `main` at
**`4d048a78d466728c2fa9a12befacc22182b71d23`**. The
[dated S2 artifact](../devtools/data/interactions_review_packet_20261005.json)
records commands, dependency versions, selected source hashes, fixture hashes,
test outcomes and consumer observations. The older checkpoint below remains
historical evidence. Distribution versions in editable environments can lag
source revisions; the artifact preserves both rather than substituting the
reader's installed version for the recorded producer.

The provider's native/result/persistence selection passed **279 tests in
37.14 s** on Python 3.14.7. A separate namespace/detector/codec/doctest selection
passed 77 tests and failed one network-dependent 5XJH download in the sandbox;
the exact failed node then passed in 3.94 s with network access. Both outcomes
are recorded separately in the artifact. No result is
inferred from partial test output or counted twice after a retry.

The fixture generator reproduced both H5MSM 0.5 files with five named analyses.
The Viewer tools listed below completed on local consumer
`eb14716f982be87f66ef8dea5218262bbabdad1d`: four real workloads and ten family
scenarios, including one- and two-water paths. Every family has a nonempty
`set_interaction_frame` projection that matches its session-restored projection.
An additional session check retained all five lifecycle analyses, original
producer versions, execution records and exported scene state.

This is **contract-tested Python compatibility**. It does not exercise browser
meshes, Qt or GPU behavior, certify an installed artifact pair or establish new
large-system performance limits. Viewer has three untracked sandbox design
files and is four commits behind its fetched upstream; Ackredit has nine local
edits. All were preserved. Selected hashes are evidence for the inspected
routes, not a fingerprint of their complete dependency import graphs.

### Acceptance reconciliation

| Required contract / owner | Executable evidence | Remaining acceptance |
| --- | --- | --- |
| Sparse queries, compound participants, nonconsecutive indices, empty coverage and images (#251/#252) | `tests/interactions/test_result.py`; `test_query_candidates.py`; `test_occurrence_pages.py` | Updated consumer frame/selection/canvas feedback; no new public lazy query requirement. |
| Versioned handles, producer/run provenance and typed persistence (#251/#252) | `tests/interactions/test_software_provenance.py`; `test_execution_provenance.py`; `test_molsysviewer_review_fixtures.py`; public workflow and codec guards | Explicit consumer acceptance of provenance display and parallel selection on the current contract. |
| Controlled edits, replacement, views and bounded resident export (#252) | `tests/interactions/test_frame_validity.py`; `test_frame_replacement.py`; `test_compaction.py`; `test_bounded_hdf5_writer.py`; native geometry/chemistry setter guards | Raw arrays/aliases require explicit invalidation. Individual editors/pruning and streaming/resumable writes are deferred to #335/#336. Historical benchmark limits remain applicable only to their recorded inputs and environments. |
| Native named analyses and public modular H5MSM (#252) | `tests/native/test_molsys_interactions.py`; `tests/form/file_h5msm/test_public_h5msm_v05.py`; `test_topology_chemistry_interactions_v05.py` | Viewer memory measurements and actual canvas/session acceptance; full installed-candidate matrix belongs to S6. |
| One chemical authority, absence/ambiguity and state associations (#254) | `tests/native/test_chemical_states.py`; `test_molsys_chemical_state_association.py`; `tests/form/molsysmt_MolSys/test_partial_domains.py`; public H5MSM guards | Lifecycle/documentation and exact-candidate recertification; bond facade retirement stays #255. |
| Namespace, legacy defaults and scientific attribution (#250) | `tests/interactions/hbonds/test_namespace.py`; Buch/Luzard–Chandler result guards; disulfide/build wrapper guards; `test_scientific_attribution.py` | Existing methods retain their evidence levels and limitations; current Viewer acceptance and final gates remain open. |
| Public input-validation boundary (#252 criterion 2) | `tests/interactions/test_argument_validation.py` protects real rejection and positive contracts across original/invalidated/recalculated results, typed decoding and standalone persistence. | Contract-tested in the later validation completion above; other lifecycle and exact-candidate gates remain open. |

Normative contracts remain in [Interaction Analysis API](interactions_api.md)
and [H5MSM format](h5msm_format.md). The owning reports retain their individual
acceptance criteria. This table neither closes #250/#251/#252/#254 nor waives
the [frozen stabilization queue](release_1_0_scope.md). The provider has
completed the bounded public validation review. Continue S3–S5 within the
frozen scope while the maintainer requests explicit Viewer feedback below.

## Historical pinned provider checkpoint

Use a clean MolSysMT checkout at
**`1986027c353cdcf290e0402b1d8fa23fee6ea637`**, on
`review/interaction-attribution-20261001` at the time of the review. The branch
is retired after integration into `main`; the pinned commit remains in its history.
This includes explicit compaction
from `4148220a9` and the updated lifecycle fixture generator. The installed
distribution version does not identify this editable source revision.

The [dated evidence artifact](../devtools/data/interactions_review_packet_20261002.json)
records the exact clean provider state, selected source hashes, dependency
versions, provider tests, generated-file hashes and consumer observations.

## Changes to review

| Area | Provider behavior |
| --- | --- |
| Execution provenance | Scientific criteria stay in `parameters`; `execution_records` partitions evaluated local structure indices by producing run, including empty frames. Compatible partial recalculation can change execution policy. |
| Persistence | H5MSM stays version 0.5 and its named collection stays schema 1. Individual interaction payloads use codec 2. Current readers migrate codec 1; older provider builds require an update to read codec 2. |
| Frame edits | Coordinate/box setters on native `MolSys` invalidate affected frames, even when only one atom moves or a frame was evaluated-empty. Scientific chemical-state setters have their documented conservative scope. No detector runs automatically. |
| Recalculation | `replace_structures()` returns a compatible new analysis; the caller attaches it explicitly. Every incoming evaluated frame replaces its old observations, including an incoming empty frame. |
| Row compaction | `compact()` returns a packed snapshot preserving occurrence/relation indices, maps, coverage and provenance. Release older analyses and views to reclaim retired rows. Unused relation definitions remain. |
| Resident export | Saving full native analyses writes active observation blocks in numeric windows without populating or altering the complete-column cache. It does not supply a detector-to-file sink. |

Query semantics and the periodic-image convention are unchanged. Repeated frame
selections do not duplicate observations. Parallel observations retain distinct
`occurrence_indices`. For compound participants, every constituent atom enters
`incident`/`internal`/`cross` and `between` tests. Producer `software` versions
continue to identify the calculation, rather than the reader.

Keep separate named analyses for different scientific definitions. Attachment
declares correspondence to the destination's local axes; matching sizes and
`source_id` do not authenticate molecular origin. Extraction/reordering remaps
indices and creates a new version; this does not embed a subsystem into a larger
destination. See the [association contract](interactions_api.md#associating-analyses-with-a-system).

## Reproducing the provider review

From the pinned checkout, verify the imported source before generating files:

```bash
git rev-parse HEAD
python -c 'import molsysmt; print(molsysmt.__file__)'
python devtools/scripts/create_molsysviewer_interactions_fixture.py /tmp/msm-viewer-review
python -m pytest --receptor=llm \
    tests/interactions/test_molsysviewer_review_fixtures.py \
    tests/interactions/test_public_molsys_h5msm_workflow.py \
    tests/interactions/test_execution_provenance.py \
    tests/interactions/test_compaction.py \
    tests/interactions/test_bounded_hdf5_writer.py
```

Choose a fresh output directory: the generator refuses to overwrite either file.
It produces `molsysviewer_full.h5msm` and
`molsysviewer_interactions_only.h5msm`. Each includes these named analyses:

| Name | Expected case |
| --- | --- |
| `review` | Five observations; evaluated frames `[0, 1, 2, 4]`; frame 1 is empty and frame 3 is unevaluated. Runs cover `[0, 1, 2]` and `[4]`. |
| `invalidated` | Frame 4 is unevaluated; observations in other frames survive. |
| `recalculated` | Frames `[1, 4]` are replaced, with frame 1 still evaluated-empty. Execution records cover `[0, 2]` and `[1, 4]`. |
| `compacted` | Same active observations, handles and provenance as `recalculated`. |
| `empty` | Zero observations with evaluated frames `[1, 5]`. |

Querying `review` with `[4, 1, 0, 4, 3]` returns occurrence handles
`[3, 4, 0, 1]` and evaluated coverage `[4, 1, 0]`. Adding atom selection `[0]`
in `incident` mode returns `[3, 4, 0]`. The two observations in frame 4 share
their relation but remain separately identifiable.

These observations, run descriptors and arbitrary measures are **synthetic
contract fixtures**. Coordinates are zero and the full file has a unit cubic
box. Coincident display endpoints can be skipped: the observed Viewer reports
frame 4 as a partial projection with one supported and one skipped observation.
This rendering status does not change scientific evaluated coverage. Use the
real detector workloads below to validate geometry.

## Local consumer evidence

**Contract-tested checkpoint, 2026-10-02:** the provider selection above passed
58 tests on the pinned clean revision. The real consumer command also passed:

```bash
python ../molsysviewer/devtools/qualify_interactions.py /tmp/msm-viewer-qualification
python ../molsysviewer/devtools/qualify_interaction_families.py /tmp/msm-viewer-families
```

These tools belong to MolSysViewer. Run them from an environment using the
intended provider and consumer sources, with fresh output directories. They
do not replace browser qualification.

The first command checks real hydrogen-bond and disulfide-candidate workloads,
nonconsecutive structure/atom queries, independently reconstructed geometric
endpoints, observed periodic images, a non-default angstrom policy and complete,
interaction-only and session round trips. Its four workloads produced 56,
76, 2,439 and 8 observations respectively; the periodic workloads included
16 and 299 observations with nonzero images. Topology stayed unchanged for
the disulfide-candidate case.

The second command produced positive scenes for all nine families and both
water mediator orders: ten scenarios in total, with no skipped observations.
After session recovery, every scenario's `set_interaction_frame` payload
matched its initial payload. This is protocol/session parity, not independent
scientific validation or an actual Mol* mesh/browser test.

The five named lifecycle analyses also preserved their execution records,
original producer versions and exported scene state through a Viewer session.
To repeat that metadata check after generating the files:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import molsysmt as msm
import molsysviewer as msv

def runs(result):
    return [(r["structure_indices"].tolist(), r["details"])
            for r in result.execution_records]

molsys = msm.h5msm.read("/tmp/msm-viewer-review/molsysviewer_full.h5msm")
expected = {name: runs(result) for name, result in molsys.interactions.items()}
view = msv.new_view(molsys)
restored = None
try:
    view.interactions.add("review", tag="review-fixture")
    with TemporaryDirectory() as directory:
        filename = Path(directory) / "review.msvz"
        view.save_session(filename)
        restored = msv.load_session(filename)
        assert restored.export_state() == view.export_state()
        for name, records in expected.items():
            analysis = restored.interactions.get_analysis(name)
            assert runs(analysis) == records
            assert analysis.software == molsys.interactions[name].software
finally:
    view.close()
    if restored is not None:
        restored.close()
```

The consumer checkout was at `1cf7826d4c34` with 322 pre-existing dirty entries;
Ackredit had nine pre-existing edits and was behind its fetched upstream.
Their worktrees were preserved. Selected source hashes are retained, but this
does not freeze their complete import graphs or certify a published package pair.
Reported runtime/RSS observations are not isolated performance benchmarks.

## Feedback and closure

Please return the exact consumer source or package identity and the outcomes of:

1. Loading/discovering named analyses and attaching a detached analysis with
   declared alignment.
2. Frame switching, atom selections and separate inspection of parallel
   occurrence handles, including evaluated-empty versus unevaluated frames.
3. Canvas projection of actual periodic images and compound participants;
   scene reconstruction, export and session recovery.
4. Preservation/presentation of scientific parameters, producer versions and
   frame-scoped execution records after partial recalculation and persistence.
5. Combined coordinate/interaction memory on the agreed workloads before
   deciding whether public file-backed queries are needed for Viewer 1.0.

The initial path loads the selected named analysis into memory. Complete-column
access, typed/pickle export, remapping or consumer signatures can still pack
edited observations; the bounded writer alone does not bound an entire session
pipeline. Direct detector-to-file accumulation, resumable append, individual-row
editors, unused-registry pruning and public lazy file queries remain absent.

### Message for the maintainer to forward

> We have refreshed the experimental Interactions review at clean MolSysMT
> `0959a0f7cf3ecf6352d0ed714afacf441563c8b6` on main, using Python 3.14.
> The review packet retains the H5MSM 0.5/codec-2 original, invalidated,
> recalculated, compacted and empty named analyses, producer versions and
> structure-scoped execution records. Public persistence now also supports
> topology/chemistry/named-analysis combinations without Structures.
>
> The provider core selection passed 279 tests. Your local qualification tools
> completed at consumer eb14716f982be87f66ef8dea5218262bbabdad1d, including all
> nine families and both water orders. Each initial/restored structure projection
> matched, and five lifecycle analyses retained producer/run metadata through
> a session. Source states, boundary tests and limitations are recorded in the
> dated artifact; this is Python compatibility, not browser or published-pair
> certification. The subsequent ArgDigest completion passes 1,520 regression
> tests plus a final overlapping delegation guard, preserving positional calls
> while rejecting lossy indices. Its dated artifact records the separate source
> phases; the earlier consumer observations are not a new Viewer run at this SHA.
>
> Please return a committed consumer identity and explicit results for structure
> switching, atom selections, parallel occurrence inspection, periodic/compound
> canvas geometry, scene export and session recovery, including provenance display.
> The initial path still loads a named analysis into memory. Combined-memory
> measurements will inform any later file-query requirement. Our frozen 1.0
> scope includes current-contract fixes and qualification; new editors, methods
> and resumable detector-to-file accumulation are deferred. The contract remains
> experimental pending your feedback and the agreed candidate gates.

Keep `uibcdf/molsysmt#250`, `#251` and `#252` open until their respective
consumer/acceptance gates are met. Once feedback settles the experimental
contract, synchronize durable rules and close with the applicable guards.
On 2026-10-02, the maintainer authorized direct local integration into `main`,
local test validation, a normal push, and removal of incorporated development
branches without requiring a pull request. Incorporate current remote changes
and run the repository's local test and validation gates before publication.
These local checks do not certify the full platform/interpreter release matrix.
The consumer must commit its current implementation before its SHA can identify
the tested clean dependency in the controlled integration workflow. The inspected
dirty checkout's HEAD alone is not that candidate. Delete development branches
only after verifying their work is integrated and preserving unrelated work.


## Main integration checkpoint — 2026-10-02

Clean-source revision `a50daad4ae457630131ea1a17ee42d06a538e601` passed the
complete local suite: 11,699 passed, 11 existing optional/environment skips,
zero failures. The additional developer-tools and Interactions doctest suite
passed 259 tests, native Rust passed 81 tests, and all 14 fast gates passed.
The [integration artifact](../devtools/data/interactions_main_integration_20261002.json)
records commands, source identity, dependency versions and scope limits.
This supersedes the earlier no-merge working-state observation, without changing
the historical review fixture fingerprints or claiming consumer acceptance.

## Immutable consumer delivery — 2026-10-06

MolSysViewer delivers `c046fca173f501c6e259761ef8f3d6b1825f17e8` for coordinated
staging, with its provider source pinned to MolSysMT
`5e2721691b6a3c175406a8e4c0926dfb7b160671`. Its source-pair workflow
[37441973999](https://github.com/uibcdf/molsysviewer/actions/runs/37441973999)
reports Python 3.14 success on Linux/macOS/Windows (2,819/2,792/2,793 passed;
27/54/53 skipped). The team also reports 39/39 core browser suites, including
17 interaction calculation forms, and closes uibcdf/molsysviewer#161, #162
and #163. Public installed-artifact qualification remains pending in its handoff.

The [provider recovery receipt](../devtools/data/stabilization_s6_source_recovery_20261006.json)
records the reported observations and our source-SHA/documentation-only
successor verification. Untracked Viewer sandbox prototypes are preserved.
This delivered source replaces the earlier candidate-availability blocker;
repeat the controlled pair with the newer corrected MolSysMT source, qualify
staged bytes and retain the remaining #114 installed/canvas/session scope
before claiming complete consumer acceptance. No new feature is added.

## Provider validation with delivered Viewer source — 2026-10-06

The corrected provider source `bb4781c5ae0b725d0c904cfd8bae1f44a1b13123`
passes its eight-cell Linux/macOS Python 3.11–3.14 full matrix with Viewer
`c046fca173f501c6e259761ef8f3d6b1825f17e8` (`37449282864`), including all
eight 54-case scientific certificates without skips. The same pair passes
wheel/runtime/public installed checks (`37449284817`). The
[pair receipt](../devtools/data/stabilization_s6_pair_20261006.json) retains
artifact identities, hashes and full-suite omission nodes/reasons.

The next MolSysMT version checkpoint is 0.23.0. Its exact package producer and
the Viewer package version must be agreed and tested as installed files;
the development-version artifacts above are supporting evidence. Consumer-owned
installed/browser/canvas/session gates remain separate from these provider
results. No 1.0 stability or publication decision is made by this checkpoint.
