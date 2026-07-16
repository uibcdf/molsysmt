# Proposal: Conda Installation-Time JIT Preheating and Cache Generation

**Status:** exploratory; do not implement without packaging and portability
validation.

> This proposal depends on the current `molsysmt.warmup()` contract and Numba
> cache behavior. Post-link scripts, ignored failures, writable cache locations,
> CPU portability, and package-manager policy must be validated experimentally.
> The "recommended" label below reflects the original proposal, not an accepted
> repository decision.

## Abstract

We propose compiling Numba JIT functions automatically during the conda/mamba package installation process. This eliminates the initial dynamic compilation lag (~4.0 seconds) that users experience during their first molecular operations in interactive environments like Jupyter notebooks or `molsysviewer` sessions. By integrating JIT preheating into the conda packaging workflow (via a host-side `post-link` script or build-time precompilation), we can ensure a seamless, instant-start experience for the end user.

---

## The Problem

MolSysMT relies on dynamic JIT compilation (via Numba) to achieve high computational speeds. By default, JIT compilation happens lazily upon the first invocation of a decorated function. This causes the first execution of coordinate conversions, topology queries, or distance calculations in a Python session to freeze for several seconds:

*   **Initial Run Overhead**: ~4,000 ms (JIT compiling).
*   **Subsequent Runs**: ~350 ms (Cache hit / native execution).

This lag propagates directly to user-facing applications:
1.  **Interactive GUIs (`molsysviewer`)**: The very first time a structure is loaded, the visual widget freezes, leading to a poor user experience.
2.  **Downstream Packages (`elastnetmt`, `pharmacophoremt`, `topomt`)**: First computations inherit this initial 4-second delay.

While we have proposed a programmatic `molsysmt.warmup()` API to compile functions in a background thread, the compilation cost is still paid during the active runtime session. Shifting this compilation overhead to the package installation step ensures that the runtime environment is pre-warmed.

---

## Proposed Solutions

We propose two primary avenues to achieve installation-time JIT preheating in the conda recipe:

### 1. Conda `post-link` Script (Recommended)
This approach triggers JIT compilation on the user's host machine immediately after conda extracts the package.

#### Implementation
In the conda recipe (`recipe/`), we introduce a `post-link.sh` script (and a corresponding `post-link.bat` for Windows):

```bash
# recipe/post-link.sh
#!/bin/bash

# Force compilation using the current environment's python interpreter
if [ -n "${PYTHON}" ]; then
    echo "Preheating MolSysMT JIT caches (this may take a few seconds)..."
    # Execute warmup and ignore errors to prevent conda install failures
    "${PYTHON}" -c "import molsysmt; molsysmt.warmup(strict=True)" >/dev/null 2>&1 || true
fi
```

#### Advantages
*   **Host CPU Optimization**: Compilation happens on the user's machine, meaning Numba generates machine instructions optimized specifically for the user's processor features (AVX2, AVX-512, etc.).
*   **Cache Validity**: Since the files are built locally, there is zero risk of cache invalidation due to hardware mismatch.

#### Considerations
*   The script must use `|| true` to guarantee that any minor runtime warning or environment permission issue does not block the entire package installation.

---

### 2. Build-Time Cache Packaging (Pre-compilation on CI)
This approach runs the warmup script on the packaging server (GitHub Actions / build system) and bundles the compiled `.nbc` and `.nbi` cache files directly into the distributed conda package.

#### Implementation
In the recipe's `build.sh` script, after copying the package into `$SP_DIR`:

```bash
# recipe/build.sh
export NUMBA_CACHE_DIR="${SP_DIR}/molsysmt/.numba_cache"
python -c "import molsysmt; molsysmt.warmup(strict=True)"
```

#### Advantages
*   **Instant Installation**: The user does not wait at all during `conda install`, as the compiled cache directory is simply extracted.

#### Considerations
*   **CPU Feature Mismatches**: Numba's caching mechanism is strictly tied to CPU architecture features. If the build server's CPU supports features (e.g., AVX-512) that the user's host CPU lacks (or vice versa), Numba will invalidate the shipped cache and recompile at runtime anyway, defeating the purpose.

---

## Conclusion and Recommendations

We recommend implementing **Option 1 (Conda `post-link` script)** for the `uibcdf` channel. Because it compiles on-site, it guarantees both maximum execution performance tailored to the user's actual processor and 100% cache compatibility, ensuring that when the user first imports `molsysmt` in a notebook, it loads and performs instantly.
