---
summary: Source-build CI must select the pinned minimal Rust toolchain explicitly
issue: uibcdf/molsysmt#319
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: high
verification: reproduced
area: [ci, deps]
guard: devtools/tests/test_source_build_toolchain.py::test_source_build_selects_pinned_minimal_rust
normative:
blocked_by: []
supersedes: []
---

# Source-build CI requests conflicting development components

**Reported:** 2026-10-04, while checking the #298 peptide-reference commit.
**Status:** Resolved; local orchestration controls and the hosted smoke build pass.

## What

CI smoke run [37208814688](https://github.com/uibcdf/molsysmt/actions/runs/37208814688)
at `9615bf1fe96e0ea6922b0cdc2365d25223d5a701` fails in `Install package`, before
compilation or any import/test gate. Rustup requests development components from
`rust-toolchain.toml` and reports:

```text
failed to install component: 'clippy-preview-x86_64-unknown-linux-gnu',
detected conflict: 'bin/cargo-clippy'
```

Setuptools-rust subsequently reports an unavailable compiler and editable-wheel
failure. Inspect the bounded authoritative failure with:

```bash
gh run-receptor inspect 37208814688 --repo uibcdf/molsysmt --profile=ci --receptor=llm
gh run view 37208814688 --repo uibcdf/molsysmt --log-failed
```

## How

The smoke, full, weekly and import workflows invoke a source installation without
an explicit Rust compiler selection. The source manifest pins Rust 1.97.1 with
Clippy/rustfmt for development. Processing its components on a partially
provisioned hosted toolchain collides with existing files. A minimal profile alone
does not override the manifest's explicit components during a later implicit
compiler lookup.

These four workflows now explicitly install `1.97.1 --profile minimal`, verify
`rustc +1.97.1 --version`, and use `RUSTUP_TOOLCHAIN=1.97.1` on the package build.
This reuses the already exercised documentation workflow's solution recorded in
[the earlier installed-extension report](ci_shadows_the_installed_rust_extension_with_the_source_checkout.md).
The developer manifest and the dedicated Rust quality campaign retain their
Clippy/rustfmt checks. No compiler version or runtime dependency floor changes.

## Why

The failure prevents hosted tests from examining a published implementation.
The same missing selection occurs in the other source-build test workflows;
their exposure is inspected, not independently reproduced on every platform.
Five other controls on the original #298 commit succeeded. Their success does
not qualify its failed smoke test.

## Evidence and scope

The original hosted job is Ubuntu x86-64, Python 3.13, pinned Rust 1.97.1, with
the controlled dependency-source installation preceding the MolSysMT build.
The failed run's logs show the toolchain conflict. This does not establish a
failure in peptide chemistry, an environmental repair algorithm or the test code.
No tests executed in that run, so no scientific acceptance is inferred from it.

`devtools/tests/test_source_build_toolchain.py` executes each owning workflow's
actual provisioning/build command text with recording stand-ins for tools.
It requires minimal provisioning before the build, an explicit compiler check,
the manifest's exact pin and the pin in the native package build's environment.
Comments or inert YAML fields cannot satisfy the execution assertions. This is
a deterministic orchestration guard, not a real compiler or matrix qualification;
the hosted smoke build supplies the independent execution check.

Local validation on Linux/Python 3.13.14 completed **5 passed in 0.94 s**:

```bash
python -m pytest --receptor=llm devtools/tests/test_source_build_toolchain.py \
  devtools/tests/test_documentation_workflow.py
```

The dependency-contract audit passes with unchanged dependency pins/floors.

## Refuted approaches

- A peptide-source defect cannot explain this run: failure occurs in rustup
  before source compilation or Python imports.
- Repeating installation without fixing compiler selection leaves the manifest
  component request intact.
- Removing development quality components globally would weaken the dedicated
  Rust checks unnecessarily. Select the build compiler at the owning boundary.

## Acceptance

The four workflow controls must pass locally; a new unskipped commit must pass
the hosted smoke installation/import/test sequence and applicable administrative
controls. Record exact hosted evidence before closure. Full Linux/macOS matrices
and Python 3.14 qualification remain separately tracked work.

## Resolution — 2026-10-04

Implemented in `800477575291124f6421f49e2fb9f15cde7d81d2`. Hosted
[smoke run 37209449854](https://github.com/uibcdf/molsysmt/actions/runs/37209449854)
completed successfully, including explicit minimal compiler selection, installation,
controlled-dependency checks, import, API/docstring/form contracts, Rust-only audit
and the unchanged smoke tests. Dependency contract, developer-guide integrity,
Ruff, MolSysSuite policy and Conda publication governance also pass on that commit.
The preceding peptide-reference commit's bundled-data check separately succeeded.

The guard executes the four workflow command sequences with recording tools and
asserts that the native source build actually receives the compiler pin. It fails
if provisioning/checking disappears, follows installation, the provisioning
command requests development components, changes the pin or leaves implicit
manifest selection on the build.
The independent hosted build confirms the correction on Ubuntu; this does not
claim a completed full Linux/macOS matrix or Python 3.14 qualification.
