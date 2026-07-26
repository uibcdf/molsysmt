# Proposal: Hybrid Columnar Molecular Engine based on ECS, CSR Graphs, and Apache Arrow (MECS-Arrow)

**Status:** proposed (2026-07-12).
**Ecosystem impact:** `molsysmt` core backend (high-performance topology, selections, and connectivity queries), zero-copy interoperability with PyArrow/Pandas.
**Prerequisites:** Cargo/Rust toolchain, Maturin/PyO3, Apache Arrow Rust bindings (`arrow` crate), ECS implementation (`hecs` or custom SoA), Graph implementation (`petgraph` or custom CSR).

**Measured caveat (2026-07-26).** Do not justify the columnar/SoA layout with an expected
SIMD win in the geometry kernels. Benchmarked against the current `[n_atoms, 3]` AoS
coordinates on all-pairs squared distances (n = 4000), SoA came out **0.94x** on the
baseline build and **0.69x** under AVX2/FMA — slower, and more so once vectorised, because a
pair kernel then reads three cache-line streams per atom instead of one. The case for this
proposal must rest on zero-copy Arrow interop, attribute-centric storage and the
topology/selection layers; the compute kernels are evidence *against* the layout change.
See `rust_kernel_redesign_beyond_faithful_ports.md` §4.D.

---

## 1. Abstract

We propose the design of a native, unified high-performance molecular core engine for `molsysmt` in Rust. Rather than wrapping JIT mathematical functions or relying on generic tabular DataFrame libraries (like Pandas or Polars), this proposal outlines a **four-tier hybrid architecture** tailored specifically to the structural, spatial, and topological properties of molecular systems:

1.  **Data Layer (Apache Arrow):** Contiguous, columnar in-memory layout ensuring zero-copy data transfer between Python (PyArrow, Pandas, Polars) and the Rust core.
2.  **Attribute and Query Layer (Entity-Component-System - ECS):** High-level parallel query engine where molecular units (atoms, residues) are entities, and their attributes (names, types, coordinates) are contiguous components.
3.  **Connectivity Layer (CSR Graph):** Adjacency list representation of bonds for $O(1)$ neighbor traversals and rapid covalent query evaluation (e.g., ring finding, bond-distance selections).
4.  **Spatial Layer (BVH/Octree):** Spatial indexing for fast $O(N \log N)$ distance queries, synchronized with trajectory frame transitions.

This hybrid engine will solve both coordinate-based math and hierarchical topology selections at native machine speed, with minimal memory allocation and zero boundary-crossing copies.

---

## 2. Why: The Limitations of DataFrame-Centric Topology

Currently, `molsysmt` represents molecular topologies using custom Pandas DataFrames linked by index relations. While DataFrames are familiar, they suffer from two major limitations when representing molecular data:

*   **Temporary Expansion for Hierarchical Queries:** A molecular system is hierarchical (Atom $\rightarrow$ Residue/Group $\rightarrow$ Molecule $\rightarrow$ Chain). Since 2026-07-13, querying across these levels gathers referenced columns directly through integer links rather than using `pd.merge()`. It still creates a temporary atom-level DataFrame, so a native engine must be compared with this improved baseline.
*   **Poor Representation of Chemical Connectivity:** Bonds represent edges in a graph. In a DataFrame, bonds are stored as a table of index pairs. Querying connectivity (e.g. finding atoms within 3 bonds, or identifying connected molecular components) requires self-joining the bonds table multiple times, which is computationally expensive and complex to write.

To achieve maximum performance, we must move away from generic relational tables toward a data structure that mirrors the physical reality of a molecule: a hierarchical, connected, spatial graph.

---

## 3. The Three-Tier Hybrid Architecture (MECS-Arrow)

The proposed core engine combines three specialized systems into a unified architecture:

```
┌────────────────────────────────────────────────────────┐
│             Layer 1: Apache Arrow Memory               │
│ - Columnar layout for zero-copy memory sharing.        │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│           Layer 2: Entity-Component-System (ECS)       │
│ - Contiguous attributes (names, types, indices).       │
│ - O(1) hierarchical dereferencing (bypasses merges).   │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌──────────────────────────────────────┬─────────────────┐
│     Layer 3: Connectivity (CSR)      │ Layer 4: Space  │
│ - O(1) covalent neighbor traversals. │ - Octree/BVH.   │
└──────────────────────────────────────┴─────────────────┘
```

### Layer 1: Memory Layout (Apache Arrow)
Apache Arrow defines a standardized, language-independent columnar memory format.
*   **Implementation:** All topology columns in Rust (atom names, types, residue indices) and coordinate buffers are laid out using the Arrow memory specification.
*   **Benefit:** Zero-copy data sharing between Python and Rust. Python libraries (like PyArrow, Pandas, or Polars) can read and write the exact same RAM buffers managed by the Rust core, eliminating serialization and memory copy overhead at the boundary.

### Layer 2: Attribute & Query Engine (Entity-Component-System - ECS)
ECS is a software pattern designed for high-performance data layouts in game engines.
*   **Implementation:**
    *   **Entities:** Atoms, Residues, and Molecules are lightweight integer IDs.
    *   **Components:** Typed contiguous arrays (e.g., `AtomName(Vec<String>)`, `GroupIndex(Vec<usize>)`) matching the Arrow layout.
*   **Query Resolution:** Instead of joining tables, cross-level queries are resolved via direct index dereferencing:
    ```rust
    // O(1) verification: no joins or copies
    atom_name[i] == "CA" && group_name[group_index[i]] == "ALA"
    ```
    This loop is evaluated in parallel using `rayon` over the contiguous component slices.

### Layer 3: Connectivity Engine (CSR Adjacency Graph)
Chemical bonds are represented as a graph.
*   **Implementation:** Bonds are stored in Rust using a **Compressed Sparse Row (CSR)** adjacency matrix or a double-linked graph representation (via `petgraph`).
*   **Benefit:** Resolving queries like `"bonded to selection"` or `"not bonded to selection"` becomes a simple BFS traversal of the adjacency list in Rust, running in $O(V+E)$ microsecond timescales.

### Layer 4: Spatial Engine (BVH / Octree with Dynamic Refitting)
Physical distance is represented using spatial partitioning.
*   **Implementation:** A Bounding Volume Hierarchy (BVH) or Octree is constructed in Rust from the coordinate array.
*   **Benefit:** Resolving spatial queries like `"within 0.5 of selection"` queries the BVH in $O(N \log N)$ rather than doing an $O(N^2)$ distance matrix scan. To prevent the overhead of rebuilding the spatial tree from scratch on every trajectory frame transition, the engine utilizes **Dynamic BVH Refitting**: it deforms the bounding boxes of the tree nodes in $O(N)$ linear time without mutating the tree topology, keeping updates extremely fast.


---

## 4. How: The Seam with Python (Lazy Conversion)

To maintain 100% backwards compatibility with the existing Python API:

1.  **Rust Storage:** `molsysmt.Topology` holds a PyO3 reference to the native `RustTopology` engine.
2.  **Lazy Properties:** Properties like `Topology.atoms`, `Topology.groups`, etc., are converted to Pandas DataFrames on-the-fly **only when the user requests them** (e.g. `df = view.topology.atoms`).
3.  **Fast Path:** High-level functions (like `select()`, `get_contacts()`, and distance calculators) bypass Pandas entirely and execute queries directly on the Rust structure.

### 4.6 End-to-End Arrow IPC Stream to MolSysViewer (Zero-Copy Visualization)

One of the most transformative advantages of this layout is how it bridges the backend (`molsysmt`) with the frontend visualizer (`molsysviewer`):
*   **The JSON Bottleneck:** Currently, sending structure and coordinate data to the TS/JS frontend requires converting arrays to massive JSON payloads, which is slow and memory-heavy.
*   **The Arrow IPC Solution:** Because Apache Arrow represents memory column-buffers identically across languages, we can serialize the topology and coordinates into an **Arrow IPC Stream** (Feather/Stream format) directly in Rust.
*   **Zero-Copy Rendering:** This binary stream is sent over the Jupyter widget websocket directly. The TypeScript frontend (`molsysviewer/js/src/`) parses the binary Arrow buffer using `apache-arrow` JS libraries, passing the coordinates directly to Mol*'s GPU vertex buffers. This completely eliminates JSON serialization, reducing widget load times by 10x-50x.

### 4.7 Coexistence, Gradual Adoption, and the Multiple-Dispatch Selection Seam

A massive architectural advantage of the MECS-Arrow engine is that it does not require a single-day, breaking replacement of the existing native forms (`molsysmt.MolSys`, `molsysmt.Topology`, and `molsysmt.Structures`).

Instead, the new hybrid format can be registered as a **new independent form** in `molsysmt`'s multiple-dispatch form registry (e.g. `molsysmt.MecsMolSys` or `molsysmt.ArrowTopology`).

This enables a highly pragmatic, gradual adoption path:
1. **Multiple Dispatch Compatibility:** Existing functions that only support `molsysmt.Topology` (Pandas) will trigger the automatic `convert(item, to_form='molsysmt.Topology')` seam. The system will continue to work perfectly, albeit with the legacy performance profile.
2. **Fast Path Incremental Opt-In:** As critical bottleneck functions (like select, distances, contacts) are updated to support the new native forms, they bypass the conversion overhead entirely and execute at maximum speed.
3. **Non-Breaking Development:** Developers can test, benchmark, and deploy the new forms in parallel with the production-tested legacy forms.
4. **Automatic Propagation of Speedups to External Forms:** Under `molsysmt`'s selection architecture (`molsysmt/basic/selector/molsysmt.py`), any query on an external third-party format (e.g., `openmm.Topology`, `mdtraj.Trajectory`, `mdanalysis.Universe`) is automatically and lazily converted to `molsysmt.Topology` before evaluation. By optimizing the native form (using DuckDB or Rust), **all 30+ external formats supported by the library automatically inherit this acceleration** without writing a single line of format-specific query code.

---

## 5. Prioritized Roadmap for Implementation

1.  **Phase 1 (Rust Crate & SoA Memory):** Initialize the Rust crate and implement the flat Struct of Arrays (SoA) layout for Atoms, Groups, and Molecules.
2.  **Phase 2 (AST Parser & Rayon Query):** Write the selection string parser in Rust (using `nom`) to compile queries to an AST. Implement the parallel query evaluator.
3.  **Phase 3 (CSR Bonds Graph):** Implement the CSR adjacency list for covalent bonds and integrate `select_bonded_to` queries.
4.  **Phase 4 (Apache Arrow & Zero-Copy):** Integrate the `arrow` crate, mapping the Rust arrays to PyArrow record batches for zero-copy Python interoperability.
5.  **Phase 5 (Octree/Spatial Integration):** Implement the native Octree spatial index to accelerate `select_within` queries.
