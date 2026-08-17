# Sub-Portal Governance: `tools/build/` (`AGENTS.md`)

This guide governs all content under `docs/content/user/tools/build/`.

---

## 🧭 Subdirectory Purpose & Scope
Houses tutorial units for system building, topology construction, missing heavy atom recovery, terminal capping, protonation, solvation, and mutation tools.

## 🧱 Scientific & Architectural Invariants for Build Tutorials
1. **Solvation & Periodic Boundary Conditions**:
   - Solvation tutorials must illustrate physiological salt conditions (`ionic_strength`) and supported box shapes (`'cubic'`, `'truncated octahedral'`, `'rhombic dodecahedral'`).
   - Solvated systems must demonstrate PBC boundary wrapping (`wrap_to_pbc`) and 3D visual validation using MolSysViewer.
2. **Structural Repair & Protonation**:
   - Missing atom and hydrogen additions must show physiological pH settings (`pH=7.4`) and verification of complete heavy/hydrogen topologies.
3. **Clash Detection & Steric Quality**:
   - Overlap removal must quantitatively prove steric quality by verifying that contact matrices at $<0.2	ext{ nm}$ contain zero clashes (`np.any(clashes) == False`).
4. **Editable System Construction**:
   - Full builder workflows using `MolSysBuilder` must illustrate additive (atoms, bonds) and subtractive (deletions, bond cleavages) modifications.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Index portal with 2-column function catalog table and hidden `toctree`.
- `add_missing_atoms.ipynb` ➔ `add_missing_atoms.ipynb.AGENTS.md`
- `add_missing_bonds.ipynb` ➔ `add_missing_bonds.ipynb.AGENTS.md`
- `add_missing_heavy_atoms.ipynb` ➔ `add_missing_heavy_atoms.ipynb.AGENTS.md`
- `add_missing_hydrogens.ipynb` ➔ `add_missing_hydrogens.ipynb.AGENTS.md`
- `add_missing_terminal_cappings.ipynb` ➔ `add_missing_terminal_cappings.ipynb.AGENTS.md`
- `build_peptide.ipynb` ➔ `build_peptide.ipynb.AGENTS.md`
- `editable.ipynb` ➔ `editable.ipynb.AGENTS.md`
- `get_disulfide_bonds.ipynb` ➔ `get_disulfide_bonds.ipynb.AGENTS.md`
- `get_missing_bonds.ipynb` ➔ `get_missing_bonds.ipynb.AGENTS.md`
- `get_missing_heavy_atoms.ipynb` ➔ `get_missing_heavy_atoms.ipynb.AGENTS.md`
- `get_missing_residues.ipynb` ➔ `get_missing_residues.ipynb.AGENTS.md`
- `get_missing_terminal_cappings.ipynb` ➔ `get_missing_terminal_cappings.ipynb.AGENTS.md`
- `get_non_standard_residues.ipynb` ➔ `get_non_standard_residues.ipynb.AGENTS.md`
- `has_hydrogens.ipynb` ➔ `has_hydrogens.ipynb.AGENTS.md`
- `is_solvated.ipynb` ➔ `is_solvated.ipynb.AGENTS.md`
- `make_bioassembly.ipynb` ➔ `make_bioassembly.ipynb.AGENTS.md`
- `make_water_box.ipynb` ➔ `make_water_box.ipynb.AGENTS.md`
- `mutate.ipynb` ➔ `mutate.ipynb.AGENTS.md`
- `remove_overlapping_molecules.ipynb` ➔ `remove_overlapping_molecules.ipynb.AGENTS.md`
- `solvate.ipynb` ➔ `solvate.ipynb.AGENTS.md`
- `solve_atoms_with_alternate_locations.ipynb` ➔ `solve_atoms_with_alternate_locations.ipynb.AGENTS.md`
