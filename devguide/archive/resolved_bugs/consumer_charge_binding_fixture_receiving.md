---
summary: Declare the supported schema in the template-sensitive charge fixture.
issue: uibcdf/molsysmt#670
status: resolved
opened: 2026-11-09
closed: 2026-11-09
severity: medium
verification: reproduced
area: [tests, build, provenance]
guard: tests/build/test_project_atom_names.py::test_template_sensitive_charge_binding_is_not_recertified_after_rename
normative:
blocked_by: []
supersedes: []
---

PR #668 full run 42689572908 fails before its intended stale-name assertion:
the declared non-calculated forcefield fixture omits the required
`molsysmt.partial_charge_assignment@1` schema. Original Linux/Python 3.14
artifact 13710862374 has SHA-256
`75da1eff153420ea884131a22cfaaa2037840b2acdab327f11bb7d999967eb25`;
its JUnit contains one failure. The isolated case reproduces on the local
review merge with CI's exact tree `94a531a4e535c12a879b74b8f62c51352c10f674`.

The proposed correction declares the supported schema. All original assertions
remain: source binding valid before/after projection; renamed output rejected
because bound chemistry changed. The fixture explicitly does not represent a
forcefield calculation. No native parser rule, computation, tolerance, skip or
source-cleanliness requirement changes. PR #668 carries owner review and hosted
receiving; the original failed run remains failed. Related macOS provisioning
is tracked separately in #671. Consumer evidence is retained under
uibcdf/molsysviewer#315.


The complete original native log archive now confirms the same single case
in all seven cells reaching the full suite: each Linux cell has 32,731 passes,
168 skips and 40 deselections; each macOS cell has 32,730 passes, 169 skips
and 40 deselections. The eighth cell never reached tests (#671). This is not
seven green jobs. The affected module passes 36/36 after declaring the schema;
the separate 563-case panel/native/preflight selection also includes it.
See devtools/data/molsysviewer_pca_refinement_receiving_421_20261109.json for
source hashes, original failures and remaining changed-source hosted evidence.


## Owner integration received — 2026-11-09

The owner merged PR #668 as 3dfe27ab6 and independently integrated the identical
strict-schema fixture correction in 3fe645437. #670 is closed under its canonical
archived owner record. This supplemental consumer intake retains its original
36-case and seven-cell observations; it does not reopen #670 or claim that the
old failed matrix passed. The next contribution contains PCA/refinement rather
than a duplicate native fixture correction.
