(user-foundations-performance-rust-core)=
# The Rust Core

MolSysMT incorporates a compiled, native Rust execution core designed for high-performance numerical computations, spatial queries, and molecular structures sequence analytics.

---

## High-Performance Compiled Kernels

While MolSysMT provides a user-friendly Python API, computationally intensive inner loops are delegated to a compiled **Rust** native core:

- **Distance Matrices & Minimum Image Convention**: Structure-by-structure pair distance evaluations and periodic boundary condition (PBC) minimum image calculations.
- **Solvent Accessible Surface Area (SASA)**: Optimized numerical integration of atomic surface accessibilities.
- **Root-Mean-Square Deviation (RMSD)**: Fast Kabsch alignment and coordinate superposition over structure sequences.

The public boundary checks inputs before invoking a numerical kernel. For rigid
fitting, both selections must provide at least three non-collinear atom centers;
repeated centers do not determine additional rotational freedom. All requested
structures are checked before an in-place fit changes coordinates. Degeneracy is
assessed with numerical rank after length-unit alignment, without a physical
near-collinearity threshold. See {ref}`Least RMSD fit <Tutorial_Least_rmsd_fit>`.

---

## Memory Safety and PyO3 / C-ABI Integration

The native core is written in Rust and integrated seamlessly with Python:

- **Memory Safety**: Rust's strict memory ownership model guarantees data race freedom and prevents memory leaks during long-running spatial sequence analyses.
- **Zero-Overhead Array Passing**: PyO3 bindings and C-ABI interfaces pass NumPy array memory buffers directly to Rust compiled kernels without unnecessary copying or serialization overhead.
