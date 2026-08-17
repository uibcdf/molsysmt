# Sub-Portal Governance: tools/structure/index.md

## Purpose
Governance rules for `docs/content/user/tools/structure/index.md` (the Structure Tools sub-portal entrance page).

## Structural Invariants
1. **Title**: `# Structure`
2. **Catalog Table**: 2-column catalog table listing all 26 structure tools (including `get_secondary_structure.ipynb`) with Markdown link titles and brief gerund descriptions.
3. **Hidden toctree**:
   ```rst
   .. toctree::
      :maxdepth: 2
      :hidden:

      align_principal_axes.ipynb
      center.ipynb
      flip.ipynb
      get_angles.ipynb
      get_center.ipynb
      get_contacts.ipynb
      get_dihedral_angles.ipynb
      get_distances.ipynb
      get_least_rmsd.ipynb
      get_maximum_distances.ipynb
      get_minimum_distances.ipynb
      get_neighbors.ipynb
      get_principal_axes.ipynb
      get_radius_of_gyration.ipynb
      get_rmsd.ipynb
      get_rmsf.ipynb
      get_secondary_structure.ipynb
      least_rmsd_align.ipynb
      least_rmsd_fit.ipynb
      move_away.ipynb
      principal_component_analysis.ipynb
      rotate.ipynb
      set_dihedral_angles.ipynb
      shift_dihedral_angles.ipynb
      show_contacts.ipynb
      translate.ipynb
   ```
