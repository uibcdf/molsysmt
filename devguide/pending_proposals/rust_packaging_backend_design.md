# C1 — Permanent crate/module and build-backend design review

**Status:** design review complete, backed by an executable spike. Awaiting acceptance.
**Segment:** C1 of [MolSysMT 1.0 Execution Plan](release_1_0_execution_plan.md); status in
[release_1_0_status.md](../release_1_0_status.md).
**Spike branch:** `packaging/rust-c1-spike` (not for merge; it is the evidence, not the change).
**Ran while:** Segment B was `BLOCKED`. C does not depend on B — both are independent
prerequisites of D — and the status ledger permits parallel packaging work provided the
branch is recorded and not merged across an unmet integration dependency. Both conditions
are met here.

## The question C1 has to answer

The execution plan states a preference and requires it be proven:

> The preferred distribution is one MolSysMT wheel containing a private extension such as
> `molsysmt._rust` […] **This preference must be confirmed by an implementation spike
> because the repository currently uses setuptools while the pilot crate uses maturin.**

Today those are two separate products: `pip` installs `molsysmt` (setuptools + versioningit),
`maturin` installs `msm_rust_kernels` as its own distribution, and
`molsysmt/_private/rust_backend.py` imports the latter by name. That is exactly the version
skew the plan wants to avoid.

Five things must survive whatever backend is chosen:

1. version derived from Git tags (`versioningit`);
2. the `molsysviewer.addons` entry point;
3. bundled `molsysmt.data` resources;
4. `py.typed`;
5. hard/soft dependency declarations.

## Decision: keep setuptools, add `setuptools-rust`. Do not migrate to maturin.

The spike built the preferred design — a single MolSysMT wheel carrying
`molsysmt/_rust.abi3.so` — with the **existing** setuptools backend, by adding
`setuptools-rust` to `[build-system] requires` and one `[[tool.setuptools-rust.ext-modules]]`
table pointing at the crate's `Cargo.toml`. No Python packaging behaviour changed.

### Measured result

```
molsysmt-0.20.0+149.gcb3341fd5.dirty-cp311-abi3-linux_x86_64.whl
```

| requirement | result |
|---|---|
| private extension inside the MolSysMT wheel | `molsysmt/_rust.abi3.so` |
| single abi3 wheel per platform | tag `cp311-abi3-linux_x86_64`, `Root-Is-Purelib: false` |
| version from Git tags | `0.20.0+149.gcb3341fd5.dirty` — versioningit untouched |
| entry points | `[molsysviewer.addons] molsysmt = molsysviewer_molsysmt` |
| `py.typed` | present |
| `molsysmt.data` | 292 files present |
| dependency declarations | unchanged |

**abi3 verified across interpreters, not assumed:** the extension was built under CPython
3.13, then loaded from a clean 3.12 virtual environment, where it exposed all 97 kernels and
returned the correct minimum-image distance (2.5 for a 3.5 nm separation in a 6 nm box). One
wheel per platform, not one per Python version.

### Why not maturin

Maturin supports mixed Python/Rust layouts, so the extension itself is not the problem.
`versioningit` is: maturin derives the version from `Cargo.toml` or a static `[project]
version`, and replacing a Git-tag-derived version with a hand-maintained one is a regression
in release hygiene that buys nothing here. Migrating would also mean re-expressing
package-data, `py.typed` and entry-point handling in a second tool's semantics, for a
capability setuptools-rust already provides. The plan's fallback design (a required,
version-locked private kernel distribution) is not needed.

## Two findings that would have cost time later

1. **The abi3 wheel *tag* is not set by the extension.** With `py-limited-api = "auto"` (and
   even `"cp311"`) on the ext-module, the build produced a correct abi3 `.so` but still
   tagged the wheel `cp313-cp313` — i.e. it would have required one wheel per Python version
   while looking correct. setuptools-rust resolves `"auto"` against
   `bdist_wheel.py_limited_api`, so the tag must be set on the *command*:

   ```toml
   [tool.distutils.bdist_wheel]
   py-limited-api = "cp311"
   ```

   Without this line the C3 wheel matrix silently triples.

2. **A stale `.so` from a previous build survives in `build/` and ships.** The second spike
   wheel contained both `_rust.abi3.so` and a leftover `_rust.cpython-313-...so`. CI must
   build from a clean tree or remove `build/` explicitly.

## Known blocker for C4, discovered here

A genuinely clean-environment install of the wheel **cannot be done today**:

```
ERROR: No matching distribution found for pyunitwizard>=0.22.0
```

The pinned sibling versions (`pyunitwizard>=0.22.0`, and by extension `smonitor>=0.11.6`,
`argdigest>=0.9.3`, `depdigest>=0.10.0`) are local development versions that are not
published. C4 ("test each artifact in a clean environment rather than the development
worktree") therefore depends on either publishing those releases or having CI install the
siblings from source. This is a release-coordination dependency, not a packaging defect, and
it should be recorded against C4 rather than discovered during it. The spike worked around it
with `--no-deps` plus a direct extension load, which is sufficient to prove the *packaging*
question but not the *installation* question.

## What this does not decide, deliberately

- **C2, the crate relocation, is deliberately not done.** Moving the crate out of
  `experiments/` changes the wheel build path and the hashes recorded in
  `release_1_0_rust_campaign_checkpoint.md`, and Segment B4 still needs "a new green
  exact-commit run". Relocating mid-campaign would invalidate the campaign's
  reproducibility. C2 should land immediately after B4 closes its exact-commit run.
- **The module rename is part of C2, not C1.** The preferred design requires
  `#[pymodule] fn _rust` and `[lib] name = "_rust"`, and `rust_backend.py`,
  `devtools/scripts/check_rust_hot_paths.py`, `tests/rust/test_hot_path_lint.py`,
  `experiments/rust_kernels/PACKAGING.md` and the `tests/rust/` imports all still say
  `msm_rust_kernels`. The spike made those edits to prove the design; they belong to C2.
- **CPU instruction baseline (C11) is already settled** with evidence: baseline,
  `x86-64-v2` and `x86-64-v3` are equal within noise on every hot kernel, so release wheels
  stay portable-baseline. See `../rust_kernel_optimization_guide.md` section 6.

## Acceptance criteria

- `[build-system] requires` gains `setuptools-rust`; `build-backend` stays
  `setuptools.build_meta`.
- One `[[tool.setuptools-rust.ext-modules]]` targets `molsysmt._rust`.
- `[tool.distutils.bdist_wheel] py-limited-api = "cp311"` is present.
- A built wheel is tagged `cp311-abi3` and contains exactly one `_rust` extension,
  `py.typed`, the `molsysmt.data` tree, the entry point, and a Git-derived version.
- The extension loads and computes correctly on a Python version other than the one that
  built it.

All of these were satisfied by the spike on Linux x86_64. The remaining platforms are C3.
