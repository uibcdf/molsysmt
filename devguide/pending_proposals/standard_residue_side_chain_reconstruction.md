---
summary: Reconstruct ambiguous standard-residue side chains with explicit geometric evidence
issue: uibcdf/molsysmt#327
status: open
opened: 2026-10-05
closed:
verification: inspected
area: [build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Standard-residue side-chain reconstruction

**Reported:** 2026-10-05, when reviewing the original acceptance scope of
uibcdf/molsysmt#298 after its template-transfer and consumer qualification.
**Status:** Future capability; no new reconstruction method selected or implemented.

## What

Extend explicitly requested standard-residue heavy-atom reconstruction to
ambiguous side-chain gaps, with independently checked geometric evidence,
preserved observed coordinates and source correspondence. Keep unsupported
cases inspectable. This is a general `build` capability, separate from assigning
chemical templates to existing atoms in `physchem`.

## How

Inspect and extend the public `build.add_missing_heavy_atoms` contract rather
than implementing a placer inside template application or interaction detectors.
Compare local internal-coordinate construction, reference rotamers and optional
constrained energy refinement before choosing a scientific method. Reuse
`topology` connectivity, `structure` geometry and `pbc` reconstruction tools;
energy operations and parameter-coverage checks belong to their owning provider.
Do not create another chemical store or infer a protonation state during repair.

Require the selected chemical state, observed fixed atoms, missing inventory and
explicit reconstruction method. Report generated atom indices, retained source
maps, coordinate evidence, method/parameters/units, reference identity and original
producer versions. Ambiguity, absent reference/parameter coverage, incompatible
chemistry or failed geometry must leave the source unchanged and remain explicit.
Process multiple structures in bounded blocks. Any affected named interaction
analyses follow the existing coordinate/atom-edit invalidation policy.

## Why

The observed 1QKU label-chain A receptor lacks SER301 OG and LYS302/LYS303
CG/CD/CE/NZ. The existing bounded native repair supports the serine case but
leaves both four-atom lysine gaps unassessed. An explicitly declared closed
fragment can support current consumer qualification; complete receptor preparation
needs a trustworthy reconstruction route for these gaps.

Consumers include uibcdf/pharmacophoremt#22 and uibcdf/dockingmt#33. Successful
template assignment to existing atoms does not supply missing coordinates.

## What is measured and what is assumed

**Historical measured evidence:** the
[resolved preflight defect](../archive/resolved_bugs/native_standard_residue_repair_must_reject_ambiguous_side_chain_placement.md)
records that the old rigid placer added nine atoms to the 1,990-atom receptor,
including a modeled LYS303 CB-CG bond of 0.1199 nm. Its reference side-chain C-C
bonds are approximately 0.15 nm. The corrected public route adds only SER301 OG,
preserves observed coordinates/IDs, and reports the two lysine gaps. That record
contains the environment and commands; these measurements were not repeated when
opening this proposal.

The current boundary is executable through:

```bash
python -m pytest --receptor=llm \
    tests/build/add_missing_heavy_atoms/test_standard_residue_preflight.py
```

**Inspected:** this guard and the provider's preflight do not implement a
validated multi-atom side-chain search. The fixture qualification intentionally
uses the closed fragment 304–550 and does not certify a repaired full receptor.

**Assumed:** a rotamer/reference search with independently validated local
geometry and, where justified, explicit environmental refinement could extend
coverage. No chosen method, energy minimum or performance advantage is claimed.

## What was refuted

- A completed inventory or equality with PDBFixer's atom count does not validate
  modeled coordinates. Do not re-enable the rejected rigid placement to satisfy
  a count or consumer recognition test.
- A rigid fit of observed atoms does not determine missing side-chain torsions.
- Neither a favorable interaction count nor default force-field availability
  establishes chemical or geometric correctness.

## Scope and exclusions

Standard-residue missing heavy side chains under explicit fixed chemistry. No
automatic repair in conversion, matching, recognition or template assignment;
no pH selection, arbitrary ligand generation, biological certification or
global-minimum claim. Modified-residue energy-based placement remains
uibcdf/molsysmt#249. Hydrogen environmental refinement remains
uibcdf/molsysmt#323; a native general ligand H engine remains uibcdf/molsysmt#308.
Those independent themes need not be implemented to close this one.

## Acceptance criteria

- A documented, form-agnostic public boundary with argument digestion, units,
  explicit optional dependencies and independently usable provider tools.
- Preserve observed atom identity, membership, physical coordinates and selected
  chemical assignments across structures and nondefault units; retain generated
  versus observed evidence and source maps through supported native persistence.
- Validate generated bonds, local stereochemistry, clashes and method-specific
  constraints against independent references. Do not validate an output solely
  against itself. Qualify the real lysine gaps and analytical positive/negative
  controls, including unsupported cases with transactional failure.
- Retain the current conservative guard for cases outside new validated coverage.
  Optional energy refinement must check parameter coverage and fixed-atom
  constraints before execution; it must not silently move observed atoms.
- Update public docstrings, User Guide and relevant course lessons. Record actual
  consumer outcomes separately from geometric validation and performance.

## Dependencies and risks

Related provider issues: uibcdf/molsysmt#298, uibcdf/molsysmt#322,
uibcdf/molsysmt#249 and uibcdf/molsysmt#323. No implementation dependency has yet
been established. No new runtime dependency or Rust routine is proposed without
method review and workload evidence. Several conformations may satisfy local
constraints; reporting a selected reconstruction must not imply an observed pose.

## Provenance

Source inspection on 2026-10-05 at MolSysMT
`93f8f28b6b0cf23673d845ccd5a679013d4fbcd4`. Historical measurements belong to
the linked #322 record, dated 2026-10-04. This proposal carries no new execution,
benchmark, consumer adoption or scientific-validation receipt.
