# Release 1.0 — Independent Gate Audit

**Status:** independent audit (read-only), 2026-07-22
**Method:** documentary claims cross-checked against code, tests, and the repository's
own validators. pytest is the authority. The full suite was **not** run (per audit
constraints); the eight in-repo validators, focused Tier-1 selections, and a public-API
smoke test were used as evidence. No code or pre-existing document was modified.

This record is an assessment, not a decision. It does not change any contract. Where it
disagrees with an older document, the code and the validators cited below are the
authority.

---

## 1. Honest readiness estimate

**~85% ready for 1.0**, with the remaining ~15% concentrated **outside** the core
scientific and API contracts.

- **Contract / API / scientific surface: strong (~90%+).** All eight repository
  validators pass; the public stable surface imports and runs end to end; focused
  Tier-1 suites are green. The **419 non-exhaustive Tier-1 conversions** are tracked,
  zero-new-debt accepted debt, not 419 failures. The earlier 346 count incorrectly
  treated 73 registered identity routes as exhaustive without route-specific evidence.
- **Documentation lifecycle: weak (~60%).** 174 course notebooks with **no automated
  execution evidence**, a **confirmed** course-numbering contradiction, and no
  executable symbol→document mapping.
- **Release process: unverified.** ~153 uncommitted working-tree entries (95 under
  `molsysmt/`); a 1.0 tag cannot be cut from a dirty tree and the **full** matrix has
  not been demonstrated green on a committed state.

The number is deliberately not higher: the code is in good shape, but "1.0" for a
library that advertises a course and a "documentation is part of the contract" policy
is gated by lifecycle verification and by landing the current WIP, not by new features.

## 2. Evidence base (all green)

| Validator / command | Result |
|---|---|
| `python devtools/scripts/validate_api_stability.py` | valid, **190 symbols** (125 stable / 57 experimental / 8 outside-contract / 1 deprecated) |
| `python devtools/scripts/validate_form_adapters.py` | **89 forms, 0 failed**; "delivery debt did not regress" |
| `python devtools/scripts/audit_conversion_fidelity.py` | 481 Tier-1 edges, 62 exhaustive, **419 accepted non-exhaustive debt, 0 new / 0 resolved** |
| `python devtools/scripts/validate_scientific_evidence.py` | **43 validated, 0 partial, 0 gaps** |
| `python devtools/scripts/validate_devguide.py` | passed |
| `python devtools/scripts/validate_dependencies.py` | no top-level soft-dependency imports |
| `python devtools/scripts/validate_demo_assets.py` | 17 H5MSM 0.4 demos + 1 0.3 fixture |
| `python devtools/scripts/validate_resources.py` | talks/papers/tutorials OK |
| `pytest tests/conversion_truth -q` | green |
| Public-API smoke (`get_form`/`get`/`convert`/`select`/`structure.get_center` on `181l.pdb`) | green |
| `molsysmt/_private/form_tier.py` | 89 forms: **75 Tier 1, 3 Tier 2, 11 Tier 3** |
| Packaging: `pyproject.toml` `requires-python=">=3.11,<3.14"`, classifiers 3.11/3.12/3.13; `ci-weekly.yaml` matrix 3.11/3.12/3.13; conda build 3.11/3.12/3.13 | consistent |

## 3. Prioritized short list of REAL blockers (category 1)

Only two findings are genuine, code-or-process 1.0 blockers. Everything else is
category 2–5.

### B1 — The release cannot be cut from the current uncommitted tree, and the full suite has not been demonstrated green on a committed state
- **Class:** 1 (confirmed release-process blocker).
- **Evidence:** `git status --short` = 153 entries (140 modified, 12 untracked, 1
  deleted); 95 under `molsysmt/` (large in-flight form/chemical-state hardening).
  Commits carry `[skip ci]`, so even `ci-smoke.yaml` (the only push-triggered gate)
  does not run on them; `ci-full.yaml` is `workflow_dispatch`-only and `ci-weekly.yaml`
  is scheduled. No evidence in this audit of a green full matrix on a committed tree.
- **Impact (users/science):** a 1.0 tag must be reproducible and CI-verified; releasing
  from a dirty tree risks shipping a state no CI ever validated.
- **Cost:** medium — land the WIP in reviewed commits, then one green `ci-weekly`/
  `ci-full` run on the tag candidate.
- **Closure:** commit the WIP in coherent units; trigger `ci-full.yaml` (or an
  unskipped weekly) on the candidate; require it green before tagging.
- **Acceptance:** `git status` clean on the tag commit **and** a green full matrix
  (3.11/3.12/3.13) recorded for that exact commit.
- **Independent?** No — depends on the WIP owners landing their work.
- **Regression risk:** committing is low-risk; the real risk is discovering full-suite
  failures the sampled gates did not surface.

### B2 — The Four Paths course and lifecycle contract are unverified, with a confirmed structural contradiction
- **Class:** 1 for the confirmed contradiction + missing execution evidence of an
  **explicitly advertised 1.0 product surface**; reasonable owners may split the
  numbering fix (blocker) from a full manifest (defer, see R/D items).
- **Evidence:** `devguide/pending_bugs/course_module_numbering_overlaps.md` (**Status:
  Confirmed**): `course/index.md` and `README.md` describe common-core modules 1–16,
  but the filesystem has 20 common-core notebooks and paths numbered 17–50, so 17–20
  are ambiguous. `find docs/content/course -name '*.ipynb'` = **174 notebooks**; the bug
  text still says 156. No `nbval`/`nbconvert --execute`/`papermill` in `.github/` or
  `devtools/` → notebooks are **not** executed in CI, yet `devguide/documentation_sync.md`
  makes "execute applicable notebooks" step 6 of the lifecycle contract and warns that
  "notebook code and outputs can be stale even when links resolve."
- **Impact:** 1.0 advertises a course and a documentation-is-contract policy; shipping a
  contradictory, unexecuted 174-notebook course undermines both. Scientific impact is
  indirect (teaching material may drift from the real API).
- **Cost:** medium — one-time renumber/id migration + one executed pass over the Tier-1
  core notebooks in a supported environment.
- **Closure:** fix the numbering to stable identifiers (per the bug's "Required
  resolution"); run the Common-Core + one representative path under execution and record
  the environment/result.
- **Acceptance:** `index.md`/`README.md` numbering matches the filesystem; a recorded
  execution pass (env + result) for at least the Common Core; the bug moved to
  `devguide/archive/resolved_bugs/`.
- **Independent?** Partly — numbering fix is independent; full execution needs the soft-
  dependency matrix.
- **Regression risk:** low (docs/notebooks), but renumbering touches many cross-links.

## 4. Important risks to resolve before 1.0 (category 2)

### R1 — Tier-1 **function** classification is silent
- **Evidence:** `devguide/support_tier_protocol.md` §"Pending design questions": *"Tier 1
  function audit … Silence currently does not distinguish an approved Tier 1 function
  from an unclassified function."* Only **forms** have an explicit registry
  (`form_tier.py`); public functions (e.g. `molsysmt.structure.*`, `molsysmt.pbc.*`) have
  no tier assertion. The API stability registry classifies *stability* (stable/
  experimental) but not *support tier*.
- **Impact:** API-truth gap — the contract can't mechanically prove a function is Tier 1.
- **Cost:** low–medium (extend the registry/decorator to functions or assert stable⇒Tier1).
- **Acceptance:** a validator asserts every public function has an explicit tier (or a
  documented stable⇒Tier-1 mapping). **Independent?** Yes. **Regression risk:** low.
- **RESOLVED 2026-07-22.** Tier is derived from the stability registry
  (stable⇒Tier 1, experimental⇒Tier 3, outside-contract⇒outside core); enforced by
  `devtools/scripts/validate_function_tiers.py`; documented in
  `pending_proposals/function_support_tier_classification.md` and `support_tier_protocol.md`.
  `molecular_dynamics` decided deferred post-1.0 (stubs, not public) and its phantom
  `@support_tier(3)` decorators removed.

### R2 — Only smoke CI gates day-to-day; full matrix is manual/weekly and commits skip CI
- **Evidence:** `ci-smoke.yaml` push-triggered; `ci-full.yaml` `workflow_dispatch`;
  `ci-weekly.yaml` scheduled; dev commits use `[skip ci]`.
- **Impact:** regressions can accumulate between weekly runs; overlaps with B1.
- **Cost:** low (policy: require a green full run on release candidates and on merge to a
  release branch). **Acceptance:** documented release-gate policy + one green full run
  per candidate. **Independent?** Yes. **Regression risk:** none.
- **RESOLVED 2026-07-22 (policy + tooling).** `devguide/release_gate.md` is the normative
  gate; `devtools/scripts/release_gate.py` aggregates the 10 validators + a public-API
  smoke into one verdict (11/11 pass). Remaining action for whoever tags: run `ci-full`
  on the committed candidate and add `release_gate.py` as an early CI step.

## 5. Recommended but deferrable improvements (category 3)

- **D1 — Label the implemented-but-unreviewed proposals in place (decided 2026-07-22:
  keep, do not archive yet).** `DOCUMENT_POLICY.md` says a completed proposal should move
  its durable rules to a normative doc and be archived. **Exception applied:** the four
  proposals (`explicit_form_support_registry`,
  `chemical_graph_and_conversion_execution_checkpoint`,
  `chemical_state_adapter_fidelity_audit`, `chemical_state_v1_executable_contract`) are
  **implemented in the working tree but not yet reviewed by the collaborator**, so they are
  **not "completed"** in the policy sense — they legitimately remain pending proposals
  (their unresolved part is review + activation). Each is banner-marked accordingly with a
  what/how summary. On collaborator review + acceptance (with the 1.0 WIP) they should then
  be archived and their durable rules folded into normative docs, per DOCUMENT_POLICY.
  (`conversion_fidelity_and_molsysdict_v1` and `topology_selection_indexing_and_pyarrow`
  remain partially-implemented and open.)
- **D2 — `documentation_lifecycle_manifest.md`** (Proposed): executable symbol→doc
  mapping. Valuable but a manifest is not required to tag 1.0. Deferrable.
- **D3 — Tier 2/3 attribute-delivery debt** (`form_attributes_declared_without_getters.md`,
  **Status: Tier 1 resolved; Tier 2/3 pending**). Outside the contractual surface;
  `get()` already raises a catalog `NotWithThisFormError` instead of leaking. Defer.
- **D4 — `benchmark_regression_gate_reliability.md`** (Proposed): statistical robustness
  of perf gates. Post-tag hardening.
- **D5 — `git_history_bloat_cleanup.md`** (pending; diagnosis done): repo hygiene, not
  release-gating.
- **D6 — `smonitor_warn_drops_structured_extra.md`**: **Severity low here** (working
  pattern exists), reported upstream. Not a blocker.

## 6. Expensive work that can legitimately continue after 1.0 (category 4)

Explicitly post-1.0 by their own status lines; none is a blocker (the user's guidance
that a pending proposal is not automatically a blocker holds here):

- `rusterization_heavy_computations.md`, `rusterization_hybrid_columnar_ecs_arrow_graph_engine.md`,
  `rusterization_parallel_trajectory_io.md`, `rusterization_topology_and_selections.md`
  (all "proposed" Rust migrations);
- `native_format_parsers_post_1_0.md`, `chemical_metadata_preservation_sdf_mol2.md`
  ("post-1.0 proposal"), `psf_force_field_mass_preservation.md` ("post-1.0 schema"),
  `optional_native_columns_memory_model.md` ("post-1.0");
- `attribute_centric_molecular_system_model.md` — its own text: the interaction slice
  *"should not become a release blocker or a stable public"* API before 1.0;
- `topology_selection_indexing_and_pyarrow.md` (phase 1 done; further phases post-tag),
  `conversion_fidelity_and_molsysdict_v1.md` (the **419** accepted-debt items and the
  MolSysDict schema-v2 migration — accepted debt, P2 remainder);
- `proposal_protor_atom_typing_and_radii.md`, `topomt_requested_spatial_helpers_and_sasa.md`,
  `trajectory_projection_onto_principal_components.md`, `conda_numba_preheating.md`
  (exploratory). `physchem_electronegativity_per_element.md` and
  `physchem_support_dummy_atoms.md` were implemented in commit `90b2a491a`
  (2026-06-15), are covered by tests, and have been archived under
  `archive/resolved_proposals/`. The former `parallel_numba_jit_segfault.md` report was subsequently
  reproduced deterministically, corrected as an ordered-relation alignment bug, and
  archived after the complete 9,417-test gate passed.

## 7. Contradictions and stale claims found in devguide (category 5)

1. **Completed proposals not archived.** `roadmap.md`: *"Completed proposals should be
   moved to an archive."* `devguide/archive/` exists, yet these carry a
   complete/implemented status while still in `pending_proposals/`:
   `chemical_state_adapter_fidelity_audit.md` ("complete"),
   `chemical_state_v1_executable_contract.md` ("implemented"),
   `chemical_graph_and_conversion_execution_checkpoint.md` ("complete"),
   `explicit_form_support_registry.md` ("implemented"),
   plus the partially-done `topology_selection_indexing_and_pyarrow.md` and
   `conversion_fidelity_and_molsysdict_v1.md` (legitimately still open).
2. **Course counts disagree.** `course_module_numbering_overlaps.md` says "156
   notebooks"; the filesystem has **174**; `index.md`/`README.md` common-core span (1–16)
   disagrees with the 20 common-core files. (Same root as B2.)
3. **Lifecycle claim vs. reality.** `documentation_sync.md` requires executing applicable
   notebooks as part of the contract, but no execution automation exists — the contract
   is currently unenforced (see B2).
4. **`support_tier_protocol.md` "Pending design questions"** documents an acknowledged
   Tier-1-function gap (R1) — a known-incomplete contract shipped as if settled.

None of these are code defects; all are documentation-truth items, cheap to fix, and
none blocks the science.

## 8. Recommended stint sequence

1. **Stint A — land the WIP (B1).** Commit the ~95 `molsysmt/` changes in reviewed units;
   trigger `ci-full` on the candidate; get a green 3.11/3.12/3.13 matrix. *Gate for
   everything else.*
2. **Stint B — course numbering + one execution pass (B2).** Fix identifiers, reconcile
   `index.md`/`README.md`, execute the Common Core in a supported env, archive the bug.
3. **Stint C — Tier-1 function classification (R1)** + **release-gate policy (R2).**
4. **Stint D — devguide hygiene (§7): archive the six completed proposals; correct the
   course counts and the lifecycle-claim wording.** Cheap, high signal-to-noise.
5. **Tag 1.0** once A–C are green and D is done. Defer all category-3/4 work.

## 9. Constraints honored

No code or pre-existing document modified; no fixes applied; the full suite and expensive
campaigns were not run (the eight validators + focused Tier-1 selections + a smoke test
were sufficient and are cited above); all existing WIP preserved; no commit, no push.
This file is the only artifact created.

## 10. Maintainer disposition after the independent audit

**Reviewed:** 2026-07-22

The audit is accepted as useful prioritization evidence, with the following
scope corrections and updated local evidence.

### Updated B1 evidence

After the audit was written, the current working tree completed the full local
gate with:

- `python -m pytest --receptor=llm -n 12 --dist loadfile`:
  **9386 passed, 2 skipped, 0 failed**;
- `ruff check molsysmt tests devtools`: passed;
- all eight validators listed in section 2: passed;
- `git diff --check`: passed.

No xdist worker crashed and the suspected Numba segfault did not recur. B1 is
therefore narrowed from "the WIP has no demonstrated full-suite result" to the
actual release-process gate: the verified WIP must be landed in coherent commits,
and the Python 3.11/3.12/3.13 CI matrix must pass for the exact release-candidate
commit. A green dirty tree is strong development evidence but is not a reproducible
release artifact.

### B2 is split into a blocker and a risk

The course numbering overlap is a confirmed documentation-contract defect and
remains a pre-1.0 blocker. The stale count in its bug record has been corrected
from 156 to 174 notebooks.

The absence of automated execution for all 174 notebooks is an important lifecycle
risk, but it is not accepted as a requirement to execute the entire course before
1.0. The lifecycle policy requires verification and execution of *applicable*
notebooks for changed behavior. The pre-1.0 gate is therefore:

1. resolve the numbering and add a structural validator;
2. execute the Common Core and the notebooks affected by the current WIP in a
   supported environment;
3. record explicit omissions and failures rather than claiming that all 174
   notebooks were verified.

Full-course execution automation remains desirable follow-up work and must not be
silently represented as already implemented.

### Function support classification

R1 identifies a real documentary ambiguity, but a second manually maintained
function-tier registry is not accepted as the default solution. Public symbols are
already classified exhaustively by the normative API stability registry. Before
1.0, the support-tier protocol should state explicitly how an active `stable`
classification defines the contractual 1.x surface, while `experimental`,
`outside-contract`, and deprecated lifecycle entries retain their declared API
status. Runtime support-tier signals and form tiers remain separate operational
mechanisms. This resolves the silence without creating two competing authorities.

### Accepted release order

1. partition and land the current verified WIP;
2. run the full Python 3.11/3.12/3.13 matrix on the exact candidate commit;
3. resolve course numbering and verify the applicable documentation notebooks;
4. clarify the function/support-tier policy and perform pending-guide hygiene;
5. run the final release audit and tag 1.0 only from a clean, verified commit.

The independent estimate of approximately 85% remains a reasonable conservative
release-readiness figure until the WIP is committed. The green local gate raises
confidence in the implementation, not yet in release reproducibility.

---

## 11. Post-Audit Correction: Conversion-Fidelity WIP — 2026-07-26

The conversion-fidelity result in Section 3.2 is valid historical evidence for
the tracked surface inspected on 2026-07-22. It must not be read as evidence
that the current untracked fidelity WIP is green.

The current working tree adds three untracked conversion-truth modules with the
following result:

| Test module | Current result |
| --- | ---: |
| `test_conversion_report_native_scopes.py` | 13 failed |
| `test_coordinate_trajectory_fidelity.py` | 4 failed |
| `test_pdb_fidelity.py` | 21 failed, 1 passed |

The 38 failures cover at least six independent gaps. Most importantly, the
untracked `audit_conversion_fidelity.py` imports audit-scope helpers that do not
exist, so the proposed release gate does not currently reach its audit logic.
Other gaps concern issue scope metadata, exhaustive schema-driven auditing of
native dictionary forms, strict handling of non-chemical losses, independent
schema and adapter defects, and a multi-cause PDB fidelity workstream.

The canonical diagnosis and four-stage closure plan are:

- [`conversion_fidelity_wip_contract_gaps.md`](../pending_bugs/conversion_fidelity_wip_contract_gaps.md)
- [`conversion_fidelity_and_molsysdict_v1.md`](conversion_fidelity_and_molsysdict_v1.md)
- [`release_1_0_execution_plan.md`](release_1_0_execution_plan.md)

### Effect on the Release Assessment

This correction does not invalidate the green tracked tests or the
architectural assessment. It does strengthen blocker B1: the WIP cannot merely
be committed and followed by a full matrix. Its fidelity surface must first be
made internally coherent.

The revised order is:

1. close the audit-scope contract;
2. implement exhaustive native-dictionary auditing and strict loss handling;
3. close the independent schema and adapter defects;
4. close the PDB fidelity workstream;
5. freeze the final Numba oracle and productize multiplatform Rust wheels;
6. remove the Numba CPU and CUDA implementations and all active JIT residue;
7. land each segment in reviewable commits;
8. run the complete Rust-only release matrix on that committed state;
9. continue with the course lifecycle and Tier-1 policy blockers described
   above.

Until those steps are complete, the honest conversion status is: **the tracked
conversion contracts are green, but the stronger untracked fidelity contracts
are not implemented, and the proposed release audit cannot currently start.**

The earlier approximately 85% readiness estimate predates the accepted
Rust-only 1.0 boundary. Because the CPU port is complete but production wheel CI,
Numba-CUDA removal, and zero-Numba cleanup are not, that percentage must not be
carried forward mechanically. Re-estimate readiness after the packaging spike
and conversion-fidelity closure provide executable evidence.
