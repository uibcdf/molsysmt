# Section: Performance Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/performance/`.

## 🧭 Subdirectory Purpose & Scope
Cover high-performance execution, Big Data trajectory scaling, Rust native core acceleration, memory management, parallel execution, low-level internal optimizations, SMonitor diagnostics/profiling, caching/memoization, benchmarks, and GPU acceleration roadmap.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `lazy_loading.md` ➔ `lazy_loading.md.AGENTS.md`: Deferred array fetching and streaming I/O.
- `chunked_execution.md` ➔ `chunked_execution.md.AGENTS.md`: Memory wall management and ChunkedExecutor.
- `rust_core.md` ➔ `rust_core.md.AGENTS.md`: Compiled C/Rust native kernels.
- `parallelization.md` ➔ `parallelization.md.AGENTS.md`: Multi-threading and SIMD vectorization.
- `internal_optimizations.md` ➔ `internal_optimizations.md.AGENTS.md`: Validation passports, fast-track units, digestion bypass, and zero-copy views.
- `diagnostics_and_profiling.md` ➔ `diagnostics_and_profiling.md.AGENTS.md`: Execution profiling, memory pressure warnings, and SMonitor telemetry.
- `caching_and_memoization.md` ➔ `caching_and_memoization.md.AGENTS.md`: Selection AST caching and form registry memoization.
- `benchmarks.ipynb` ➔ `benchmarks.ipynb.AGENTS.md`: Empirical performance throughput and RAM scaling metrics.
- `gpu_roadmap.md` ➔ `gpu_roadmap.md.AGENTS.md`: Post-1.0 GPU acceleration roadmap.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, design principles, and performance models. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Concise Section Titles**: Headings (`H2`, `H3`) must be brief, crisp, and direct (typically 2 to 4 words).
- **MyST Anchors**: Use MyST anchors (e.g. `(user-foundations-05-performance)=`, `(user-foundations-performance-lazy-loading)=`).
- **Pre-execution Policy**: Pre-execute updated notebooks via `python docs/execute_notebooks.py -f [notebook_path]` before committing.
