---
summary: Read PDBQT pose ensembles against a known ligand source
issue: uibcdf/molsysmt#226
status: open
opened: 2026-09-22
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Read PDBQT pose ensembles against a known ligand source

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Open; MolSysMT proposal is post-1.0.

## What

Read multi-model docking PDBQT poses and place their coordinates on a known ligand molecular graph.

## How

Parse pose boundaries and atom records, require a source ligand plus explicit atom mapping or equivalent carried metadata, and reconstruct supported structures without guessing absent bond orders or hydrogens.

## Why

Docking output loses chemical information; a bare PDBQT pose cannot reliably regenerate the original ligand graph.

## What is measured and what is assumed

**Inspected:** Inspected the initial PDBQT proposal, which excludes multi-model output; Meeko export documentation describes preserved ligand metadata and mapping.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Inferring a complete chemical graph from each output PDBQT was rejected because bond orders and omitted carbon-bound hydrogens are absent.

## Scope and exclusions

Pose ensemble parsing and reconstruction against a known source; score/rank interpretation and experiment provenance belong to DockingMT.

## Acceptance criteria

- Representative multi-model outputs reconstruct atom-aligned ligand structures and preserve available pose coordinates.
- A missing or inconsistent source map produces a clear error; no unsupported chemistry is claimed as recovered.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#214
Cross-component implementation links: uibcdf/dockingmt#8.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.
