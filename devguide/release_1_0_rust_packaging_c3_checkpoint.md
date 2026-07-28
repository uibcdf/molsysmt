# C3 Multiplatform Rust-Wheel Checkpoint

**Date:** 2026-07-28
**Stage:** C3 — Linux, macOS, and Windows abi3 wheel CI
**Status:** `DONE`
**Implementation commits:** `30b86cdf2`, `072eb7cdc`, `f79ccb4f0`

## Delivered CI Contract

The C3 implementation adds a dedicated, non-publishing workflow:
`.github/workflows/ci-rust-wheels.yaml`.

The full manual matrix contains exactly five native targets:

| Target | GitHub runner | cibuildwheel identifier |
| --- | --- | --- |
| Linux x86_64 | `ubuntu-24.04` | `cp311-manylinux_x86_64` |
| Linux aarch64 | `ubuntu-24.04-arm` | `cp311-manylinux_aarch64` |
| macOS x86_64 | `macos-15-intel` | `cp311-macosx_x86_64` |
| macOS arm64 | `macos-15` | `cp311-macosx_arm64` |
| Windows x86_64 | `windows-2022` | `cp311-win_amd64` |

Pull requests affecting the native build run only Linux x86_64. The complete
five-target matrix runs through `workflow_dispatch`; this keeps routine
validation proportional while preserving an executable release gate.

The build contract is:

- cibuildwheel 3.4.1;
- one CPython 3.11 limited-API build per architecture;
- `cp311-abi3` wheel output rather than three interpreter-specific builds;
- `manylinux_2_28` for both Linux architectures;
- macOS deployment target 11.0;
- portable CPU baseline with no `target-cpu=native`;
- Rust 1.97.1 selected by `rust-toolchain.toml`;
- committed `Cargo.lock`;
- no publication token or upload step other than GitHub build artifacts.

## Artifact Validation

Every job:

1. builds and repairs the wheel through cibuildwheel;
2. receives cibuildwheel's default strict `abi3audit`;
3. runs `validate_rust_wheel.py`;
4. installs the wheel with `--no-deps`;
5. proves that the installation is not editable and the extension resolves
   inside the active environment;
6. loads the private extension without executing the full package initializer;
7. checks 97 Rust exports and a 2.5 minimum-image result;
8. uploads the wheel as a retained GitHub artifact.

The isolated extension load is deliberate. The supported distribution route is
Conda, and the sibling versions required for a clean full-package import are
not all available in the UIBCDF channel yet. Pretending that pip can resolve
that graph would mix the C4/C5 dependency-coordination gate into C3. C4/C5 must
repeat the test with a complete installed MolSysMT environment and execute the
public API.

## Local Evidence

The following local checks passed:

- 12 wheel-validator and workflow-contract tests;
- 80 Rust unit tests;
- Ruff on the changed Python files and the complete `molsysmt` tree;
- dependency-boundary validation;
- TOML and workflow YAML parsing;
- `git diff --check`;
- cibuildwheel expands to exactly the five identifiers listed above;
- the reusable installed-wheel validator passes against the exact C2 Linux
  wheel, finding 97 exports and the expected 2.5 minimum image.

## Exact-Commit Remote Evidence

The full matrix passed on exact commit
`f79ccb4f0bac9ac89eb5b0ffd1ddc20a432c0bda`:

- run: <https://github.com/uibcdf/molsysmt/actions/runs/30346103646>;
- conclusion: `success`;
- five of five required native jobs passed;
- every job completed build/audit, installed-extension validation, and artifact
  upload.

| Target | Runner image and version | Wheel | Wheel SHA256 |
| --- | --- | --- | --- |
| Linux x86_64 | `ubuntu-24.04` `20260720.247.2` | `molsysmt-0.20.0+161.gf79ccb4f0-cp311-abi3-manylinux_2_28_x86_64.whl` | `b18be4d637f286d75adfbe1e6da05be2f4719bd5b7eec8245caf1f468d39ffeb` |
| Linux aarch64 | `ubuntu-24.04-arm` `20260719.67.1` | `molsysmt-0.20.0+161.gf79ccb4f0-cp311-abi3-manylinux_2_28_aarch64.whl` | `02d2e538b76cbf8b99889674defce1d40e4232b2e33fef928fec5bee6eb44eda` |
| macOS x86_64 | `macos-15` `20260720.0353.1` | `molsysmt-0.20.0+161.gf79ccb4f0-cp311-abi3-macosx_11_0_x86_64.whl` | `077bdb10d0587f7b4d92d2d29a0e030b6200c176796685bf6613acf2023cc0bb` |
| macOS arm64 | `macos-15-arm64` `20260715.0234.1` | `molsysmt-0.20.0+161.gf79ccb4f0-cp311-abi3-macosx_11_0_arm64.whl` | `46d687be3eb133645a48e6f5b40fd85249642a6ac4838cd1776db4b47ee5eb48` |
| Windows x86_64 | `windows-2022` `20260720.249.2` | `molsysmt-0.20.0+161.gf79ccb4f0-cp311-abi3-win_amd64.whl` | `ebce5f4dcaf1e41f50c1eab3b0d5d234ab657caba667b5f169ae92d9f8c27b48` |

The SHA256 values above are for the downloaded wheel files, not for GitHub's
artifact ZIP wrappers.

## Failed-Run Evidence and Correction

The first accepted workflow run,
<https://github.com/uibcdf/molsysmt/actions/runs/30345646277>, passed four
targets and failed Linux aarch64 during `build_rust`. The manylinux container
had already received the pinned minimal Rust toolchain, but the repository
toolchain manifest then attempted to add Clippy and collided with an existing
`bin/cargo-clippy`. Commit `f79ccb4f0` fixes the build boundary by setting
`RUSTUP_TOOLCHAIN=1.97.1` inside the cibuildwheel Linux environment. The second
run proves the correction on both Linux architectures.

C3 is complete. C4 must now test installed wheels across Python 3.11–3.13 and
the supported NumPy range; it must not reuse a source checkout as the imported
package.

## Independent C7 Debt Found

`cargo fmt --check` currently reports formatting differences throughout the
pre-existing crate. No scientific Rust source was reformatted as part of C3.
The required normalization, Clippy run, dependency/security/license audit, and
panic/portability review remain C7 work and must be closed before Segment C can
earn its weighted release credit.
