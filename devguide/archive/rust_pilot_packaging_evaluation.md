# Rust Pilot Packaging Evaluation

> **Historical pilot note — superseded 2026-07-26**
>
> The abi3 measurements and five-platform wheel estimate remain useful
> evidence. The optional Numba fallback described below is no longer the target:
> MolSysMT 1.0 will ship a required Rust implementation and remove Numba. The
> current packaging and installed-wheel gates are defined in
> `devguide/pending_proposals/release_1_0_execution_plan.md`.

## Where compilation happens (the key point)

- **Binary packages (the target):** compile once in CI per platform and publish the
  resulting Conda packages in the UIBCDF channel. The pilot used a wheel to prove
  the binary-extension contract; installing a prebuilt `.so` requires **no compile
  at install, no compile at import, and no warmup**. Importing a compiled extension
  only loads a shared library.
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

The pilot included an unwired `ci/build-wheels.skeleton.yml`. It estimated a
**five-leg** binary matrix (Linux x86_64/aarch64, macOS x86_64/aarch64, and
Windows x64), with aarch64 cross-compiled. That skeleton was removed when the
crate became production code: it used Maturin, whereas C1 selected the existing
Setuptools backend with `setuptools-rust`, and the release target is Conda. The
portable-platform estimate remains useful; the obsolete workflow is not an
implementation guide.

## Item 3 — historical opt-in fallback seam

The pilot also contained an illustrative `fallback_seam.py` that imported a
separate package:

```python
try:
    import msm_rust_kernels as _rust
    HAVE_RUST = True
except Exception:
    HAVE_RUST = False
```

That prototype was removed during C2. Production uses the private integrated
`molsysmt._rust` extension and the temporary coexistence seam in
`molsysmt/_private/rust_backend.py`. The old snippet is retained only as historical
evidence of the pilot decision; it must not be copied into current code.

## Bottom line

Both blockers to "the warmup win reaches the user" are cleared in principle: a single
abi3 wheel per platform is buildable and runs across 3.11–3.13, and the opt-in seam is
trivial and safe. The remaining real cost is standing up and maintaining the multi-OS
wheel CI + the second toolchain — a decision, not a technical unknown.
