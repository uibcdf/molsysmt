---
summary: Extend indexed water bridges to exact two-water paths.
issue: uibcdf/molsysmt#282
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api, structure, tests]
guard: tests/interactions/water_bridges/test_two_water_bridges.py
normative: devguide/interactions_api.md
blocked_by: []
supersedes: []
---

# Extend indexed water bridges to exact two-water paths

**Reported:** 2026-10-01, maintainer request following the single-water detector.
**Status:** Resolved; implementation and validation complete.

## What

Add exact `order=2` water-mediated paths without changing single-water numerical
behavior (`order=1`). The descriptive method `hbond_water_path` generalizes the
construction; the explicit `two_hbonds_one_water` selector remains supported for
order one. Each result continues to be an independent named-analysis candidate.

## How

Reuse explicit neutral-water recognition and attributed hydrogen-bond observations.
Join three simultaneous legs through two distinct water oxygens, with distinct
nonwater endpoint heavy atoms. Canonicalize reversal by endpoint index, preserving
every directed D-H-A triple. Keep nine singleton participant roles, per-leg measures,
and observed lattice images joined through both shared oxygens.

Use only observed sparse water-water edges and bounded endpoint fan-out blocks.
Extend the existing PBC image join helper to arbitrary participant counts; keep
chemistry, geometry and persistence in their established owning tools.

## Why

MDAnalysis WaterBridgeAnalysis and ProLIF WaterBridge support multi-water paths.
Two-water mediation captures connections outside the immediate hydration shell;
this is a geometric observation, not an energetic or biological-importance claim.
References: [MDAnalysis](https://docs.mdanalysis.org/stable/documentation_pages/analysis/wbridge_analysis.html),
[ProLIF source](https://prolif.readthedocs.io/en/stable/_modules/prolif/interactions/water_bridge.html).

## What is measured and what is assumed

Implemented and contract-tested by exact-order, actual-atom scope, frame coverage,
reversal, alternate-hydrogen, extraction and memory-exhaustion assertions.
Scientifically validated against eight analytic three-leg direction cases and
independently enumerated simple paths of original ProLIF HBDonor observations.
The generated reference contains 24 structures and 16 paths; 33 combined one-/two-
water reference-form cases passed in 21.77 seconds. This is reference-leg and
atom-path validation, not complete ProLIF WaterBridge pipeline equivalence.
Two documentation notebooks executed successfully (11.1 and 10.3 seconds including
kernel startup); all six public docstring examples passed. These are validation
elapsed times, not performance benchmark statistics.
Numeric memory accounting is an estimate; Python overhead and process RSS are not
fully modeled. Accepted leg and bridge outputs remain resident.

## What was refuted

An unrestricted graph walk would introduce uncontrolled combinatorial growth.
Mixed maximum-order results would need heterogeneous measure columns and make the
exact meaning of each analysis less transparent. This extension instead returns
one exact order per call; users can store both orders as separate named analyses.

## Scope and exclusions

Order one or two only, explicit indexed neutral waters, automatic leg-site profiles,
actual-atom selection scopes, existing coordinate streaming and H5MSM persistence.
No implicit hydrogen repair, energy estimates, residue aggregation, higher-order
networks or incremental result writer.

## Acceptance criteria

Independent analytic and reference-leg path truth; simultaneous-frame and reversal
identity; selection, empty coverage, nonconsecutive frames; orthogonal/triclinic
observed images and nondefault units; form parity, H5MSM named/typed round trips,
extraction/removal, bounded coordinate reading and numerical memory failures.
Update public docstrings, User Guide, Cookbook, course and developer contracts.

## Provenance

2026-10-01; Linux x86_64, Python 3.13.14, RDKit 2025.09.5, optional isolated
unmodified ProLIF 2.2.2. The fixture records source hashes, upstream revision,
versions and platform. Runtime MolSysMT metadata reports
`0.22.4+60.g7a8350f76.dirty`; this is producer metadata, not the checkout revision.
Source baseline: `2442b7cad` plus this change.

```bash
PYTHONPATH="$PROLIF_REFERENCE_DIR" python devtools/scripts/two_water_bridge_validation_systems.py devtools/data/two_water_bridge_validation_systems.json
python -m pytest --receptor=llm tests/scientific_truth/curated/test_water_bridges.py
python docs/execute_notebooks.py -q -n 3 docs/content/user/tools/interactions/get_water_bridges.ipynb docs/content/user/cookbook/saving_mediated_interactions.ipynb
```

The isolated reference installation path above is an execution setup, not a
production dependency. Neither a new Rust speedup nor an arbitrary-scale RAM/RSS
guarantee has been measured.


## Resolution

Implemented exact order one/two with the descriptive `hbond_water_path` default.
Existing `two_hbonds_one_water` calls retain their single-water meaning. Nine
roles preserve the three directed legs, including alternate hydrogens; endpoint
reversal does not duplicate paths. The general PBC helper joins arbitrary role
counts and checks repeated-atom consistency and int32 range. No dependency or
H5MSM schema change was required.

Validation on 2026-10-01:

```bash
python -m pytest --receptor=llm tests/interactions tests/physchem tests/pbc tests/form/file_h5msm tests/form/molsysmt_InteractionsDict tests/scientific_truth/curated/test_water_bridges.py tests/scientific_truth/curated/test_attributed_interaction_methods.py
```

**1,518 passed**, 264.54 seconds, exit 0. The 638 warnings consist of 615 legacy
H5MSM read warnings, 17 intentionally small numerical-budget memory-pressure
warnings and six unavailable-GPU fallback warnings. This is an affected-area
validation, not a complete release gate or a performance benchmark.

All six water-bridge doctest examples passed. Both changed notebooks executed
and retained their outputs. Ruff passed for `molsysmt` and the changed tests and
reference generator. Dependency validation, docstring fidelity (220 public
functions), API signature/stability registry (238 symbols), developer-guide and
course structure (156 notebooks) checks passed. Sphinx built with exit 0;
pre-existing course heading, toctree and API cross-reference warnings remain.
New two-water examples introduced no parser warnings. No new benchmark is claimed.

The guard checks exact directed participants and geometric values, scopes,
coverage, reversal, alternative H, nondefault units and observed PBC geometry;
it also tests public typed/named H5MSM round trips, mediator removal, coordinate
streaming and explicit memory failures. Independent scientific guards remain in
`tests/scientific_truth/curated/test_water_bridges.py`. Durable rules are absorbed
in [the interaction contract](../../interactions_api.md) and
[scalability guidance](../../SCALABILITY.md). User Guide, Cookbook and all four
advanced hydrogen-bond course narratives were updated.
