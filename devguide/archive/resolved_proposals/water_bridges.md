---
summary: Explicit single-water hydrogen-bond bridges
issue: uibcdf/molsysmt#281
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api]
guard: tests/interactions/water_bridges/test_get_water_bridges.py
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Explicit single-water hydrogen-bond bridges

**Reported:** 2026-10-01, maintainer request to complete the remaining families.
**Status:** Resolved with independent evidence and bounded experimental contracts.

## What

Compose two same-frame attributed hydrogen-bond observations sharing one explicitly indexed neutral water molecule. Preserve both directed D-H-A triples, images, geometry and producer attribution. All-participant selection semantics remain those of Interactions; internal requires mediator atoms in the selection. Higher-order water networks and implicit-hydrogen bridges are excluded.

## How

Reuse complete state-specific chemical graphs, sparse numeric observations,
projected geometry execution and H5MSM 0.5 typed persistence. Reference packages
are not runtime dependencies. Keep visualization and sessions in MolSysViewer.

## Why

Complete the explicitly scheduled interaction families in #250 without confusing
observed geometry with chemical-state assignments or making claims about energies.

## What is measured and what is assumed

Source conventions and executable evidence are recorded below.
Memory limits are numeric working estimates, not a process-RSS guarantee.

## What was refuted

A dense atom-by-atom-by-frame tensor does not suit typed roles and sparse observations.
Method names identify scientific criteria, not reference software authorship.

## Scope and exclusions

Experimental independent analyses; attachment remains explicit. No implicit
chemical repair, minimization, renderer or session implementation.

## Acceptance criteria

Independent reference/analytical truth, selection and empty coverage, form parity,
PBC geometry reconstruction, units under non-default policy, bounded execution,
producer attribution and named/typed H5MSM round trips. Executed tutorials and
updated developer, Foundations, Cookbook and course documentation.

## Scientific evidence and alternatives

**Scientifically validated, bounded controls:** the offline oracle uses original
ProLIF 2.2.2 HBDonor observations plus independent pair enumeration, not
MolSysMT's detector and not the complete reference WaterBridge pipeline. Three
water-role systems, nine structures and six paths match exact branch/occurrence
keys and D-A distances/D-H-A angles across RDKit, native MolSys and H5MSM.
Default Baker-Hubbard and Wernet-Nilsson observations are also checked against
controlled straight-leg analytical geometry for water donating both branches,
accepting both, and donating/accepting one each.

[ProLIF WaterBridge](https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/water_bridge.py)
and [MDAnalysis WaterBridgeAnalysis](https://docs.mdanalysis.org/stable/documentation_pages/analysis/wbridge_analysis.html)
provide the reference graph concept. The named leg criterion retains its own
paper/profile attribution. Mol* uses different implicit-hydrogen and water-angle
criteria; they are not treated as numerical aliases. Complete reference residue
handling, force-field typing, network orders and aggregation are not reproduced.

Same-frame tests reject legs observed only in separate frames and two legs to
the same external heavy atom. Bifurcated indexed H preserves two chemical roles
without duplicate occurrences. All actual branch atoms define query scope;
endpoint-only internal selection returns zero rather than silently inserting
a mediator. Orthogonal and triclinic controls reconstruct both branches and
confirm a repeated atom has one coherent image. Neutral-water graph controls
exclude alcohol, peroxide, hydroxide, hydronium and implicit-H water.

Fifty-frame native and H5MSM inputs use eight projected leg chunks at
chunk_size=7; nonconsecutive duplicated requests evaluate each frame once.
Resident leg/join/packing budget checks reject dense per-water fan-out.
No process-RSS, large-trajectory latency or incremental-writer guarantee is
claimed. Higher-order water networks and endpoint-only scope modes would need
separately stated public contracts; they are not silent extensions of this one.

Six singleton D-H-A roles were selected instead of a water-oxygen-only pair
because the latter loses scientific branch direction, alternative hydrogens
and reproducible observed geometry. Repeated oxygen/H indices are permitted
across roles by the existing sparse relation contract. Joining integer images
belongs in the PBC owner; chemical water recognition belongs in physchem, and
the interaction module owns scientific composition and atom-scope filtering.

## Completed validation — 2026-10-01

**Contract-tested / parity-tested:** affected regression: **705 passed**, exit 0,
175.89 s. The 22 warnings are expected controlled low-RAM warnings (17) and
deprecated H5MSM 0.4 reader controls (5). This is the affected selection, not
a full repository or release-candidate certification.

```bash
python -m pytest tests/interactions tests/physchem/test_get_hbond_sites.py \
  tests/physchem/test_get_halogen_bond_sites.py \
  tests/physchem/test_get_hydrophobic_sites.py \
  tests/physchem/test_get_metal_coordination_sites.py \
  tests/physchem/test_get_water_sites.py \
  tests/scientific_truth/curated/test_attributed_interaction_methods.py \
  tests/scientific_truth/curated/test_halogen_bonds.py \
  tests/scientific_truth/curated/test_hydrophobic_interactions.py \
  tests/scientific_truth/curated/test_metal_coordination.py \
  tests/scientific_truth/curated/test_water_bridges.py \
  devtools/tests/test_validate_docstrings.py --receptor=llm
```

- All four new public docstrings: 20 deterministic doctest examples, zero failures.
- Five new notebooks executed and saved through `docs/execute_notebooks.py`:
  two chemical site tutorials, two detector tutorials and the named persistence
  recipe. Times including kernel startup: 13.4, 10.2, 10.3, 11.2 and 9.9 seconds.
  These are execution observations, not detector performance benchmarks.
- `python devtools/scripts/validate_docstrings.py`: 220 public functions pass.
- `python devtools/scripts/validate_api_stability.py`: 238 symbols classified.
- `python devtools/scripts/validate_public_api_stability.py --base HEAD`: no
  existing public signature drift against the pre-delivery checkout.
- Dependency lazy-import gate, Ruff on source and changed tests/generators,
  developer-guide lifecycle/index gate and `git diff --check` pass.
- `python devtools/scripts/validate_course.py`: 156 notebooks consistent.
  Module 38 prose is updated in all four paths; existing biological code and
  outputs are preserved and were not rerun. The retired validator under
  `docs/content/course/devtools/` was also invoked accidentally and rejected
  its obsolete template expectations; it is not the maintained release gate,
  as already recorded in the attribution pilot.
- Incremental Sphinx HTML build exits 0; the final new detector/site/recipe
  pages have no parser/reference diagnostics. Existing unrelated warnings
  remain under the established documentation-debt report; this is not a
  warning-free release documentation claim.

## Provenance

Linux 7.0.0-28-generic x86_64, glibc 2.39; Python 3.13.14, RDKit 2025.09.5.
Installed MolSysMT runtime reports `0.22.4+60.g7a8350f76.dirty`; this metadata
is not the source checkout revision. Work starts from `e842308cf` on the
interaction-attribution review branch. No shared environment packages were
installed. Oracle generation reused an isolated, unmodified ProLIF 2.2.2
installation; its exact source hashes and host versions are in each manifest.

## Resolution

Implemented the bounded experimental public contract, its reusable chemical
recognition, sparse typed persistence and documented limitations. The guard
asserts actual observed roles, scopes, geometry and stored provenance rather
than merely the presence of an exported name. Durable rules are absorbed by
[Interaction Analysis API](../../interactions_api.md). Visualization and
session implementation remain owned by MolSysViewer. Broader science and
performance certification are not implied by this delivery.
