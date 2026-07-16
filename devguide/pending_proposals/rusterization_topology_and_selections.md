# Proposal: Rusterization of Topology and Selection Engine in MolSysMT

**Status:** proposed (2026-07-12).
**Ecosystem impact:** `molsysmt` (topology storage and selection resolution), Jupyter user experience.
**Prerequisites:** Cargo/Rust toolchain, Maturin/PyO3 for compilation, Polars/Nom crates.

---

## 1. Abstract

We propose migrating the core topology representation and selection query engine of `molsysmt` from custom Pandas DataFrames (`Atoms_DataFrame`, `Groups_DataFrame`, etc.) to a native, high-performance **Rust Topology Engine**.

The historical selector dynamically merged multiple Pandas DataFrames and then
evaluated text query strings through `DataFrame.query(engine='python')`. Since
2026-07-13, the production Python path gathers hierarchy columns directly by
integer links; the exact-parity 100,000-atom benchmark is recorded in
`topology_selection_indexing_and_pyarrow.md`. Query parsing/evaluation and the
mutable Pandas representation remain relevant baselines for a Rust experiment.

By implementing the topology engine in Rust, selections could be evaluated in
native compiled code using either **Polars DataFrames** or a **custom Abstract
Syntax Tree (AST) evaluator** over a Struct-of-Arrays (SoA) layout. Any claimed
gain must be measured against the current direct-gather Python baseline; no
microsecond-scale result is assumed in advance.

---

## 2. Why: The Overhead of Pandas-Based Selection

`molsysmt.Topology` represents the molecular hierarchy (Atoms $\rightarrow$ Groups $\rightarrow$ Components $\rightarrow$ Molecules $\rightarrow$ Entities $\rightarrow$ Chains) using linked Pandas DataFrames. When a user runs a selection query like `atom_name == 'CA' and group_name == 'ALA'`, the selector must:

1.  **Resolve Hierarchical Fields:** Detect which columns belong to which DataFrame levels (e.g. `atom_name` is atom-level, `group_name` is group-level).
2.  **Gather Hierarchical Columns:** Expand only the referenced columns through
    the stored integer hierarchy links into a temporary atom-level DataFrame.
3.  **Dynamic Evaluation:** Run `aux_df.query(selection, engine='python')`, which compiles the query string to Python bytecode in heat-of-execution and evaluates it using Python's `eval()`.

The direct-gather path removed the former relational-join overhead, but it still
allocates an atom-level DataFrame and evaluates a dynamic expression. Those
remaining costs, plus topology mutation and Python/Rust boundary costs, must be
profiled before this proposal advances.

---

## 3. What: The Two Rust Paradigms

We evaluate two distinct approaches for implementing the high-performance Rust Topology Engine:

```
                                  ┌─────────────────────────┐
                                  │      Selection Query    │
                                  │ "atom_name == 'CA' ..." │
                                  └────────────┬────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
         [Approach 1: Polars Engine]                     [Approach 2: Custom AST Engine]
     - Swap Pandas for Rust Polars.                   - Store topology as flat typed vectors.
     - Compile queries to Polars LazyExpr.            - Parse query string to AST once.
     - Fast multi-threaded joins/filters.            - Evaluate AST via O(1) index dereference.
```

### Approach 1: Polars-Based DataFrames in Rust
Polars is a blazingly fast, multi-threaded DataFrame library written in Rust. In this paradigm, we swap Python Pandas DataFrames for Polars DataFrames managed in Rust memory.

*   **How it works:**
    *   `molsysmt_core` represents `atoms`, `groups`, etc., as Polars DataFrames.
    *   The selection string is executed using Polars' native **SQL Context** or compiled into a **Lazy Expression (LazyFrame)**.
    *   Polars automatically optimizes the physical query plan (e.g., pushdown filters, parallel hash joins) before execution.
*   **Pros:**
    *   Preserves the tabular/relational database paradigm.
    *   Very high development speed due to Polars' existing SQL parser and Python bindings.
    *   Supports full relational algebra out-of-the-box.
*   **Cons:**
    *   Still performs relational joins (`JOIN` / `merge`) under the hood, which creates temporary tables in memory.
    *   Slightly larger binary footprint due to the Polars library size.

### Approach 2: Custom AST Interpreter & Struct of Arrays (SoA)
This is the approach utilized by traditional high-performance molecular packages (like VMD or MDAnalysis). The molecular hierarchy is represented as a typed **Struct of Arrays (SoA)** in Rust, and selections are evaluated via direct index dereferencing.

*   **How it works:**
    *   Topology columns are stored as flat, contiguous vectors in Rust: `atom_name: Vec<String>`, `group_index: Vec<usize>`, `group_name: Vec<String>`.
    *   A custom parser (written in Rust using `nom` or `pest`) compiles the selection query string into an **Abstract Syntax Tree (AST)** once (e.g., `And(Eq(Field::AtomName, "CA"), Eq(Field::GroupName, "ALA"))`).
    *   To evaluate the query, Rust iterates over all atom indices `0..n_atoms` in parallel (via Rayon). For each index `i`, it evaluates the AST:
        ```rust
        fn evaluate(expr: &Expr, topo: &RustTopology, i: usize) -> bool {
            match expr {
                Expr::Eq(Field::AtomName, val) => topo.atom_name[i] == *val,
                Expr::Eq(Field::GroupName, val) => {
                    let g_idx = topo.group_index[i];
                    topo.group_name[g_idx] == *val // O(1) dereference, no join
                }
                Expr::And(left, right) => evaluate(left, topo, i) && evaluate(right, topo, i),
                // ...
            }
        }
        ```
*   **Pros:**
    *   **Absolute Maximum Performance:** Bypasses `pd.merge` completely. Hierarchy lookup is a simple $O(1)$ memory dereference.
    *   **Zero Memory Allocation:** No temporary DataFrames are created during query evaluation. The only output is a lightweight `Vec<usize>` containing matching atom indices.
    *   **Domain-Specific Syntax:** Allows implementing biology-specific query keywords easily (e.g. `backbone`, `water`, `protein`, `within 5.0 of selection`).
*   **Cons:**
    *   Requires writing and maintaining a custom query string parser in Rust.

---

## 4. How: The Seam with Python and Backwards Compatibility

To avoid breaking the user-facing API and maintain compatibility with existing analysis notebooks, the Rust Topology Engine will use a **Lazy Conversion Seam**:

1.  **Rust Core Storage:** The class `Topology` in `molsysmt` will store the topology in the Rust native `RustTopology` structure.
2.  **Lazy Pandas Properties:** The properties `Topology.atoms`, `Topology.groups`, etc., will still exist. However, instead of storing Pandas DataFrames continuously, they will be generated **on-demand (lazily)** from the Rust structure only when the user explicitly requests them (e.g., `view.topology.atoms`).
3.  **Seamless Selections:** `select()` calls will route directly to the Rust binary, bypassing Pandas. The Rust binary resolves the selection and returns a NumPy array of indices, which Python consumes directly.

## 4.5 Synergy with Spatial and Connectivity Queries (select_within & select_bonded_to)

A key architectural benefit of rusterizing the topology engine is the massive synergy gained during complex query evaluations like `select_within` (spatial neighbors) and `select_bonded_to` (chemical bonds):

1. **Spatial Selections (`select_within`):**
   Queries like `"within 0.5 nanometers of protein"` require resolving both the topology (to identify the `"protein"` atom indices) and calculating Euclidean distances between those atoms and other coordinates.
   * *The Python Loop:* In Python, this requires crossing the boundary multiple times: calling `select()` for both selections, and then executing `get_contacts()` on the coordinate arrays, and filtering.
   * *The Rust Loop:* By having both topology and `get_contacts` (via cell-lists) in Rust, the query is resolved entirely on the Rust side. Python passes the query string and a reference to the coordinates. Rust parses the selection, queries the coordinates using its native spatial cell-list in memory, and returns the filtered index list in a **single boundary crossing**.
2. **Connectivity Selections (`select_bonded_to`):**
   Resolving chemical bonding queries (e.g. `"not bonded to selection2"`) is computed using Rust's Compressed Sparse Row (CSR) adjacency graph representation of bonds. Rust evaluates the connectivity in microsecond timescales, bypassing expensive list intersections and NumPy diff checks in Python.

---

## 5. Prioritized Roadmap for Implementation

1.  **Phase 1 (Proof of Concept - Polars):** Set up a test crate that loads a PDB topology into Polars DataFrames in Rust. Run select queries using Polars' SQL Context and benchmark the speedup against Python Pandas.
2.  **Phase 2 (AST Engine Prototype):** Write a simple selection compiler in Rust using `nom` to parse `atom_name == "CA"` and evaluate it over flat arrays. Compare its execution speed and memory usage against the Polars engine.
3.  **Phase 3 (Integrate Seam):** Replace `Atoms_DataFrame` and `Groups_DataFrame` initialization in `topology.py` with lazy properties. Route `select_standard` queries to the Rust engine.
4.  **Phase 4 (Advanced Selectors):** Implement spatial selectors (`within X of ...`) and connectivity selectors (`bonded to ...`) in Rust using the fast CSR adjacency list representation of bonds.
