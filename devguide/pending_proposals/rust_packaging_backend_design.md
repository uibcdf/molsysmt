# C1 — Permanent crate/module and build-backend design review

**Status:** **ACCEPTED AND INTEGRATED**. C1 closed on 2026-07-26; C2 closed on
2026-07-28 at `17be9ea50`. C3-C7 remain open.

> **Accepted decision.** MolSysMT keeps `setuptools` as its build backend, adds
> `setuptools-rust`, and distributes a single private `molsysmt._rust` extension inside the
> official Conda package. Maturin is not adopted — not because it is incapable, but because
> it offers no advantage that would justify disturbing `versioningit`, the bundled
> resources, the entry points, the typing marker, and the rest of the Python packaging.
> A separate `msm_rust_kernels` distribution is therefore not needed, which removes any
> possibility of version skew between the Python code and the Rust kernels.
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

Before C2 these were two separate products: `pip` installed `molsysmt`
(Setuptools + versioningit), Maturin installed `msm_rust_kernels`, and the
coexistence seam imported the latter by name. C2 removed that version-skew
surface by integrating the private extension.

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

**Development evidence**, per the ledger's update procedure: the wheel was built from a
dirty working tree, as its own version string records. It settles the *design* question. It
is not exact-commit release evidence, which belongs to C3/C4.

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

## Sibling availability: a channel requirement for C4/C5, not a blocker

The spike could not install the wheel into a genuinely clean environment:

```
ERROR: No matching distribution found for pyunitwizard>=0.22.0
```

**This was first reported here as a blocker. That framing was wrong and is corrected:** the
official distribution channel is the project's own Conda channel, not PyPI, so an unmet PyPI
resolution does not block release. The correct contract is:

- Conda resolves `pyunitwizard`, `smonitor`, `argdigest` and `depdigest`;
- the Conda recipes declare their minimum compatible versions;
- the Rust-bearing wheel may be installed during the build with `pip install --no-deps`;
- real dependency resolution is Conda's responsibility;
- **clean-environment tests must be run against environments created from the declared
  channels**, never assuming every dependency exists on PyPI.

This would only become a blocker if MolSysMT promised a standalone public
`pip install molsysmt` as a supported route. While that is not an official route, it is
enough to document that the supported installation is via Conda.

The spike's own workaround (`--no-deps` plus a direct extension load) proves the *packaging*
question and deliberately says nothing about the *installation* question, which is C4's.

## Contracts these findings become (accepted, binding on C3)

The two findings above are not development anecdotes; they are gate requirements.

### Clean build is mandatory, and enforced by inspection

A stale `.so` can survive inside `build/` and ship in a later wheel. Manually cleaning a
developer machine is not a control. Therefore:

- CI builds from a clean checkout;
- `build/`, `dist/` and Rust artefacts are never reused across builds;
- every produced wheel is inspected automatically;
- the gate requires **exactly one** `molsysmt/_rust.*` extension;
- a wheel containing both an abi3 extension and a CPython-specific one is **rejected**.

Isolation must be part of the workflow, not a habit.

### abi3 is stated, not yet proven across the matrix

The 3.13 → 3.12 load proves abi3 genuinely works, but the `cp311-abi3` tag expresses an
*intention* of compatibility that C3/C4 must demonstrate on every target still unverified:

- Python 3.11;
- Linux aarch64;
- macOS x86_64;
- macOS arm64;
- Windows x86_64;
- the supported NumPy range.

### Portable CPU baseline stays

`x86-64-v2` and `x86-64-v3` showed no improvement sufficient to justify less compatible
wheels. Release builds must not carry developer-machine-dependent flags such as
`-C target-cpu=native`. Evidence: `../rust_kernel_optimization_guide.md` section 6.

## C2 Delivery Update

C2 implemented the accepted design after B4 closed:

- the final crate path is `rust/Cargo.toml`;
- the PyO3 module and library name are `_rust`;
- `molsysmt/_private/rust_backend.py` imports `molsysmt._rust`;
- the old separate Maturin package, illustrative fallback, and unwired CI
  skeleton are removed;
- a clean exact-commit wheel passed an automated content validator and an
  installed-extension smoke.

The complete evidence, commands, wheel name, and hashes are in
[C2 Rust Packaging Artifact](../release_1_0_rust_packaging_c2_artifact.md).

## Historical C1 Deferrals

- **C2, the crate relocation, was deliberately not done during C1.** Moving the
  crate out of `experiments/` would have changed the hashes recorded while B4
  still required a green exact-commit run. C2 landed after B4 closed.
- **The module rename belonged to C2, not C1.** The preferred design required
  `#[pymodule] fn _rust` and `[lib] name = "_rust"`, and `rust_backend.py`,
  `devtools/scripts/check_rust_hot_paths.py`, `tests/rust/test_hot_path_lint.py`,
  and the `tests/rust/` imports all still said `msm_rust_kernels`. C2 applied
  those changes to production.
- **CPU instruction baseline (C11) is already settled** with evidence: baseline,
  `x86-64-v2` and `x86-64-v3` are equal within noise on every hot kernel, so release wheels
  stay portable-baseline. See `../rust_kernel_optimization_guide.md` section 6.

## Accepted configuration

```toml
[build-system]
requires = [
    "setuptools>=68.0",
    "versioningit>=3.0",
    "setuptools-rust>=1.10",
]
build-backend = "setuptools.build_meta"

[[tool.setuptools-rust.ext-modules]]
target = "molsysmt._rust"
path = "rust/Cargo.toml"
binding = "PyO3"
py-limited-api = "cp311"
features = ["extension-module"]

# Required: py-limited-api on the extension yields an abi3 .so but does not by itself
# make the wheel carry the cp311-abi3 tag.
[tool.distutils.bdist_wheel]
py-limited-api = "cp311"
```

The final crate path was selected and integrated by C2 after B4 closed.

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
