---
summary: Implement cation-pi observations with reusable charge and plane tools
issue: uibcdf/molsysmt#270
status: resolved
opened: 2026-10-01
closed: 2026-10-01
verification: measured
area: [api, structure, tests, docs, performance]
guard: tests/scientific_truth/curated/test_cation_pi_interactions.py::test_prolif_original_observations_survive_forms
normative:
blocked_by: []
supersedes: []
---

# Implementing attributed cation-pi methods with reusable tools

**Reported:** 2026-10-01, during the accepted interaction-family sequence.
**Status:** Resolved. The attributed default and separately identified proposal
are implemented; broader scientific comparison remains open under uibcdf/molsysmt#271.

## What

Add `interactions.cation_pi.get_cation_pi_interactions` with ProLIF 2.2.2 as the
attributed default. Expose the custom centroid_angle_offset proposal separately.
Return sparse Interactions/InteractionsDict with source axes, whole participants,
evaluated empty structures, unit-bearing measurements, images and producer versions.

## How

ProLIF's pinned source is commit `19f1800218387c49536eb9d3e8cd3044fdb337ee`:
[recognition and detector](https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/interactions/interactions.py),
[geometry](https://github.com/chemosim-lab/ProLIF/blob/19f1800218387c49536eb9d3e8cd3044fdb337ee/prolif/utils.py),
and [original paper](https://doi.org/10.1186/s13321-021-00548-6).
Its defaults are 0.45 nm and an inclusive acute angle interval [0,30] degrees.
Reproduce the cation SMARTS (including amidine/guanidine resonance and bonded-opposite
charge exclusions), 5/6-member aromatic SMARTS, arithmetic ring centroid and cross
product of centroid-to-first/second matched atom vectors. Preserve SMARTS membership
order in the result, so geometric references survive serialization/remapping.
Do not add planarity, offset or covalent-link filters to this method. A matched
neutral resonance atom can have formal charge zero; record its actual stored charge.

The general `topology.get_substructure_matches` tool owns batch SMARTS matching,
selected-state chemical conversion, source-index identity, limits and dependency
availability. It requires declared charges/aromatic flags and does not let RDKit
sanitization silently change them. No structural series is copied for recognition.
Coordinate delivery is shared by pi-pi/cation-pi in `_private.execution`;
centroids and point/plane geometry belong in `structure`, whole-image checks in `pbc`.
RDKit remains optional. No production ProLIF dependency or new compiled kernel.

MolSysMT extends the original per-molecule detection with single-source atom scopes,
requested frames, sparse output, projected block delivery and optional MIC. It does
not reproduce ProLIF ligand/residue preprocessing, neighborhood pruning or fingerprint
aggregation. Undefined geometric rows produce no angular candidates rather than
reproducing the original DirectionVector exception; this defensive adaptation is
explicit. Roles are cation then ring; the observed image shifts the ring using row
box vectors. Split periodic participants fail without implicit reconstruction.

The custom method and comparison are tracked separately in uibcdf/molsysmt#271.
Its participant centroid, least-squares plane, offset/planarity filters and direct
covalent exclusions must not be described as ProLIF or a published energy method.

## Why

The maintainer explicitly prefers attributable known methods before exploring new
science. Clients need common sparse analysis/persistence semantics across families.
[Gallivan and Dougherty](https://pmc.ncbi.nlm.nih.gov/articles/PMC22230/) use an energetic
criterion (CAPTURE); their method is not reproduced by a geometric detector. Our
observations remain geometric evidence, not energetic favorability.

## Reference inspection and exclusions

- Mol* local commit `4807179589f43c20f38d689e4acbc3fc8590df14`, charged.ts:
  distance 0.6 nm and offset 0.2 nm; three-atom triangle normal and different cation
  feature assignment/refinement. It is a distinct future comparison candidate.
- PLIP documentation/source: distance/offset plus tertiary-amine special handling,
  OpenBabel/residue-based charged groups and aromatic recognition. Reproducing only
  the generic distance filter would not reproduce PLIP; it is not shipped here.
- Local RDKit, MDTraj and MDAnalysis searches found no cation-pi detector in the
  inspected Python/C++ sources. RDKit supplies SMARTS and chemistry; trajectories,
  MIC and ordinary geometry are support capabilities rather than detector methods.
- No AmberTools checkout was present at the searched path. No negative claim about
  its complete capabilities is made.

## What is measured and what is assumed

Original ProLIF 2.2.2 is downloaded and run in a temporary isolated path, not installed
into the MolSysMT environment. Its generated committed oracle covers aromatic 5/6
rings, fused rings, guanidinium resonance, bonded-opposite-charge exclusions, warped
rings, distance/angle rejection and multiple structures. Runtime tests need only
RDKit and the fixed oracle. A discovered native hydrogen-loss regression is fixed
under uibcdf/molsysmt#272 before claiming cross-form parity.
Estimate: coordinate/geometry blocks reserve one quarter of the configured numerical
RAM budget; candidate search one eighth; sparse accumulation/packing one half.
These are not process-RSS limits. Measurements are recorded in the
[operational benchmark guide](../../benchmarking/cation_pi.md), with raw artifacts
and source hashes. The coordinate/result/chemistry boundaries are stated explicitly.

## What was refuted

A generic centroid/angle/offset rule is not automatically a reproduction of a named
method. Least-squares and original centroid-edge normals differ for warped rings.
Formal-charge clusters are not ProLIF singleton/resonance matches. Reusing the same
participants to compare all methods silently changes scientific definitions.
A smaller output or faster run does not establish better scientific discrimination.

## Acceptance criteria

1. Execute the original pinned detector and preserve its independent numerical oracle.
2. Compare occurrence memberships and distance/angle values across RDKit/native/H5MSM.
3. Test scope orientations, units, MIC/image reconstruction, empty coverage, budgets,
   named/standalone round trips and guarded coordinate-only file execution.
4. Document API, Foundations, Toolbox, Cookbook and all applicable course paths.
5. Record reproducible performance/serialization scope and limits without accuracy claims.

## Scope

Only ProLIF CationPi plus explicitly named experimental proposal. No energy scoring,
force-field fallback, implicit protonation, cross-family refinement, internal image
reconstruction, residue preprocessing, incremental writer or publication claim.
The complete sparse output remains resident; no automatic named attachment.

## Resolution — 2026-10-01

**Implemented, contract-tested and parity-tested.** ProLIF 2.2.2 is the default
known definition; its recognition/normal/defaults are pinned and attributed.
The custom proposal is selectable and requires four explicit thresholds.
Original SMARTS attribution and Apache license are preserved in the distribution.
The general SMARTS tool, projected execution, centroid/plane geometry and periodic
validation are reusable. Bracket-declared hydrogen persistence is fixed separately
in uibcdf/molsysmt#272. No new mandatory dependency or detector-specific Rust code.

The unmodified original detector generated eleven cases. Seven controlled chemical/
geometric cases and default/broader-window cases for both checksum-fixed proteins
are compared across RDKit, native and H5MSM forms (33 oracle comparisons).
Default protein windows yield zero observations; broader explicitly recorded windows
provide 92/10 observations for geometry reproduction, not recommended physical cuts.
The focused final checkpoint passed **329 tests in 53.17 s**, with expected legacy-file
and deliberately small-budget warnings. Scope/PBC/unit, sparse-output, named/standalone
persistence and pi-pi regression tests are included. Both new function doctests passed
(14 examples total). Three new tutorials/recipe and the updated attribute catalog
executed successfully. All applicable course-path chapters and API inventory are updated.

**Benchmarked.** On the regular 10,000-atom/1,000-structure control, ProLIF-definition
native eager median is 2.709 s and custom eager median 1.091 s; 146,600 occurrences.
Frame/atom queries and compressed typed H5MSM persistence are measured separately.
The 100,000-atom/100-structure ProLIF control also succeeds (73,320 occurrences),
using one timed call per worker, explicitly not a timing distribution. All recorded
implementation hashes match the final source. These results do not establish a
scientifically better rule or a speed advantage over the original ProLIF package.

Ruff, dependency delivery/contract, form adapters, API classification, docstring and
course-structure gates pass. HTML builds successfully with existing unrelated
reference/navigation warnings; new cation-pi/SMARTS pages have no remaining warnings.
The contract remains experimental. Comparison and physical/reference tasks stay open
in uibcdf/molsysmt#271; no publication conclusion is claimed.
