# MolSysMT 1.0 Execution Status

**Role:** operational status ledger
**Last updated:** 2026-08-13
**Plan:** [MolSysMT 1.0 Execution Plan](pending_proposals/release_1_0_execution_plan.md)
**Release checklist:** [Release Gate](release_gate.md)

## Purpose

This is the single current answer to:

- what is complete;
- what is in progress;
- what remains pending;
- what is blocked or deliberately deferred;
- what evidence permits the next stage to start.

The execution plan defines scope, order, weights, and exit criteria. Detailed
bug reports and proposals define individual contracts. This ledger records only
current execution state and evidence; it must not duplicate or redefine those
contracts.

## Status Vocabulary

| Status | Meaning |
| --- | --- |
| `DONE` | The declared exit gate passed with recorded evidence on an identified commit. |
| `IN PROGRESS` | This is the active segment or stage; work has started but its exit gate is not complete. |
| `PENDING` | Accepted work that has not started or cannot start until an earlier dependency closes. |
| `BLOCKED` | Work cannot advance because a named external decision, defect, resource, or prerequisite is unresolved. |
| `DEFERRED` | Explicitly outside the 1.0 critical path unless new correctness evidence promotes it. |

Only one top-level segment should normally be `IN PROGRESS`. If independent
packaging work runs in parallel, record the responsible branch or collaborator
and do not merge it across an unmet integration dependency.

## Current Release Snapshot

- **Active segment:** F — lifecycle and release candidate
- **Active stage:** F5 exact-commit recertification after bounded pre-1.0 fixes
- **Completed weighted closure:** 96% of the remaining 1.0 execution plan
- **Development-progress estimate:** Segments A and B are certified complete;
  the final exact-commit campaign passed the bounded two-backend oracle,
  independent scientific evidence, and all 9,774 effective application tests
  with Rust forced
- **Current repository state:** F1–F4 are closed. F5 passed previously on
  `8faf62785`, but subsequent pre-1.0 corrections to the selection-syntax
  contract, large-string form detection, and published API reference require a
  new exact-commit campaign. The remaining Common Core
  exception was removed in `c87a14036`: all 20 modules now use their permanent
  semantic manifest identities and the validator pins the 1–20 contract. The
  PyTraj, OpenFF, OpenMM construction, and missing-converter work that followed
  the 2026-08-07 snapshot is landed through `929d4363e`
- **Current exact Rust campaign commit:** `6485a0c08`; this is verified
  migration evidence but is not itself a release candidate, because Segment F
  lifecycle work is still open and no candidate has been tagged
- **Current exact Rust packaging commit:** `17be9ea50`; C2 is verified by a
  clean exact-commit `cp311-abi3` wheel and installed-extension smoke
- **Current C3 exact evidence commit:** `f79ccb4f0`; all five native abi3
  wheels build, audit, install, execute the private-extension smoke, and upload
  successfully in GitHub Actions run `30346103646`
- **Current C4–C7/E4 exact evidence commit:** `c4d8e9074`; five native wheels,
  15 platform/Python installed checks, three NumPy floors, three public smokes,
  the sdist round trip, and Rust quality/security gates pass in GitHub Actions
  run `30394881487`
- **Current E3 exact evidence commit:** `692479097`; 9,585 tests pass, two are
  accepted skips, and the fast release gate passes 12/12
- **Previous F5 exact candidate:** `8faf62785`; fast gates passed 12/12 locally, full matrix
  run `31589594289` passed on Ubuntu and macOS with Python 3.11--3.13, wheel run
  `31589594286` passed the supported Linux/macOS build and installed-runtime matrix
  (with Windows also green as experimental evidence), documentation run `31589594273`
  passed, and smoke run `31589594438` passed
- **Release readiness measure:** the formal weighted closure is 96%; no second
  subjective percentage is mixed into this operational ledger
- **Normal pytest:** the authority for test results
- **pytest-receptor:** the systematic compact reporter; disagreements must be
  reported upstream immediately
- **Next action:** land the three bounded pre-1.0 corrections, run the complete F5
  exact-commit campaign again, and only then complete F6 in one release sign-off
  commit: update `CITATION.cff`
  with the 1.0.0 title, version, release date, and selected Zenodo DOI; obtain
  maintainer approval; run every release gate on that exact commit; and tag only that
  verified commit. The current status-only checkpoint is not itself the tag candidate
- **Parallel packaging action:** Segment C is closed, and installed-wheel
  validation with it, so the only packaging work left is the Conda delivery
  track — coordinate sibling and MolSysMT Conda publication during manuscript
  writing or review
- **Parallel documentation and paper action:** with A–E and F1–F5 closed, the
  presentation surface, the documentation and the methods paper are a principal
  parallel workstream rather than a finishing touch. The framing and factual
  corrections landed as `d2b805e74`. Of the three items that required a maintainer
  decision, two are settled on 2026-08-07: Daniel Ibarrola-Sánchez is not an author
  and was removed from `CITATION.cff`, which also removes the ORCID misattributed to
  him, and the unreferenced duplicate landing page is deleted. Updating the DOI and
  version is deferred to F6 — `CITATION.cff` is a placeholder until the release
  closes, the canonical concept-versus-version DOI still requires selection, and the
  step is now in the release-gate sign-off. Only the timing of the
  Conda installation instructions remains open, in
  [Presentation and Citation Surface](pending_proposals/presentation_and_citation_surface.md).
  Public-facing code examples must be executed against the installed package
  before they are written: the 2026-07-29 audit found that none of the README's
  examples ran
- **Known independent release-gate debt:** the fast release gate passes 12/12
  on 2026-08-12. Form-adapter delivery is green with 89/89 forms, 78 accepted
  lower-tier declarations across nine forms, 343 resolved baseline
  declarations, and no Tier-1 debt. Conversion fidelity reports 40 exhaustive
  Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges,
  and zero new debt

The 99% figure measures only the newly defined remaining-plan exit gates. It
does not attempt to restate the much larger body of MolSysMT development,
consolidation, or Rust kernel work completed before this ledger was created.

## Segment Ledger

| Segment | Weight | Status | Earned | Current evidence or reason |
| --- | ---: | --- | ---: | --- |
| A — conversion-fidelity coherence | 25% | `DONE` | 25% | 40 exhaustive Tier-1 edges, 441 accepted non-exhaustive edges, 29 resolved baseline edges, zero new debt, and all conversion/form gates pass |
| B — final Numba oracle | 10% | `DONE` | 10% | exact commit `6485a0c08` passes the 264-test bounded two-backend oracle, combined scientific and blocker gates, and the complete forced-Rust suite with 9,769 passed and 5 accepted skips; the dated artifact preserves source and binary hashes |
| C — Rust packaging | 20% | `DONE` | 20% | C1–C7 pass: permanent backend, private abi3 integration, five native wheels, Python 3.11–3.13, NumPy floors, sdist/package parity, and Rust quality/security gates |
| D — Rust-only cut | 20% | `DONE` | 20% | the runtime, dependencies, tests, controls, and GPU experiments are Numba-free; compatibility facades route to Rust, the executable zero gate passes, and the affected scientific surface passes 450 tests |
| E — scientific and ecosystem validation | 15% | `DONE` | 15% | E1–E6 pass: Rust/scientific/full-suite gates, installed-wheel matrix, maturity-weighted consumers, and runtime/thread benchmarks |
| F — lifecycle and release candidate | 10% | `IN PROGRESS` | 6% | F1–F4 are done; F5 must be recertified after three bounded pre-1.0 corrections, then F6 sign-off and tag remain |
| **Total** | **100%** | **`IN PROGRESS`** | **96%** | A–E use complete segment gates; F uses the explicit stage weights below |

### B4 Pause Checkpoint — Transactional Structural Growth

The active uncommitted vertical defines one structural-axis contract for
`Structures`, `StructuresDict`, `MolSys`, `append_structures()`, and
`concatenate_structures()`:

- topology-free structural sources remain valid when atom counts match;
- every materialized structural series covers the complete structure axis;
- append validates the source and target before mutation;
- `attribute_policy='intersection'` retains shared series and reports all
  discarded one-sided attributes;
- `attribute_policy='strict'` rejects one-sided attributes without modifying
  the target;
- the public API, User Guide, Common Core course, and native contract describe
  the same behavior.

Evidence before pausing:

- focused native/API gate: 51 passed;
- expanded native-form/H5MSM gate: 1,254 passed;
- warning reconstruction and public structural-growth gate: 20 passed;
- both edited User Guide notebooks parse as valid JSON;
- pytest-receptor agreed with pytest on every verdict and exit code.

This checkpoint is landed in the current structural-growth commit. Resume with
the remaining NGL adapter causes, then rebuild the exact-commit Rust wheel and
repeat the forced-Rust release gate. Do not absorb the independent
release-plan, conversion, Rust, or archive WIP already present in the working
tree.

The H5MSM 0.5 independent-layer design discovered during this vertical is
recorded separately in
[H5MSM 0.5 Modular Layer Contract](pending_proposals/h5msm_0_5_modular_layers.md).
It is not part of this implementation checkpoint or the default 1.0 critical
path.

### B4 NGLView Fidelity Checkpoint

The three remaining NGLView causes from the first campaign are closed in this
checkpoint:

- MolSysMT-created single-component widgets retain an isolated private topology
  snapshot instead of losing identifiers and chemical bond metadata through
  PDB;
- external, empty, coordinate-only, and multicomponent widgets do not
  implicitly acquire that snapshot or claim topology they do not contain;
- multi-structure trajectories keep their complete coordinate axis without
  retaining one-structure PDB metadata as a partial series;
- group-level hydrogen-bond rendering preserves the input pair order instead
  of relying on the canonical sorted selection result.

Evidence at landing:

- complete NGLView surface: 45 passed under forced Rust;
- broad conversion/get/compare/view/PDB/Structures surface: 746 passed under
  forced Rust;
- Ruff and `git diff --check`: pass.

The instance-level contract is recorded in
[NGLView Adapter Contract](nglview_adapter_contract.md). With this checkpoint
landed, B4 has no known targeted application root cause remaining and must move
directly to the new exact-commit campaign.

## Segment A — Conversion-Fidelity Coherence

**Canonical bug:**
[Conversion Fidelity WIP Exposes Multiple Contract Gaps](archive/resolved_bugs/conversion_fidelity_wip_contract_gaps.md)

| Stage | Status | Dependency | Closure evidence required |
| --- | --- | --- | --- |
| A1 — audit-scope contract | `DONE` | none | landed as `504df91d0`; scope API, compatibility, tests, and lifecycle docs complete |
| A2 — exhaustive native-dictionary audit | `DONE` | A1 | three evidence-backed native-to-dictionary profiles landed; 51 focused tests and the Tier-1 ratchet pass |
| A3 — independent schema/adapter repairs | `DONE` | A1–A2 stable | direct native projections and all four builder routes have evidence-backed exhaustive reports; the broad native-scope module is green |
| A4 — PDB fidelity | `DONE` | A1–A2 stable | one handler-owned normalized parser feeds file, text, and handler routes; 22 fidelity tests and the historical PDB corpus pass; 11 exhaustive profiles landed as `1f656fe9f` |
| A5 — segment integration gate | `DONE` | A1–A4 | 40/481 edges are exhaustive, 441 are accepted debt, 29 baseline edges are resolved, zero are new; adapter delivery and lifecycle gates pass |

| A2 cohort | Status | Evidence |
| --- | --- | --- |
| A2.1 — `Structures -> StructuresDict` | `DONE` | exhaustive 22-attribute contract partition, current schema-loss reporting, strict rejection, lifecycle documentation, and conservative fidelity ratchet landed as `cb123e226` |
| A2.2 — `Topology -> TopologyDict` | `DONE` | 76-attribute contract partition, 24 value-dependent loss candidates, multi-state collapse, conditional aromatic mapping, strict rejection, and lifecycle documentation landed as `4a4773986` |
| A2.3 — `MolSys -> MolSysDict` | `DONE` | composed 114-attribute contract, seven structural losses, 18 mechanical losses, state association, strict rejection, and lifecycle documentation landed as `01067f2c5` |

### Completed A1 Objective

Implement one authoritative scope contract:

1. add backward-compatible `ConversionIssue.scope`;
2. add `get_conversion_audit_scopes(source, target)`;
3. add `is_conversion_audit_exhaustive(source, target)`;
4. make the helpers authoritative for conservative static graph coverage;
5. let instance-aware reports strengthen the static result only with explicit
   evidence;
6. keep the exhaustive-pair registry empty until A2 implements and tests the
   corresponding schema traversal.

### Current A1 Non-Goals

- exhaustive schema traversal, which belongs to A2;
- independent schema and adapter fixes, which belong to A3;
- PDB identifier and strictness repairs, which belong to A4;
- implementing or repairing the complete conversion graph;
- Rust packaging or Numba deletion.

### Conversion Critical-Path Rule

A conversion blocks Segment A only when it exposes:

- shared audit or conversion infrastructure failure;
- silent corruption or incorrect success;
- atom/structure misalignment;
- an advertised Tier 1 contract violation;
- new, unclassified fidelity debt.

Known, reported non-exhaustive behavior and low-priority Tier 2/3 routes remain
visible in the baseline or backlog and may be addressed later. They must not be
silently reclassified merely to make the gate green.

### A2 Cohort Design

The native-dictionary audit is divided into three reviewable cohorts:

1. **A2.1 — `Structures -> StructuresDict`:** classify every semantic in the
   declared `molsysmt.Structures` form contract as preserved, derived, absent in
   the source instance, or lost by the current dictionary schema.
2. **A2.2 — `Topology -> TopologyDict`:** apply the same contract to stable
   topology and chemical-state semantics, including optional bond and atom
   state fields.
3. **A2.3 — `MolSys -> MolSysDict`:** compose the proven topology and
   structures audits, then add molecular-mechanics and
   structure-to-chemical-state association semantics.

`is_exhaustive` is relative to the declared public semantic contract of the
source form, not every private implementation field and not every attribute
that another form happens to expose. Derived attributes are not reported as
lost when their required information remains representable.

Each cohort requires an explicit conversion-schema manifest. The ordinary form
`attributes` mapping is not sufficient evidence: it describes query
capabilities, while conversion fidelity asks which source semantics the
specific serializer actually preserves. This distinction is already visible
in `TopologyDict`, whose capability declaration mirrors `Topology` although
the current 0.1 serializer stores a narrower payload.

The first cohort is deliberately `Structures -> StructuresDict`: its native
storage contract is bounded, and it can prove the audit machinery before the
multi-state topology model is involved. A2.1 must report current unsupported
thermodynamic and bioassembly payloads honestly; extending the dictionary
schema or converter remains an independent A3 repair.

### A2.2 Topology Profile Design

The `Topology -> TopologyDict` profile covers the 76 attributes declared by
the native topology form. It must classify them in the following groups:

1. **Direct stable inventory:** atom, group, chain, molecule, and entity
   identifiers, names, types, membership, isotope, bond endpoints, formal bond
   order, and bond relationship type written by the 0.1 converter.
2. **Derived without loss:** indices, counts, inner-bond views, bonded-atom
   views, and biomolecule counts whose complete source data remain available.
3. **State-inventory limitations:** multiple chemical states collapse to one
   resolved state; a non-default state identifier, reference-state choice, and
   completeness/evidence metadata require value-aware checks.
4. **Component limitations:** version 0.1 has no component section. Connectivity
   can reconstruct a partition, but explicit component membership and
   component IDs, names, types, completeness, and evidence are not thereby
   proven preserved.
5. **Optional atom-state limitations:** formal charge, aromaticity, radicals,
   implicit-hydrogen policy, and stereochemistry are absent from the 0.1
   payload.
6. **Optional bond-state limitations:** bond ID, fractional order, conjugation,
   stereochemistry and reference atoms, donor/acceptor direction,
   component-joining semantics, and evidence are absent.
7. **Conditional aromatic mapping:** the converter can encode an aromatic flag
   through the legacy `bond_order="aromatic"` value only when no formal bond
   order takes precedence. The audit must not call this preservation in a
   source row that carries both semantics.

Presence checks must inspect the selected native chemical state directly.
`Topology.has_attribute()` is a public query-capability helper and currently
returns true for some default or absent state metadata; using it blindly would
create false losses. Multi-state inspection must cover every stored state even
when a reference state exists, because the serializer emits only one state.

A2.2 reports current schema losses. It does not add fields to `TopologyDict`,
change component inference, or repair an independent converter defect. Those
remain focused A3 work.

### A3 Repair Partition

The nine remaining failures in the broad native-scope module are not one gate:

| Cohort | Classification | Release treatment |
| --- | --- | --- |
| unconditional preflight on ordinary `convert()` | systemic performance and layering defect | first A3 repair |
| `atom_index` and `n_atoms` not classified as structural | central attribute-policy contradiction | second A3 repair |
| missing thermodynamic series in `StructuresDict` | schema and two-way adapter gap | focused A3 repair |
| `StructuresDict -> MolSys` lacks `skip_digestion` | adapter signature defect | focused A3 repair |
| unconditional `chemical_state_id` expectation for a `None` ID | WIP test-contract error | correct the test; do not invent an ID or loss |
| native `MolSys` projections | additional exhaustive route profiles | assess after systemic repairs; not part of the dictionary-profile gate |
| `MolSys <-> MolSysBuilder` and builder-to-dictionary routes | additional exhaustive route profiles | assess after systemic repairs; do not make them block unrelated work |

The four coordinate-trajectory failures are also route-promotion requests
(`XYZ`, ASCII XYZ, DCD, and XTC), not demonstrated conversion failures. Their
selection, units, and cursor assertions execute beyond the report assertion.
They remain visible candidates for bounded Tier-1 profiles but do not join the
A3 critical path merely because they request `is_exhaustive=True`.

The PDB `evidence` and `int("fram")` symptoms belong to A4 with the rest of the
PDB fidelity causes. Moving them out of A3 prevents a PDB-specific parser
workstream from blocking independent schema repairs.

A3 order:

1. bypass preflight when no report or strictness is requested;
2. align atom-inventory attribute classification;
3. extend and round-trip the selected `StructuresDict` thermodynamic fields;
4. repair the `skip_digestion` adapter signature;
5. correct the invalid `chemical_state_id` expectation;
6. decide which remaining native projection or builder profiles are required
   for the advertised 1.0 Tier-1 surface and defer the rest explicitly.

| A3 cohort | Status | Evidence |
| --- | --- | --- |
| A3.1 — opt-in conversion preflight | `DONE` | ordinary conversion bypass, explicit-report execution, strict rejection, public doctest, and lifecycle documentation landed as `dd13cb351` |
| A3.2 — atom-inventory classification | `DONE` | shared topological/structural classification, focused policy tests, 74 consumer tests, lifecycle documentation, and course validation landed as `998abe325` |
| A3.3 — `StructuresDict` thermodynamic series | `DONE` | two-way unit-bearing series, derived total energy, ordered selection, capability queries, report preservation, lifecycle documentation, and 19 focused tests landed as `006d9e4ed` |
| A3.4 — `StructuresDict -> MolSys` signature | `DONE` | standard signatures, correct local mechanics adapter, matched selected atom axes, lifecycle documentation, and 15 form tests landed as `ab28213c0` |
| A3.5 — invalid state-ID expectation | `DONE` | WIP expectation corrected without fabricating an ID; explicit tracked regression landed as `0434b9b42` |
| A3.6 — remaining native/builder profiles | `DONE` | direct projections, complete builder contracts, builder routes, and bounded coordinate-trajectory profiles are integrated |

A3.6 is split so incomplete builder metadata cannot block or weaken direct
native projection evidence:

| A3.6 cohort | Status | Decision and closure boundary |
| --- | --- | --- |
| A3.6a — direct native projections | `DONE` | four Tier-1 profiles traverse every declared source attribute with instance-aware scope and strict-loss evidence; 37 focused tests and the 481-edge ratchet pass; landed as `c40e3154e` |
| A3.6b — complete native/builder attribute contract | `DONE` | native presence composes stored state; builder declares the exact 96-attribute topology/structures union and delivers every declaration directly; landed as `53fec7b09` and `eb07e6e28` |
| A3.6c — builder conversion profiles | `DONE` | four routes are exhaustive; selected dictionary export canonicalizes atoms, preserves structure order, reports reduced-schema loss, and reconstructs components without inventing hierarchy fallbacks; landed as `4bc1dde7b` |

Direct projection profiles may use one declared-contract traversal shared by
the four approved pairs. This is exhaustive only because it iterates every
attribute the source form declares, performs instance-aware presence checks,
and records every present attribute unsupported by the target with its
topology, structures, chemical-state, or molecular-mechanics scope. It must
not be applied to `MolSysBuilder` until the builder's declaration matches its
actual stored semantics.

A3.6b has two ordered prerequisites:

1. **A3.6b.1 — native instance presence.** Complete and test
   `Topology.has_attribute()` and `Structures.has_attribute()`, then make
   `MolSys.has_attribute()` compose those authoritative helpers rather than
   duplicate partial lists. Minimal empty objects currently report absent
   `temperature`, energy, occupancy, bioassembly, state-ID, and component
   metadata as present; reference-state semantics require an explicit
   single-state versus multi-state distinction.
2. **A3.6b.2 — builder contract.** Define `MolSysBuilder.attributes` as the
   exact union of the native topology and structures contracts (96 current
   attributes, 64 more than its present declaration), delegate missing getters
   directly to `builder.topology` or `builder.structures` without calling
   `build()`, and compose instance presence from the corrected native helpers.

The builder must not declare molecular-mechanics fields or
`structure_chemical_state_index`: it stores neither domain. A test must assert
both union equality and getter availability for every declared attribute so
the contract cannot silently drift again.

The untracked native-scope test module was not one A2 gate. It originally
exposed 13 failures across:

- the three A2 audit cohorts;
- attribute-policy classification;
- thermodynamic schema expansion;
- a `skip_digestion` adapter defect;
- ordinary-conversion preflight bypass;
- `MolSysBuilder` fidelity;
- reverse and projection routes.

Tests must be split or selected by contract rather than made green through one
cross-cutting change.

After A2, A3.1, and A3.2, the same module reports 7 failures and 6 passes. The
atom-inventory failure closed independently; the remaining failures still map
to A3.3–A3.6.

### A3.3 Design Boundary

`molsysmt.native.structures_dict.structures_parameters` already declares
`temperature`, `potential_energy`, and `kinetic_energy`. A3.3 therefore repairs
an incomplete implementation of the existing native dictionary contract; it
does not introduce a new schema or require an H5MSM version increase.

The focused repair must:

1. serialize the three materialized series from `Structures`, preserving
   quantity units and requested structure order;
2. expose them through the `StructuresDict` attribute map, getters, and
   instance-aware `has_attribute()`;
3. derive `total_energy` only when both energy series are present;
4. rebuild `Structures` with the three series and preserve repeated or
   non-monotonic `structure_indices`;
5. update the exhaustive conversion profile so these fields cease to be
   reported as losses only after the executable round trip passes;
6. keep absent optional series absent rather than synthesizing values.

A3.3 does not silently absorb the broader coordinate-free native-structures
contract. `native_structures_contract.md` says that a thermodynamic-only
representation is valid, while the current `Structures.n_structures` and parts
of `StructuresDict` still infer axes primarily from coordinates, velocities,
or box. That systemic inconsistency requires its own bounded repair and
evidence; it must not be hidden inside the dictionary adapter commit.

The untracked compact baseline was created with 62 routes already assumed
exhaustive, before executable audit profiles existed. Because it has never
landed as a release baseline, it must be regenerated once from the conservative
A1 state. Thereafter, each A2 cohort removes only the route it has earned from
accepted non-exhaustive debt. This is a correction of an aspirational initial
baseline, not permission to weaken a landed ratchet.

### Current A1 Evidence to Capture

- **Focused contract and regression tests:** 28 passed with
  `tests/_private/test_conversion_report_scopes.py` and
  `tests/conversion_truth/test_native_bond_seam_adapters.py`.
- **Combined audit observation:** 31 passed and 2 expected A2 failures. The
  former five-test ImportError root cause is closed.
- **Static audit:** reaches its report and records 481 non-exhaustive edges,
  including 62 new relative to the aspirational baseline. A2 must earn those
  exhaustive classifications; A1 does not hide them.
- **Compatibility:** existing two- and three-positional-argument
  `ConversionIssue` construction remains valid because `scope` follows `kind`
  with a `chemical_state` default.
- **Ruff:** changed Python files pass.
- **Public docstring doctest:** 1 passed.
- **Lifecycle documentation:** the existing User Guide Foundations, Toolbox,
  Cookbook, and Common Core conversion-report explanations now document issue
  scope; all four notebooks remain valid JSON.
- **Developer-guide validation and `git diff --check`:** pass.
- **Files changed for implementation:**
  `molsysmt/basic/conversion_report.py`,
  `molsysmt/_private/conversion_report.py`, and
  `tests/_private/test_conversion_report_scopes.py`.
- **Landing:** focused implementation, tests, and lifecycle documentation
  committed as `504df91d0`.

## Segment B — Final Numba Oracle

| Stage | Status |
| --- | --- |
| B1 — generated active-Numba inventory | `DONE` |
| B2 — CPU kernel-to-consumer/evidence manifest | `DONE` |
| B3 — deliberate divergence and tolerance record | `DONE` |
| B4 — final forced-Rust campaign plus bounded Numba oracle | `DONE` |
| B5 — dated, committed oracle artifact | `DONE` |

Existing Rust port and dogfooding results are prerequisites, not B-segment
completion. No new Numba capability may be added while this segment is pending.

## Segment C — Rust Packaging

| Stage | Status |
| --- | --- |
| C1 — permanent crate/module and build-backend design review | `DONE` |
| C2 — production crate relocation and private extension integration | `DONE` |
| C3 — supported Linux/macOS and experimental Windows abi3 wheel CI | `DONE` |
| C4 — Python 3.11–3.13 and supported NumPy installed-wheel tests | `DONE` |
| C5 — sdist contract | `DONE` |
| C6 — metadata, resources, entry points, typing, and lazy-discovery parity | `DONE` |
| C7 — Rust quality, security, license, and portability gates | `DONE` |

Conda publication is tracked separately and does not block C4: controlled
preinstalled sibling dependencies may be used to validate the MolSysMT wheel.
The local pilot wheel closed the C1 design question. The clean exact-commit
wheel recorded in
[C2 Rust Packaging Artifact](release_1_0_rust_packaging_c2_artifact.md)
closes C2 but does not substitute for the C3-C7 matrices.

C1 is closed by [C1 — Permanent crate/module and build-backend design
review](archive/resolved_proposals/rust_packaging_backend_design.md): keep `setuptools`, add
`setuptools-rust`, ship one private `molsysmt._rust` abi3 extension inside the official
Conda package, and do not adopt maturin or a separate `msm_rust_kernels` distribution. Two
findings became binding C3 contracts (clean-build isolation with automated wheel
inspection, and abi3 proven per target rather than assumed from the tag). The earlier
report of a PyPI resolution failure as a C4 blocker is **corrected**: neither
PyPI nor the coordinated Conda channel is a prerequisite for validating the
MolSysMT wheel itself.

C2 started only after B4 closed. Commit `17be9ea50` relocates the crate to
`rust/`, integrates it as `molsysmt._rust`, removes the obsolete separate-package
prototype, and adds an executable wheel-content validator. A clean clone of that
exact commit produced
`molsysmt-0.20.0+156.g17be9ea50-cp311-abi3-linux_x86_64.whl` with SHA256
`a7da5d72804e0df12bbeb7b32c52e55cd34633ae9f0bc3ee34bcf15e4a7ecca5`;
the installed extension exposed all 97 entries and passed a minimum-image smoke.

C4–C7 close on exact commit `c4d8e9074` and GitHub Actions run
`30394881487`. Five native wheels pass 15 platform/Python checks, three NumPy
floors, three installed public smokes, the source-distribution round trip, and
the complete Rust quality/security boundary. The exact artifact names, hashes,
scope, and non-Conda qualification are recorded in
[C4–C7 Rust Packaging Artifact](release_1_0_rust_packaging_c4_c7_artifact.md).

## Segment D — Rust-Only Cut

| Stage | Status |
| --- | --- |
| D1 — direct Rust CPU routing and dispatch removal | `DONE` |
| D2 — CPU Numba/JIT implementation deletion | `DONE` |
| D3 — GPU capability audit and Numba-CUDA deletion | `DONE` |
| D4 — dependencies, warmup, diagnostics, API, docs, and course cleanup | `DONE` |
| D5 — executable zero-Numba/Numba-CUDA/llvmlite gate | `DONE` |
| D6 — session and per-function Rayon resource controls | `DONE` |

## Segment E — Rust-Only Validation

| Stage | Status |
| --- | --- |
| E1 — Rust unit, property, error, panic, GIL, and threading tests | `DONE` |
| E2 — independent scientific-truth matrix | `DONE` |
| E3 — complete MolSysMT suite and release fast gates | `DONE` |
| E4 — installed-wheel platform/Python matrix | `DONE` |
| E5 — maturity-weighted direct-consumer smoke | `DONE` |
| E6 — cold/warm, memory, thread, and oversubscription benchmarks | `DONE` |

### E1–E2 Closure Evidence — 2026-07-28

- `cargo test --manifest-path rust/Cargo.toml --no-default-features`: 80 passed.
- `cargo clippy --manifest-path rust/Cargo.toml --no-default-features -- -D warnings`:
  pass. Deliberate fixed-size and FFI exceptions are local, documented, and do
  not rewrite hot loops solely to satisfy style.
- `python -m pytest --receptor=llm tests/basic/test_parallel_control.py tests/rust -n 4`:
  100 passed before the three boundary regressions were added.
- `tests/rust/test_threading_boundaries.py`: 3 passed, proving representative
  GIL release, simultaneous cached Rayon pools with bounded oversubscription,
  result stability, and conversion of a native panic into a contained Python
  process failure.
- `python -m pytest --receptor=llm tests/scientific_truth -n 12`: 98 passed.
- `validate_scientific_evidence.py`: 43 validated, 0 partial, 0 gaps.
- `check_rust_hot_paths.py`: 18 Rust hot-path files clean.

E1 validates the private extension through representative boundary families;
public wrappers remain the authority for typed argument validation. The
private extension is not a supported user API.

### E5 Consumer Compatibility Evidence — 2026-07-28

Consumer evidence is weighted by release maturity. MolSysViewer is a
foundational MolSysSuite component and therefore a blocking integration gate.
TopoMT and PharmacophoreMT are earlier-stage consumers: their smoke workflows
are diagnostic, and consumer-local adaptation debt does not block MolSysMT
1.0.

- MolSysViewer direct MolSysMT integration and loader smoke: 5 passed.
- TopoMT pocket, physicochemistry, and parity smoke: 7 passed.
- PharmacophoreMT import smoke: passed.
- PharmacophoreMT ER-alpha workflow: failed in consumer code because
  `complex_based.py` calls `msm.get(..., element=True)`. In MolSysMT,
  `element` selects the semantic element level and is not an attribute request.
  The consumer must request the atom element-symbol attribute through the
  current public contract. This is classified as non-blocking
  PharmacophoreMT adaptation debt.

No consumer repository was modified during this audit. TopoMT also retains a
best-effort, exception-swallowed call to the removed `msm.warmup()` in its test
configuration; that cleanup belongs to TopoMT and does not affect the passing
runtime smoke.

### E6 Runtime Benchmark Evidence — 2026-07-28

The exact clean commit `746e22c5f` was measured through the isolated,
correctness-checking Rust-only release benchmark. The machine-readable result
is `release_1_0_rust_runtime_benchmark.json`; its interpretation and
reproduction command are in
[MolSysMT 1.0 Rust Runtime Benchmark](release_1_0_rust_runtime_benchmark.md).

- first native call / best repeated call: 1.60x, with zero Numba cache files;
- incremental peak over a 27.48 MiB payload: 3.80 MiB;
- measured two/four-thread speedups: 1.93x and 3.47x;
- four concurrent calls using two Rayon threads each completed with identical
  correct results;
- the complete suite had already passed under `-n 12`, covering the
  xdist-plus-Rayon process surface.

The numbers describe one recorded host and are not cross-platform performance
guarantees. Installed-wheel identity is separately proven by the closed C4/E4
matrix.

## Parallel Conda Delivery Track

This track is required before claiming a validated package is available from
the `uibcdf` Conda channel, but it is not part of the technical critical path
for the 1.0 source/tag, scientific validation, or manuscript:

1. publish compatible sibling versions for Python 3.11–3.13;
2. update and test the MolSysMT recipe with the Rust toolchain and runtime pins;
3. build MolSysMT for the supported Conda platform/Python matrix;
4. verify a clean channel-only installation with no checkout leakage.

## Segment F — Lifecycle and Release Candidate

| Stage | Weight | Status | Earned |
| --- | ---: | --- | ---: |
| F1 — Four Paths numbering and structural validation | 1% | `DONE` — 20 + 4x34 notebooks, semantic manifest identities and no validator exception at `c87a14036` | 1% |
| F2 — applicable Common Core and changed-behavior notebook execution | 2% | `DONE` — 40/40 pass from clean kernels at `2f6fd59d1` | 2% |
| F3 — function support-tier and pending-guide hygiene | 1% | `DONE` — 117 Tier 1, 56 Tier 3, seven outside-contract; completed records archived | 1% |
| F4 — User Guide, Cookbook, API, demos, and course lifecycle closure | 2% | `DONE` | 2% |
| F5 — clean exact-commit fast, full, wheel, and documentation gates | 3% | `IN PROGRESS` — the previous exact campaign remains valid historical evidence, but the new candidate must pass again | 0% |
| F6 — 1.0 release candidate and tag | 1% | `PENDING` — waits for the recertified F5 commit | 0% |
| **Segment F total** | **10%** | **`IN PROGRESS`** | **6%** |

## Deferred Work

These remain `DEFERRED` unless a correctness defect promotes them:

- additional native format parsers;
- Arrow and optional-column memory experiments;
- reactive interactions and chemical-state expansion beyond the 1.0 boundary;
- speculative Rust GPU work and fused multi-observable kernels;
- broad Tier 2 and Tier 3 adapter expansion;
- nonessential post-threshold micro-optimization;
- paper extensions that alter no release contract.

## Update Procedure

Update this ledger whenever a stage changes status:

1. change only the affected stage and segment rows;
2. record the exact command, result, and commit in the execution log;
3. add earned weight only when the applicable segment or explicit F-stage exit
   gate passes; never count the F total again after summing its stages;
4. name blockers explicitly; never hide them inside `PENDING`;
5. preserve accepted omissions and deferred work;
6. identify the next active stage;
7. run `python devtools/scripts/validate_devguide.py`;
8. include the ledger update with the stage-closing commit.

If evidence was produced on a dirty tree, label it development evidence. Replace
it with exact-commit evidence before marking a release gate `DONE`.

## Execution Log

| Date | Segment/stage | Transition | Evidence | Commit |
| --- | --- | --- | --- | --- |
| 2026-07-26 | Overall plan | status ledger created | planning and repository audit; no implementation gate claimed | dirty WIP at `7ab96e791` |
| 2026-07-26 | A / A1 | `PENDING` → `IN PROGRESS` | 38-failure diagnosis and four-stage resolution plan accepted | dirty WIP at `7ab96e791` |
| 2026-07-26 | A1 implementation | remains `IN PROGRESS` pending landing | 28 focused passes; 1 doctest; combined audit surface 31 passed / 2 A2 failures; Ruff, notebook JSON, and devguide green | dirty WIP based at `7ab96e791` |
| 2026-07-26 | A1 | `IN PROGRESS` → `DONE` | scope contract, regression tests, and lifecycle documentation landed | `504df91d0` |
| 2026-07-26 | A2 design | `PENDING` → `IN PROGRESS` | conservative registry exposes 62 aspirational exhaustive routes requiring evidence-backed cohorting | dirty WIP after `504df91d0` |
| 2026-07-26 | A2 design audit | remains `IN PROGRESS` | 118 canonical attributes inspected; form capability maps and serialized-schema fidelity are distinct; focused module reports 13 independent root causes; A2 split into three native-to-dictionary cohorts | dirty WIP after `504df91d0` |
| 2026-07-26 | A2.1 | `IN PROGRESS` → `DONE` | 38 focused tests; 1 exhaustive and 480 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `cb123e226` |
| 2026-07-26 | A2.2 | `PENDING` → `IN PROGRESS` | topology serialization-boundary audit selected as the next cohort | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 design audit | remains `IN PROGRESS` | 76 declared topology attributes partitioned into stable, derived, state-inventory, component, optional atom/bond, and conditional aromatic semantics | dirty WIP after `cb123e226` |
| 2026-07-26 | A2.2 | `IN PROGRESS` → `DONE` | 44 focused tests; 2 exhaustive and 479 accepted non-exhaustive Tier-1 edges; zero new debt; Ruff, lifecycle notebooks, and developer-guide validation pass | `4a4773986` |
| 2026-07-26 | A2.3 | `PENDING` → `IN PROGRESS` | composed native MolSys audit selected as the next cohort | dirty WIP after `4a4773986` |
| 2026-07-26 | A2.3 | `IN PROGRESS` → `DONE` | 51 focused tests; 3 exhaustive and 478 accepted non-exhaustive Tier-1 edges; zero new debt; broad native-scope module reduced to 9 independent failures | `01067f2c5` |
| 2026-07-26 | A2 | `IN PROGRESS` → `DONE` | all three native dictionary cohorts landed with explicit complete-source contracts | `cb123e226`, `4a4773986`, `01067f2c5` |
| 2026-07-26 | A3 | `PENDING` → `IN PROGRESS` | remaining independent schema, attribute-policy, adapter, and preflight repairs selected for classification | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3 classification | remains `IN PROGRESS` | 9 broad native-scope failures split into 5 focused repairs and optional route promotion; 4 coordinate failures classified as profile requests; PDB-specific symptoms assigned to A4 | dirty WIP after `01067f2c5` |
| 2026-07-26 | A3.1 | `IN PROGRESS` → `DONE` | 54 focused tests and public doctest pass; ordinary conversion no longer constructs an unused preflight; broad native-scope module reduced to 8 independent failures | `dd13cb351` |
| 2026-07-26 | A3.2 | `PENDING` → `IN PROGRESS` | atom inventory classification selected as the next systemic repair | dirty WIP after `dd13cb351` |
| 2026-07-26 | A3.2 | `IN PROGRESS` → `DONE` | 74 consumer tests pass across attribute policy, compare, iterator, get, and StructuresDict round-trip; broad native-scope module reduced from 8 to 7 independent failures; Ruff, notebook JSON, and course validation pass | `998abe325` |
| 2026-07-26 | A3.3 design audit | `PENDING` → `IN PROGRESS` | thermodynamic keys already belong to the declared StructuresDict contract; missing two-way adapters, getters, capabilities, selection, and audit-profile preservation identified; coordinate-free native contract explicitly kept separate | dirty WIP after `998abe325` |
| 2026-07-26 | A3.3 | `IN PROGRESS` → `DONE` | optional temperature and energy series preserve units and arbitrary requested order in both directions; total energy remains derived; broad native-scope module reduced from 7 to 6 failures | `006d9e4ed` |
| 2026-07-26 | A3.4 | `PENDING` → `DONE` | standard adapter signatures, correct local mechanics dispatch, and matching selected topology/structure atom axes; 15 form tests pass | `ab28213c0` |
| 2026-07-26 | A3.5 | `PENDING` → `DONE` | absent optional state ID no longer expected as a loss; production unchanged; 15 contract tests pass and broad module reduced to 5 route-profile failures | `0434b9b42` plus corrected untracked WIP test |
| 2026-07-26 | A3.6 design audit | `PENDING` → `IN PROGRESS` | four direct native projections accepted as Tier 1; builder profiles held behind a complete builder attribute-contract audit | dirty WIP after `0434b9b42` |
| 2026-07-26 | A3.6a | `IN PROGRESS` → `DONE` | 37 focused tests; four direct profiles accepted; exhaustive coverage 3 → 7 and accepted debt 478 → 474 with zero new or unresolved baseline drift; lifecycle documentation and course validation pass | `c40e3154e` |
| 2026-07-26 | A3.6b | `PENDING` → `IN PROGRESS` | complete builder attribute contract selected as the prerequisite to any builder-profile promise | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b design audit | remains `IN PROGRESS` | builder declares 32 of 96 stored native attributes; 64 missing; empty native forms demonstrably return false-positive presence for optional thermodynamic, occupancy, bioassembly, state-ID, and component fields; reference-state semantics require separate review; native presence repair ordered before builder delegation | dirty WIP after `c40e3154e` |
| 2026-07-26 | A3.6b.1 | `IN PROGRESS` → `DONE` | native `Topology`, `Structures`, and composed `MolSys` presence contracts now distinguish declared capability from instance state; 1,601 broad consumers and 70 focused tests pass | `53fec7b09` |
| 2026-07-26 | A3.6b.2 | `IN PROGRESS` → `DONE` | builder declares the exact 96-attribute stored union, all declarations have direct getters, representative chemistry and thermodynamic reads do not materialize `MolSys`, 185 consumer tests pass, and five lifecycle notebooks execute successfully | `eb07e6e28` |
| 2026-07-26 | A3.6c | `PENDING` → `IN PROGRESS` | the broad native-scope module now has exactly three independent failures, all caused by missing exhaustive builder conversion profiles; conversion ratchet remains 7 exhaustive, 474 accepted debt, and zero drift | dirty WIP after `eb07e6e28` |
| 2026-07-26 | A3.6c | `IN PROGRESS` → `DONE` | four builder routes promoted with distinct evidence; atom selection and structure ordering fixed; isotope and derived-component seams repaired; 13 broad-scope, 88 builder/dictionary, and 49 convert tests pass; five lifecycle notebooks execute; coverage 7 → 11 and accepted debt 474 → 470 with zero drift | `4bc1dde7b` |
| 2026-07-26 | A3 | `IN PROGRESS` → `DONE` | all independent native schema, adapter, presence, projection, and builder-profile repairs are landed; PDB-specific work remains isolated in A4 | `dd13cb351` through `4bc1dde7b` |
| 2026-07-26 | A4 design audit | `PENDING` → `IN PROGRESS` | 21 PDB failures reduced to five shared causes; duplicate parsing between the handler and native adapters identified as the architectural root | dirty WIP after `18136a95d` |
| 2026-07-26 | A4 | `IN PROGRESS` → `DONE` | handler-owned normalized content now governs file, text, and handler input; canonical alternate sites, explicit chemistry, bioassemblies, canonical writing, payload-aware reports, 22 PDB tests, 139 historical/integration tests, and 60 convert tests pass; exhaustive coverage 11 → 22 with zero new debt | `1f656fe9f` |
| 2026-07-26 | A5 | `PENDING` → `IN PROGRESS` | Segment A integration gate selected; known external-form attribute-delivery debt remains explicit and PDB adapters themselves pass | dirty WIP after `1f656fe9f` |
| 2026-07-26 | A5 / Segment A | `IN PROGRESS` → `DONE` | isolated committed-snapshot reconstruction passes 85 tests; form adapters 89/89; exhaustive conversion coverage 22 → 37; accepted debt 470 → 444; zero new debt; Ruff, dependencies, devguide, course, demos, resources, scientific evidence, Rust hot paths, and public smoke pass; the only aggregate-gate red is independent F3 function-tier hygiene | `9660f6e79` |
| 2026-07-26 | B / B1 | `PENDING` → `IN PROGRESS` | Segment A dependency closed; generated active-Numba runtime inventory selected as the next oracle stage | dirty WIP after `9660f6e79` |
| 2026-07-26 | B1 | `IN PROGRESS` → `DONE` | AST inventory freezes 48 direct Numba/llvmlite imports, 108 CPU JIT callables, 52 CUDA JIT callables across 13 CUDA-coupled modules, and 46 direct consumers; broader runtime, dependency, test, tool, build, experiment, and documentation surfaces are recorded; three ratchet tests, Ruff, YAML parsing, and the live audit pass; smoke CI rejects new guarded coupling | `de2ccf988` plus the immediate nested-`try` traversal correction |
| 2026-07-26 | B2 | `PENDING` → `IN PROGRESS` | B1 baseline landed; CPU kernel-to-Rust-consumer-evidence classification selected | dirty WIP after `de2ccf988` |
| 2026-07-26 | B2 | `IN PROGRESS` → `DONE` | generated manifest maps all 108 CPU JIT callables across 15 families: 87 direct Rust dispatchers, one alias, and 20 explicitly absorbed helpers; every family names consumers, parity tests, and independent scientific or property evidence; 264 Rust tests and 82 selected scientific-truth tests pass; the live and isolated-environment audits, six ratchet tests, Ruff, CI YAML, and devguide validation pass | `863c77fb7` |
| 2026-07-26 | B3 | `PENDING` → `IN PROGRESS` | complete B2 map landed; deliberate numerical and behavioral divergence extraction selected as the next oracle gate | dirty WIP after `863c77fb7` |
| 2026-07-26 | B3 | `IN PROGRESS` → `DONE` | all 14 parity modules have accepted policies; 77 closeness sites declare both tolerances; 63 formerly implicit `rtol=1e-5` comparisons remain green with explicit strict contracts; eight deliberate divergences and four must-match contracts have executable evidence; 274 Rust/validator tests and 82 selected scientific-truth tests pass; zero provisional decisions remain | `b4b6bae25` |
| 2026-07-26 | B4 | `PENDING` → `IN PROGRESS` | closed B3 contract landed; reproducible final two-backend campaign selected | dirty WIP after `b4b6bae25` |
| 2026-07-26 | B4 strategy refinement | remains `IN PROGRESS` | the release runtime receives the complete forced-Rust suite; Numba is limited to the bounded oracle surface and failed-node attribution because it will not ship in 1.0 | `481271204` |
| 2026-07-26 | B4 checkpoint | `IN PROGRESS` → `BLOCKED` | exact source and wheel hashes recorded; forced-Rust smoke 15/15, Rust oracle 264 passed with three documented skips, and 82 scientific tests pass; complete forced-Rust suite reaches 9,361 passed but has 36 failed and 342 errors in 11 non-Rust root causes; all 378 unsuccessful node IDs reproduce with forced Numba; B4 requires a new green exact-commit run after the active WIP is landed | `481271204`; see `release_1_0_rust_campaign_checkpoint.md` |
| 2026-07-26 | B4 blocker reduction | remains `BLOCKED` | native bioassembly translations remove the 342-error PDB cascade; `MolSys` now delivers `structure_index`; H5MSM preserves optional structural and thermodynamic series, repeated structure order, partial-layer semantics, and multi-state inventory queries; the relevant H5MSM/report gate passes 1,074 tests and the known targeted residual is six root causes | `30d12a7c9`, `64ac440de`, `7cf7d7206` |
| 2026-07-26 | C1 packaging design review | `PENDING` → `DONE` | `python -m pip wheel . --no-deps` on branch `packaging/rust-c1-spike` produced `molsysmt-0.20.0+149.gcb3341fd5.dirty-cp311-abi3-linux_x86_64.whl` carrying `molsysmt/_rust.abi3.so`, `py.typed`, 292 `molsysmt.data` files, the `molsysviewer.addons` entry point and a versioningit Git version; the extension built under CPython 3.13 loaded in a clean 3.12 virtualenv, exposed 97 kernels and returned the correct minimum-image distance; development evidence from a dirty tree, accepted for the design question only; C keeps 0% earned weight | `87317ba76` (branch, not merged) |
| 2026-07-28 | B4 NGLView blocker reduction | remains `BLOCKED` pending exact campaign | optional topology snapshots preserve MolSysMT-origin IDs and chemical bond metadata without granting fictitious topology to generic widgets; multi-structure conversion drops partial PDB metadata; group-level hydrogen bonds preserve pair order; 45 NGLView and 746 broad consumer tests pass under forced Rust | NGLView fidelity checkpoint following `6f527bb44` |
| 2026-07-28 | B4 final exact campaign | `BLOCKED` → `DONE` | clean source archive and exact Rust wheel rebuilt from `6485a0c08`; bounded oracle passes 264 tests with 3 documented skips; combined migration/scientific gate passes 501 tests with 3 skips; complete forced-Rust suite passes 9,769 tests with 5 accepted skips and zero unsuccessful outcomes | `6485a0c08`; `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | B5 oracle artifact | `PENDING` → `DONE` | dated artifact preserves the exact commit, environment, commands, source archive hash, wheel hash, installed-extension hash, bounded two-backend result, independent evidence, and complete application result | `release_1_0_final_numba_oracle_artifact.md` |
| 2026-07-28 | C2 production Rust integration | `PENDING` → `DONE` | crate relocated to `rust/`; private `molsysmt._rust` integrated through setuptools-rust; separate-package traps removed; 80 Rust and 270 Python tests pass with 3 documented skips; exact-commit Linux wheel is `cp311-abi3`, passes automated content validation, installs non-editably, exposes 97 entries, and computes the minimum image correctly | `17be9ea50`; `release_1_0_rust_packaging_c2_artifact.md` |
| 2026-07-28 | C3 multiplatform wheel CI implementation | remains `IN PROGRESS` | five native targets, pinned Rust/cibuildwheel configuration, strict abi3/content inspection, isolated installed-extension smoke, and artifact retention implemented; 12 contract tests, 80 Rust tests, Ruff, dependency validation, and local C2-wheel smoke pass; remote five-target run pending; pre-existing rustfmt debt assigned to C7 | `30b86cdf2`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C3 exact-commit remote matrix | `IN PROGRESS` → `DONE` | GitHub Actions run `30346103646` passes Linux x86_64/aarch64, macOS x86_64/arm64, and Windows x86_64; every `cp311-abi3` wheel passes build/audit, non-editable installed-extension validation, 97-export and minimum-image smoke, and artifact upload; exact wheel hashes and runner images are preserved | `f79ccb4f0`; `release_1_0_rust_packaging_c3_checkpoint.md` |
| 2026-07-28 | C4 installed-wheel matrix | `PENDING` → `IN PROGRESS` | C3 portability dependency closed; Python 3.11–3.13 and supported NumPy installed-wheel execution selected as the active packaging gate | after `f79ccb4f0` |
| 2026-07-28 | D1–D5 / Segment D | `PENDING` → `DONE` | production routing is Rust-only; CPU JIT, CUDA, incomplete Taichi experiments, runtime controls, dependencies, JIT warm-up API, diagnostics, and migration parity tests are removed; low-level compatibility paths remain Rust-backed; the executable zero gate passes; 122 focused and 450 broad affected tests pass, with one separate network-dependent test excluded | dirty implementation; `release_1_0_rust_only_cut_artifact.md` |
| 2026-07-28 | D6 Rayon controls | `PENDING` → `DONE` | session defaults and function-local overrides resolve to reusable Rayon pools; nested overrides remain local; 1/2/4-thread execution is directly observable; 165 affected tests pass; representative release-build speedups at four threads are 2.99× distances, 3.54× centers, 3.51× radius of gyration, and 2.73× RMSF | dirty implementation; resolved bug record and `performance_and_jit.md` |
| 2026-07-28 | WIP integration | dirty tree → clean `main` | release gates, function-tier policy, conversion-fidelity records, and native dictionary extraction landed in three focused commits; fast gate 12/12 and 107 conversion-truth tests pass | `83a573f09`, `8579b8e7a`, `0a9353ffc` |
| 2026-07-28 | Conda scheduling | critical-path prerequisite → parallel delivery track | coordinated sibling and MolSysMT Conda publication may proceed during manuscript writing/review; local installed-wheel evidence remains in C/E, while channel availability blocks only the Conda delivery claim | maintainer decision recorded in the execution plan and Conda coordination report |
| 2026-07-28 | E1–E2 | `PENDING` → `DONE` | 80 Rust unit/property tests, Clippy with warnings denied, 103 Python Rust/control/boundary tests, 98 scientific-truth tests, 43/0/0 evidence registry, and 18-file hot-path lint pass; representative GIL release, concurrent Rayon pools, bounded oversubscription, and panic containment are executable regressions | stage-closing Rust validation commit |
| 2026-07-28 | E3 | `IN PROGRESS` → `DONE` | complete Rust-only suite passes 9,585 tests with two accepted skips under `-n 12`; fast release gate passes 12/12; Ruff passes across package, tests, devtools, and root conftest | `692479097` |
| 2026-07-28 | E5 | `PENDING` → `DONE` | maturity-weighted consumer audit: MolSysViewer passes 5/5 as the blocking foundational consumer; TopoMT passes 7/7; PharmacophoreMT imports but its ER-alpha workflow exposes a consumer-local obsolete `element=True` call, recorded as non-blocking adaptation debt | status-ledger commit following `9fbb95569` |
| 2026-07-28 | E6 | `IN PROGRESS` → `DONE` | exact clean-commit Rust-only benchmark records first/repeated calls, memory, raw 1/2/4-thread samples, bounded nested concurrency, native-extension hash, scientific checks, and zero JIT-cache creation | `746e22c5f`; `release_1_0_rust_runtime_benchmark.{md,json}` |
| 2026-07-28 | Minimal installed-runtime defect | discovered → `DONE` | optional forms remain visible but detectors whose mapped soft dependency is absent no longer execute; the missing OpenMM mapping is restored; 449 basic tests and local non-editable smoke without OpenMM pass | `c4d8e9074`; `archive/resolved_bugs/optional_form_detection_broke_minimal_install.md` |
| 2026-07-28 | C4–C7 / E4 / Segments C and E | `IN PROGRESS` → `DONE` | exact run passes five native abi3 wheels, 15 platform/Python checks, three NumPy floors, three installed public smokes, sdist round trip, exact 99-export validation, and Rust formatting, Clippy, tests, advisory, dependency, and license gates | `c4d8e9074`; run `30394881487`; `release_1_0_rust_packaging_c4_c7_artifact.md` |
| 2026-07-28 | F1 status correction | `PENDING` → `DONE` | commit history and the live validator confirm that F1 had already landed: 156 notebooks, core 1–20, four paths 21–54, complete toctrees, unique semantic labels, and a matching manifest; the two remaining editorial references and Sphinx confirmation belong to later lifecycle stages | `f5d96218b`; `python devtools/scripts/validate_course.py` |
| 2026-07-28 | F / F2 | `PENDING` → `IN PROGRESS` | F1 historical evidence recovered; existing notebook-execution evidence must be audited before scheduling new execution or edits | after `03a170442` |
| 2026-07-28 | F2 execution audit checkpoint | remains `IN PROGRESS` | required union reconstructed as 37 notebooks; in-memory clean-kernel run passes 14/26 deterministic notebooks, exposes 12 failures requiring ownership classification, and defers 11 network/interactive notebooks; no notebook outputs or content were modified | `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-28 | F2 correction pass | remains `IN PROGRESS`, ready to land | all 26 deterministic and all 11 network/headless notebooks pass from clean kernels; seven bounded library-contract corrections have regression coverage; affected User Guide notebooks execute; formal closure awaits validation, landing, and exact-commit 37/37 rerun | dirty worktree based on `2340d1eff`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F2 exact-commit closure | `IN PROGRESS` → `DONE`; F3 becomes active | final scope expands from 37 to 40 because Scalability corrections affect all four Paths; the complete Common Core plus notebooks 28, 29, 47, 48, and 49 of every Path pass from fresh kernels with no persisted outputs | `2f6fd59d1`; `release_1_0_f2_notebook_execution_checkpoint.md` |
| 2026-07-29 | F3 support-tier and lifecycle reconciliation | `IN PROGRESS` → `DONE`; F4 becomes active | function tiers derive from the exhaustive API stability registry and validate as 117 Tier 1, 56 Tier 3, and seven outside-contract; nine completed/superseded proposals and one historical audit leave the pending queue; normative links and resolution records are updated | `release_1_0_f3_support_and_lifecycle_checkpoint.md`; documentation-only work based on `fd19f9196` |
| 2026-07-29 | F4 documentation lifecycle | `IN PROGRESS` → `DONE`; F5 becomes active | final course narrative references use stable semantic targets; the numbering report and Rust migration residue are archived; the missing dihedral broadcast regression passes on vacuum and periodic paths; checked-in autosummary surfaces are refreshed; 11 stale toctree targets are repaired; Sphinx builds successfully and the remaining warning families are measured as accepted documentation debt | `672f8f065`; `release_1_0_f4_documentation_lifecycle_checkpoint.md` |
| 2026-07-29 | Segment F progress accounting | no stage transition; weighted closure 90% → 96% | the fixed 10% Segment F budget is partitioned across six independently gated stages; completed F1–F4 earn 6%, while F5 and F6 retain the remaining 4%; no technical exit criterion or release requirement changes | maintainer-approved accounting update after `075cb0432` |
| 2026-07-29 | Atom-axis `add()` WIP integration | dirty pre-F5 worktree → clean candidate base; no stage transition | native and public addition share one atom-axis contract; MolSys mutation is transactional; adapters, multiple-source dispatch, scalar returns, lifecycle documentation, and regressions are synchronized; 30 focused and 554 expanded tests pass, two notebooks execute, Ruff passes, and the fast gate passes 12/12 | `2865c3122`; `release_1_0_atom_axis_add_checkpoint.md` |
| 2026-07-29 | Atom-axis `add()` semantic follow-up | F5 remains active; bounded audit inserted before its expensive exact-commit matrix | multi-source selection/cardinality, whole-call transaction scope, one-sided atom-aligned data, structure metadata and energy validity, coordinate-free structures, adapter parity, diagnostics, and memory are recorded with phases and acceptance criteria; no behavior or weighted progress changed | `87ccfc289`; `pending_proposals/atom_axis_add_semantic_audit.md` |
| 2026-07-28 | Developer-guide coherence pass | no stage transition | post-migration documentation debt cleared: four Numba-era bug reports and four Numba-era proposals archived with resolution notes after verifying each against the Rust runtime; one stale duplicate report removed; the three Numba migration documents relabelled as historical evidence; snapshot sentences that still called Segment C open corrected; `pending_bugs` and `pending_proposals` indexes rewritten; 11 broken intra-guide links repaired; devguide validation and the fast gate pass 12/12; code, tests, and notebooks untouched, with the residue recorded in `archive/resolved_proposals/rust_migration_documentation_and_test_residue.md` | `2340d1eff` |
| 2026-07-29 | Presentation surface | no stage transition | the README and documentation landing pages described MolSysMT as middleware between other libraries and advertised the removed Numba/CUDA architecture; `docs/content/about/what.md` disowned the library's own native capability. Reframed with the molecular system as subject. Verified against the installed package: seven `to=` calls should be `to_form=`, the sequence and dihedral examples raise, and the cross-library showcase raises `NotImplementedConversionError` because no route to `MDAnalysis.Universe` exists. The tier table showed about eleven Tier 1 forms where the live registry reports 75 of 89, and claimed any Tier 1 pair converts. The Conda recipe had an empty summary. Every example now executes; ruff, devguide, course, and fast gate 12/12 pass | `d2b805e74`; `pending_proposals/readme_positioning_and_1_0_refresh.md` |
| 2026-07-29 | Documentation and paper track | critical-path work → named parallel track | with A–E and F1–F4 closed, presentation, documentation and the methods paper become a principal parallel workstream; the three items the positioning pass could not close are specified with acceptance criteria | `pending_proposals/presentation_and_citation_surface.md` |
| 2026-08-03 | Topology vocabulary, DCD backend noise and the course gate | three reports → `DONE`; no stage transition | `get_covalent_chains` is renamed `get_covalent_paths`: `chain` is an element of a molecular system while the function walks the covalent graph returning paths, and `get_covalent_blocks` was already named to avoid the same collision with `component`. No deprecation cycle, the policy starts at 1.0.0. `get_dihedral_quartets(with_blocks=True)` raised on every real system by pushing ragged block sets through `np.array`; on T4 lysozyme 158 of 161 phi quartets split in two and 3 do not, and those 3 are the prolines. Module 13 of the Common Core taught `get_covalent_blocks` as the way to obtain components, contradicting its own tutorial, and the quickstart placed four topology functions in `molsysmt.structure`. MDTraj's DCD reader printed to the C standard output on every open and every read with no way to disable it; suppressed behind `configure.silence_backend_stdout`, 26 lines to 0, and recorded as evidence in the native-parser proposals rather than as a reason to write one. `validate_course.py` was red with 20 errors because it asserted a Common Core module count and a label scheme the section has not settled; both deferred explicitly, gate green at 155 notebooks | `dfa57c073`; `647694061`; `1541f8775`; `acd4404c7`; `archive/resolved_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md`; `pending_bugs/course_gate_red_after_common_core_renumbering.md` |
| 2026-08-03 | Structure axis of a composite molecular system | two reports → `DONE`; no stage transition | a molecular system spread over complementary items had no structure axis of its own, so `where_is_attribute` broke its tie between providers that are not interchangeable. `msm.get([h5msm, dcd], n_structures=True)` returned 20 while `msm.get([dcd, h5msm], n_structures=True)` returned 1, `msm.convert` on the second order discarded nineteen structures with no diagnostic, and `get` returned `time` of length 1 beside `coordinates` of length 20 for one system. The axis is now the largest structure count among the items carrying structural data, order-independent; only items spanning it may deliver a structural attribute, with the existing last-matching-item tie-break applying among those; an item holding zero or one structure below the axis is a reference conformation whose series are dropped with the new `StructuralAttributeOffAxisWarning` (`MSM-WARN-STRUCT-006`); and two items each holding more than one structure, of different lengths, raise `StructuralInconsistencyError` naming `molsysmt.concatenate_structures`. This completes on the structure axis the consistency contract already enforced on the atom axis by `_private/molecular_system_validation.py:144-151`, and the asymmetry between raising on atoms and warning on structures is deliberate: `[pdb, xtc]` is one structure beside a trajectory and must keep working. `convert` needed its own intervention because it never resolved attributes through `where_is_attribute`. The `Iterator` defects closed with it, including an unguarded `append` that yielded zero items without error depending on keyword order, and an H5MSM reader indexing an empty `structures/id` dataset. 7913 tests pass; the only failure is a pre-existing third-party `openff.toolkit` import error reproducible without MolSysMT | `2de6b4d6d`; `archive/resolved_bugs/structural_attribute_resolution_ignores_the_structure_axis.md`; `archive/resolved_bugs/iterator_without_explicit_attributes_fails_for_partial_forms.md` |
| 2026-08-03 | `msm.info()` table styling in the built documentation | reported → `DONE`; no stage transition | compiled pages rendered `msm.info()` flat while the notebooks stayed striped. `info()` returns a `Styler`, which emits no HTML class, so it was styled only by MyST-NB's class-agnostic pandas rule — dropped in v1.4.0, the dark-mode rework — while pydata-sphinx-theme reaches notebook tables solely through `table.dataframe`. `info()` now tags the table `dataframe`, the class `DataFrame.to_html()` emits, which restores striping in both themes and removes a dark-mode fallback that painted the output as an inverted light box. Verified on a rebuilt page: all 8 tables of `info.ipynb` emit the class under `.bd-content` → `div.cell_output`, with the striping now coming from the theme alone. A CSS override and pinning `myst-nb<1.4` were both rejected as patches; a stable `Styler` uuid was rejected because no library-side value is both stable and unique — 5 of 62 notebooks hold two identical tables by design. `docs/execute_notebooks.py` keys staleness off notebooks, never the library, so the remaining 61 need an explicit force | `d92d4fe76`; `archive/resolved_bugs/docs_styler_zebra_striping_lost_with_myst_nb_1_4.md` |
| 2026-07-31 | `MolSys → ViewerJSON` deep-copy defect | reported → `DONE`; no stage transition | the conversion read two fresh, local, discarded intermediates through the deep-copying default of `ViewerJSON.to_dict()`, spending about 93% of its time in 1,350,867 `deepcopy` calls; reading them with `copy=False` takes the reported 62-atom × 5,000-structure case from 1.67 s to 0.32 s. Neither intermediate aliases the source, so the copy protected nothing: a non-aliasing regression test mutates the returned payload and asserts the source `MolSys` and a second conversion are untouched, and it stays green with `copy=True` restored while the timing regresses to 1.58 s. The `ViewerJSON` identity conversion was audited and deliberately left deep-copying: it is unreachable from this chain. 508 viewer, form, view and cross-repo tests and Ruff pass | `b63a2f6c5`; `archive/resolved_bugs/viewer_json_conversion_deep_copies_twice.md` |
| 2026-08-07 | Fast release gate | `FAIL` (11/12) → `PASS` (12/12); no stage transition | the developer-guide gate had been red since the documentation queues were reorganized: `devguide/README.md` still linked the deleted `docs/README.md`, and `forms_and_conversions.md` and `pending_proposals/docs/README.md` both linked a proposal that `ae29169e8` had archived. The archiving was correct — the *Multiple items into one* section of `convert.ipynb` now composes a PSF topology with a DCD trajectory and states that the multi-structure item dictates the structure axis — but its two referrers were never updated, and the empty `devguide/docs/` tree was left behind. This ledger's previous claim that the gate passed 12/12 was measured before that reorganization | see the commit closing this row |
| 2026-08-07 | `file:prmtop → molsysmt.MolSys` | reported → `DONE`; no stage transition | the converter imported a `to_molsysmt_Structures` sibling that never existed in the form package. The name was unused — the body builds an empty `Structures()` because a prmtop carries topology only — but the import runs at call time, so the library's central form was unreachable from an entire input format, and MolSysViewer failed the same way. Conversions register in `_convert_to` as function objects and their inner imports are function-local, so the catalogue proves only that `to_*.py` imports; nothing calls every registered edge. The sweep that found it is now `tests/form/test_converter_imports_resolve.py`, carrying the two remaining cases as a baseline that cannot grow, and the conversion is guarded by `tests/form/file_prmtop/test_to_molsysmt_MolSys.py`. 115 supported, conversion-truth and form tests pass; fast gate 12/12; Ruff clean | see the commit closing this row |
| 2026-08-07 | Presentation and citation surface | two of three items `PENDING` → `DONE`; no stage transition | maintainer decisions taken and applied. Daniel Ibarrola-Sánchez is not an author: removing him from `CITATION.cff` also removes the ORCID that file attributed to him but which belongs to Diego Prada-Gracia, and the record now agrees with `.zenodo.json` on the same two authors and with the README, which acknowledges his contributions to MolSysMT's early development. The unreferenced duplicate landing page `docs/content/user/index_v2.ipynb` is deleted with its two `nbconvert` artifacts, verified to have no inbound reference from any page; three further orphans of the same `_v2` experiment are recorded in the proposal. The DOI, version, title and date are decided but deferred: `CITATION.cff` is a placeholder until 1.0 closes, and the update is now a line in the release-gate sign-off so it cannot drift again as it did for two years. Item 3, the timing of the Conda installation instructions, stays open | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phases 1-3 `PENDING` → `DONE`; Phase 4 open; no stage transition | Phase 1 audited the contract read-only and measured every claim with a probe. It found the scope far narrower than assumed — only `molsysmt.MolSys` and `molsysmt.Structures` implement `add()`, and the dispatcher selects on the target form — and it found most of audit question 1 unreachable, because digestion rejects a list of independent molecular systems before the target × source loop can run. Two of the audit's own premises were wrong: adding a topology-only source does not drop the coordinates, it fails first with an `ArgumentLengthError` naming an argument the caller never passed; and the one list that survives digestion is a composite system, which `add` iterated as independent sources, contradicting the composite contract. Phase 2 landed the regression matrix with the decisions as `xfail(strict=True)`, which is also how a cross-cutting defect surfaced: a test asserting `add()` honours `attribute_policy` passed against a function with no such parameter, filed as `pending_bugs/public_functions_silently_ignore_unknown_keywords.md`. Phase 3 implemented D1-D7 and the four defects: the target's box prevails with `IncompatibleBoxWarning` (MSM-WARN-STRUCT-007), `temperature` and the energies are dropped while `structure_id`, `time` and `time_step` survive, `attribute_policy` gains `intersection`/`strict`, bioassemblies merge on the chain axis with `BioassemblyIdentifierCollisionWarning` (MSM-WARN-STRUCT-008), `alternate_location` merges with remapped atom indices, `atoms_ff` follows the policy, and `add()` is one-to-one with the loop deleted. 40 add tests pass with no pending markers; 886 basic, native and element tests pass; the contract is now in `native_structures_contract.md` | see the commit closing this row |
| 2026-08-07 | Atom-axis `add()` semantic audit | Phase 4 `PENDING` → `DONE`; proposal archived; no stage transition | the lifecycle closed and all ten acceptance criteria hold, so the proposal and its Phase 1 findings moved to `archive/resolved_proposals/`. `molsysmt.basic.add` documents `attribute_policy` and the four Notes that changed; the User Guide page gained two sections and a warning admonition, written against a real case rather than an illustrative one — T4 lysozyme from a PDB carries B factors and a unit cell, a built peptide carries neither, so one addition exercises the drop and both new diagnostics — and the notebook was re-executed so its printed outputs are measured. Common Core modules 17 and 18 needed no correction: they already use one target and one source. Writing the documentation surfaced a diagnostic defect of its own, a doubled period in the `strict` rejection message, fixed at both call sites. Two coverage gaps found while walking the criteria were closed rather than waived: `velocities` joined the one-sided parametrisation, and a string selection over an assembled composite source is now pinned. 43 add tests pass; Ruff, dependencies, devguide and course gates green; fast release gate 12/12 | see the commit closing this row |
| 2026-08-07 | Public argument contract | reported → `DONE`; no stage transition | a typo in a keyword argument was silent in 22 of the 26 public callables and uncatalogued in the other four: `structure_indeces` for `structure_indices` returned all 5,000 structures of a trajectory instead of the three requested, with a well-formed result and no diagnostic. The cause was a binding step making a policy decision — ArgDigest discarded any keyword outside the signature before the layer designed to judge it could see it — which left it more permissive than Python itself, and left MolSysMT's own `STRICTNESS='warn'` policy unreachable for those 22. Fixed upstream in ArgDigest 0.10.0 by adding the missing axis, the function argument contract, and declared here with three configuration lines, one domain pointing at the attribute catalogue, and two contract modules; the 19 closed signatures are protected with no declaration at all. Two claims in the original triage were wrong and are corrected in the archived report: `contains` and `is_composed_of` implement deliberate no-criterion branches, so no `requires_any_of` rule was declared. Reading those bodies found a real defect instead — `get_label` declares `**kwargs` and never reads it. `molsysmt.basic.convert` keeps the permissive default because its domain resolves from `to_form` at call time; the gap is recorded and pinned by a test. ~8300 tests pass with the policy at `error`, plus 1296 MolSysViewer tests with nothing declared on its side; Ruff clean; fast release gate 12/12 | see the commit closing this row; `archive/resolved_bugs/public_functions_silently_ignore_unknown_keywords.md` |
| 2026-08-07 | Cross-repo test drift | reported → `DONE`; no stage transition | two tests in `tests/molsysviewer_molsysmt/` read `MolSysView._message_history`, a private attribute MolSysViewer replaced with a narrower `_shape_history` and a `scene_history` model, so the suite carried two known failures — and a suite with known failures stops detecting new ones, which blocks the F5 exact-commit gate. Both tests already intercepted `apply_system_edit` and recorded the edited molecular system, then ignored it to inspect the message the viewer built from it. That was the defect the refactor exposed: what the facade owes the viewer is an edited system handed to `apply_system_edit`, and how the viewer serializes it afterwards is not this side's business. They now assert on the recorded system. Renaming the attribute to `_shape_history` was deliberately not done: it is not the same thing, so the tests would have passed asserting something else. 115 cross-repo tests pass and the MolSysMT suite is clean | see the commit closing this row; `archive/resolved_bugs/cross_repo_test_reads_a_removed_molsysviewer_attribute.md` |
| 2026-08-12 | Pre-F5 adapter and course consolidation | no stage transition; candidate base ready | comparison now treats incompatible shapes as unequal; OpenFF unit adapters coexist safely; PyTraj trajectory conversion preserves its supported contract; OpenMM simulations are built only from complete inputs and initialize from the selected structure; every registered converter module resolves; conversion fidelity advances to 40 exhaustive / 441 accepted / 29 resolved with zero new debt; the Common Core is fixed at 20 modules and all labels match permanent manifest identities with no validator exception. The fast gate passes 12/12, Ruff is clean, form adapters pass 89/89 with 78 accepted lower-tier declarations, and the course contract passes 156/156 notebooks | `3fb639010` through `c87a14036` |
| 2026-08-12 | F5 exact-commit release gates | `IN PROGRESS` → `DONE`; weighted closure 96% → 99%; F6 becomes active | exact commit `8faf62785` passes the fast gate 12/12; full matrix run `31589594289` passes Ubuntu and macOS on Python 3.11--3.13; wheel run `31589594286` passes supported Linux/macOS builds, abi3 Python/NumPy compatibility, installed public smoke, sdist, Rust quality and security, with Windows green as experimental evidence; documentation run `31589594273` and smoke run `31589594438` pass. Packaging defect #145 and clean-source CI defect #146 satisfy their acceptance criteria and are archived | `8faf62785`; `archive/resolved_bugs/built_wheels_omit_the_dynamic_form_catalogue.md`; `archive/resolved_bugs/ci_shadows_the_installed_rust_extension_with_the_source_checkout.md` |
| 2026-08-13 | Bounded pre-1.0 corrections | F5 `DONE` → `IN PROGRESS`; weighted closure 99% → 96% | the declared selection syntaxes become an executable directional contract, large molecular strings no longer enter unbounded filename tokenization, and the stale `_private` API branch is removed from the published reference. Focused and expanded guards pass; a new exact-commit release campaign is required before F5 can close again | uibcdf/molsysmt#148, #149, #150; implementation worktree before landing |
| 2026-08-13 | Generated form-function identity | reported → `DONE`; no stage or weighted-progress transition | nine `exec()`-based getter modules created 2,162 distinct decorated functions without `__module__`, so ArgDigest received `None.<name>`, caller-specific contracts could not identify them, and diagnostics named no resolvable origin. Each generator now seeds `__name__` before decoration; exact module identity, structured diagnostics, and future generators are guarded. The passport decision remains independent and untouched | uibcdf/molsysmt#152; see the commit closing this row |
