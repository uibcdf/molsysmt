(user-foundations-performance-rust-core)=
# The Rust Core

MolSysMT incorporates a compiled, native C/Rust execution core designed for high-performance numerical computations, spatial queries, and trajectory analytics.

---

## High-Performance Compiled Kernels

While MolSysMT provides a user-friendly Python API, computationally intensive inner loops are delegated to a compiled C/Rust native layer:

- **Distance Matrices & Minimum Image Convention**: Frame-by-frame pair distance evaluations and periodic boundary condition (PBC) minimum image calculations.
- **Solvent Accessible Surface Area (SASA)**: Optimized numerical integration of atomic surface accessibilities.
- **Root-Mean-Square Deviation (RMSD)**: Fast Kabsch alignment and coordinate superposition over trajectory frames.

---

## Memory Safety and Zero-Overhead C-API

The Rust core is integrated directly via C-API and PyO3 bindings:

- **Memory Safety**: Rust's strict memory ownership model guarantees data race freedom and prevents memory leaks during long-running trajectory analyses.
- **Direct Pointer Interoperability**: NumPy array memory buffers are passed directly to Rust native kernels without unnecessary copying or serialization overhead.
