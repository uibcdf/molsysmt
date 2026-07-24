# Packaging evaluation (items 2 & 3)

## Where compilation happens (the key point)

- **Binary wheels (the target):** compile ONCE in CI per platform, publish binaries
  to PyPI. `pip install` downloads a prebuilt `.so` → **no compile at install, no
  compile at import, no warmup**. Importing a compiled extension is just loading a
  shared library.
- **Compile-at-install** happens only as an **sdist fallback** when no matching wheel
  exists — and it needs the Rust toolchain on the user's machine (to avoid).

Contrast with Numba: install fast, import fast, but the **first call JITs** (the
warmup we want to remove).

## Item 2 — abi3 single-wheel: VALIDATED here

Cargo feature `abi3-py311` was enabled and a real wheel built:

```
msm_rust_kernels-0.1.0-cp311-abi3-manylinux_2_34_x86_64.whl
```

- **One `cp311-abi3` wheel serves Python 3.11 / 3.12 / 3.13** (and later) — the CI
  matrix is `(os × arch)`, not `(os × arch × python)`. Verified by installing this
  cp311-abi3 wheel and running it on **Python 3.13** with exact parity.
- `rust-numpy` works fine under abi3 (its NumPy C-API access is at runtime).
- `manylinux_2_34` tag → portable Linux binary.

Net: the "single wheel across 3.11–3.13, no user-side compile" claim is real, not
aspirational.

## Item 2 — CI cost

See `ci/build-wheels.skeleton.yml` (a skeleton, not wired to run). With abi3 the
build matrix is **5 legs** (linux x86_64/aarch64, macOS x86_64/aarch64, windows x64),
one wheel each, via `PyO3/maturin-action`. aarch64 legs are cross-compiled. Ongoing
cost: a pinned Rust toolchain, reacting to `pyo3`/`rust-numpy` releases, and running
the parity suite on every platform before publishing. Moderate, standard, bounded.

## Item 3 — opt-in fallback seam

See `fallback_seam.py` (illustrative, NOT added to molsysmt). Pattern:

```python
try:
    import msm_rust_kernels as _rust
    HAVE_RUST = True
except Exception:
    HAVE_RUST = False
```

molsysmt would dispatch to Rust when the wheel is present and fall back to the Numba
kernel otherwise, behind an explicit `backend='auto'|'rust'|'numba'` flag. The Numba
path stays as the oracle; nothing breaks if the wheel is absent. This makes adoption
gradual and reversible — exactly the coexistence model in the MECS-Arrow proposal.

## Bottom line

Both blockers to "the warmup win reaches the user" are cleared in principle: a single
abi3 wheel per platform is buildable and runs across 3.11–3.13, and the opt-in seam is
trivial and safe. The remaining real cost is standing up and maintaining the multi-OS
wheel CI + the second toolchain — a decision, not a technical unknown.
