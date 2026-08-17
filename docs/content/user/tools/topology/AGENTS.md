# Sub-Portal Governance: `tools/topology/` (`AGENTS.md`)

This guide governs all content under `docs/content/user/tools/topology/`.

---

## 🧭 Subdirectory Purpose & Scope
Houses tutorial units for covalent connectivity, molecular graphs, connected components, covalent paths, sequence alignment, sequence identity, and dihedral angle quartets.

## 🧬 Scientific & Architectural Invariants for Topology Tutorials
1. **Graph Representation**:
   - Covalent bond graphs must interface cleanly with NetworkX (`to_form='networkx.Graph'`) and illustrate 2D connectivity visualization with atom labels.
2. **Dihedral Definitions & Blocks**:
   - Dihedral quartets follow IUPAC/standard structural definitions for backbone ($\\phi, \\psi, \\omega$) and sidechains ($\\chi_1 - \\chi_5$).
   - Tutorials illustrating `with_blocks=True` must explain and visualize the partition into rigid rotating blocks around the rotatable bond.
3. **Sequence Analysis**:
   - Sequence tools must illustrate both prettyprinted visual alignments and structured identity matrices.

## 📄 Pages List & Paired Micro-`AGENTS.md` Files
- `index.md` ➔ `index.AGENTS.md`: Index portal with 2-column function catalog table and hidden `toctree`.
- `get_bondgraph.ipynb` ➔ `get_bondgraph.ipynb.AGENTS.md`
- `get_covalent_blocks.ipynb` ➔ `get_covalent_blocks.ipynb.AGENTS.md`
- `get_covalent_paths.ipynb` ➔ `get_covalent_paths.ipynb.AGENTS.md`
- `get_dihedral_quartets.ipynb` ➔ `get_dihedral_quartets.ipynb.AGENTS.md`
- `get_sequence_alignment.ipynb` ➔ `get_sequence_alignment.ipynb.AGENTS.md`
- `get_sequence_identity.ipynb` ➔ `get_sequence_identity.ipynb.AGENTS.md`
