# Micro-Governance: `installation.md` (`installation.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/installation.md`](installation.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-installation)=`

3. **Inviolable Technical Directives**:
   - **Header H2**: MUST be `## Official Installation`.
   - **Official Distribution Link**: MUST link to `https://anaconda.org/channels/uibcdf` with `-c uibcdf -c conda-forge`.
   - **Python Scope**: Current source targets Python 3.11–3.14; routine
     development uses 3.14. Distinguish source policy from the tested scope of
     a particular published artifact.
   - **Development Environment Path**: MUST specify `devtools/conda-envs/development_env.yaml`.
   - **Editable Installation Command**: MUST specify `pip install --no-deps --editable .`.
   - **Precompiled Kernels Admonition**: Distinguish the bundled precompiled
     extension in binary packages from a source installation's Rust/Cargo and
     platform compiler requirements. The toolchain is owned by
     `rust-toolchain.toml`; avoid duplicating its version here.
   - **Editable Build Boundary**: Explain that `--no-deps` controls runtime
     dependencies, while declared build requirements and native compilation
     still apply. Do not instruct users to reuse an unrelated old extension.
