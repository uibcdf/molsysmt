---
summary: Course contributor guide names an obsolete validator entrypoint.
issue: uibcdf/molsysmt#637
status: partial
opened: 2026-11-07
closed:
severity: low
verification: reproduced
area: [docs, course, validation]
guard: devtools/tests/test_validate_course.py::test_legacy_course_entrypoint_matches_the_maintained_checker
normative:
blocked_by: []
supersedes: []
---

# Maintained course validation entrypoint

## What

The course contributor guide names a legacy checker with obsolete editorial
requirements, while release/source validation uses the maintained root checker.
Its `--help` invocation runs validation instead of showing help. A correct current
course must not be rewritten to satisfy that superseded set of headings.

## How

The incoming #637 diagnosis is reproduced by five actual CLI guards, all failing
before correction. The legacy command returns a different verdict/output, and
both entrypoints fail proper help and unknown-option controls. Existing release
validation uses `devtools/scripts/validate_course.py`, not the legacy profile.
Historical records of legacy failures remain dated evidence and are not rewritten.

## Why

Contributors need one maintained course contract. A misleading entrypoint can
drive unnecessary content changes or make an old checker look like a failed
current gate. Help and rejected options must not execute an unintended checker.

## Local correction and acceptance

The guide now names the canonical command. The legacy file is a thin forwarder
to that implementation, not a copied second policy. The canonical script has
standard help/unknown-option handling; its importable `main()` and ordinary
no-argument validation keep their existing contract. No notebook is changed to
satisfy legacy boilerplate.

All seven course/entrypoint/navigation tests pass without omissions. They execute
both real entrypoints from another working directory, require identical maintained
verdict/output, check help without validation, reject unknown flags, and retain
the existing canonical curriculum/navigation controls. Ruff passes after import
formatting. Source delivery and issue closeout remain pending; no publication or
scientific qualification follows from this developer-tool correction.

The portable [combined receiving receipt](../../../devtools/data/axis_angle_and_transform_receiving_602_633_634_637_20261107.json) retains native exits, original failed attempts, source fingerprints and the separately incomplete candidate/host gates. All fourteen final fast source gates pass.
