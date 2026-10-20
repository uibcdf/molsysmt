---
summary: Preserve explicit atom stereo declarations through chemical-template handoff.
issue: uibcdf/molsysmt#390
status: resolved
opened: 2026-10-20
closed: 2026-10-20
verification: reproduced
area: [api, docs]
guard: tests/physchem/test_chemical_template_stereochemistry.py
normative:
blocked_by: []
supersedes: []
---

# Chemical-template stereo handoff

**Reported:** 2026-10-20 by DockingMT, consumer uibcdf/dockingmt#49.
**Status:** Resolved with explicit atom declaration transfer and strict downstream checks.

## What

Keep explicit supported atom stereo declarations through template application,
then let the existing strict correspondence operation check potential stereo.
The incoming BEN example lost `unspecified` during transfer and required a
separate consumer declaration. Correspondence rejection was correct.

## How

The private template reader classified `unspecified` as absent. Atom stereo reads
now retain it, alongside R/S/r/s. Comparison handles it as an explicit value:
missing source fields receive it, equal source fields are preserved, and any
different explicit source label conflicts. Unknown/missing template values do
not authorize a declaration. Unsupported labels cannot become compatible.
Bond stereo and its reference-atom rules are unchanged.

Supported composition: assess/apply an explicitly mapped prepared template;
optionally materialize H with fixed-state RDKit; request atom correspondences.
Template application still records stereogenicity as unassessed. The last
operation independently rejects unassigned potential atom or double-bond stereo.

## Why

One general transfer operation should retain the template's actual declarations.
A separate blanket setter would obscure their origin and might be mistaken for
assigning an arbitrary chiral molecule. No correspondence criterion is relaxed.

## What is measured and what is assumed

The new synthetic benzamidinium control uses `NC(=[NH2+])c1ccccc1`, nine observed
heavy atoms with removed assignments/connectivity, explicit template completion
and fixed-state H addition. It expects eighteen resulting atoms and two heavy
correspondences with distinct N roles fixed. This is a composition test, not a
new experimental-conformer or stereochemistry validation study.

The DockingMT checkout was inspected read-only. Its clean main was three commits
behind upstream when the suite inventory was refreshed; it was deliberately
preserved. Its newly reported regression is not present locally. This report
does not claim to have executed that exact consumer revision or frozen 3PTB input.

## What was refuted

- Weakening correspondence admission would hide missing chemistry and is excluded.
- Inferring labels from coordinates changes chemical preparation semantics.
- Treating `unspecified` as assigned CIP or proof of achirality is incorrect.
- Extending bond-label vocabulary is unnecessary for this atom-declaration handoff.

## Scope and exclusions

Existing form-agnostic template APIs, signatures, maps, selected/context scopes,
producer provenance, optional Ackredit attribution and copy semantics are retained.
No new classifier, dependency, scientific method, stereo perception or normalization.

## Acceptance criteria

- Explicit unspecified transfer, repeated unchanged application and provenance.
- Achiral correspondence after transfer, with unchanged source/template/coordinates.
- Missing/unknown/unsupported and conflicting declaration controls.
- Potential atom and double-bond stereo remain rejected without assignments.
- Template/H/correspondence regression, doctests and affected guide/course updates.

## Provenance

Local Linux development environment, Python 3.14.7, 2026-10-20. Tests use the existing
RDKit provider and do not introduce a new scientific algorithm or attribution source.

## Resolution and validation

**Contract-tested:** 238 template/correspondence/fixed-state H cases pass with
`python -m pytest tests/physchem/test_chemical_template*.py
 tests/topology/test_get_atom_correspondences.py
 tests/build/add_missing_hydrogens/test_fixed_state.py -n 12 --receptor=llm`.
The nine focused cases pass again after adding explicit H5MSM/history retention
assertions. Both public template doctests pass. Restoring the previous private
reader behavior in-process makes both the achiral and benzamidinium positive
controls fail (missing stereo column / strict missing-metadata rejection).

The guard checks actual transferred values, independent expected N roles and
counts, original coordinates, conflicts, strict potential-stereo rejections and
round-trip history. It cannot pass merely by suppressing an exception. Existing
FutureWarnings about H5MSM pandas downcasting are recorded without claiming
that this change repairs them. Docstring fidelity passes for all 247 public
functions. Changed API, guide, recipe, foundations and course prose are rendered
with a focused Sphinx build; no pre-existing notebook code/output is recomputed.

All fourteen fast release checks pass, as do whole-repository Ruff lint and
formatting checks and the public-signature guard (no signature drift). These
are source checks, not qualification of a replacement release artifact.
