# C2 Rust Packaging Artifact

**Date:** 2026-07-28
**Stage:** C2 — production crate relocation and private extension integration
**Status:** `DONE`
**Exact commit:** `17be9ea50ca1dd874c5e658e5b1a3727300acb07`

## Purpose

This artifact records the executable evidence that closes C2. It proves that
the former Rust pilot is production source inside the MolSysMT repository and
that the accepted C1 design builds an integrated private extension from the
exact committed source.

It does not close C3-C7. In particular, it is not multiplatform wheel CI, the
supported Python/NumPy installed matrix, the final Conda recipe, or the
Rust-only cut.

## Delivered Architecture

- the production crate lives under `rust/`, outside the Python module tree;
- Setuptools remains the build backend and uses `setuptools-rust`;
- the extension target and PyO3 module are both `_rust`;
- the built module is private: `molsysmt._rust`;
- the wheel uses the `cp311-abi3` contract;
- the separate `msm_rust_kernels` distribution and its Maturin configuration
  are removed;
- pilot benchmarks live under `benchmarks/rust/`;
- obsolete pilot build and fallback examples are removed or archived;
- the temporary coexistence seam imports the integrated extension and catches
  only `ImportError`;
- an automated wheel validator rejects duplicate native extensions, legacy
  package entries, bytecode/cache contamination, a non-abi3 tag, missing
  resources, and missing MolSysViewer entry points.

## Source and Native Verification

Commands run from the repository:

```bash
cargo test --manifest-path rust/Cargo.toml --no-default-features
python -m pytest --receptor=llm --molsysmt-kernel=rust \
  tests/_private/test_forced_kernel_pytest_option.py \
  tests/rust \
  devtools/tests/test_validate_rust_wheel.py
python devtools/scripts/check_rust_hot_paths.py
python devtools/scripts/audit_numba_oracle_map.py
python devtools/scripts/audit_rust_numba_divergences.py --require-closed
python devtools/scripts/audit_numba_surface.py
```

Results:

- 80 Rust unit tests passed;
- 270 Python tests passed and 3 documented upstream minimum-image cases were
  skipped;
- 17 Rust hot-path files passed the lint;
- all 108 CPU oracle entries remain classified;
- all 14 parity modules and 8 deliberate divergences remain closed;
- the Numba ratchet reports no new kernels or direct coupling;
- the old experimental Rust surface is zero files.

Ruff passed on every changed Python source, test, benchmark, and validation
tool. `git diff --check` also passed before the technical commit.

## Exact-Commit Wheel

A local clone was created from the committed repository rather than from the
dirty development tree:

```bash
git clone --local --no-hardlinks . /tmp/molsysmt-c2-exact
git -C /tmp/molsysmt-c2-exact rev-parse HEAD
python -m pip wheel /tmp/molsysmt-c2-exact \
  --no-deps --no-build-isolation \
  --wheel-dir /tmp/molsysmt-c2-exact-wheelhouse
```

The clone resolved to:

```text
17be9ea50ca1dd874c5e658e5b1a3727300acb07
```

Produced artifact:

```text
molsysmt-0.20.0+156.g17be9ea50-cp311-abi3-linux_x86_64.whl
sha256=a7da5d72804e0df12bbeb7b32c52e55cd34633ae9f0bc3ee34bcf15e4a7ecca5
```

`devtools/scripts/validate_rust_wheel.py` passed and established:

- exactly one `molsysmt/_rust.*` platform extension;
- `Root-Is-Purelib: false`;
- a `cp311-abi3` wheel tag;
- no `msm_rust_kernels` entry;
- no `.pyc` or `__pycache__` entry;
- `molsysmt/py.typed` and the bundled demo manifest;
- the `molsysviewer.addons` entry point.

## Installed-Wheel Smoke

The exact wheel was installed with `--no-deps` in a temporary Python 3.13
virtual environment and imported from `/tmp`, outside the repository. Both
`molsysmt` and `molsysmt._rust` resolved below that environment's
`site-packages`; the installation was not editable.

The extension exposed 97 callable/public entries and returned a minimum-image
distance of 2.5 for the vector `[7.5, 0.0, 0.0]` in a 10 nm orthogonal box.

The first draft of the smoke probe requested a non-exported singular helper
name and raised `AttributeError`. Inspection showed that packaging and module
loading were already correct; the probe was corrected to the actual exported
`wrap_to_mic_vector_single_structure` contract before C2 was accepted.

## Exit Decision

C2 is complete. C3 is now active and must turn the locally proven contract
into clean platform CI for Linux, macOS, and Windows, including the required
architectures. Segment C earns no weighted release credit until its complete
C1-C7 exit gate passes.
