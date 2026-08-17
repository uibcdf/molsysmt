# Sub-Portal Governance: tools/topology/index.md

## Purpose
Governance rules for `docs/content/user/tools/topology/index.md` (the Topology Tools sub-portal entrance page).

## Structural Invariants
1. **Title**: `# Topology`
2. **Catalog Table**: 2-column catalog table listing all topology tools with Markdown link titles and brief gerund descriptions.
3. **Hidden toctree**:
   ```rst
   .. toctree::
      :maxdepth: 2
      :hidden:

      get_bondgraph.ipynb
      get_covalent_blocks.ipynb
      get_covalent_paths.ipynb
      get_dihedral_quartets.ipynb
      get_sequence_alignment.ipynb
      get_sequence_identity.ipynb
   ```
