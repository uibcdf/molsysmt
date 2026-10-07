(Tutorial_Hydrogen_Inventory)=
# Inspecting hydrogen inventory

*Separating indexed H atoms from virtual hydrogen annotations.*

{func}`molsysmt.physchem.get_hydrogen_inventory` reads a selected chemical state
from any supported form with the necessary assignments. It never changes the
source, fills missing counts, predicts protonation or requires RDKit.

:::{admonition} API documentation

{func}`molsysmt.physchem.get_hydrogen_inventory`
:::

:::{versionadded} 1.0.0
:::

For each selected atom, `indexed_hydrogen_counts` counts its covalent indexed H
neighbors. `missing_hydrogen_counts` is the sum of stored `n_implicit_hydrogens`
and `n_explicit_hydrogens`: both are virtual annotations, not indexed atoms.
`total_hydrogen_counts` adds the two kinds. Unknown stored counts and unknown
totals are **-1**, not zero. All counts are dimensionless int64 arrays aligned to
`atom_indices`. `parent_hydrogen_pairs` has integer shape `(n_pairs, 2)`, parent
first, and retains only pairs whose parent is selected. A selected indexed H is
listed separately in `explicit_hydrogen_atom_indices`.

The full graph is inspected before output selection. Integer atom selections
are deduplicated and returned in sorted order; empty results have defined types
and shapes. `chemical_state='structure'` resolves the single selected frame's
association. Structure indices are zero-based indices, not structure IDs.

The detached `molsysmt.hydrogen_inventory@1` report can be `available`,
`unassessed`, `conflict` or `empty`. Read its indexed issues and remaining
`unassessed_checks`. Available certifies that this inventory is readable;
**valence, protonation and coordinate quality are not independently validated**.
A graph with existing H but missing virtual counts remains unassessed rather than
being declared complete. Do not use this inventory alone as a hydrogen-addition
or chemical-readiness certification.

:::{seealso}

- {ref}`Tutorial_Chemical_Readiness` — inspecting additional stored fields.
- {ref}`Tutorial_Fixed_State_Hydrogens` — materializing a validated fixed inventory.
:::
