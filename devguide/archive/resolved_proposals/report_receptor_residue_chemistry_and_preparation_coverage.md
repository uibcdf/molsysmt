---
summary: Report receptor residue chemistry and preparation coverage
issue: uibcdf/molsysmt#218
status: resolved
opened: 2026-09-22
closed: 2026-10-03
verification: inspected
area: [build, diagnostics]
guard: tests/build/test_get_residue_chemical_coverage.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# Report receptor residue chemistry and preparation coverage

**Reported:** 2026-09-22, from the MolSysMT–DockingMT Vina preparation and conversion review.
**Status:** Resolved. The experimental read-only report is implemented and
contract-tested. Repair and environmental protonation remain separate operations.

## What

Expose which receptor residues have been assessed against a chemical template and what is missing or inconsistent.

## How

Report template match, missing or unexpected heavy atoms and hydrogens, bond and protonation coverage, and an explicit unassessed status for unsupported residues. A parent-residue alias used for sequence normalization is not evidence that the modified residue has the parent's atom inventory.

## Why

Existing native heavy-atom and protonation paths process known amino-acid templates and can leave other residues unevaluated without a returned coverage report.

## What is measured and what is assumed

**Inspected:** Inspected molsysmt/build/get_missing_heavy_atoms.py and molsysmt/build/reconcile_protonation.py. Broad nonstandard-residue repair has not been validated.
**Assumed:** The proposed contract is useful for the stated consumer; quantitative impact and complete chemical coverage need representative validation.

## What was refuted

Treating absence from a missing-atom list as proof of completeness was rejected because unsupported residues can be skipped.

## Scope and exclusions

Assessment and diagnostics first; repair algorithms for specific nonstandard residues and environment-dependent pKa remain separate.

## Acceptance criteria

- Every selected residue reports assessed, incomplete, or unassessed with a reason and supported template identity.
- Tests distinguish complete standard residues, incomplete residues, and unsupported nonstandard residues.
- The MSE fixture is assessed against selenium chemistry or marked unassessed; it is never reported as requiring MET sulfur. The same rule applies to modifications with additional atoms, such as SEP.

## Dependencies and risks

Related tracked work: uibcdf/molsysmt#177, uibcdf/molsysmt#227,
uibcdf/molsysmt#228, uibcdf/molsysmt#249.
Cross-component implementation links: uibcdf/dockingmt#4.
New functionality requires tests of scientific semantics and documentation appropriate to its public surface.

## Preparation work ordering — 2026-10-03

The maintainer requested chemical preparation alongside real SDF/PDBQT
validation. Follow [the maintained sequence](../../roadmap.md) and the consumer
profile review in uibcdf/dockingmt#33. Related template and fixed-state H
capabilities are owned by uibcdf/molsysmt#298 and uibcdf/molsysmt#300.
Prioritization does not establish implementation, scientific coverage or a new
blanket 1.0 gate. Keep this issue's acceptance criteria and general-tool owner
distinct from format parsing and DockingMT protocol decisions.

## Implementation contract — 2026-10-03

Expose `build.get_residue_chemical_coverage` with group selection, one resolved
state/frame and a detached versioned report. Reuse the stored-field audit behind
`physchem.get_chemical_readiness`, exact curated templates and the existing public
amino-acid database/heavy-atom expectation tools. No new optional provider or
attribution boundary is introduced.

Every selected group gets assessed/incomplete/unassessed status, reasons, source
indices and exact template identity. Unsupported groups, including cofactors,
remain explicitly unassessed. MSE/SEP/TPO/MLY use their own heavy templates and
elements; sequence parent aliases never establish chemical coverage. Atom names
must map uniquely. Report missing/unexpected heavy atoms and element conflicts.
Terminal OXT expectation is outside this inventory comparison when not observed;
neither group order nor an absent peptide bond proves a biological terminus.

Compare stored intra-group covalent relationships against supported template
graphs without adding edges or claiming inter-group completeness. Retain edge
evidence. Curated modified templates provide reference bond orders; the legacy
amino-acid variant database does not. Distinguish absent stored edges, untyped
edges, unknown order and explicit conflicts.

Retain candidate hydrogen inventories by exact database variant rather than
choosing a variant from a missing-H count. Differing naming, terminal or chemical
variants remain unassessed, with their individual missing/unexpected H names
available for inspection. Heavy-only modified templates cannot establish H
coverage. A unique inventory comparison still does not validate environmental
protonation. Protonation, terminal context, repair/placement, inter-group chemistry
and force-field readiness remain explicit unassessed dimensions.

## Resolution — 2026-10-03

Accepted and completed as a bounded, form-agnostic public assessment, not a
chemical-preparation certificate. The public contract and its exclusions are in
[forms and conversions](../../forms_and_conversions.md). The User Guide
Foundations, Toolbox, Cookbook, API reference, stability registry and course
Module 12 now describe the operation. Course code cells and existing executed
outputs are unchanged; its new narrative links to tested examples.

**Contract-tested:** Independent ALA, MSE, SEP, TPO and MLY fixture inventories and
stored graphs protect exact modified identity, element/order conflicts, absent
versus untyped edges, missing endpoints, duplicate names, ambiguous H variants,
whole-group selections, source indices and read-only/detached results. Real
bundled 3C8H MSE and the curated 2,702-atom Vina 1IEP receptor fixture exercise
source forms. Tests include unresolved/multiple chemical states, H5MSM bounded
frame access, invalid arguments, absent hierarchy and optional-provider blocking.
The reused coordinate audit tests non-default PyUnitWizard length/time settings.
The guard is the complete addressable module
`tests/build/test_get_residue_chemical_coverage.py`; its scientific assertions
reject parent-residue substitution and invented completeness for unsupported
chemistry, rather than just checking report field names.

Reproducible focused command from the repository root, with ArgDigest 0.13.0
imported from an isolated source snapshot at
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`:

```bash
python -m pytest --receptor=llm \
  tests/build/test_get_residue_chemical_coverage.py \
  tests/build/get_missing_heavy_atoms \
  tests/build/add_missing_heavy_atoms/test_modified_residues.py \
  tests/physchem/test_get_chemical_readiness.py tests/basic/select \
  tests/basic/get/test_explicit_chemical_state.py \
  --doctest-modules molsysmt/build/get_residue_chemical_coverage.py \
  molsysmt/physchem/get_chemical_readiness.py
```

The expanded cohort passed **172 tests in 64.24 s**, with three expected legacy
H5MSM warnings. After the final internal auditor extraction retained its original
signature, the two assessment modules and their doctests passed **43 tests in
31.38 s**. Environment: Linux, Python 3.13.14, NumPy 2.4.6, pandas 2.3.3, h5py
3.16.0, local source PyUnitWizard/SMonitor/DepDigest. This is focused source
validation, not an installed-wheel, complete dependency-floor or release gate.
Python 3.14 routine-route adoption remains owned by uibcdf/molsysmt#237; this
checkpoint supplies no 3.14 evidence. The concurrently published policy 1.5.4
update was incorporated without changing its declared migration scope.
The local installed ArgDigest remains below the public floor; the isolated
released snapshot was used for pytest. The existing skip-flag compatibility
validation remains tied to uibcdf/argdigest#17.

Ruff, docstring fidelity, dependency declarations/lazy-import audit, maintained
course structure and public API stability passed. Both new Markdown pages'
Python examples executed successfully. Sphinx HTML built successfully with
existing warning debt tracked separately; no warning mentions either new page.
The older course-local validator is not the maintained release validator and
still rejects existing course structure; it was not used as passing evidence.

**Inspected performance boundary:** Source domains are loaded once per operation;
reference resources are cached by residue name/observed inventory; bond-field
lookups and internal/boundary partitions are built once. Per-group connectivity
uses its partition without a full selected-bond scan. No throughput, large-system
memory or scientific preparation-performance claim has been established.

A supported PDB hierarchy-selection defect discovered during this work is fixed
and independently guarded in uibcdf/molsysmt#303. Remaining actual chemical
completion belongs to uibcdf/molsysmt#298 and uibcdf/molsysmt#300, followed by
named charge/type assignments. No new optional-provider or attribution boundary
was added, and no SMonitor limitation requiring a provider issue was found.
