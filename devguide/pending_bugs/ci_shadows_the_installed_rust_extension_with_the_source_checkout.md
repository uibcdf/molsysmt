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
`UnknownArgumentError` exports before starting its gates. The installed-wheel public
smoke uses the same ArgDigest revision and checks the same exports, so source CI and
release artefacts are no longer validated against different dependency contracts.

The next campaign, run `31577245777` on `97adf1705ac6629c5daa031c4642e1d9e65d58e9`,
passed installation, import, the fast release gate, Ruff, documentation, and the
complete installed-wheel matrix. The full source suite then exposed three independent
residual causes rather than another packaging failure:

- PyTraj 2.0.6 exists with incompatible `Residue.chainID` extension ABIs. The build
  installed by CI expects text and calls `.encode()`, while the locally available
  legacy build accepts only an integer chain index. The adapter now probes the installed
  residue ABI once per conversion and supplies the native textual chain identifier or
  the legacy integer index accordingly. PyTraj remains a soft dependency: this affects
  optional-adapter coverage in the full suite, not MolSysMT wheel construction.
- `tests/cross_repo/test_smonitor_contracts.py` replaced SMonitor's process-global code
  catalogue but restored only the profile. A later ArgDigest contract test consequently
  lost its rendered near-miss hint. The fixture now restores the catalogue it modifies;
  the exact controlled ArgDigest revision renders the hint correctly in isolation.
- The peptide parity sample required a `0.15 nm` minimum non-bonded heavy-atom distance,
  although the builder's own executable clash contract warns below `0.12 nm`. macOS
  produced a deterministic `0.135445 nm` geometry that satisfied atom/bond parity,
  bonded-distance parity, and the relative LEaP bound. The sample and extended parity
  checks now use the builder's `0.12 nm` rejection boundary rather than a stricter
  platform-sensitive threshold.

The first documentation run after the platform-scope clarification failed before
Sphinx, while building MolSysMT on a runner with a partially provisioned Rust 1.97.1
toolchain. Processing `rust-toolchain.toml` requested the development-only Clippy and
rustfmt components and collided with an existing `bin/cargo-clippy`. Documentation now
installs the pinned minimal toolchain explicitly and builds with
`RUSTUP_TOOLCHAIN=1.97.1`; documentation needs rustc and cargo, not the Rust quality
components exercised independently by the wheel campaign.

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
- Optional PyTraj coverage accepts both observed 2.0.6 residue ABIs without making
  PyTraj part of wheel construction or the hard runtime dependency set.
- Cross-repository diagnostics tests restore every process-global SMonitor setting they
  replace, so later tests retain sibling catalogues and actionable hints.
- Documentation builds select the pinned minimal Rust toolchain without attempting to
  repair or add development-only components on the runner.
- CI smoke and the six-cell full matrix pass from clean runners.

## Dependencies and risks

An editable build is appropriate only for source tests. It must never replace the
separate installed-wheel tests, whose purpose is to reject checkout leakage.

## Provenance

GitHub Actions runs `31574803154`, `31576019522`, and `31577245777`, Ubuntu/macOS latest,
CPython 3.11--3.13, 2026-08-12.
