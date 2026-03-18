# Next Steps Toward 1.0.0

This temporary document records the currently agreed action plan for the next phase toward `1.0.0`.

It is intentionally broader than a support-contract note. The current state of the repository already justifies moving from broad stabilization to explicit product-definition work, but several strategic tasks still need to be completed before the `1.0.0` line can be considered professionally closed.

This file exists to keep those immediate priorities explicit before the corresponding canonical documents are fully updated.

## Why this plan exists

MolSysMT has recently reached a strong technical checkpoint:

- the full test suite is green;
- distributed validation with `pytest -n 12 --dist loadfile ...` is established as the default large-scale testing workflow;
- the current honest coverage baseline is `78%` (target 70-80% reached);
- `0.17.0` already marks the current declarative-serialization and builder-editing checkpoint;
- `MolSysBuilder` is integrated as the native editable path;
- declarative serialization forms are available;
- the heavy-trajectory roadmap has been rewritten as an executable `v2` working draft.

The next step is no longer broad stabilization. The next step is to turn that technical state into an explicit and defensible `1.x` support contract, backed by a stronger validation story and by developer-facing documentation that matches the architecture we have already implemented.

Once this plan is in active execution, no new broad architectural lines should be opened unless they are required directly by the `1.0.0` support contract itself.

## Agreed priority order

The following priorities have been agreed.

### 1. Formalize the support contract

The first priority is to strengthen `devguide/support_tiers.ipynb` so that it becomes an actual support contract for the `1.0.0` line rather than just an inventory.

This work should answer, explicitly and defensibly:

- which forms are Tier 1, Tier 2, or Tier 3;
- what "Tier 1" guarantees in practical terms;
- which forms are verified by contract tests;
- which forms are parity-verified;
- which forms are candidates for promotion but not yet contractual;
- which forms are in scope for future heavy-mode support but are not yet committed.

The main reason this is the first priority is simple: without a real support contract, users do not know which parts of the library are safe to treat as production-grade in the `1.x` line.

### 2. Define the parity-testing strategy from the support contract

Once the support tiers are explicit, `devguide/testing_strategy.md` should be updated so that parity testing follows the contract rather than an implicit notion of importance.

Two parity dimensions should be treated separately:

- **form parity**
  - equivalent molecular content represented in different supported forms should produce equivalent observable results where parity is expected;
- **execution parity**
  - eager and heavy execution paths should produce equivalent results for operations that officially support both.

The support contract must come first because it determines which forms and operations deserve systematic parity guarantees.

### 3. Synchronize the performance and JIT manifesto with current reality

After the support contract and parity strategy are aligned, `devguide/performance_and_jit.md` should be updated so that it reflects the architecture that is already present in the repository.

This includes, at minimum:

- trusted/validated payload handling;
- fast-track / trusted path concepts;
- unit-agnostic kernel boundaries;
- explicit `float64` normalization at public-to-kernel boundaries where required;
- the performance role of native rebuild paths and minimized redundant digestion.

This is not the first priority because a performance manifesto is only useful if it is aligned with the actual support contract and testing policy.

### 4. Continue increasing coverage toward a realistic `1.0.0` baseline

The repository is now at a much stronger testing checkpoint than before, but the current global coverage number is still modest.

Current agreed state:

- full-suite validation is green;
- the honest global coverage baseline is `78%` — the 70-80% target has been reached;
- active coverage pursuit is paused: further gains should come from meaningful
  tests for new features rather than percentage chasing;
- `molsysmt.molecular_dynamics/**` is explicitly outside the `1.0.0` support contract and outside the local/Codecov stabilization coverage scope.

The coverage objective is considered met for the 1.0.0 stabilization pass. The
focus now shifts to hardening the contractual Tier 1 surface with correct and
meaningful tests, not to raising the global number further.

The working rule remains:

- prioritize coverage on the contractual Tier 1 surface first;
- only then use the global percentage as a secondary quality signal.

### 5. Use `MolSysBuilder` and declarative forms to reduce truth ambiguity in tests

The repository now has a better testing primitive than it had before:

- `MolSysBuilder`

and a new declarative family:

- `MolSysDict`
- `TopologyDict`
- `StructuresDict`
- YAML file forms detected by content

This changes how converter tests should be designed.

Whenever possible, truth should be declared before the format under test is produced. In practice, this means that new converter tests should increasingly follow this pattern:

1. declare a system explicitly with `MolSysBuilder`;
2. materialize the form under test from that declared truth;
3. convert back from the tested form;
4. compare against the predeclared truth.

This is now an explicit priority because it reduces circular testing where a format becomes both the object under test and the accidental source of truth.

### 6. Synchronize infrastructure-library releases before the `1.0.0` line

MolSysMT cannot close its `1.0.0` line while depending, in practice, on floating `main` branches of sibling infrastructure libraries.

This applies at least to:

- `smonitor`
- `argdigest`
- `depdigest`
- `pyunitwizard`

The recent work has already demonstrated that MolSysMT depends on concrete upstream behaviors, not only on abstract package names. Therefore, before the `1.0.0` line is finalized, the suite must define and document the minimum released versions or tags that MolSysMT officially targets.

This does not require that all sibling repositories reach the same milestone on the same day, but it does require that MolSysMT `1.0.0` be paired with a clearly documented infrastructure baseline.

### 7. Stabilize public functions, not only forms

The support contract cannot be form-only.

Forms are one axis of stability, but the user-facing contract also includes public functions. A `1.0.0` line should say more than "this form is supported." It should also say, in practical terms, which public functions are:

- stable for the `1.x` line;
- still experimental;
- or intentionally outside the committed `1.0.0` contract.

This means that, after the form support contract is clarified, a rapid stability sweep should be performed across the public API surface, especially in areas such as:

- `msm.basic`
- `msm.structure`
- `msm.build`
- other user-facing namespaces that are part of normal daily workflows

The goal is not to classify every helper in the repository. The goal is to make the public surface professionally explicit.

### 8. Define the deprecation policy for the `1.x` line

A serious `1.0.0` contract needs a clear deprecation policy.

Once the `1.x` line begins, compatibility expectations become stronger. This means the project should define, in plain terms:

- what kinds of changes require formal deprecation;
- what the minimum warning period is for a Tier 1 public function or form;
- how exceptions are handled when a bug fix requires behavior correction;
- how deprecation signals are communicated in code and in developer documentation.

This policy does not need to become bureaucratic, but it must exist. Without it, the support contract is incomplete.

### 9. Validate release engineering and packaging for the `1.0.0` line

The `1.0.0` line also requires an explicit release-engineering checkpoint.

This should include, at minimum:

- the final CI matrix used as the release gate;
- packaging validation for the supported Python versions and supported dependency baseline;
- confirmation that MolSysMT is paired with explicit sibling-library versions or tags rather than floating development heads;
- verification that the release path is compatible with the support contract and with the documented user-facing install story.

This is not a cosmetic packaging concern. It is part of the practical meaning of a support contract.

## Specific guidance for `support_tiers.ipynb`

The current agreement is that `support_tiers.ipynb` should not stay as a loose descriptive list. It should evolve into a structured support contract.

At minimum, each relevant form should eventually carry or be associated with:

- `tier`
- `support_scope`
- `contract_guarantee`
- `verified_capabilities`
- `known_limitations`
- `heavy_mode_status`
- optional promotion note if it is a realistic near-term Tier 1 candidate

For Tier 1, the contract should say clearly that:

- regressions are patch-priority;
- semantics are expected to remain stable across the `1.x` line except for explicit bug corrections;
- support status is based on actual validation, not only on implemented adapters.

## Relationship with heavy trajectories

The repository now has a working draft:

- `devguide/scalability_and_heavy_trajectories_v2.md`

That document is considered the current execution-ready roadmap for pre-`1.0.0` heavy-trajectory work.

However, heavy-mode support should not be declared Tier 1 for any form until the support contract says so explicitly and the corresponding parity/testing obligations are defined.

In other words:

- the heavy-trajectory roadmap defines what should exist;
- the support contract defines what users may rely on.

For the near-term `1.0.0` path, one additional point should remain explicit:

- the Tier 1 implementation of the chunked heavy-execution path must validate the heavy-mode SMonitor contract in practice, not only in documentation.

The reserved `MSM-*-HVY-*` codes are therefore not merely naming placeholders. They are part of the implementation obligations of the first committed heavy-processing slice.

## Relationship with the declarative-serialization roadmap

The repository also now has a second architectural line that is no longer hypothetical:

- `MolSysBuilder`
- `MolSysDict`
- `TopologyDict`
- `StructuresDict`
- YAML file forms detected by content

That line is already part of the active product surface. It should therefore be reflected in the support contract and in the future parity strategy.

In particular:

- these forms should be classified explicitly in `support_tiers.ipynb`;
- parity expectations should be described where they are part of the supported contract;
- `MolSysBuilder` should continue to be used as a deterministic fixture source for converter tests.

## Immediate actionable sequence

The agreed immediate sequence is:

1. rewrite `devguide/support_tiers.ipynb` into a real support contract;
2. update `devguide/testing_strategy.md` so that parity obligations follow that support contract;
3. update `devguide/performance_and_jit.md` so that it matches the currently implemented trusted/validated execution model;
4. implement the remaining new `1.0.0` capabilities that are already in scope, especially the Tier 1 heavy-trajectory slice described in `scalability_and_heavy_trajectories_v2.md`;
5. define the sibling-infrastructure release baseline that MolSysMT `1.0.0` can safely depend on;
6. perform a public-function stability sweep so that support status applies to functions as well as forms;
7. define the deprecation policy for the `1.x` line;
8. validate release engineering and packaging against the intended `1.0.0` support baseline;
9. continue meaningful coverage work, prioritizing high-return technical areas rather than low-value percentage chasing;
10. continue replacing ambiguous fixture strategies with builder-based deterministic test design where appropriate.

## Exit Criteria Toward Paper and `1.0.0` Stabilization

The repository should not enter the final paper-writing and stabilization phase merely because the codebase feels mature. The transition should happen only once a small set of explicit preconditions is satisfied.

The current agreement is that the path to that phase is:

1. a real support contract;
2. a materially stronger coverage baseline;
3. a documentation pass that aligns the repository with the actual implemented architecture.

Once those three pillars are in place, the project can reasonably move into:

- paper writing;
- a stabilization window focused on fixes, validation, packaging, and release preparation;
- and final `1.0.0` release work.

### 1. Support-contract completion

Before the final stabilization phase begins, MolSysMT should have:

- an explicit form support contract in `support_tiers.ipynb`;
- an explicit stability classification for the public API surface, not only for forms;
- an explicit `1.x` deprecation policy;
- a documented sibling-infrastructure baseline for:
  - `smonitor`
  - `argdigest`
  - `depdigest`
  - `pyunitwizard`

Without this, `1.0.0` remains technically strong but institutionally ambiguous.

### 2. Coverage threshold with technical meaning

The global coverage baseline is `78%` — the 70-80% working target has been reached.

Active coverage pursuit is paused. The end condition is not a percentage; it is
that the contractually supported surface is well defended. The focus now is on
ensuring that the full Tier 1 contractual surface is strongly covered and
explicitly identified as such, not on raising the global number further.

### 3. Documentation alignment

Before paper writing begins, the documentation should be brought into alignment with the actual architecture of the repository.

This includes:

- `devguide`
- `docs/content/developer`
- the user-facing or API-facing documentation that describes supported workflows

The purpose of this pass is not cosmetic cleanup. It is to force explicit decisions about:

- what is in the `1.0.0` contract;
- what is outside it;
- what remains experimental;
- and what is guaranteed in the `1.x` line.

### 4. Readiness to enter the stabilization window

The final stabilization window should begin only when the repository satisfies all of the following:

- the support contract is explicit;
- the public-function stability story is explicit;
- the deprecation policy is explicit;
- the heavy-trajectory `v2` roadmap stands as the official pre-`1.0.0` working design;
- the documentation is aligned with the current implementation;
- the validation and coverage baseline are strong enough to support release hardening without reopening architectural uncertainty.

At that point, the project should stop introducing broad new architectural lines unless a missing piece is required by the support contract itself.

In practical terms, that is the point at which MolSysMT should move from active architectural shaping to controlled release stabilization.

During that stabilization window, the project should also encourage controlled beta-testing and dogfooding:

- close collaborators and technically capable external users should be encouraged to exercise the release-candidate line using the current tutorials and documentation;
- the goal is to expose gaps between the documented workflow and the real user experience before the paper and final `1.0.0` release;
- this should be treated as a final validation layer, not as a substitute for the internal support contract and test baseline.

## Temporary status

This file is temporary by design.

It should be removed or merged once:

1. `support_tiers.ipynb` has been rewritten as a real support contract;
2. `testing_strategy.md` has been aligned with parity obligations derived from that contract;
3. `performance_and_jit.md` has been synchronized with the implemented architecture;
4. the infrastructure baseline and public-function stability policy are reflected in the canonical `devguide` documents;
5. the current next-step priorities are reflected directly in the canonical `devguide` documents rather than in this temporary note.


## Ordered To-Do Checklist

This checklist is intentionally short. It is the execution-order summary of the broader discussion in this document. Each item below maps back to one or more sections above. If a future task does not fit under one of these headings, the plan is incomplete and this file must be updated before work continues.

1. **Lock the support contract**
2. **Derive parity obligations from that contract**
3. **Synchronize the performance and JIT manifesto**
4. **Implement the remaining in-scope `1.0.0` capabilities**
5. **Freeze sibling-library release baselines**
6. **Classify public API stability**
7. **Define the `1.x` deprecation policy**
8. **Validate release engineering and packaging**
9. **Raise meaningful coverage on the Tier 1 surface**
10. **Expand deterministic builder-based fixtures where they reduce truth ambiguity**
11. **Align developer and user-facing documentation with the implemented architecture**
12. **Enter beta-testing, dogfooding, paper writing, and the final stabilization window**

### Coverage of topics in this file

The checklist above covers every major topic described in this document:

- support tiers, capability guarantees, parity expectations, and heavy-mode status map to steps 1 and 2;
- `scalability_and_heavy_trajectories_v2.md`, Tier 1 heavy execution, and `MSM-*-HVY-*` implementation map to step 4;
- sibling version pinning across `smonitor`, `argdigest`, `depdigest`, and `pyunitwizard` map to step 5;
- the public-function stability sweep maps to step 6;
- the `1.x` deprecation policy maps to step 7;
- release CI, packaging validation, and install-story verification map to step 8;
- coverage growth and Tier 1 protection map to step 9;
- `MolSysBuilder` and declarative forms as deterministic test truth map to step 10;
- `devguide`, `docs/content/developer`, and user-facing documentation alignment map to step 11;
- beta-testing, dogfooding, paper writing, and release stabilization map to step 12.
