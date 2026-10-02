# Reviewing Interactions with MolSysViewer

This operational packet belongs to `uibcdf/molsysmt#251` and
`uibcdf/molsysmt#252`, in coordination with `uibcdf/molsysviewer#114`.
The [Interaction Analysis API](interactions_api.md) defines the current contract;
this page provides a reproducible review checkpoint and requested feedback.

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

> We have prepared the updated experimental Interactions review at MolSysMT
> `1986027c353cdcf290e0402b1d8fa23fee6ea637`, on
> the historical review branch, now integrated into `main`. The packet provides H5MSM 0.5/codec-2
> fixtures for original, invalidated, partially recalculated, compacted and empty
> named analyses, with frame-scoped execution records and original producer versions.
>
> The clean provider review passed 58 tests. Your current Python qualification
> tools passed locally, including all nine families and both water orders;
> their initial and session-restored frame payloads matched. We also checked
> preservation of the five lifecycle analyses' execution records through a session.
> The consumer checkout includes your existing changes, so this is local
> compatibility evidence, not published-pair or browser certification.
>
> Please review the packet and return the exact consumer identity and feedback
> on the frame/selection/canvas/export/session workflow and on presenting
> execution provenance. The initial route continues to load a named analysis
> into memory; public lazy file queries and detector-to-file accumulation remain
> separate capabilities. The contract stays experimental until this feedback
> and the agreed integration gates are settled.

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
