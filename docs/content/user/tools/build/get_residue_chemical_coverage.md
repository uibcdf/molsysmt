(Tutorial_Residue_Chemical_Coverage)=
# Get residue chemical coverage

*Comparing stored residue chemistry with exact supported templates.*

Use this experimental report to find missing heavy atoms, unexpected names and
stored connectivity conflicts before choosing a preparation operation. Every
selected group appears in the report, including unsupported residues and cofactors.
The source remains unchanged.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

See {func}`molsysmt.build.get_residue_chemical_coverage` for arguments and errors.
:::

## Basic usage

Inspect the bundled T4 lysozyme structure without requiring a manual conversion:

```python
import molsysmt as msm

molsys = msm.systems['T4 lysozyme L99A']['181l.pdb']
report = msm.build.get_residue_chemical_coverage(molsys, structure_indices=0)
print(report['summary'])
unknown = [group for group in report['groups'] if group['status'] == 'unassessed']
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See the {ref}`bundled systems <user-foundations-entrance-demo-systems>` catalog.
:::

The detached dictionary has schema `molsysmt.residue_chemical_coverage@1`. Group,
atom, bond and structure indices refer to the source; group IDs are separate string
labels. NumPy index arrays retain integer types for empty selections.

| Group status | Meaning |
| :--- | :--- |
| `assessed` | Supported, bounded inventory and stored-graph comparisons ran without a known discrepancy. Consult the individual dimensions for remaining unknowns. |
| `incomplete` | A supported comparison found missing/unexpected atoms, an element conflict, a stored-graph discrepancy or a reference-order conflict. |
| `unassessed` | No exact template, ambiguous atom-name correspondence or unresolved chemical state prevents assessment. |

Each group includes `reason_codes`, `template`, `heavy_atoms`, `hydrogens`,
`connectivity`, `protonation`, `atom_indices` and `boundary_bond_indices`.
An unsupported group has `template=None` and unknown inventories represented by
`None`; an empty list of missing atoms means a comparison actually ran.

## Selecting whole groups

Integer selections are **group indices**, not atom indices or residue IDs. Results
are sorted and deduplicated. A string selects atoms through the ordinary selection
machinery and inspects every whole group containing those atoms:

```python
selected = msm.build.get_residue_chemical_coverage(
    molsys, selection=[2, 0, 2], structure_indices=0)
water = msm.build.get_residue_chemical_coverage(
    molsys, selection="group_name=='HOH'", structure_indices=0)
assert selected['group_indices'].tolist() == [0, 2]
assert water['groups'][0]['reason_codes'] == ['no_exact_residue_template']
```

Pass `syntax` when using another supported selection language. Required group
membership and atom names must be available in the source form. A coordinate-only
system or an ungrouped ligand cannot acquire an invented residue hierarchy through
this operation.

## Choosing a state and structure

Select at most one structure when coordinates exist. With several chemical states,
use `chemical_state` to choose an explicit state index, `'reference'`, or
`'structure'` to resolve the chosen frame's association. Ambiguous references and
unassociated structures remain explicitly unassessed; the first state is never
selected as a substitute. A source without structures can still be inspected.

The nested `chemical_readiness` report preserves stored fields, their coverage,
edge evidence and limited integrity checks. Coordinate finiteness is checked
through PyUnitWizard in nm, independent of your configured length unit; no
coordinates are returned or retained by the report. Numeric H5MSM 0.5 selections
read the selected frame and atom rows through the existing bounded reader. Rich
string selections retain the source form's public selection behavior and may
require broader loading.

## Understanding chemical limits

Exact names in the amino-acid database and curated **MSE, SEP, TPO and MLY** heavy
templates are supported. A sequence alias does not authorize substitution of a
parent residue: MSE uses selenium, and SEP/TPO retain their phosphate atoms. Other
modifications and cofactors remain unassessed. Template identity records the
packaged resource hash and available source provenance. Reference elements are
declared in curated templates or identified as standard atom-name mappings in the
legacy database.

Duplicate or absent atom names prevent a unique correspondence. Missing terminal
`OXT` is outside this comparison when it is not observed; peptide breaks and group
order do not establish biological termini.

Connectivity compares **stored intra-group heavy covalent relationships**. Crossing
bonds are recorded by source index without validating inter-group chemistry.
Existing untyped edges are unknown, rather than silently treated as absent or
covalent. Missing endpoint names block the relevant template edge comparison.
Reference bond orders are available only for the curated modified templates;
unknown stored orders remain unknown, and differing declared orders are conflicts.
This comparison does not normalize resonance or alternative Kekulé assignments.

Hydrogen inventories remain separate from environmental protonation. The report
retains each compatible amino-acid variant and its missing/unexpected H names;
it never chooses a protomer by minimizing the missing-H count. Differing variants
remain unassessed. Heavy-only modified templates cannot establish H coverage.
Explicit H atoms and stored virtual/implicit H counts remain distinct observations.

:::{warning}
`assessed` is not a chemical validity certificate or permission to dock. Consult
the individual dimensions and `unassessed_checks`: environmental protonation,
terminal context, valence, aromaticity perception, repair placement and force-field
coverage are not validated here. No atoms, bonds, charges or protonation states
are added or changed.
:::

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Chemical_Readiness` — {func}`molsysmt.physchem.get_chemical_readiness`
  inspects stored fields without a residue-template comparison.
- {func}`molsysmt.build.get_missing_heavy_atoms` queries supported heavy-atom gaps.
- {func}`molsysmt.build.add_missing_heavy_atoms` performs a separate explicit repair.
- {ref}`Cookbook_Auditing_Residue_Chemistry` combines inventory and coverage queries.
:::
