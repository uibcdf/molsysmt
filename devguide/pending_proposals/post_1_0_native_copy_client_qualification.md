---
summary: Extend native-copy qualification with representative client workflows after 1.0
issue: uibcdf/molsysmt#408
status: open
opened: 2026-10-22
closed:
verification: inspected
area: [tests, native]
guard:
normative:
blocked_by: []
supersedes: []
---

# Representative client qualification for native copying

**Reported:** 2026-10-22, during maintainer review of #121's evidence limits.
**Status:** Open future qualification proposal; no additional client is certified.

## What

Extend native-copy evidence to a bounded set of realistic client branching and
editing workflows. Distinguish ownership/validity correctness, resource costs,
installed compatibility and scientific evidence. This extends the
[source qualification](../native_copy.md) without treating a large passing-test
count as certification of every application.

## How

Use existing owner-local coordination rather than duplicate client development:
uibcdf/molsyssuite#122, uibcdf/topomt#97, uibcdf/dockingmt#51,
uibcdf/molsysviewer#259, uibcdf/pharmacophoremt#60 and uibcdf/elastnetmt#28.
Select concrete workflows with their maintainers: editable molecular variants,
preparation/pose branches, named analyses and scene/session recovery, feature
registries, intentional live references and model/cache reuse as applicable.

For each selected workflow, declare the expected independent data, intentionally
shared immutable data and client-specific derived state. Exercise edits and
recovery across public boundaries. Record exact provider/client source identity
or installed artifact identity; neither substitutes for the other. Reuse
owner-local guards and persist result records where supported.

## Why

The [production campaign](../benchmarking/native_copy.md) supplies reproducible
synthetic workloads and an actual TopoMT source-route probe. That does not
establish all client engines, persistence/session paths, external extensions,
platforms or scientific methods. A bounded acceptance inventory can expose
specific missing checks without creating another indefinite stabilization queue.

## What is inspected and what is assumed

**Inspected:** The scope and exclusions in the native-copy contract and benchmark
guide at source `655892f7b563ab6e6d6acc07555ccf6c2d0bc082`, including the retained
[TopoMT probe record](../../benchmarks/baselines/topomt_native_copy_20261022.json).
Its success is source-route evidence, not installed-package or engine qualification.

**Not established:** The outcome of additional client runs, realistic workload
performance or all-platform compatibility. This report adds no measurements or
new executed integration results. Scientific validity remains method-specific.

## What was refuted

Passing many tests cannot certify behavior those tests never exercise. Copy
independence and parity are not scientific validation. The recorded correction
of an obsolete benchmark guard reinforces the need for tests that reject wrong
ownership or stale results, rather than merely accepting expected output shapes.
These observations do not invalidate the scoped source results already delivered.

## Scope and exclusions

This is post-1.0 evidence expansion. Mandatory exact-candidate and installed-pair
qualification remains in #334 under the [scope freeze](../release_1_0_scope.md).
Do not make every suite client a new initial-release dependency. Suite adoption
remains owned by uibcdf/molsyssuite#122. Conversion-edge execution (#181),
scientific evidence classification (#190) and cation-pi method comparison (#271)
retain their own scopes; this proposal links gaps to those owners rather than
reimplementing their programs.

## Acceptance criteria

- Agree a finite inventory with an owner and expected outcome for each workflow;
  mark unselected or unavailable paths explicitly, without implying support.
- Exercise source preservation, supported edit invalidation, failed edits and
  restoration, sparse occurrence identity, units and persistence where promised.
- Include adversarial checks that genuinely reject shared writable data or stale
  coverage, including evaluated-empty structures and parallel observations.
- For copy-only paths, compare molecular values and scientific results with the
  original; after edits, use declared expected behavior or independent evidence
  rather than claim accuracy from self-comparison alone.
- Measure realistic workload time and memory with reproducible inputs and scoped
  provenance, separating retained state, traced allocations and process RAM.
- Record installed artifact/platform evidence separately from checkout runs,
  and route any newly observed provider/client defects to their owning issues.
- Close against the bounded inventory with addressable guards or a maintained
  normative qualification document, retaining remaining gaps in owned issues.

## Dependencies and risks

Client maintainers own client implementation and acceptance. This proposal is not
permission to change their source, publish packages or modify release pins.
Representative workloads must be small enough for routine guards; larger resource
campaigns remain opt-in measurements rather than fragile timing thresholds.
