---
summary: Alzheimer capstone preparation uses unsupported builder keywords and drops independent repairs.
issue: uibcdf/molsysmt#593
status: open
opened: 2026-11-05
closed:
severity: medium
verification: reproduced
area: [docs, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# Alzheimer capstone preparation contract

**Reported:** review of #589 on 2026-11-05.
**Status:** open; the interface correction does not qualify preparation.

## What

Steps 1–4 of Alzheimer Module 54 are not an execution-qualified preparation
workflow. Its peptide builder uses three unsupported keywords. Heavy-atom and
hydrogen repair calls also discard their returned independent molecular systems.

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
