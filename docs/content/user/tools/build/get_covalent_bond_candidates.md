(Tutorial_Covalent_Bond_Candidates)=
# Get covalent bond candidates

*Inspecting exact heavy-atom group-template candidates without changing chemistry.*

Use {func}`molsysmt.build.get_covalent_bond_candidates` to obtain candidate
intra-group edges and inspect their coverage before choosing a repair policy.
The experimental method `exact_heavy_group_templates` reuses the existing
{ref}`exact-template auditor <Tutorial_Residue_Chemical_Coverage>`.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

See {func}`molsysmt.build.get_covalent_bond_candidates` for arguments and errors.
:::

## Understanding the result

The detached dictionary uses schema `molsysmt.covalent_bond_candidates@1`.

| Field | Meaning |
| :--- | :--- |
| `bonded_atom_pairs` | Sorted candidate pairs on the source atom axis, with shape `(n_candidates, 2)` and `int64` dtype. |
| `group_indices` | The source group index for each candidate row. |
| `missing_mask` | Boolean per row: no stored edge has these endpoints. An existing edge is not thereby certified as covalent. |
| `groups` | Template identity/hash, whole-group atom indices, candidate count, exclusions and blocked endpoint names. |
| `coverage` | The complete detached audit that supports the candidate decision, including stored edge evidence and unresolved chemistry. |
| `structure_index`, `chemical_state_index` | Selected source indices; no structure index is fabricated for topology-only input. |
| `method`, `rule_version`, `software` | The executed rule and original producer versions. |

All candidates have evidence `inferred_candidate`; this is distinct from a
file-declared covalent bond. Arrays remain typed and correctly shaped when empty.
Source indices are positions, and group/structure IDs remain separate labels.

## Choosing atoms, a structure and a state

Integer selections are **atom indices**. Both endpoints of a returned pair must
be selected. Whole containing groups are audited to detect ambiguous naming or
conflicting stored chemistry; atoms outside the selection are not returned as
candidate endpoints. Repeated selections do not duplicate pairs.

Choose one structure for a source with multiple structures. A topology without
coordinates can still provide exact template candidates. No geometry is used
to propose bonds; the nested audit reports coordinate coverage in nm independently
of your configured length units. Numeric/all H5MSM 0.5 queries read the selected
coordinate structure; rich selections follow the source form's public behavior.
PDB parsing remains eager and disables existing reader bond inference.

Choose the chemical state explicitly when needed. Numeric/all selections can
still identify atoms when that state is unresolved; the groups then remain
unassessed. A rich selection that requires an unavailable state cannot be evaluated.

## Understanding coverage

| Group status | Meaning |
| :--- | :--- |
| `assessed` | The bounded mapping and template candidate comparison ran. This does not certify the stored chemical graph. |
| `partial` | Some reference edges have missing endpoint names; only mapped pairs are returned. |
| `unassessed` | No exact template, ambiguous names, unknown/conflicting heavy elements, unresolved state or contradictory stored intra-group chemistry blocks candidates. |

The method covers exact names in the amino-acid database and the auditor's
curated MSE, SEP, TPO and MLY heavy templates. It never replaces a modified group
with its sequence parent. Template identity retains the packaged resource hash
and available reference provenance. The legacy database's original-source
provenance can remain unassessed.

Water, ions, lipids and arbitrary small molecules remain unassessed in this first
method. It does not infer hydrogen edges, links between groups, disulfides or
metal coordination. Bond orders, protonation and valence remain unassessed.
Nonconsecutive group/chain identity cannot authorize a polymer link here because
this method proposes no inter-group links at all.

## Reviewing before preparation

The function does not append candidate edges or modify coordinates, chemical
assignments or named interaction analyses. Preserve the report when choosing a
subsequent, explicit preparation policy. Its `missing_mask` differs from the
legacy {func}`molsysmt.build.get_missing_bonds`, which combines templates with
geometric fallback and optional inter-group candidates.

This is a reusable building block for a qualified native PDB inference route;
it does not change the PDB reader's default or select a chemical state for you.
See the {ref}`PDB connectivity recipe <cookbook-pdb-connectivity-policy>`.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Residue_Chemical_Coverage`
- {ref}`Tutorial_Get_missing_bonds`
- {ref}`Tutorial_Chemical_Templates`
:::
