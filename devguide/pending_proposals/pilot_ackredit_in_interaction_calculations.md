---
summary: Pilot Ackredit in interaction calculations
issue: uibcdf/molsysmt#27
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [api, deps, docs]
guard: tests/interactions/test_scientific_attribution.py
normative:
blocked_by: []
supersedes: []
---

# Piloting Ackredit in interaction calculations

**Reported:** 2026-10-01, maintainer authorization to begin the first real client.
**Status:** Interaction pilot implemented and validated; whole-library and suite-wide
adoption remain future work.

## What

Use optional Ackredit registration, scopes and explicit runtime tracking for
interaction calculations. Preserve a detached bibliography in each result,
independent of the session registry, and use this pilot to inform provider and
suite-wide integration guidance.

## How

`molsysmt/_ackredit.py` lazily loads the optional provider. The host does not
enable import hooks, network enrichment, reminders or a journal. Host-owned
scientific declarations remain separate from runtime observations.

Each successful detector/recognizer records references, including completed
calculations with zero observations. Invalid or failed calculations do not
credit a completed detector. Attribution is performed once per calculation,
never per atom pair, frame or occurrence. A successfully completed child tool
can still be credited if its enclosing detector later fails.

`parameters["attribution"]` carries schema
`molsysmt.scientific_attribution@1`, the producer function and detached
bibliographic items with contextual roles: `scientific_criterion`,
`reference_implementation`, and `executed_software`. The existing versioned
parameter serialization preserves the payload in InteractionsDict and H5MSM.
Reading a result neither calls Ackredit nor rewrites original producer versions.

Runtime scopes contribute to the application's current session. Individual
result bibliographies are constructed from the actual selected definition and
producer dependencies, not by subtracting a global session's credited IDs.
Repeated works remain present in each result even after the enclosing session
deduplicates them.

Bibliographic declarations are verified offline. RDKit's official recommended
website citation is used with the actual producer version, without guessing
authors or an exact-release DOI. Historical Buch attribution has no invented
paper; its mathematical distance criterion is named descriptively.

## Why

MolSysViewer receives named analyses and persists them with scientific origin.
Its workflow report and each original analysis both need accurate attribution.
This is a bounded first real client for Ackredit.

## What is measured and what is assumed

**Real client checkpoint, 2026-10-01:** After the pilot was published as
`e21f03d9992b87af2cc9285211adee888462be41`, the local real MolSysViewer qualification
passed its four scientific/persistence workloads. The [implementation record](../archive/resolved_proposals/implement_experimental_sparse_interactions_results_and_queries.md#consumer-and-attribution-checkpoint--2026-10-01)
separates the clean provider commit from the consumer's dirty source checkout
and states the limits of that evidence. A new optional public-client test in
`tests/interactions/test_scientific_attribution.py` explicitly protects original
Baker–Hubbard bibliography and software versions in named Viewer metadata,
queries, complete and analysis-only H5MSM, and saved-session recovery. Reader
sessions do not receive a new calculation credit. All 18 tests in that module
passed locally; Ackredit and MolSysViewer were installed, so none were skipped.
This is not a new browser/GPU qualification or public-distribution gate.

Contract-tested and parity-tested with the real editable provider:

- Interaction/recognizer/scientific-control selection: 511 tests passed.
- Attribution and diagnostic/catalog/worker reconstruction selection: 310 passed.
  This selection overlaps the interaction suite; the counts are not additive.
- Eight public modules: 63 doctest examples passed after resolving their lazy
  public exports before testing implementation modules. Raw pytest collection
  of nested implementation files can shadow their public callable names.
- Four updated Toolbox/site-recognizer notebooks executed successfully.
  All four Module 38 paths received the naming/provenance explanation; their
  existing remote biological code cells were unchanged, not re-executed.
- The maintained `devtools/scripts/validate_course.py` gate confirms 156
  consistent notebooks, manifest, labels and toctrees. The historical linter
  under `docs/content/course/devtools/` is not that release gate.
- Dependency validation, dependency-contract audit, public docstring validation,
  developer-guide validation and Ruff passed.

The fixed-cost probe is reproducible with:

```bash
python devtools/scripts/benchmark_interaction_attribution.py --repetitions 50 --structures 3
```

Measured on Linux x86_64, Python 3.13.14, installed MolSysMT producer version
`0.21.0+606.ga03eb4bf6`, Ackredit `0.8.0+4.ge4ff20a.dirty`, with the pilot patches
on repository base `85aeef186`. Ackredit's human worktree changes were preserved.
For six atoms and three structures, final medians were 8.788 ms without a provider and
9.154 ms with workflow tracking, a 0.366 ms difference. Both modes still construct
the same portable bibliography (1,413 JSON bytes for this analysis), so this is
not the total cost against a pre-attribution release. It is not a large-trajectory
throughput, RAM or HDF5-size benchmark. Bibliography is retained once per analysis;
no occurrence column or trajectory dimension was added.
Published Ackredit microbenchmarks are not treated as MolSysMT measurements.

## What was refuted

- Journalling item IDs alone cannot preserve bibliography in a fresh reader.
- A before/after session-ID difference misses a paper reused by two analyses.
- An isolated inner session does not automatically credit its enclosing session.
- Importing software is insufficient evidence that its algorithm ran.

## Scope and exclusions

Interaction detectors and their reusable site recognizer are the first pilot.
Automatic attribution of every converter, format backend and general tool is
not claimed. No hard Ackredit dependency or user filesystem/network side effect.
Publication and Python compatibility follow provider availability rather than
forcing Ackredit into MolSysMT's supported environments.

## Acceptance criteria

- Scientific outputs are identical with and without Ackredit.
- Two analyses have exact individual references and contribute to one workflow.
- Independent results preserve reused citations and original software versions.
- Empty evaluated frames and nonconsecutive structure indices remain intact.
- Named H5MSM and typed conversions retain bibliography without reader tracking.
- Importing MolSysMT does not import Ackredit.
- Provider feedback and suite guidance are linked to real pilot evidence.

## Dependencies and risks

Portable contextual capture and host-guide improvements are requested in
uibcdf/ackredit#75. This host adapter does not access the provider's private
registry or implement a competing bibliography renderer. The capture adapter
will use a provider contract when available; scientific declarations remain
owned by MolSysMT. Provider distribution is tracked by uibcdf/ackredit#22.

Shared adoption guidance is proposed in uibcdf/molsyssuite#68. The current canonical
Ackredit guide recommends eager registration/imports and an import-time optional
shim. MolSysMT's existing lazy soft-dependency rule takes precedence here:
declarations remain offline constants, while provider registration is deferred
until a completed calculation. This difference is explicitly part of the guide
revision request rather than an independent component edit to the synchronized
guide. There is no public installation extra while distribution and supported
Python floors remain unresolved; this is an editable-source pilot, not a claim
that an unpublished package can be installed from the normal channel.

## Remaining work

- Ackredit: agree portable capture/export/import, contextual report roles and the
  canonical lazy-client guide (uibcdf/ackredit#75); publish supported distribution
  and compatibility (uibcdf/ackredit#22).
- MolSysSuite: review and synchronize the accepted adoption rules
  (uibcdf/molsyssuite#68).
- MolSysMT: extend verified runtime attribution to other meaningful tools in
  future phases of uibcdf/molsysmt#27. This pilot does not expose a whole-library
  citation facade or silently instrument converters and format backends.
