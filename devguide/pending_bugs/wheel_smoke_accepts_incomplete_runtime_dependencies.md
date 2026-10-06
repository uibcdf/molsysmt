---
summary: Installed-wheel gate accepts incomplete and inconsistent runtime dependencies.
issue: uibcdf/molsysmt#344
status: partial
opened: 2026-10-06
closed:
severity: high
verification: reproduced
area: [ci, deps, packaging]
guard:
normative:
blocked_by: []
supersedes: []
---

# Installed-wheel gate accepts incomplete runtime dependencies

**Reported:** 2026-10-06 during S6 wheel qualification preparation.
**Status:** corrected in `865ff6ec6`; installed dependency gates pass; the complete
wheel workflow awaits correction of an independent Rust formatting failure.

## What

The wheel public-smoke workflow manually installs dependencies and then installs
MolSysMT with `--no-deps`. Its list omits the required `mmcif>=1.1.1` dependency.
The installed-runtime validator exercises H5MSM and geometry, but does not check
the installed distribution's required dependency metadata. A passing subset can
therefore conceal an incomplete installation.

The controlled manifest also selects ArgDigest 0.13.0 alongside PyUnitWizard
0.28.1, whose exact source and installed metadata require `argdigest>=0.14.0`.
The existing controlled gate compares providers only with MolSysMT's direct
floors, so it accepts this transitive conflict.

## How

Inspect `.github/workflows/ci-rust-wheels.yaml`,
`devtools/scripts/validate_installed_molsysmt.py`,
`devtools/scripts/validate_controlled_dependencies.py` and
`devtools/controlled_sources.txt`. The PyUnitWizard requirement is present at
source `25a4bc2468da4ef3af2a638c0bf068becf2acfb4`; the old ArgDigest source is
`9880fa7b990fd0987ff0de715b665eb9e11c11b2`. Neither an import nor satisfying
MolSysMT's own `argdigest>=0.13.0` floor validates this relationship.

## Why

Exact-candidate qualification requires a coherent installed closure. This is an
admitted stabilization defect under #334, not new scientific functionality.
It affects installed-wheel evidence and controlled-source validation; prior
successful editable execution retains its recorded development scope.

## What is measured and what is assumed

The omitted installer entry and provider metadata conflict are inspected.
The original omission does not imply that its molecular smoke calls fail; they
can pass without exercising the missing dependency. ArgDigest 0.14.0
is a published, non-prerelease release at
`0fa776af2d271065c60727c28480b20c3ce09aee` (2026-10-04); publication was
verified through GitHub's release API. Mutation guards and executed installed
artifact results are recorded below; the independent global workflow failure
remains tracked under #334.

## Scope and exclusions

Resolve required dependencies from the installed wheel metadata, check active
runtime requirements recursively with default extras, reject missing and
incompatible distributions, and select the compatible released ArgDigest pin.
Optional extras and scientific algorithms are unchanged. Installed runtime
validation does not qualify browser rendering or replace the final eight-cell
source/16-cell Conda pair gates.

## Acceptance criteria

- Actual installed-runtime validation rejects absent/old required mmcif.
- Controlled validation rejects PyUnitWizard 0.28.1 with ArgDigest 0.13.0,
  despite both satisfying MolSysMT's direct floors.
- Runtime markers exclude unrequested extras; dependency cycles terminate.
- The workflow resolves wheel-declared dependencies and checks the environment
  with pip, retaining exact controlled provider source provenance.
- Focused guards and the corrected installed-wheel workflow execute; retain
  failures, artifact identities and any still-unexecuted platforms separately.

## Provenance

Linux x86_64, Python 3.14.7, source `3f6642ecd`, 2026-10-06. Existing source
suite evidence is recorded under #237/#244/#334; it is not installed qualification.

## Correction and preflight

The new installed-runtime regression initially fails four cases: the public
validator does not reject absent/old mmcif, the controlled gate accepts the
PyUnitWizard/ArgDigest conflict, and no recursive closure checker exists.
The corrected selection passes 37 cases with twelve workers and receptor's
`llm` profile in 5.25 s, retaining one existing setuptools-rust deprecation.
The real corrected CLI rejects the old installed source set with exit 1 and
the explicit `pyunitwizard: installed argdigest 0.13.0 violates argdigest>=0.14.0`
diagnostic; the newly installed controlled set passes.

The installed validator owns a reusable dependency-closure checker. Both the
public runtime and controlled-source gates call it; it reads installed metadata,
checks required extras and active environment markers, excludes unrequested
extras and terminates distribution cycles. The public gate performs this check
before importing molecular code. The wheel workflow now resolves its declared
requirements using constraints frozen from the already installed provider
sources, runs `pip check`, and rechecks the controlled closure. The ArgDigest
pin advances to published 0.14.0 without changing MolSysMT's public floors.

The [preflight receipt](../../devtools/data/wheel_dependency_preflight_20261006.json)
retains both regression outcomes, actual provider source/version identities,
old-closure rejection and changed-file hashes. No new full or installed wheel
qualification is inferred from those focused checks. The original full shared
run remains accurate execution evidence; its transitive metadata conflict now
has this explicit correction. The subsequent complete execution is recorded below.

## Corrected source and installed execution — 2026-10-06

At clean source `865ff6ec60dde5b637bc1a99705b8ac5d12c74aa`, the complete
shared Python 3.14 suite with compatible ArgDigest 0.14.0 passes 13,313 cases,
skips two, and has no failures/errors in 404.84 s with 1,770 warnings. It uses
twelve workers and receptor's `llm` profile. The separate registered scientific
runner passes all 54 cases from 47 nodes without skips in 6.94 s; its certificate
records the same clean source. Editable Viewer/Ackredit limits remain explicit.

Wheel run [37438849560](https://github.com/uibcdf/molsysmt/actions/runs/37438849560)
uses published Viewer baseline `cf427942d0b08a1c5c60f262c6a6b33f248d6f8b`.
All four installed public smokes (Python 3.11–3.14) pass dependency resolution,
`pip check`, controlled closure validation and actual runtime checks outside
the source checkout. The 3.14 log records mmcif 1.2.0 resolved from the wheel
metadata and the package/native extension loaded from site-packages.

Four native builds, sixteen current-NumPy runtime cells, four NumPy-floor cells
and the sdist round trip also pass. The workflow's global conclusion is still
**failure**: its Rust formatting check rejects one import ordering in
`rust/src/mic.rs`. Clippy, Rust kernel tests and cargo-deny do not execute. The
local formatting-only correction passes the same Rust 1.97.1 check; its new
exact-source matrix remains pending under #334. The pull-request-only profile
is the one expected skipped job in this manual run.

The [execution receipt](../../devtools/data/wheel_execution_20261006.json)
preserves the failed global conclusion, actual per-job states, all five retained
artifact identities and independently hashed wheel/sdist bytes. Successful
dependency checks establish this defect's correction; they do not qualify
publication, the final Viewer consumer, or the source/Conda pair matrices.
