# Micro-Governance: `installation.md` (`installation.md.AGENTS.md`)

This micro-governance contract governs [`docs/content/user/foundations/entrance/installation.md`](installation.md).

---

## 🔒 Frozen & Inviolable Content

1. **Format Policy**:
   - MUST remain a pure MyST Markdown (`.md`) page.

2. **Mandatory MyST Section Anchor**:
   - `(user-foundations-entrance-installation)=`

3. **Inviolable Technical Directives**:
   - **Official Distribution**: Channel MUST be specified as `-c uibcdf -c conda-forge`.
   - **Supported Python Versions**: Python 3.13 (recommended), 3.12, 3.11.
   - **Development Environment Path**: MUST specify `devtools/conda-envs/development_env.yaml`.
   - **Editable Installation Command**: MUST specify `pip install --no-deps --editable .`.
   - **Precompiled Kernels Admonition**: Note explaining precompiled Rust extension with 0ms JIT warmup.
