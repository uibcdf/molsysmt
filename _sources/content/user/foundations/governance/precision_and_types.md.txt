(user-foundations-governance-precision-and-types)=
# Numeric Precision & Data Standards

MolSysMT enforces strict numeric precision standards and array dimension invariants across all native data structures and converters.

---

## Floating Point Precision Standards

- **32-Bit Floating Point (`float32`)**: Default precision for 3D coordinate arrays `(n_structures, n_atoms, 3)` and box vectors. `float32` balances spatial accuracy (sub-picometer resolution) with optimal memory footprint and GPU hardware compatibility.
- **64-Bit Floating Point (`float64`)**: Preserved for high-precision energy evaluations, double-precision numerical integrations, and physical unit conversions.

---

## Dimension and ID Invariants

- **Coordinate Arrays**: Always shaped as `(n_structures, n_atoms, 3)` in nanometers.
- **Box Matrices**: Always shaped as `(n_structures, 3, 3)` in nanometers.
- **Time Arrays**: 1D NumPy arrays in picoseconds.
- **String Identifier Invariant**: In native MolSysMT objects (such as `molsysmt.Topology` and `molsysmt.MolSys`), element ID fields (`*_id`) are stored strictly as **normalized strings**. Numeric inputs are automatically converted to string representations to maintain invariants across form adapters.
