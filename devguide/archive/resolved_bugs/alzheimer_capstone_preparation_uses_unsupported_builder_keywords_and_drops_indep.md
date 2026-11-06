---
summary: Alzheimer capstone preparation uses unsupported builder keywords and drops independent repairs.
issue: uibcdf/molsysmt#593
status: resolved
opened: 2026-11-05
closed: 2026-11-06
severity: medium
verification: reproduced
area: [docs, build]
guard: tests/documentation/test_alzheimer_preparation_examples.py
normative:
blocked_by: []
supersedes: []
---

# Alzheimer capstone preparation contract

**Reported:** review of #589 on 2026-11-05.
**Status:** bounded preparation statements and scientific/ownership controls are
implemented, contract-tested and included in owner integration after #304.
The full biological route remains an explicitly
unqualified outline, as permitted by the acceptance criteria.

## What

At the reported source, Steps 1–4 of Alzheimer Module 54 are not an
execution-qualified preparation workflow. Its peptide builder uses three
unsupported keywords. Heavy-atom and hydrogen repair calls also discard their
returned independent molecular systems.

```python
msm.build.build_peptide('KLVFF', n_terminal='ACE', c_terminal='NME',
                       configuration='beta-strand')
```

On main `8e9e3d2078ef41d22f6198e1d5c23379e11f4619`, this raises native
UnknownArgumentError before constructing the peptide. The public builder
accepts molecular_system, to_form, engine, skip_digestion and from_naming_scheme.
There is no documented compatibility alias for the extra keywords.

## How

The lesson implies builder/capping/conformation behavior that its public call
cannot request. The earlier repair statements are expression statements;
public preparation implementations return the prepared system. Their results
are not retained as the target/candidate used by merge. Whether every repair is
needed for this particular downloaded structure remains unqualified.

Use the existing independent repair tools, explicit terminal-capping tools and
supported conformational geometry tools according to their own contracts.
Do not add unsupported keyword aliases or arbitrary cap/conformation behavior
solely to make the old notebook call pass. Verify spatial assembly and physical
parameterization explicitly; merge and solvation are not docking operations.

## Why

An executable final project must use its actual prepared outputs and supported
public contracts before a later geometric characterization or simulation can
be interpreted. A corrected surface-area formula does not establish this.

## What is measured and what is assumed

The builder rejection was executed without downloading the target or entering a
scientific backend. Lost repair-return references were inspected in the actual
lesson AST and native public contracts. Full network, reconstruction, cap
chemistry, assembly pose, force-field admission and relaxation have not been
qualified on the biological project.

## Scope and exclusions

Keep the 2BEG/KLVFF capstone context. #589 independently corrects the geometric
observable using bounded analytic controls and explicitly labels this upstream
route as an outline. Do not publish synthetic outputs under biological labels
or infer biological effects from successful tool calls.

## Acceptance criteria

- Preparation and conformational calls use supported public arguments.
- Every independent result is retained by later steps; source ownership remains
  explicit and is verified on bounded bundled fixtures before network execution.
- Capping, hydrogen inventory, intended pose and parameterization are declared
  and checked, including prerequisites and actual source/output atom maps.
- Full-project execution is qualified separately with reproducible environment,
  source/version and data provenance, or unqualified branches remain explicitly
  marked and excluded from claims of a ready-to-run preparation protocol.
- A regression guard executes the actual lesson statements and checks their
  scientific/ownership intent, not only matching signatures or code spelling.

## Provenance

Linux / shared Python 3.14.7, source identified above. Source inspections:
`molsysmt/build/build_peptide.py`, `add_missing_heavy_atoms.py`,
`add_missing_hydrogens.py` and the actual Alzheimer Module 54 notebook.


## Source correction and bounded receiving — 2026-11-06

The corrected target cell retains the independent heavy repair and passes that
actual output to the explicit OpenMM pH hydrogen route. Its result is retained
as the target used downstream. Native source connectivity and structure index 0
are explicit; a real heavy-template coverage report replaces the unconditional
"prepared and repaired" claim. Coverage is not whole chemical readiness.

The candidate cell calls the existing builder, then the existing terminal tool
with `N_terminal='ACE'` and `C_terminal='NME'`, retaining its result. Hydrogen
preparation precedes current-axis phi/psi quartet lookup and independent torsion
edits. The illustrative -135/+135 degree targets are declared inputs, not a
prediction of a beta sheet, bound pose, minimum or biological effect. No aliases
for invented builder arguments or new preparation algorithm are added.

Assembly now requires a supplied `candidate_pose_coordinates` length quantity
for one reviewed final-candidate pose. An explicit None placeholder stops before
solvation; it does not silently assemble an unplaced builder configuration.
The candidate is copied before the public setter applies rank-two/rank-three
coordinates to structure index 0. Merge-order maps are made after preparation,
then an explicit AMBER14/TIP3P request is bound before the existing OpenMM
solvation route. Atom edits or a different preparation path require their own
maps. Model declaration/admission and solvation do not establish a biological
pose, chemical suitability or equilibration.

The accepted disposition of the full 2BEG route remains an **explicit outline**:
no network execution, full-source repair/pose maps, full-complex parameterization,
solvation or relaxation is qualified here. The acceptance criteria allow this
when the unqualified branch is marked and excluded from ready-to-run claims.
No synthetic output is saved under a biological label. The #562 minimizer
continuation and #589 geometric definition/code are preserved exactly.

### Executed controls and limits

The new `tests/documentation/test_alzheimer_preparation_examples.py` executes
the actual cells, replacing only the remote target identifier with a declared
local fixture. Spies retain and inspect real preparation returns; no repair
result is fabricated. Removing one known H or O from bundled alanine dipeptide
produces 21 source atoms; both corrected repair flows end with 22 atoms. The
hydrogen call consumes the heavy result, and its result is the downstream target.
An independent unique group/name oracle maps all 21 controlled source atoms to
the result, preserving their elements and coordinates. That controlled oracle
is not a general identity-resolution algorithm. Input objects remain unchanged.

Actual KLVFF construction/capping/H calls produce 109 atoms in seven named
groups, five phi and five psi quartets, and measured requested targets within
2e-5 degrees. Finite coordinates are checked; rotamers, clashes, environmental H
directions and a complete chemical state remain unassessed. A finite energy
control confirms that the constructed candidate admits the declared model;
it does not validate the force field, molecular geometry or the biological complex.

Pose/assembly controls execute the actual pre-solvation statements with rank-two
and rank-three quantities under nm and pm application policies. They check
physical coordinates, independent candidate ownership, exact target/candidate
source populations and the stored model request. The missing-pose control
must stop before the solvation backend is entered. Existing #589 independent
sphere/interface oracles still run, and all five actual #562 minimization
continuations run on their bounded bundled model.

The initial ten controls fail against the old statements: discarded preparation
returns, unsupported builder arguments and absent explicit pose/model use. The
expanded module has twelve cases after separating both pose ranks. The final
combined documentation/affected selection passes **1,118 cases in 50.25 s**,
with no failures or omissions and warnings retained. The published four-provider
floor selection passes **22 overlapping cases in 8.76 s**, using ArgDigest
0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and Ackredit 0.9.0 payload routes.
Other development dependencies remain reused; the incompatible development
SMonitor pytest plugin is disabled only in that floor profile, with runtime
diagnostics active. This is not a clean installed or all-dependency-floor gate.
Both final selections use four workers. OpenMM is installed and every selected
optional-engine case executes; expected absence skips do not provide this evidence.

Ruff lint/formatting of the complete checkout and the 156-notebook course
validator pass. The course function inventory records the two reused preparation
helpers at their existing Common Core introduction. Notebook cell inventory,
IDs, outputs, execution counts and metadata are retained; empty outputs are not
replaced with synthetic results or a claim of full-notebook execution.

The [receiving receipt](../../../devtools/data/alzheimer_capstone_preparation_receiving_593_20261106.json)
retains hashes, actual execution counts, unsuccessful baseline, runtime/backend,
quality checks and precise scientific limits. The source is based on the frozen
#304 candidate and is prepared separately so it cannot move that running matrix's
input. Main integration and issue closeout remain pending in the authorized order.

## Resolution — 2026-11-06

Fixed by the source correction 5f2ecdd8ff3b8d24664cd6dc1b1cff61430f7898,
included in the maintainer integration of prepared source 8941bcfd4 after #304.
The guard `tests/documentation/test_alzheimer_preparation_examples.py` executes
the real lesson statements and rejects the original unsupported keywords,
discarded independent repairs and implicit unplaced-pose continuation. It also
checks actual outputs, retained coordinates/maps, physical units and deliberate
model prerequisites rather than checking code spelling alone.

All issue acceptance criteria are satisfied by those bounded controls and the
explicitly unqualified full-project outline. Full 2BEG preparation/pose/model
qualification was never executed here and is not claimed. The issue expressly
allows that disposition; keeping the corrected syntax/ownership defect open
until general release qualification would conflate different obligations.
The archived receipt and the unchanged #562/#589 controls retain that boundary.
