---
summary: Sequence-superposition course examples confuse aligned systems with RMSD values
issue: uibcdf/molsysmt#455
status: resolved
opened: 2026-10-24
closed: 2026-10-24
severity: low
verification: reproduced
area: [docs]
guard: tests/documentation/test_sequence_alignment_examples.py
normative:
blocked_by: []
supersedes: []
---

# Sequence-superposition course examples confuse aligned systems with RMSD values

**Reported:** 2026-10-24 during lifecycle review for uibcdf/molsysmt#452 and
uibcdf/molsysmt#453. **Status:** resolved; corrected examples and executable guards are qualified.

## What

The four Path Module 34 examples print a returned molecular system as though
it were an optimized RMSD. Biophysics also supplies a second system in the
positional selection slot. Enzyme uses an invalid vector keyword and an invalid
range expression, with no in-place edit. Alzheimer leaves the composite file
input unmaterialized before editing and selects protein only although HP35 is
classified as a peptide. The common module measured all atoms after fitting only
protein components, so unselected water contributes a nonzero residual.

## How

Keep the aligned molecular system and separately call get_rmsd with matching
anchor populations and reference structure. Use explicit reference keywords,
unit-bearing translation vectors and an actual in-place flag where intended.
For HP35, obtain the topology domain explicitly from the single-pose H5MSM and
combine it with the coordinate trajectory, then select a bounded native ensemble
and the protein-or-peptide population. Use nonconsecutive original structures
and the input's original reference structure. Correct CA RMSDs and before/after
plots replace unconfigured live views. Retain each path's biological system.

## Why

The examples teach the wrong return contract or fail before reaching a usable
comparison. An object representation printed after alignment does not measure
RMSD or establish a successful scientific result.

## What is measured and what is assumed

Baseline code cells from 99cb83107 were executed before their original view
calls: Enzyme raises UnknownArgumentError for vector; Alzheimer requests
structure 100 from a 20-structure source; Biophysics supplies a molecular system
as its atom selection; Antiviral prints a MolSys as its RMSD. Remote PDB
identifiers were replaced with a bundled protein for this baseline contract
reproduction. Updated offline guards
execute the four actual code-cell workflows, substituting only remote PDB inputs
with a bundled protein; the HP35 example uses its actual bundled sources.
Those five guards, including the related Cookbook, pass in 13.65 seconds with
pytest-receptor and 12 workers. Actual full notebooks on the intended remote
biological systems are being executed separately. No substitution is treated
as proof of biological model equivalence.

## What was refuted

Renaming the returned object RMSD, measuring all atoms after moving only selected
components, ignoring failed translations, or silently substituting a different
reference would conceal the errors. The corrected Enzyme example explicitly
models a local coordinate displacement, not a chemical mutation. Rigid-pose
examples check zero residual; a genuine conformational difference need not
have zero optimized RMSD.

## Scope and exclusions

Four Module 34 notebooks, their protection contracts, and the affected common
module are updated with the alignment tutorial and recipe. General provider
contracts remain in their native tools. Existing Sphinx/course presentation
debt stays under uibcdf/molsysmt#144; no new viewer runtime is generated.

## Acceptance criteria

Execute all corrected notebooks, verify actual returned native systems and
unit-bearing before/after RMSDs, preserve source/reference ownership, and retain
an addressable guard in tests/documentation/test_sequence_alignment_examples.py.
Qualify public tutorial and recipe alongside the native #452/#453 correction.

## Provenance

2026-10-24, Linux/Python 3.14.7, existing development environment and 12 workers.
Intended sources remain HP35, PDB 6EQE, PDB 6LU7 and PDB 1K4C. This is source
course qualification, not an installed package or novel biological prediction.

## Real-source execution and scope correction

All six affected notebooks execute, including the common module and the public
alignment tutorial. The real 6LU7 example initially exposed a further population
mistake: its N3 ligand is a separate peptide with CA atoms. Translating only the
protein and then fitting all CA atoms is not one rigid displacement; the
residual was 0.12526916178964764 nm. Qualify anchors by protein membership on
both axes, keeping peptide ligands and ions out of the intended target-protein
comparison. Other protein examples use the same explicit scope.

The final offline guard supplies an extra CA-containing peptide in its 6LU7
substitution. Reintroducing the broad CA population fails its zero-residual
assertion, instead of passing merely because a substitute contains no ligand.
The recipe and four course guards pass **5 tests in 14.09 seconds**. Real
Enzyme/Antiviral/Biophysics executions pass in 14.3/12.2/13.4 seconds; the initial
successful tutorial, common and Alzheimer executions are retained. Comparisons
use actual unit-bearing RMSD values and source-preservation assertions. Existing
Sphinx warning debt is retained; no false warning-free claim is made.

## Final local verification — 2026-10-24

The broad structural/PBC/sequence/argument matrix passes **1,950 tests in
51.66 seconds** with pytest-receptor and 12 workers. Network-marked tests are
excluded explicitly; the existing unmarked RCSB-neighbor case was allowed its
required network access. No failures or skips occurred. Legacy H5MSM,
intentional GPU-unavailability and deliberately tiny-memory-budget warnings are
retained; GPU fallback checks do not establish GPU execution.

The final focused native, argument, recipe/course and real-view fitting matrix
passes **633 tests in 28.87 seconds**, after adding malformed ragged-selection
rejection. The one public alignment doctest passes. Six actual notebooks execute
successfully, and all 14 fast repository gates, signature stability and full Ruff
lint/format checks pass. Sphinx HTML builds with the accepted existing warning
population under uibcdf/molsysmt#144. No public signature, dependency floor,
installed artifact, release or optional GPU qualification is changed or claimed.
Publication and applicable CI are verified separately after the source commit.
