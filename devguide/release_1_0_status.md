# MolSysMT 1.0 Execution Status

**Role:** operational status ledger
**Last updated:** 2026-07-26
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

- **Active segment:** B — final Numba oracle
- **Active stage:** B4 — forced-Rust blocker reduction and exact-commit campaign
- **Completed weighted closure:** 25% of the remaining 1.0 execution plan
- **Development-progress estimate:** Segment A is certified complete; Segment
  B is approximately 93% complete internally after the first B4 campaign,
  blocker reduction, and the structural-growth stabilization pass, but has not
  yet earned additional weighted closure
- **Current repository state:** dirty WIP; not a release artifact
- **Current landed blocker-reduction HEAD:** the transactional structural-growth
  checkpoint at the current committed `HEAD`; this is not yet a verified
  release-candidate commit because unrelated WIP remains unlanded
- **Release readiness percentage:** intentionally not asserted until Segment A
  and the Rust packaging spike provide executable evidence
- **Normal pytest:** the authority for test results
- **pytest-receptor:** the systematic compact reporter; disagreements must be
  reported upstream immediately
- **Next action:** land the validated transactional structural-growth
  checkpoint, then continue the remaining NGL adapter causes before rebuilding
  the exact-commit Rust wheel and repeating the forced-Rust release gate
- **Next packaging stage:** C2 — production crate relocation and the
  `msm_rust_kernels` → `molsysmt._rust` rename, held until B4 closes its
  exact-commit run so the campaign's build path stays reproducible. C1 is
  `DONE`; the accepted design is recorded in
  [rust_packaging_backend_design.md](pending_proposals/rust_packaging_backend_design.md)
- **Known independent release-gate debt:** the fast release gate passes 11/12
  checks. Its only red is F3 lifecycle work: the two Tier-3 molecular-dynamics
  decorators do not correspond to symbols in the tracked public-API registry.
  Form-adapter delivery is green with 89/89 forms, 101 accepted lower-tier
  declarations, 320 resolved baseline declarations, and no Tier-1 debt

The 25% figure measures only the newly defined remaining-plan exit gates. It
does not attempt to restate the much larger body of MolSysMT development,
consolidation, or Rust kernel work completed before this ledger was created.

## Segment Ledger

| Segment | Weight | Status | Earned | Current evidence or reason |
| --- | ---: | --- | ---: | --- |
| A — conversion-fidelity coherence | 25% | `DONE` | 25% | 37 exhaustive Tier-1 edges, 444 accepted non-exhaustive edges, zero new debt, 85 integration tests, and all conversion/form gates pass on `9660f6e79` |
| B — final Numba oracle | 10% | `BLOCKED` | 0% | the exact-commit Rust campaign proved no backend-specific regression; the dominant 342-error PDB cascade, missing `MolSys.structure_index`, and the H5MSM structural-fidelity/multi-state causes are now landed, leaving six known targeted root causes before a new exact-commit campaign |
| C — Rust packaging | 20% | `PENDING` | 0% | C1 accepted 2026-07-26: setuptools + setuptools-rust with a single private `molsysmt._rust` abi3 extension, proven by spike `87317ba76` (development evidence, dirty tree); C2 is gated on B4 closing its exact-commit run, and C3-C7 including multiplatform installed-wheel CI remain open, so no weight is earned |
| D — Rust-only cut | 20% | `PENDING` | 0% | depends on B and C; 48 direct imports, 108 CPU JIT callables, 52 CUDA JIT callables, and 13 CUDA-coupled modules remain at the audit checkpoint |
| E — scientific and ecosystem validation | 15% | `PENDING` | 0% | requires the Rust-only installed runtime |
| F — lifecycle and release candidate | 10% | `PENDING` | 0% | course, documentation, exact-commit matrix, and clean release candidate remain open |
| **Total** | **100%** | **`IN PROGRESS`** | **25%** | Segment credit is earned only when its complete exit gate passes |

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

## Segment A — Conversion-Fidelity Coherence

**Canonical bug:**
[Conversion Fidelity WIP Exposes Multiple Contract Gaps](pending_bugs/conversion_fidelity_wip_contract_gaps.md)

| Stage | Status | Dependency | Closure evidence required |
| --- | --- | --- | --- |
| A1 — audit-scope contract | `DONE` | none | landed as `504df91d0`; scope API, compatibility, tests, and lifecycle docs complete |
| A2 — exhaustive native-dictionary audit | `DONE` | A1 | three evidence-backed native-to-dictionary profiles landed; 51 focused tests and the Tier-1 ratchet pass |
| A3 — independent schema/adapter repairs | `DONE` | A1–A2 stable | direct native projections and all four builder routes have evidence-backed exhaustive reports; the broad native-scope module is green |
| A4 — PDB fidelity | `DONE` | A1–A2 stable | one handler-owned normalized parser feeds file, text, and handler routes; 22 fidelity tests and the historical PDB corpus pass; 11 exhaustive profiles landed as `1f656fe9f` |
| A5 — segment integration gate | `DONE` | A1–A4 | 85 integration tests pass from an isolated `HEAD` plus staged snapshot; 37/481 edges are exhaustive, 444 are accepted debt, zero are new; adapter delivery and lifecycle gates pass |

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
| B4 — final forced-Rust campaign plus bounded Numba oracle | `BLOCKED` |
| B5 — dated, committed oracle artifact | `PENDING` |

Existing Rust port and dogfooding results are prerequisites, not B-segment
completion. No new Numba capability may be added while this segment is pending.

## Segment C — Rust Packaging

| Stage | Status |
| --- | --- |
| C1 — permanent crate/module and build-backend design review | `DONE` |
| C2 — production crate relocation and private extension integration | `PENDING` |
| C3 — Linux, macOS, and Windows abi3 wheel CI | `PENDING` |
| C4 — Python 3.11–3.13 and supported NumPy installed-wheel tests | `PENDING` |
| C5 — conda and sdist contract | `PENDING` |
| C6 — metadata, resources, entry points, typing, and lazy-discovery parity | `PENDING` |
| C7 — Rust quality, security, license, and portability gates | `PENDING` |

The local pilot wheel is useful evidence but does not complete any production
packaging stage.

C1 is closed by [C1 — Permanent crate/module and build-backend design
review](pending_proposals/rust_packaging_backend_design.md): keep `setuptools`, add
`setuptools-rust`, ship one private `molsysmt._rust` abi3 extension inside the official
Conda package, and do not adopt maturin or a separate `msm_rust_kernels` distribution. Two
findings became binding C3 contracts (clean-build isolation with automated wheel
inspection, and abi3 proven per target rather than assumed from the tag). The earlier
report of a PyPI resolution failure as a C4 blocker is **corrected**: the official channel
is Conda, so C4/C5 require the sibling versions on the Conda channel rather than on PyPI.

**C2 must not start before B4 closes.** Relocating the crate and renaming
`msm_rust_kernels` to `molsysmt._rust` changes the wheel build path and the hashes recorded
in the Rust campaign checkpoint, which would invalidate the exact-commit reproducibility
B4 still needs.

## Segment D — Rust-Only Cut

| Stage | Status |
| --- | --- |
| D1 — direct Rust CPU routing and dispatch removal | `PENDING` |
| D2 — CPU Numba/JIT implementation deletion | `PENDING` |
| D3 — GPU capability audit and Numba-CUDA deletion | `PENDING` |
| D4 — dependencies, warmup, diagnostics, API, docs, and course cleanup | `PENDING` |
| D5 — executable zero-Numba/Numba-CUDA/llvmlite gate | `PENDING` |

## Segment E — Rust-Only Validation

| Stage | Status |
| --- | --- |
| E1 — Rust unit, property, error, panic, GIL, and threading tests | `PENDING` |
| E2 — independent scientific-truth matrix | `PENDING` |
| E3 — complete MolSysMT suite and release fast gates | `PENDING` |
| E4 — installed-wheel platform/Python matrix | `PENDING` |
| E5 — MolSysViewer, TopoMT, PharmacophoreMT, and direct-consumer smoke | `PENDING` |
| E6 — cold/warm, memory, thread, and oversubscription benchmarks | `PENDING` |

## Segment F — Lifecycle and Release Candidate

| Stage | Status |
| --- | --- |
| F1 — Four Paths numbering and structural validation | `PENDING` |
| F2 — applicable Common Core and changed-behavior notebook execution | `PENDING` |
| F3 — function support-tier and pending-guide hygiene | `PENDING` |
| F4 — User Guide, Cookbook, API, demos, and course lifecycle closure | `PENDING` |
| F5 — clean exact-commit fast, full, wheel, and documentation gates | `PENDING` |
| F6 — 1.0 release candidate and tag | `PENDING` |

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
3. add earned weight only when the full segment exit gate passes;
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
