# C3 Multiplatform Rust-Wheel Checkpoint

**Date:** 2026-07-28
**Stage:** C3 — Linux, macOS, and Windows abi3 wheel CI
**Status:** `IN PROGRESS`
**Implementation commit:** `30b86cdf2`

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

## Open Evidence

C3 is not complete until the workflow is present on GitHub and the full
five-target matrix passes on an identified commit. The resulting wheel names,
hashes, runner images, and run URL must be appended to this checkpoint before
C3 changes to `DONE`.

## Independent C7 Debt Found

`cargo fmt --check` currently reports formatting differences throughout the
pre-existing crate. No scientific Rust source was reformatted as part of C3.
The required normalization, Clippy run, dependency/security/license audit, and
panic/portability review remain C7 work and must be closed before Segment C can
earn its weighted release credit.
