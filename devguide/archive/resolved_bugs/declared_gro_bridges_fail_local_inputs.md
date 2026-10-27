---
summary: Declared GRO bridges fail on local inputs and default handler copies.
issue: uibcdf/molsysmt#476
status: resolved
opened: 2026-10-26
closed: 2026-10-26
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/file_gro/test_bridge_contract.py
normative:
blocked_by: []
supersedes: []
---

# Declared GRO bridges fail on local inputs and default handler copies

## What

The new GRO execution slice under uibcdf/molsysmt#181 finds four failing
registered routes on a valid single water structure. File-to-OpenMM topology
calls an unimplemented delegate. File-to-Modeller forwards a structure_indices
keyword to an incompatible delegate. Both native/MDTraj handler identity
conversions request independent copies through unimplemented extract paths.

## How

Use the existing native GRO-to-MolSys and MolSys-to-OpenMM bridges, with native
selection before provider dispatch so topology and coordinates remain aligned.
Use the existing public copy/extract adapter slots to implement independent
complete-handler copies; retain explicit rejection of unsupported subset or
file-output operations. No new conversion edge or scientific method is added.

## Why

Declared default operations must execute. Copy requests need independent resource
ownership; aliasing the input or weakening a test to request no copy would hide
the missing default path. Local source labels, coordinates, box and connectivity
must remain aligned under selection. Heavy calculations or new chemistry stores
are unnecessary; existing owning tools provide the required operations.

## Reproduction and initial evidence

The expanded profile selects 22 new routes. The initial test attempt reports
six failures and sixteen passes in 14.05 seconds. Two failures are test-authoring
errors: the resource check invoked MDTraj's unimplemented public GRO seek().
Replacing that check with actual open-handle inspection leaves four conversion
failures and eighteen passing controls. Scientific assertions are not changed
to bypass a bridge failure. No provider absence or runtime failure becomes a skip.

## Acceptance

All 22 selected routes execute directly and through public convert with fresh
sources. OpenMM outputs retain independently specified source labels, selected
atom positions, covalent bonds and triclinic boxes under nm and pm policies.
Independent native/MDTraj copies preserve caller cursor/metadata, own their
handles and can be closed without closing the source. Existing unsupported
subset modes fail explicitly without changing the source. Native GRO remains
a single-entry reader; this repair does not promise a new trajectory parser,
velocity/time availability in other providers, ligand preparation or all GRO
dialects. See the primary GROMACS GRO-format reference for nm, nm/ps and the
nine-value box order: https://manual.gromacs.org/current/reference-manual/file-formats.html#gro.

## Resolution — 2026-10-26

All 22 GRO routes execute through direct and public calls after the four
repairs. The mirrored guard checks literal output labels/coordinates, retained
water bonds and triclinic boxes under nm/pm policies. It checks all public copy,
extract and identity routes for independent mutable metadata and handle closure,
plus explicit aliasing and rejected subsets. The file-to-OpenMM bridges keep
native sorted extraction and first-entry scope; independent MDTraj copies open
at the beginning of the same backing file instead of attempting an unsupported
cursor clone. Existing optional-provider paths stay lazy.

Test-authoring follow-ups used the native class's actual import location and
stopped asking TextIOWrapper.tell() after provider iteration disables it. The
copy itself was also made independent of that opaque cursor state. These
adjustments do not remove scientific assertions or skip a failing route.

The final combined GRO/conversion-plan selection passes 437 cases with no
failures or skips in 36.15 seconds using twelve workers and Pytest Receptor;
21 intentional legacy H5MSM warnings remain. Both converter/query doctest
modules pass, the 491-notebook raw-schema guard passes and all fourteen fast
gates pass. Ruff lint/format pass. Incremental HTML compilation exits 0 with
zero errors and 21 warnings; broader documentation debt remains #144. Exact
scope/environment/hashes and commands are in
[the GRO receipt](../../devtools/data/conversion_execution_gro_20261026.json).
The current [form contract](../forms_and_conversions.md) and
[execution guide](../conversion_execution.md) own the durable rules. No
installed-artifact, full-suite, large-file benchmark, universal chemistry or
release pass is asserted. #181 retains remaining execution coverage debt.
