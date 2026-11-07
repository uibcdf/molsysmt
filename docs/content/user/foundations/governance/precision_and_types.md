(user-foundations-governance-precision-and-types)=
# Numeric Precision & Data Standards

MolSysMT enforces strict numeric precision standards and array dimension invariants across all native data structures and converters.

---

## Floating Point Precision Standards

- **64-Bit Floating Point (`float64`)**: Native coordinates, box vectors and CPU working arrays use double precision. The bundled Rust CPU kernels compute in float64. Shared coordinate preparation and chunked execution report `MSM-WARN-PRECISION-001` when they consume a `precision='single'` request; they keep float64 working values.
- **32-Bit Floating Point (`float32`)**: Some operations, including least-RMSD fitting, explicitly support final single-coordinate quantization. This is a lossy output choice, not float32 Rust arithmetic. A quantity can retain float32 magnitudes; a native container stores the quantized values in float64. Single-coordinate publication therefore does not halve native-container memory. Its absolute resolution depends on coordinate magnitude and units.

External objects and file formats have their own storage contracts. Already
quantized float32 inputs cannot recover their missing bits when converted to
native float64. Select output precision separately from the precision required
by a numerical backend; there is no automatic GPU or mixed-precision guarantee.

---

## Dimension and ID Invariants

- **Coordinate Arrays**: Always shaped as `(n_structures, n_atoms, 3)` in nanometers.
- **Box Matrices**: Always shaped as `(n_structures, 3, 3)` in nanometers.
- **Time Arrays**: 1D NumPy arrays in picoseconds.
- **String Identifier Invariant**: In native MolSysMT objects (such as `molsysmt.Topology` and `molsysmt.MolSys`), element ID fields (`*_id`) are stored strictly as **normalized strings**. Numeric inputs are automatically converted to string representations to maintain invariants across form adapters.
