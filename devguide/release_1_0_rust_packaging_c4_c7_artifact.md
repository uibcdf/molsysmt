# MolSysMT 1.0 Rust Packaging C4–C7 Artifact

**Date:** 2026-07-28  
**Exact commit:** `c4d8e9074a571384cd114471e294b8248fb2363f`  
**GitHub Actions run:** [30394881487](https://github.com/uibcdf/molsysmt/actions/runs/30394881487)  
**Conclusion:** `success`

## Scope

This artifact closes packaging stages C4–C7 and installed-wheel validation
stage E4. It proves the supported Rust-only Python distribution boundary. It
does not claim that MolSysMT or its sibling packages have been published or
validated through the `uibcdf` Conda channel; that remains a separate delivery
track.

## Exact Matrix

Five native `cp311-abi3` wheels were built, audited, installed, and executed:

| Platform | Architecture | Wheel SHA256 |
| --- | --- | --- |
| Linux manylinux 2.28 | x86_64 | `0c33e9dcf36be9a5468f24e0c568f0f65de89c72c6e240112317ec473e6eebf2` |
| Linux manylinux 2.28 | aarch64 | `c08e5b4b4d355fc876be6c7523beb5ae52ab7784c8dd6ecba51c473e40cd6a24` |
| macOS 11+ | x86_64 | `0b4b76a1e859bd7e1716cf766ddfb8d78c6f9784765ec608bedff2cfd503ba85` |
| macOS 11+ | arm64 | `5d76071ec46604a208a89e632f260c693debd5bee947df33da95e51304e14c85` |
| Windows | x86_64 | `3cd34ec59d4e79c56e1587fa716d52a5df7987c37f4d6a41cd95b135680c0c24` |

Every wheel loaded and executed on Python 3.11, 3.12, and 3.13, for 15 green
platform/interpreter jobs. The private extension exposed the exact committed
99-entry manifest and passed its minimum-image calculation.

The declared NumPy floors also passed:

- Python 3.11 with NumPy 1.26.4;
- Python 3.12 with NumPy 1.26.4;
- Python 3.13 with NumPy 2.1.3.

The current supported range remains `numpy>=1.26,<3`.

## Installed Public Runtime

The Linux wheel was installed with controlled hard sibling sources and without
dependency resolution from a local checkout. Python 3.11, 3.12, and 3.13 each
passed the public installed-runtime smoke from outside the repository.

The smoke verifies:

- non-editable package and private-extension paths inside the environment;
- bundled scientific resources, `py.typed`, and the MolSysViewer addon entry
  point;
- H5MSM conversion and native `MolSys` form discovery;
- `get`, `select`, centers, distances, RMSD, PCA, SASA, PBC wrapping, and
  topology component discovery.

A local preflight built a fresh wheel and repeated the same validator in an
isolated Python 3.13 environment where OpenMM was confirmed absent. This
detected and then verified the correction recorded in
[Optional Form Detection Broke a Minimal Installation](archive/resolved_bugs/optional_form_detection_broke_minimal_install.md).

## Source Distribution and Package Contents

The exact source distribution is
`molsysmt-0.21.0+14.gc4d8e9074.tar.gz`, SHA256
`d85d8755af374dbe2914c1f12a288b7fe42fa2e990eab4580afde8b2f87047fb`.

The source-distribution job:

1. built and validated the sdist;
2. confirmed that the Rust crate, lockfile, toolchain declaration, package
   sources, resources, and build metadata were present;
3. built a wheel from that sdist rather than from the checkout;
4. validated and executed the installed private extension.

Wheel validation rejects unexpected top-level packages and requires the native
extension, MolSysMT package, MolSysViewer addon, typing marker, resources,
metadata, and entry point. Clean package discovery prevents tests, development
caches, and repository-only build products from leaking into artifacts.

## Rust Quality and Security

The exact commit passed:

- `cargo fmt --check`;
- Clippy with warnings denied;
- 80 Rust unit and property tests;
- `cargo-deny` dependency, advisory, license, and source checks;
- the portable CPU policy and committed Rust toolchain/lockfile contract.

The packaging campaign did not suppress the PyO3 advisories discovered in an
earlier run. The boundary was upgraded from PyO3/Rust NumPy 0.23 to 0.29,
Python thread detachment was migrated to the current API, and the crate now
declares its MIT license. The final security gate is green without advisory
ignores.

## Feedback Latency

The Linux x86_64 artifact is an independent prerequisite. In the exact run it
completed in 3 minutes 19 seconds, after which the three public smokes and
NumPy-floor checks started immediately. Linux aarch64, macOS, and Windows
continued in parallel. This prevents a shared installed-runtime failure from
waiting for the slowest portability build.

## Closure Decision

- C4 — Python and NumPy installed-wheel matrix: `DONE`;
- C5 — source-distribution contract: `DONE`;
- C6 — metadata, resources, typing, entry-point, and discovery parity: `DONE`;
- C7 — Rust quality, security, license, and portability gates: `DONE`;
- E4 — installed-wheel platform/Python matrix: `DONE`.

With C1–C7 and E1–E6 complete, Segments C and E earn their full 20% and 15%
weights. The formal remaining-plan closure therefore advances from 55% to 90%.
