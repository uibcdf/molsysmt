---
summary: Provide explicit read-only molecular geometry and steric plausibility assessment.
issue: uibcdf/molsysmt#555
status: open
opened: 2026-11-04
closed:
verification: inspected
area: [structure, physchem, api]
guard:
normative:
blocked_by: []
supersedes: []
---

# Read-only geometry and steric plausibility assessment

**Reported:** DockingMT requests molecular assessment independently of pose-recovery
RMSD, under uibcdf/dockingmt#33 and uibcdf/dockingmt#49.
**Disposition:** scope a future general-purpose capability after the frozen initial
release. No new numerical bug or mandatory 1.0 gate is established by the request.

## What

Assess declared molecular geometry without repairing or modifying it. Candidate
checks include bond lengths, angles, aromatic planarity, intra/intermolecular
steric overlap and coordinate-derived stereochemical consistency. A result must
distinguish assessed pass/fail from unassessed/unsupported, retain the affected
source indices and quantities, and name the rule, reference model and version.
There is no proposed universal certificate that a molecule is scientifically valid.

## How

Review existing tools before choosing a public function or optional validator:

- `physchem.get_chemical_readiness` describes stored-field coverage and explicitly
  unassessed checks. Its Notes state that it does not validate valence, perceive
  aromaticity, choose protonation or certify chemistry.
- `physchem.get_cip_stereochemistry(from_coordinates=True)` supports explicit
  inference from one nonperiodic 3D conformer on a copied complete graph. Reading
  declared labels is not coordinate verification.
- General distance, angle, dihedral and fitted-plane geometry, atomic radii and
  selected-state graph tools provide reusable measurements. Their availability
  does not define chemically justified thresholds or bonded-neighborhood exclusions.

Keep geometric primitives in `structure`, reference chemical models in `physchem`
and graph prerequisites/exclusions in `chemical_states`. Determine the owning
public assessment boundary during design; do not embed molecular rules in
DockingMT or create a competing chemical-state store. Review named external
methods before adopting thresholds or another dependency. PoseBusters is a
consumer-suggested reference to study, not a method qualified by this triage.

## Why

Reference-pose similarity and molecular plausibility answer different questions.
DockingMT needs per-check evidence while preserving every original pose and score.
The same general tools can serve preparation and other molecular workflows.
This is a consumer requirement and source-inspection finding, not measured
accuracy or proof that a new orchestration function is necessary.

## Evidence and refuted interpretations

The owner reviewed the public readiness and coordinate-CIP boundaries on main
1f462976d, whose runtime matches the pre-audit 93d29bf23 source for these tools.
No new geometry computation, benchmark, external-validator evaluation or
scientific oracle was executed for #555.

Radii plus distances do not alone define a clash model. RMSD does not establish
valence, stereo or steric plausibility. A missing check cannot count as a pass.
#323 is environment-aware hydrogen refinement, not this read-only assessment.
#310 correspondence/RMSD and #521 partial PDBQT representation retain their scopes.

## Scope and acceptance criteria

Start with an explicitly reviewed nonperiodic small-molecule/protein-ligand
profile if supported by the selected reference. Before implementation:

- define each optional named check, reference, threshold/tolerance, bonded-pair
  exclusions, hydrogen policy and chemical applicability;
- specify selections, source atom/bond/pair identities, units, rule versions and
  per-check outcomes/reasons;
- distinguish retained heavy-only PDBQT coordinates from missing/merged H;
  never restore absent observed coordinates from a stale preparation;
- report missing chemistry, coordinate/radius/model coverage and provider errors
  explicitly, without silently repairing or substituting another method;
- retain source/pose immutability and use applicable ArgDigest, SMonitor,
  PyUnitWizard, DepDigest and optional Ackredit boundaries;
- guard known favorable/adverse geometries, coordinate stereo, excluded bonded
  pairs, empty selections, missing chemistry/H, nondefault units and failures
  against independent, justified expected outcomes.

API shape, multi-structure/PBC support and detailed ownership remain design
decisions. No implicit hydrogen addition, bond inference, state selection,
relaxation, minimization or file-schema change is authorized by this proposal.

## Dependencies and next action

The current stabilization sequence remains #548, #554, #549, #504 and #543 under
#334. After that bounded work, study available reference methods and agree a
contract with the requesting consumer. A future implementation requires its own
reviewed scope; this disposition does not promise a delivery date or expand 1.0.

The original request and its full acceptance context remain in
[uibcdf/molsysmt#555](https://github.com/uibcdf/molsysmt/issues/555).
