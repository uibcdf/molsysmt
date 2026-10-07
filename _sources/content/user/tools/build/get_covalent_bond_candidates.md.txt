(Tutorial_Covalent_Bond_Candidates)=
# Get covalent bond candidates

*Inspecting heavy-atom or observed-hydrogen template candidates without changing chemistry.*

Use {func}`molsysmt.build.get_covalent_bond_candidates` to obtain candidate
intra-group edges and inspect their coverage before choosing a repair policy.
Both experimental methods reuse the existing
{ref}`exact-template auditor <Tutorial_Residue_Chemical_Coverage>`.
The default `exact_heavy_group_templates` returns heavy intra-group pairs.
Choose `method='observed_hydrogen_template_consensus'` for a separate report of
candidate bonds between already observed H atoms and their heavy parents.

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
| `partial` | Some reference edges have missing endpoints, or observed H names or their joint inventory remain unassessed; only eligible mapped pairs are returned. |
| `unassessed` | No exact template, ambiguous names, unknown/conflicting heavy elements, unresolved state or contradictory stored intra-group chemistry blocks candidates. |

The method covers exact names in the amino-acid database and the auditor's
curated MSE, SEP, TPO and MLY heavy templates. It never replaces a modified group
with its sequence parent. Template identity retains the packaged resource hash
and available reference provenance. The legacy database's original-source
provenance can remain unassessed.

Water, ions, lipids and arbitrary small molecules remain unassessed in this first
method. The default does not infer hydrogen edges. Neither method infers links between groups, disulfides or
metal coordination. Bond orders, protonation and valence remain unassessed.
Nonconsecutive group/chain identity cannot authorize a polymer link here because
this method proposes no inter-group links at all.

For a separate bounded peptide-link report, use
{ref}`Tutorial_Peptide_Bond_Candidates`. It preserves the same source axes while
adding explicit adjacency, chain, geometry and alternate-site criteria.

## Inspecting observed hydrogen parents

```python
report = msm.build.get_covalent_bond_candidates(
    molsys, structure_indices=0,
    method='observed_hydrogen_template_consensus',
)
```

This method returns only H-parent candidates. It does not add H atoms or place
coordinates. For each existing H name, every heavy-compatible reference variant
containing that **exact name** must agree on the same single heavy parent.
Both elements must be known and compatible, and the parent must exist in the
group. It does not select the first variant, interpret aliases or choose the
nearest atom. The curated modified-group heavy templates provide no H reference.

Conflicting stored H partners, noncovalent types, nonsingle orders or aromatic
bonds block that H. A known nonzero H formal charge, radical count, virtual H
count or aromatic assignment also blocks it; unknown assignments stay unknown.
Stored incident edges outside the atom selection still participate in these
checks. Whole-group heavy-template and chemical-state exclusions continue to
apply. Other recognized H names can remain eligible when one H is unassessed.

Each `groups` entry adds a `hydrogen_coverage` record:

| Field | Meaning |
| :--- | :--- |
| `atom_indices`, `parent_atom_indices` | Parallel `int64` arrays of observed source H indices and reference parents; an unresolved parent is `-1`. |
| `eligible_mask` | Boolean per H: the local criteria passed, independently of the output selection. |
| `selected_mask` | Boolean per H: both mapped endpoints belong to the requested atom selection; eligibility is checked separately. |
| `variant_offsets`, `variant_indices` | CSR arrays identifying exact reference variants consulted for each H. Row `i` uses `variant_indices[variant_offsets[i]:variant_offsets[i+1]]`. |
| `joint_variant_indices` | Reference variants containing the entire observed H-name inventory. |
| `inventory_status` | `compatible_subset` when a joint naming inventory is supported, otherwise `unassessed`. This does not assess missing H atoms or protonation. |
| `issues` | Sparse failed-H records with source index, name, possible reference parent names and reason codes. |

Local parent consensus and a coherent whole-group inventory are separate evidence.
Mixed naming conventions may produce useful local candidates while no single
reference variant contains all the observed names; the group then remains
`partial`. Even `compatible_subset` does not establish a complete protonation
state, terminal assignment, valence or correct H placement. Review both the pairs
and the exclusions before adopting any reconstruction policy.

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
