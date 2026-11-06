---
summary: Native add misaligns selected atom identities across domains and retains unselected mechanics.
issue: uibcdf/molsysmt#618
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [basic, native]
guard: tests/basic/add/test_selected_domain_alignment.py::test_selected_add_keeps_atom_identity_in_every_domain
normative:
blocked_by: []
supersedes: []
---

# Native add misaligns selected atom identities across domains

**Reported:** 2026-11-06, independently reproduced during the pre-1.0 audit.
**Status:** resolved in the native source; public-source delivery/issue closure follow the checkpoint verification.

## What

On `4a80c22941090257d8ef78df09c944831413ee31`, this public operation gives
source atoms different identities in inventory, structural/chemical fields and
mechanics:

```python
result = msm.add(target, source, selection=[2, 0], in_place=False)
```

The one-atom target is L0; source atoms R0/R1/R2 have x=0/1/2 nm and synthetic
formal/mechanical charges 0/1/2. Inventory becomes L0/R0/R2, but x/formal
charges become 0/2/0. Mechanics retains four rows for the three-atom result.
These fields are index markers; no physical parameterization is evaluated.

## How

`MolSys.add` sends the original selection to separate owners. `Topology.add`
uses native sorted extraction, while structures and chemistry retain supplied
order. `_merged_molecular_mechanics` receives the complete source table.
Assembly chain references also receive only a target offset, without restricting
or compacting the source chains first.

The working correction normalizes one unique, valid ascending source subset at
the native boundary and passes it to every affected owner. Mechanical columns
are projected before concatenation. A shared private native assembly projection
is reused by extraction and addition: retain complete operations, compact their
chains, select matching transforms and offset into the destination. Assembly
metadata is copied independently. Structural extraction still selects source
coordinates once; no preliminary full-source molecular copy is introduced.

## Why

Successful composition must preserve identity across attached domains. Wrong
coordinates/assignments can silently change subsequent scientific calculations;
extra mechanics rows violate the atom axis. Matching sizes alone is insufficient.

## What is measured and what is assumed

The audit probe and portable receipt retain the original values. The maintained
regression additionally checks IDs/names, coordinates and velocities with explicit
units, B factors/occupancy, formal/mechanical fields, induced bonds/components,
alternate locations, assemblies and original-input independence. Public, native
and form-adapter paths are tested in both mutation modes.

The first two test-authoring attempts failed before reaching the operation
(incorrect root constructor/plural table spelling); their JUnit records remain.
The corrected counterexample selection records 23 failures and seven passes on
the original runtime, including one assertion-authoring error comparing quantity
objects directly. The first corrected-runtime run records 27 passes and three
diagnostic-wording failures, with unit-stripping warnings in the B-factor
assertions. Subsequent assertions explicitly convert quantities and the native
diagnostic names `atom_indices`; these are not a change to numerical expectations.
Final receiving is recorded below when complete.

Resource preservation is source-inspected, not benchmarked. No speed or process
memory improvement is claimed.

## What was refuted

- A sorted selection/count-only assertion does not detect reversed identity.
- Sorting only coordinates leaves chemistry and mechanics inconsistent.
- Selecting structural fields alone cannot restrict assembly chain references.
- Repeating source atoms is not an admitted chemical subset: chemical-state
  extraction already rejects duplicate indices. Reject them at the native add
  boundary before staging, rather than relying on later incidental errors.

## Scope and exclusions

Preserve native ascending atom-subset order, explicit structure order/repetitions,
IDs, strict/intersection attribute policies and existing unsupported multistate
or incoming-analysis merge behavior. Preserve partial topology/chemistry systems
without structures. This is not a new atom permutation, chemical merge policy,
detector, mechanical assignment or file schema.

## Acceptance criteria

- Identity-aware cases pass for reversed/nonconsecutive, empty and full subsets.
- Mechanical rows, bonds/components, alternate locations and assemblies align.
- Source inputs and independent targets survive unchanged; errors and warnings
  promoted to errors publish no partial target.
- Relevant native, add, extraction, composition and interaction guards pass.
- Public documentation explains the existing atom-subset convention and paired
  structure order. Publish the correction and close with the addressable guard.

## Provenance

Linux, existing `molsyssuite@uibcdf_3.14`, Python 3.14.7, published Pytest Receptor
1.2.1, 12 pytest workers. Controlled Viewer source and unchanged extension identity
are recorded in the [audit packet](../../pre_1_0_robustness_audit_20261106.md).
Local JUnit evidence is under `.pytest_cache/pre1-review-20261106/618-*.xml`.
No environment was installed or replaced. Package/platform/release qualification
remains separate.

## Resolution checkpoint — 2026-11-06

Implemented in `19d6d55c1663bf3c6c7adfb9433fc775326292b5`. The final joint native,
composition, H5MSM and named-interaction selection passes **2,748 cases**, with
zero failures/errors/skips and 746 retained warnings. The expanded string/append
and module-doctest selection passes **40 cases** separately; scopes overlap and
are not summed. All-code Ruff checks/formatting, dependency validation and the
156-notebook course structure check pass. Tutorial/course edits preserve every
code cell, output, ID and metadata; affected public docstrings, tools, cookbook
and native-domain guidance describe the contract.

The [portable phase-one receipt](../../../devtools/data/pre_1_0_robustness_phase1_receiving_20261106.json)
retains original failed/authoring attempts, exact test summaries/digests, source
identity/hashes, versions and limits. Source delivery is verified on origin
before board closure. A source closeout does not qualify another platform, an
installed Viewer pair or a release artifact. PR #543's remaining graphical/session
receiving and other linked defects retain their own scope.
