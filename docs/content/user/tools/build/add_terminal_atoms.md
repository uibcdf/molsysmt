(Tutorial_Add_Terminal_Atoms)=
# Attaching terminal atoms

*Expanding a native system without reordering its existing atom axis.*

Use {func}`molsysmt.build.add_terminal_atoms` when you have already decided the
new atoms, their existing parents and their coordinates. This general tool does
not predict chemistry or generate geometry. It accepts supported forms with
native-compatible topology, exactly one chemical state and coordinates, and
returns a detached native system and a `molsysmt.terminal_attachment@1` report.
It requires neither RDKit nor Ackredit.

:::{admonition} API documentation

{func}`molsysmt.build.add_terminal_atoms`
:::

:::{versionadded} 1.0.0
:::

Each record requires `parent_atom_index` and `atom_type` (a chemical element
symbol). Optional `atom_name`, string/numeric `atom_id`, `isotope`,
`bond_order` (integer 1, 2 or 3) and `chemical_attributes` declare identity and
canonical ChemicalStates assignments. Each new atom has one covalent bond to an
existing parent and inherits its group, chain and component membership.
Atoms are appended in record order. Explicit IDs must not collide; absent IDs
are synthesized deterministically and stored as strings. Existing IDs are retained.

Provide a length quantity with shape `(n_structures, n_new_atoms, 3)` covering
**every** source structure. PyUnitWizard converts units explicitly to native nm.
Existing positions and indices are retained, and `atom_correspondence` and
`parent_atom_pairs` have integer shape `(n_original, 2)` and `(n_new, 2)`.
This boundary deliberately does not accept a multi-state source or bonds between
new atoms; explicitly choose a different construction workflow for those cases.

The `attribute_policy` and named-interaction rules are the same as
{ref}`Tutorial_Fixed_State_Hydrogens`: strict rejects unsupported attributes,
intersection reports their removal, and analyses become unevaluated after atom
expansion. Sparse alternate locations retain their old indices. Empty records
with coordinates of shape `(n_structures, 0, 3)` return an unchanged independent
copy. Success and failure leave the source unchanged.

Each successful operation, including empty addition, also retains an independent
report in the output's ChemicalStates preparation history. Retrieve it with
`output.chemical_states.get_preparation_history()`. The report declares the
original source atom/structure counts, all examined `structure_indices` as `int64`,
attribute policy, producing MolSysMT version and `coordinate_evidence='supplied_coordinates'`.
Coordinates use the report's fixed `nm` protocol; the report does not duplicate
coordinate arrays. This records attachment, not a new scientific geometry calculation.
H5MSM 0.5 and `ChemicalStatesDict` preserve these records without recalculating them.

Historical indices belong to the original operation, even after extraction or
reordering. They are not remapped or certified as current. Import an isolated
producer's evidence with `output.chemical_states.append_preparation_history(records)`
when needed; this archives independent copies without applying chemistry, aligning
atoms/structures or verifying authenticity. Records append in caller order and
retain their original dimensions. Keep intervening maps separately.

Attachment preserves existing parent chemical fields, including virtual H
counts. When materializing a declared H inventory, explicitly update those counts
after checking the generated-parent map; indexed H and virtual H are distinct.
The public {ref}`reinsertion recipe <cookbook-component-hydrogen-reinsertion>`
composes this tool with fixed-state generation and `msm.set()` without moving
existing atoms. It also makes attribute-loss and global-completeness limits
explicit. No general component-replacement engine is implied by this tool.

:::{seealso}

{ref}`Tutorial_Fixed_State_Hydrogens` generates missing H on a prepared pose.
:::
