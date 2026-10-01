---
summary: Compare attributed cation-pi detectors with the MolSysMT geometric proposal
issue: uibcdf/molsysmt#271
status: partial
opened: 2026-10-01
closed:
verification: measured
area: [api, structure, tests, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Comparing attributed cation-pi detectors with the MolSysMT proposal

**Reported:** 2026-10-01, explicit maintainer request after distinguishing a custom
geometric rule from a reproduction of known methods.
**Status:** Partial baseline established; scientific classification comparison remains open. No claim of superior accuracy.

## What

Compare known definitions (initially ProLIF 2.2.2, subsequently Mol*/PLIP/CAPTURE where
faithful reproduction is feasible) with MolSysMT's centroid_angle_offset proposal.
A potential future scientific article requires independent evidence beyond correct
implementation or smaller/faster outputs.

## How

The proposed custom method uses whole positive formal-charge centers, whole-center
arithmetic means, declared aromatic minimum-cycle-basis rings and unweighted
least-squares planes. Require four explicit cuts: positive centroid distance, acute
normal angle strictly below 90 degrees, lateral offset and maximum atom-plane deviation.
Inclusive cutoffs allow one float64 ULP; angle roundoff remains below pi/2. Exclude
shared atoms/direct covalent links; retain other intramolecular candidates. Its rule
version is `cation_centroid_angle_offset@1`; it has no published method attribution.
Use ordinary sparse Interactions with the exact method, units, evidence and versions.

The cation centroid includes guanidinium's carbon and nitrogens and is not a charge-
weighted electrical center or the ionic detector's minimum-distance reference subset.
Participants are reconstructible from the stored membership without an extra store.

Separate comparison layers: (a) chemistry/feature membership; (b) geometry on fixed
shared participants; (c) complete detector observations; (d) scientific classification;
(e) execution, RAM, queries and serialization. Report disagreements instead of
normalizing away different original atom/ring definitions. Include resonance forms,
protonation, fused/heteroaromatics, metals, distorted rings, periodic images, ligands
and protein contexts. Use explicit source indices, never molecule/structure IDs.

## Why

The maintainer requests a powerful implementation supported by evidence. A future
paper is conditional on a measurable scientific or engineering contribution. Existing
method defaults and heuristics are baseline definitions, not ground truth.

## What is measured and what is assumed

Initial known-method oracle and contract checks belong to uibcdf/molsysmt#270.
Both methods are implemented, with four required explicit cutoffs for the custom
proposal. The actual original ProLIF detector produced the fixed oracle. Separate
10,000-atom/1,000-structure controls measure full calculation, numeric storage,
queries and H5MSM; see [benchmark scope and raw records](../benchmarking/cation_pi.md).
No timing of the original ProLIF package is included.
Small analytical disagreements can demonstrate distinct behavior but cannot determine
which rule is scientifically better. Performance controls describe their fixture and
source representation; they do not establish accuracy or energetic favorability.
No experimental/quantum reference benchmark or superiority result is available yet.

## Initial controlled disagreements

- Guanidinium: ProLIF singleton SMARTS recognize three reference atoms, including
  neutral resonance nitrogens; the proposal represents one whole positive center
  containing carbon and nitrogens. Counts and centers differ before any cutoff.
- Warped rings: original centroid-edge and fitted least-squares normals differ;
  ProLIF applies no planarity or offset filter, while the proposal requires both.
- Bonded opposite-charge atoms: ProLIF excludes them in chemical recognition;
  custom recognition follows its separately documented formal-charge-center rules.
- Intramolecular/shared/directly bonded participants: the proposal adds exclusions
  that are not part of the reproduced original core CationPi method.

The contract tests preserve these differences instead of hiding them behind one
participant assignment. These are behavioral differences, not evidence of error
rates or physical improvement. Mol*/PLIP and energetic reference tasks remain
unimplemented comparison candidates.

## What was refuted

- A faster detector is not necessarily a more physically accurate detector.
- Agreement with a software baseline proves reproduction, not universal physical truth.
- A geometric contact must not be labeled an attractive energy without evidence.
- A common cutoff across different charge centers/ring definitions is not a fair
  scientific comparison unless those changes are reported separately.

## Acceptance criteria

1. Attributed implementations and controlled disagreements with documented cause.
2. Prespecified physical/reference tasks and held-out systems with data provenance.
3. Error/coverage measures, uncertainty and conditions for declaring an improvement.
4. Reproducible speed/RAM/disk/query comparisons, including realistic trajectories.
5. A documented decision: retain, refine or withdraw the proposal; an article is
   considered only after the scientific or engineering contribution is established.

## Scope and exclusions

No publication promise, automatic superiority conclusion or pre-1.0 release gate.
This remains an open comparison issue after the first attributed detector ships.
