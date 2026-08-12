---
summary: CI shadows the installed Rust extension with the source checkout
issue: uibcdf/molsysmt#146
status: active
opened: 2026-08-12
closed:
severity: high
verification: reproduced
area: [ci, build]
guard:
normative:
blocked_by: []
supersedes: []
---

# CI Shadows the Installed Rust Extension with the Source Checkout

**Reported:** 2026-08-12, by CI smoke run `31574803154` on candidate
`3eda3fa219ae2663760de764d11ed69b7e17f3ec`.
**Status:** Active; the contradictory installation/import contract is being corrected.

## What

The Conda environment and package installation complete, but pytest collection fails
before the smoke tests run:

```text
ModuleNotFoundError: No module named 'molsysmt._rust'
```

## How

The three source-test workflows install a regular wheel with `pip install .`, which
places `molsysmt._rust` under `site-packages`. They then prepend the repository checkout
through `PYTHONPATH`. Python consequently imports `molsysmt` from the checkout instead
of the installed wheel, but a clean checkout has no generated `_rust.abi3.so`.

The source-test contract must instead use `pip install --editable . --no-deps`, which
builds the extension for the checkout being tested, and must not inject a competing
`PYTHONPATH`. Non-editable installed-wheel behavior remains covered independently by
the Rust wheel workflow.

The first controlled-dependency attempt also demonstrated that MolSysViewer's exact
revision contains file pairs that differ only by case. Linux can build it, but Git
cannot check it out on the case-insensitive macOS runners. CI full therefore builds one
`py3-none-any` MolSysViewer wheel on Linux and supplies that exact artefact to all six
cells. This preserves the hard dependency and avoids weakening the macOS matrix.

The next exact-commit campaign exposed a second clean-runner-only mismatch. The
controlled ArgDigest revision predated its public function-contract API, while
MolSysMT's tests already imported `UnknownArgumentError`. All six full-matrix cells
therefore stopped during collection with the same `ImportError`. The controlled pin now
targets ArgDigest 0.11.0, the revision against which this MolSysMT surface was developed,
and every source-test workflow checks the required `Domain` and
`UnknownArgumentError` exports before starting its gates.

## Why

This blocks smoke, weekly and full CI on every clean runner after the Rust-only
migration. A developer machine can hide it with an ignored extension left by an earlier
editable build, so the clean-runner guard is important.

## What is measured and what is assumed

Measured in run `31574803154`: setup, Conda resolution and package installation pass;
collection imports `molsysmt/native/topology.py` from the checkout and cannot import
`molsysmt._rust`. No estimate is used.

## What was refuted

- The Rust wheel is not missing its extension: the private installed-extension checks
  pass in the dedicated wheel campaign.
- The controlled hard dependencies are not the cause: installation completed and the
  Ubuntu traceback originates at the checkout/package boundary. The macOS source
  checkout has a separate case-collision constraint handled by the portable dependency
  wheel.
- Adding another path override would preserve the ambiguity; the source test must have
  exactly one package identity.

## Scope and exclusions

This covers `ci-smoke.yaml`, `ci-full.yaml` and `ci-weekly.yaml`. It does not change the
non-editable wheel smokes or the eventual Conda publication process.

## Acceptance criteria

- All three source-test workflows install MolSysMT editably and contain no manual
  `PYTHONPATH` override.
- The full matrix installs an exact, platform-independent MolSysViewer wheel rather
  than omitting the hard dependency on macOS.
- A static workflow regression guards that contract.
- The controlled ArgDigest revision exports the function-contract API required by
  MolSysMT, and each source workflow checks it before running tests.
- CI smoke and the six-cell full matrix pass from clean runners.

## Dependencies and risks

An editable build is appropriate only for source tests. It must never replace the
separate installed-wheel tests, whose purpose is to reject checkout leakage.

## Provenance

GitHub Actions runs `31574803154` and `31576019522`, Ubuntu/macOS latest,
CPython 3.11--3.13, 2026-08-12.
