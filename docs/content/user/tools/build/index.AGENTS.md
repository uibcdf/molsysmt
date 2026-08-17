# Sub-Portal Governance: tools/build/index.md

## Purpose
Governance rules for `docs/content/user/tools/build/index.md` (the Build Tools sub-portal entrance page).

## Structural Invariants
1. **Title**: `# Build`
2. **Catalog Table**: 2-column catalog table listing all 20 build tools with Markdown link titles and brief gerund descriptions.
3. **Hidden toctree**:
   ```rst
   .. toctree::
      :maxdepth: 2
      :hidden:

      add_missing_bonds.ipynb
      add_missing_heavy_atoms.ipynb
      add_missing_hydrogens.ipynb
      add_missing_terminal_cappings.ipynb
      build_peptide.ipynb
      editable.ipynb
      get_disulfide_bonds.ipynb
      get_missing_bonds.ipynb
      get_missing_heavy_atoms.ipynb
      get_missing_residues.ipynb
      get_missing_terminal_cappings.ipynb
      get_non_standard_residues.ipynb
      has_hydrogens.ipynb
      is_solvated.ipynb
      make_bioassembly.ipynb
      make_water_box.ipynb
      mutate.ipynb
      remove_overlapping_molecules.ipynb
      solvate.ipynb
      solve_atoms_with_alternate_locations.ipynb
   ```
