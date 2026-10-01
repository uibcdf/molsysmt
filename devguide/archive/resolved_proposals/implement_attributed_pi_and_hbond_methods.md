---
summary: Implement attributed pi and hydrogen-bond methods with reusable tools.
issue: uibcdf/molsysmt#274
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [interactions, physchem, structure, pbc]
guard: tests/scientific_truth/curated/test_attributed_interaction_methods.py
normative:
blocked_by: []
supersedes: []
---

# Implementing attributable interaction methods

**Reported:** 2026-10-01, maintainer request to learn from other scientific tools.
**Status:** Resolved. Supported attributed cores and general tools are implemented and validated; physical method comparison remains open under uibcdf/molsysmt#271.

## What

Add explicit reference methods for cation–pi, pi–pi and hydrogen bonds without
silently combining one package's chemistry with another package's geometry.
Keep established Buch/Luzard–Chandler defaults and the separately named
MolSysMT centroid/angle/offset proposal. Scientific comparison remains tracked
in [the comparison record](../../pending_proposals/compare_attributed_cation_pi_detectors_with_the_molsysmt_geometric_proposal.md)
and uibcdf/molsysmt#271.

## How

- Mol*: reproduce charged.ts geometry as `molstar_geometry`, explicitly using
  MolSysMT's declared formal-charge centers/aromatic basis rather than claiming
  parity with Mol*'s valence-model feature discovery or contact refinement.
- ProLIF: extend the already attributed core to FaceToFace/EdgeToFace and
  HBDonor/HBAcceptor, using original chemical SMARTS and ordered ring normals.
- MDTraj: reproduce per-structure Baker–Hubbard and Wernet–Nilsson observations;
  expose pi-stacking geometry with its original ordered-normal construction,
  default angular intervals and plane-intersection test. No first-frame pruning.
- CPPTRAJ (the engine behind pytraj): reproduce individual donor/H/acceptor
  observations, including the actual inclusive source comparisons, not just
  the strict inequalities printed by its documentation.
- MDAnalysis: expose its geometric criterion with explicit supplied sites;
  do not replace its partial-charge chemical guesses with formal charges.
- Put reusable site recognition in physchem and plane/triplet operations in
  structure/pbc; use existing bounded spatial kernels and execution tools.

## Why

Named scientific definitions need pinned sources and original-code comparisons.
AmberClassic FIRST and pytraj's CPPTRAJ are different detectors. A method name
must state whether it describes the full chemical core or only a geometric
profile applied to independently declared participants.

## What is measured and what is assumed

Pinned source inspection and executed original-detector core comparison:

| Reference | Revision | Relevant source |
|---|---|---|
| Mol* | 4807179589f43c20f38d689e4acbc3fc8590df14 | src/mol-model-props/computed/interactions/charged.ts and hydrogen-bonds.ts |
| ProLIF 2.2.2 | 19f1800218387c49536eb9d3e8cd3044fdb337ee | prolif/interactions/interactions.py, base.py, utils.py |
| MDTraj | 80f7cf2ddb43dd0d32905e490464f2d8765329df | mdtraj/geometry/pi_stacking.py and hbond.py |
| MDAnalysis | 9531c6e157d0211bfcc086374e3da429d1e3c8d1 | package/MDAnalysis/analysis/hydrogenbonds/hbond_analysis.py |
| pytraj | 96083c77ee6f355a6cbffd66518401e832a8f8c2 | pytraj/analysis/hbond_analysis.py |
| CPPTRAJ 6.24.0 | 0793fd579c5bb41377462d70df0b249a48bc9eb7 | src/Action_HydrogenBond.cpp, Version.h |
| AmberClassic | 656e5c6fcb05149e6aa936e1d69d1426b37ea3c7 | src/xtalutil/forFIRSThbond.F90, src/antechamber/ring.c |
| RDKit | a24ed4f06a4f73ef419e9b6347999d0abfbacabd | chemical graph, SMARTS and aromaticity support |

Installed original runtimes inspected: MDTraj 1.11.1, MDAnalysis 2.10.0,
pytraj 2.0.6 (import succeeds), CPPTRAJ V6.24.0, RDKit 2025.9.5.
Runtime version and checkout revision are separate facts; reference artifacts
must identify the source actually executed.

## What was refuted

- No pi-stacking implementation in MDTraj: refuted by geometry/pi_stacking.py.
- AmberClassic lacks useful hydrogen-bond code: refuted by FIRST's geometric
  and Mayo-derived energetic criteria. The prior AmberTools path search did
  not inspect this checkout.
- CPPTRAJ uses strict documented distance/angle inequalities: its actual
  solute code accepts distance <= cutoff and angle >= cutoff.
- All methods use a least-squares ring plane: Mol* uses the first three
  member atoms; ProLIF/MDTraj use the first two centroid-relative vectors.
- RDKit aromaticity and Amber's AM1-BCC aromatic typing are interchangeable:
  antechamber/ring.c explicitly has parameterization-specific five-membered
  ring rules; these are not a general interaction definition.

## Scope and exclusions

Sparse geometric evidence is not an energetic classification. Mol* hydrogen
bonds additionally use valence-derived ideal donor/acceptor geometry, sulfur
rules and explicit/implicit hydrogen alternatives. FIRST additionally requires
its atom types, hybridization, acceptor-base geometry and energetic network
policy (see [Rader et al., PNAS 2002](https://doi.org/10.1073/pnas.062492699)).
Do not expose a placeholder or label a generic distance/angle filter as either
full detector. This implementation uses the supported cores listed above;
these more extensive chemical/energetic pipelines remain comparison inputs.

No optional reference package becomes a hard production dependency. No source
from LGPL/GPL reference packages is copied into the production implementation.
Reproduced ProLIF SMARTS retain Apache-2.0 attribution. No new H5MSM schema is
required: metadata, measurements and observations use the existing codec.

## Acceptance criteria

- Original-code reference artifacts and meaningful tests for supported methods.
- Explicit chemistry/geometry attribution, producer versions, units, scopes,
  empty evaluated frames and coherent observed periodic images.
- Form parity, bounded execution, selection semantics and H5MSM round trip.
- API docstrings, User Guide, Cookbook and course updates, locally executed.
- Existing detector contracts and focused regressions remain passing.

## Dependencies and risks

Plane intersection is role-dependent in the inspected ProLIF/MDTraj core.
Canonical source memberships define ring_a/ring_b; the role ordering and its
effect must be documented and tested instead of silently symmetrizing it.
Independently imaged distances and angles can be inconsistent in small boxes;
a stored occurrence must not claim a single coherent image that was not used.

## Executed reference evidence — 2026-10-01

The developer-only [oracle generator](../../../devtools/scripts/attributed_interaction_oracles.py)
executes unmodified ProLIF 2.2.2 detectors, the pinned MDTraj and MDAnalysis Python
implementations using their installed native backends, CPPTRAJ V6.24.0 as a binary,
and unchanged Mol* geometric tester excerpts with its original Vec3 implementation.
Mol* feature discovery and refinement are intentionally outside this oracle.
The [fixed artifact](../../../devtools/data/attributed_interaction_oracles.json) records
source hashes, runtime versions, precision and the CPPTRAJ binary hash.

Reproduction from the repository root requires developer reference checkouts,
ProLIF 2.2.2 and its dependencies, MDTraj, MDAnalysis, RDKit, CPPTRAJ and esbuild:

```bash
python devtools/scripts/attributed_interaction_oracles.py \
    --references /path/to/reference/checkouts --esbuild /path/to/esbuild
```

The artifact contains one pi-pi case with 93 frames, one cation-pi case with 16
frames, and five hydrogen-bond chemical contexts with 45 frames each: water,
amide, thiol, fluoride and aromatic NH. This covers positive and negative decisions,
warped rings, angular/distance/offset differences and direction-dependent intersection.
The water references contain respectively 18/10/4/2/18 occurrences for
Baker–Hubbard/Wernet–Nilsson/CPPTRAJ/MDAnalysis/ProLIF. A guard asserts actual positive
and negative reference decisions; empty output cannot silently certify a broken oracle.
The scientific tests compare exact participants and per-frame decisions across RDKit,
native MolSys and projected H5MSM; ProLIF pi distances also compare numerically.
These are **independent core comparisons on controlled geometries**, not a classification
benchmark against experimental energies or a claim of superiority of any definition.

### Refuted implementation and fixture paths

- The initial CPPTRAJ MOL2 writer used atom names `a0`, etc. CPPTRAJ determines element
  identity from those names and found no F/O/N sites. Real element-prefixed names fixed
  this false-empty oracle. Separate case directories prevent stale series contamination.
- Some original runtimes store float32 trajectory coordinates. Exact perpendicular or
  offset-limit geometry acquired different floating roundoff from float64 MolSysMT.
  External grids now avoid those ambiguous boundaries (89 degrees instead of 90 and
  0.19 nm instead of exactly 0.20 nm). Separate analytical tests require exact 90-degree
  endpoint acceptance and strict/inclusive DHA endpoint behavior. No external result
  was rewritten to match MolSysMT and no extra tolerance was added to reference rules.
- New tests originally treated `Interactions.query()` as a dictionary and assigned
  through MolSys's read-only interactions mapping. They now use the established view
  codec and explicit validated domain setter. The public contracts were preserved.
- The RDKit input exposed an integer chemical-state delegation rejected by charge-center
  argument validation. A native read-only chemical view sets the chosen reference state
  before calling the general charge-center tool, without copying coordinates or bypassing
  public validation.
- `pytraj` 2.0.6 imports but aborts while loading the small valid MOL2 fixture in this
  environment (double-free diagnostics). CPPTRAJ processes that fixture successfully.
  The binary provides the original detector oracle; there is no claimed pytraj runtime
  validation, and pytraj is not a production dependency.

### Implementation ownership

Chemical graph/state preparation is shared in topology. ProLIF SMARTS/constants moved
from the cation detector to physchem with the existing Apache-2.0 attribution retained.
The supported general tool `physchem.get_hbond_sites` owns reusable site recognition.
Plane construction/intersection and triplet geometry live in structure; coherent image
construction lives in pbc. Feature-specific thresholds and scope orchestration remain
in interactions. Existing Rust spatial/MIC/plane primitives are reused; no new compiler
or dependency is introduced without a measured need.

Baker–Hubbard and Wernet–Nilsson references include their original criterion papers,
separate from the MDTraj software paper. Method-reference revisions are not producer
versions: MolSysMT is the producer of these adapted observations. H5MSM preserves both.

### Validation checkpoint

- Focused regression: **463 passed**, including existing cation/pi/hbond behavior,
  original-core/form comparisons, general SMARTS, aromatic chemistry and plane fitting.
- Additional periodic-profile/optional-NaN round trips and ring-context regression:
  **28 passed**.
- Docstrings: **27 examples passed** across both new tools and the two extended detectors.
- All five changed/new tool and recipe notebooks executed successfully. Course modules
  receive conceptual updates and links to those executed examples; their pre-existing
  network-dependent cells are preserved and not claimed as newly validated.
- Dependency-laziness, Ruff, docstring fidelity, public-signature and course guards pass.
- The final HTML build succeeds after removing incompatible course cell IDs and fixing
  custom titles in the new tool directives. The new hydrogen-bond/site pages have no
  remaining warnings; pre-existing navigation, course-heading and other directive
  warnings remain. A successful build is not claimed to be warning-free.

**Bounded memory:** a 1,000-frame test verifies 143 projected chunks at size seven,
nonconsecutive file indices and failure rather than full H5MSM materialization.
Native coordinates and final sparse output remain resident. Numerical estimates do not
cap process RSS; the deliberately tiny test budget emits memory-pressure warnings.
See [the scalability contract](../../SCALABILITY.md).

Physical comparison and a possible article remain under uibcdf/molsysmt#271.
Completion of this implementation does not close that scientific study.

## Resolution — 2026-10-01

**Implemented, contract-tested and parity-tested**, with independent comparisons of
supported scientific reference cores. The final metadata/periodic/typed-output
checkpoint passed **86 tests in 23.49 s**; an additional strict boolean/index-overflow
boundary guard passed **3 tests**. These checkpoints overlap the 463-test regression
and are not summed as separate coverage. Five executed notebooks, two conceptual
course updates, Foundations, API registry and scalability docs complete the public
lifecycle. No H5MSM format or mandatory dependency change is required.

The guard module compares all new supported reference cores across RDKit/native/file
forms and explicitly rejects an all-empty oracle. Its analytical perpendicular
endpoint guard protects the documented float64 adaptation rather than copying
external float32 rounding. Public-contract tests separately cover scopes, units,
periodic image reconstruction, strict/inclusive endpoints, frames without observations,
named H5MSM round trips and bounded file execution.

The scientific comparison and energetic/feature-discovery extensions excluded here
remain tracked in uibcdf/molsysmt#271. Completing this issue does not claim universal
chemical accuracy, full Mol*/MDAnalysis/Amber FIRST pipeline parity, or a scientific
improvement over the original methods.
