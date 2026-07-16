# Competitive Performance Comparison Strategy

MolSysMT is uniquely positioned in the structural biology and molecular dynamics ecosystem as a bridge between multiple formats and tools. To ensure that our safe, interoperable API remains highly competitive, we must systematically benchmark MolSysMT against established industry-standard tools: **MDTraj**, **MDAnalysis**, **OpenMM**, and **BioPython**.

---

## 1. The Strategic Trade-Off: Safety vs. Speed

Unlike tools that bypass type-checking or unit-safety for pure execution speed, MolSysMT prioritizes topological validity and form-agnosticism. This design introduces two layers of processing:

```
+-------------------------------------------------------------+
| Public API Overhead (argdigest, type-checks, unit resolution)| -> ~15-500 μs constant cost
+-------------------------------------------------------------+
                              v
+-------------------------------------------------------------+
| Kernel Execution (JIT-compiled, unit-stripped arrays)       | -> Scalable math (O(N) or O(N^2))
+-------------------------------------------------------------+
```

When comparing against competitors, our benchmark protocol must explicitly distinguish:
1. **Raw Math/Kernel Speed:** Running our underlying JIT kernels against our competitors' math engines. We expect to be as fast or faster than MDTraj/MDAnalysis because both use optimized compiled code (C/Cython vs. Numba).
2. **API Latency Overhead:** The cost of the safety layers for small systems. We must keep this overhead small (measured in microseconds) so that it is negligible for large-scale operations.

---

## 2. Competitive Comparison Matrix (Target Dimensions)

We evaluate and compare performance across three vital dimensions of structural workflows:

| Dimension | Target Operations | Competitors | Success Criteria |
| :--- | :--- | :--- | :--- |
| **File I/O & Loading** | Reading `.pdb`, `.dcd`, `.xtc`, and `.h5` | `MDTraj`, `MDAnalysis` | MolSysMT's chunked iterator loading should achieve parity in loading speed and maintain a smaller memory peak than `MDAnalysis`. |
| **Selection Language** | Resolving atom selections (e.g., `'atom.name == "CA"'`) | `MDTraj`, `MDAnalysis` | Parity in resolution speed. MolSysMT must optimize string parsing and caching to avoid recompiling queries. |
| **Geometric Kernels** | RMSD, distances, center of mass, and PBC wrapping | `MDTraj`, `MDAnalysis`, `OpenMM` | Raw JIT kernels must execute within 1.1x speed of MDTraj's C-implementations and exceed `MDAnalysis` NumPy operations. |

---

## 3. Comparison Strategy & Setup by Dimension

### A. File I/O Loading
* **Protocol:** Measure time and peak memory when reading trajectories of varying frame sizes (100, 1,000, 10,000 frames) and atom counts (1,000 to 100,000 atoms).
* **Metrics:** 
  - Time to first frame (latency).
  - Total load time (throughput).
  - Peak resident memory (RSS).
* **Target:** Assert that MolSysMT's lazy disk readers (`Iterator`) load frames on-demand without memory leaks, outperforming `MDAnalysis` when reading massive datasets that exceed RAM limits.

### B. Selection Language Speed
* **Protocol:** Profile the execution of standard selection strings on large structures (e.g., a ribosome or large solvated box):
  - Simple query: `'atom_name == "CA"'`
  - Complex query: `'(atom_name == "CA" or atom_name == "CB") and residue_name in ["ALA", "VAL", "LEU"]'`
* **Analysis:** Isolate selection parsing (converting to internal AST/indices) from index slicing.
* **Target:** Ensure MolSysMT's cached selection resolver compiles strings in `< 1 ms`.

### C. Geometric Calculation Kernels
* **Protocol:** Compare the execution times of:
  - **RMSD:** Fitting and alignment of $N$ frames to a reference structure.
  - **Contacts/Distances:** Calculation of all-to-all atom distances with and without Periodic Boundary Conditions (PBC) wrap.
* **Evaluation:**
  - `molsysmt.lib.structure` (JIT-compiled Numba) vs.
  - `mdtraj.rmsd` / `mdtraj.compute_contacts` (compiled C) vs.
  - `MDAnalysis.analysis.rms.rmsd` (Cython/NumPy).

---

## 4. Transparent Reporting Policy

All competitive comparisons must be fully reproducible:
1. **Public Benchmarking Scripts:** Scripts comparing libraries must live in the public repository (e.g., under `benchmarks/competitors/`).
2. **Version Transparency:** All compared package versions, hardware specifications, compiler backends, and environment details must be declared.
3. **No Cherry-Picking:** Benchmarks must cover both the strengths of MolSysMT (memory-efficient iteration, rich topologies, physical unit safety) and its current weaknesses (warm-up JIT compilation times and digestion overhead on tiny systems).
