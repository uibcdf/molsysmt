---
summary: mmCIF conversion silently drops earlier generators with the same assembly ID.
issue: uibcdf/molsysmt#563
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [form, convert, bioassembly]
guard: tests/form/mmcif_PdbxContainers_DataContainer/test_bioassembly_generators.py
normative:
blocked_by: []
supersedes: []
---

# Repeated assembly generator rows overwrite earlier operations

**Reported:** 2026-11-05 UTC, during a public-coordinate capability review for
Sabueso's structural journey (uibcdf/sabueso#173).
**Status:** Owner-reviewed correction integrated locally on main; the final
source checkpoint publishes this resolution and its receiving evidence.

## What

Converting a DataContainer with two generators `['1', 'A', '1']` and
`['1', 'A', '2']` retains only the second row. With identity operator 1 and a
10 angstrom x translation for operator 2, bundled public 1BRS chain A contains
864 atoms; building assembly 1 returns 864 atoms instead of 1,728. Reversing
the rows changes which copy survives. Only the in-memory assembly categories
are synthetic; the bundled coordinate file is unchanged.

```bash
python -m pytest --receptor=llm -m 'not network and not heavy' \
  tests/form/mmcif_PdbxContainers_DataContainer/test_bioassembly_generators.py
```

## How

`molsysmt/form/mmcif_PdbxContainers_DataContainer/to_molsysmt_MolSys.py`
assigns a new dictionary to the same assembly ID at the end of each row.
The correction appends operations to that parent's existing record. It keeps
common ordered chain sets flat and expands distinct scopes per operation,
without union, deduplication or reassignment to another assembly. Existing
operation expansion/composition and unit-bearing translation vectors are reused.

Empty or unsupported factors previously produced empty/partial operations.
The correction refuses these with the existing catalog `FormatError`, rather
than making accumulation conceal an uninterpreted generator.

## Why

Silent coordinate loss can affect assembly-dependent contacts and downstream
interpretation. A successful conversion must not imply that only the last
source generator exists. Different-chain storage must also not imply that the
current builder supports constructing heterogeneous per-operation scopes.

## What is measured and what is assumed

The defect is reproduced on refreshed base
`5ccad1d8a2537b24e52474bd95103cc94700cba1` with Python 3.14 in the shared editable
workspace. Seven initial regression cases fail on that base: source-order copy
counts, interleaved parents/products, distinct chain scopes and unsupported/empty
factor refusal. The corrected seven-case run passes; subsequent final receiving
adds empty-expression and reversed-range cases.

Analytical coordinates independently check the two transformed copies under
a non-default angstrom standard-unit policy. H5MSM receiving checks retained
heterogeneous chain scopes and explicit builder refusal. No public installed
artifact, full platform matrix or general importer qualification is claimed.
Final selected receiving passes 467 cases and deselects one live-data case,
with four expected `LegacyH5MSMWarning` messages for supported 0.4 inputs.
The earlier broad run passed 467 and failed one unmarked live `3U71` download.
That independent test-classification defect is tracked in uibcdf/molsysmt#565;
adding its network marker retains the original online assertions. Hosted status
belongs in the PR evidence and is not implied by local receiving.

## What was refuted

The builder is not the cause of the common-chain two-operation loss: supplying
both operations explicitly already yields the expected analytical coordinates.
Heterogeneous construction remains an existing documented limitation, not a
capability added by this fix. Labels and equal coordinates are not identity or
physical-uniqueness proofs.

## Scope and exclusions

Preserve supported generator operations across repeated parent rows, keeping
single-row/common-chain shapes and separate assembly IDs. No new parser grammar,
construction mode, schema, Rust kernel, scientific inference, dependency floor
or consumer workaround is introduced. Invalid references still fail conversion.

## Acceptance criteria

All cases in the guard module pass, including exact operation order, units,
analytical coordinates, H5MSM persistence and controlled refusal. Neighboring
CIF/BinaryCIF, builder and persistence gates pass. User tutorial, cookbook,
course and maintained form contract describe the same boundary. Owner review and integration are complete; final publication and issue closure
use the source checkpoint linked by the closing comment.

## Provenance

Original public coordinate input: bundled `Barnase-Barstar/1brs.bcif.gz`, SHA-256
`aed172bd303f4de89f9458494985064d9ff878279726b2b01b46bb24a4791e82`.
Synthetic operator/generator categories are declared in the regression module.
All receiving is offline, with socket connections forbidden. The shared Python
3.14 workspace uses the PR checkout editable; no separate environment is created.
The Sabueso consumer record retains exact commands, resource observations and
original failing controls under uibcdf/sabueso#173.

## Resolution — 2026-11-05

Received PR #566 at exact head `3635c90acc9ca2453479f5dcdf1b361f84c5bf4f`.
Its full required run
[41952069798](https://github.com/uibcdf/molsysmt/actions/runs/41952069798)
is successful at that exact head: all eight Linux/macOS × Python 3.11–3.14
test lanes, the controlled-Viewer build and the aggregate job pass. Public
GH Run Receptor 1.3.0 returns exit 0 for the inspected terminal run. This is
PR-source qualification, not an installed artifact or the later combined main.

A true merge onto main 532d0362 retains the contributor commit in history:
`fcf76b7556add446c769d35d20b139ca471161f9`. All nine assembly regressions
reproduce on the receiving baseline, then pass on the merge, together with
2,020 selected reader, assembly, PBC, translation/contact and H5MSM cases
(exit 0, four workers). The same nine controls also pass with the published
support-library floors during combined occupancy receiving. No assembly-test
assertion or synthetic geometry oracle is weakened.

The companion #565 marker correction preserves the live 3U71 test. Explicit
offline collection of its original node reports zero selected and one
deselected (expected pytest exit 5), without downloading coordinates. The
original online assertions remain available in the successful PR full suite.
No installed/release evidence or heterogeneous assembly construction is claimed.

The wwPDB [generator category](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Categories/pdbx_struct_assembly_gen.html)
defines repeated source rows, and its
[operation expression](https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Items/_pdbx_struct_assembly_gen.oper_expression.html)
defines right-to-left product application. These format rules support the
analytical controls; they are not a new interaction-detection method. Existing
ArgDigest, native transformations, PyUnitWizard and catalog FormatError are
reused, with no dependency-floor or attribution-registry addition.
