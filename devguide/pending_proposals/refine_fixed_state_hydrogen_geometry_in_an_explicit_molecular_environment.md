---
summary: Refine fixed-state hydrogen geometry in an explicit molecular environment
issue: uibcdf/molsysmt#323
status: open
opened: 2026-10-04
closed:
verification: measured
area: [build, structure, preparation]
guard:
normative:
blocked_by: []
supersedes: []
---

# Environment-aware fixed-state hydrogen refinement

**Reported:** 2026-10-04, while composing the prepared 1QKU receptor fragment
and EST for uibcdf/molsysmt#298.
**Status:** Proposed future capability; no refinement implemented or executed.

## What

Provide an explicitly requested, reusable refinement of generated hydrogen
positions in a declared molecular environment, after chemical-state selection
and fixed-state H addition. Preserve chemical assignments and observed heavy-atom
coordinates. Report the refined atoms, method, parameters, units, environment,
software versions and unresolved parameter or geometric coverage. The owning
public API and scientific method require review before implementation.

## How

Use `build` for preparation orchestration, `structure` for geometry, `pbc` for
periodic reconstruction, and `molecular_mechanics` for energy-based refinement.
Reuse their general tools and extend a provider where a capability has standalone
use. Do not embed a competing minimizer or hydrogen orientation engine in an
interaction detector. The existing `potential_energy_minimization` interface
has no explicit frozen-heavy-atom selection; its default parameter choices do
not establish ligand/receptor coverage.

Require an explicit chemical state, movable H indices, fixed atoms and environment.
Compare documented orientation/relaxation methods, including hydroxyl/thiol
rotations and supported force-field minimization. Validate parameter coverage
before energy evaluation. Keep charges, atom typing and complete force-field
parameterization distinct. Failure or absent coverage must remain inspectable.
For several structures, process bounded blocks with explicit periodic conventions.
Changing H coordinates invalidates affected named analyses under the existing
coordinate-edit policy; recalculation is a separate operation.

## Why

Fixed-state H addition generates local positions without optimizing the receptor
environment. The prepared 1QKU receptor-fragment/EST composition produces no
H-bond observations under the selected distance/angle definition. This is a
geometry checkpoint, not evidence of biological absence. DockingMT and
PharmacophoreMT need to distinguish an assigned chemical state, local H placement
and environment-aware preparation.

## What is measured and what is assumed

**Contract-tested:** the fixture in
`tests/physchem/test_chemical_template_receptor.py` composes 4,003 receptor atoms
and 44 EST atoms using `msm.merge`. Fixed-state H addition retains all 1,995
deposited heavy-atom positions. The `donor_acceptor_distance_angle` method with
`smarts_donor_acceptor` recognition and `pbc=False` produces zero observations;
hydrophobic detection produces 12, checked against independent pair distances.

Reproduce the public composition and detection controls:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
    tests/physchem/test_chemical_template_receptor.py
```

**Contract-tested local diagnostic:** public `get_hbond_sites` identifies both
ligand hydroxyl donor/H pairs and nearby receptor acceptors. Independent NumPy
geometry for triples `(4006, 4025, 379)` and `(4021, 4043, 1754)` confirms D–A
distances below 0.35 nm but D–H–A angles below the required 130 degrees. These
are local indices of the composed system. The test above preserves this
diagnosis, without treating it as biological validation of the pose.

**Assumed:** explicit environmental refinement could improve some H orientations.
No energy calculation, force-field coverage, experimental H reference, optimal
pose or increased H-bond count has been established.

## What was refuted

- Correct H inventory and unchanged heavy coordinates do not establish optimized
  H geometry in the surrounding environment.
- Close donor–acceptor distances alone do not satisfy an angular H-bond method.
- Unconstrained whole-system minimization cannot satisfy a contract that freezes
  observed heavy atoms. Default parameterization is not proof of ligand coverage.
- Maximizing the number of H bonds is not an independently justified physical
  objective and must not become the acceptance criterion.

## Scope and exclusions

Future explicit refinement after fixed-state H placement; it does not block the
current bounded template-transfer contract. No automatic optimization during
conversion, recognition or H addition. No pH/protonation search, chemical-state
changes, missing heavy-atom reconstruction, docking, global-minimum guarantee or
biological certification. uibcdf/molsysmt#308 concerns a future native general H
addition engine; uibcdf/molsysmt#249 concerns energy-based modified-residue heavy
coordinates. Those are separate themes.

## Acceptance criteria

- A documented method and public form-agnostic contract with ArgDigest, explicit
  units and optional dependencies, shared provider tools and producer attribution.
- Tests retain chemical assignments and observed coordinates exactly, move only
  authorized H, reject unsupported coverage without mutation and check independent
  geometric/energy criteria, including nondefault units and periodic cases.
- Results preserve source maps and report environment, parameters, constraints,
  unresolved coverage and detached provenance; no silent parameter fallback.
- Named analyses become unevaluated for changed structures and can be explicitly
  recalculated. User Guide and course distinguish placement from refinement.
- Real-input evaluation precedes any claim of improved consumer scientific results.

## Dependencies and risks

Related provider workflows: uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Consumer context: uibcdf/pharmacophoremt#22 and uibcdf/dockingmt#33.
Force-field selection and ligand parameters can change results; inferred chemical
readiness must not substitute for parameter coverage. This proposal is independent
of persistence of experimental MolecularMechanics in a future H5MSM version.

## Provenance

Linux local development environment, 2026-10-04; Python 3.13.14, NumPy 2.4.6,
pandas 2.3.3, RDKit 2025.09.5 and released ArgDigest 0.13.0. Python uses the bounded
uibcdf/molsysmt#237 migration exception, not Python 3.14 qualification. MolSysMT
base source is `879c13894fbea7c09dd6b3c62f4ec458e61c1780` with the receptor
composition regression added in this checkpoint. Six tests passed in 34.36 s;
one existing pandas future warning came from the H5MSM chemical-state reader.
These timings describe this test execution, not a performance benchmark.
