# Section: Performance Directives (`AGENTS.md`)

This guide governs all content under `docs/content/user/foundations/performance/`.

## 🧭 Subdirectory Purpose & Scope
Cover high-performance execution, Big Data structure sequence scaling, Rust native core acceleration, memory management, parallel execution, low-level internal optimizations, SMonitor diagnostics/profiling, caching/memoization, benchmarks, and GPU acceleration roadmap.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Group landing page with `toctree`.
- `lazy_loading.md` ➔ `lazy_loading.md.AGENTS.md`: Deferred array fetching and streaming I/O.
- `chunked_execution.md` ➔ `chunked_execution.md.AGENTS.md`: Memory wall management, ChunkedExecutor, and user Iterator scripts.
- `rust_core.md` ➔ `rust_core.md.AGENTS.md`: Compiled Rust native kernels and PyO3/C-ABI bindings.
- `parallelization.md` ➔ `parallelization.md.AGENTS.md`: Multi-threading and SIMD vectorization.
- `internal_optimizations.md` ➔ `internal_optimizations.md.AGENTS.md`: Fast-track units, explicit digestion bypass, kernel-input preparation, and zero-copy views.
- `diagnostics_and_profiling.md` ➔ `diagnostics_and_profiling.md.AGENTS.md`: Execution profiling, memory pressure warnings, SMonitor docs link, and telemetry.
- `caching_and_memoization.md` ➔ `caching_and_memoization.md.AGENTS.md`: Selection AST caching and form registry memoization.
- `benchmarks.ipynb` ➔ `benchmarks.ipynb.AGENTS.md`: Empirical performance throughput and comparative metrics.
- `gpu_roadmap.md` ➔ `gpu_roadmap.md.AGENTS.md`: Post-1.0 GPU acceleration roadmap.

## 📐 Foundations Editorial & Style Standards
- **Conceptual Scope**: Pages in `foundations/` explain conceptual architecture, design principles, and performance models. They do NOT document specific function API signatures, nor do they include `tools/` artifacts such as `:::{versionadded}`, top italic gerund summaries (`*Doing...*`), or API function `{seealso}` boxes.
- **Published Table Formatting Standard**: All tables MUST expand to full line width (`class="table"`, `width: 100%`), feature zebra striping, and have all headers and cells left-aligned (`text-align: left`).
- **Terminology Standard**: Avoid "trajectory analytics"; use "molecular structures sequence analytics" or "spatial calculations".
- **Nested Toctree Chaining**: References to index pages in `toctree` directives MUST use relative index paths without `.md` extensions (e.g. `performance/index`) to ensure Sphinx cascades the navigation tree cleanly and renders Section Navigation and breadcrumbs across all child pages.
