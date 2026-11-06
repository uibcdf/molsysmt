(Cookbook_Auditing_Residue_Chemistry)=
# Auditing residue chemistry before repair

*Combining supported atom-gap queries with explicit chemical coverage.*

An empty missing-heavy-atom query can hide an unsupported residue. Inspect both
the gaps and the assessment scope before choosing a repair policy. This narrative
recipe uses bundled data; its executable controls are in the coverage tests.

:::{versionadded} 1.0.0
:::

## Inspect the source inventory

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.pdb'],
                     to_form='molsysmt.MolSys')
missing = msm.build.get_missing_heavy_atoms(molsys)
report = msm.build.get_residue_chemical_coverage(molsys, structure_indices=0)
print(report['summary'])
```

Conversion lets repeated queries reuse the loaded native domains. It does not
establish chemical completeness. Both public queries also accept supported source
forms directly. Group, atom and structure indices refer to the system being queried.

## Separate gaps from unknown chemistry

```python
gaps = [group for group in report['groups'] if group['status'] == 'incomplete']
unknown = [group for group in report['groups'] if group['status'] == 'unassessed']
for group in unknown[:3]:
    print(group['group_index'], group['group_name'], group['reason_codes'])

water = msm.build.get_residue_chemical_coverage(
    molsys, selection="group_name=='HOH'", structure_indices=0)
assert water['groups'][0]['heavy_atoms']['missing_atom_names'] is None
```

Water is outside the exact amino-acid/curated modified-residue template scope;
the `None` inventory makes this explicit. Unsupported modifications and cofactors
receive the same honest treatment. A supported group's empty missing list means
the bounded comparison found no heavy-atom gap, while its protonation, hydrogen
variants or reference orders may still be unassessed.

When querying stored chemistry directly with
{func}`molsysmt.physchem.get_chemical_readiness`, default-reference atom selections
also accept an available external syntax, such as MDTraj `name CA`. The report
retains the declared reference state and sorted unique source atom indices.
For explicit or structure-associated state queries, keep the common selector's
restrictions: use MolSysMT syntax or explicit indices rather than guessing a
state or translating selections downstream. See {ref}`Tutorial_Chemical_Readiness`.

## Preview a reference-rule removal without changing the source

```python
assessment = msm.build.assess_protonation(molsys, pH=7.4)
preview = assessment.to_dict()
print(preview['coverage'])
print(preview['removed_atom_indices'])
retained = preview['atom_map']['output_to_source_atom_indices']
```

This preview reads reference-state naming and connectivity. It does not remove
atoms or select a chemical state. Coverage separates assessed groups from
unsupported or unassessed layouts and states, including when the proposed removal
is empty. The retained array lists original atom indices in proposed output order;
the inverse map has one entry per original atom and uses -1 for removed atoms.
It never matches repeated atom IDs or names.

Keep the assessment when a consumer needs to validate this correspondence before
deliberate publication. Applying it executes the same decision without repeating
the reference-rule query. This recipe stops at the preview; see
{ref}`Tutorial_Protonation_Assessment` for independent output, explicit native
in-place execution, stale-source rejection and the limits of the fixed-pKa model.

## Choose a separate preparation operation

Use the individual reason codes and template identity to decide which gaps can
be handled by {func}`molsysmt.build.add_missing_heavy_atoms` and which need a
different supported template or explicit external chemical assignment. This
recipe does not perform a repair or select a protonation state. Reassess after
an authorized transformation; do not convert unknown chemistry into neutral
charges, empty hydrogen expectations or an assumed covalent graph.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Residue_Chemical_Coverage` — coverage dimensions and limits.
- {ref}`Tutorial_Chemical_Readiness` — stored fields in the nested assessment.
- {ref}`user-foundations-molecular-system-definition` — forms and partial domains.
:::

## Checking the source vocabulary

Declare a known group vocabulary on Topology before interpreting ambiguous names.
The coverage report keeps undeclared ambiguous groups unassessed; native expectation
queries and preparation require context. An Amber HID reference and a CCD HID
component cannot share a cached template. Verification of a reference inventory
still does not establish placement support or environmental protonation. Consult
{ref}`user-foundations-group-naming-schemes` and the executed
{ref}`Tutorial_Get_expected_heavy_atoms` and
{ref}`Tutorial_Get_expected_hydrogens` examples.

When you construct a peptide, retain its producer declaration instead of guessing
it later from its native class. Group conventions do not force atom conventions:
checked historical and Amber construction H layouts can differ. Inspect coverage
candidates and `variant_sources` when names differ; do not treat an alternative
H name as proof that another physical hydrogen is missing. See
{ref}`Tutorial_Build_peptide` for exact-label construction and its limits.

Before exporting that vocabulary to a representation that only stores labels,
inspect `msm.get_conversion_report()` or request `strict=True` in `msm.convert()`.
A PDB round trip can keep a group name while losing its source convention.
Use native inventory, a supported typed dictionary or H5MSM when that declaration
must accompany the system. See {ref}`Tutorial_Get_Conversion_Report`.

If an output gains missing naming context, the existing policy invalidates its
evaluated interaction coverage. Preflight reports that invalidation, including
an analysis evaluated without occurrences; it leaves the original system and its
snapshots intact. Review the report before deciding whether to export normally
and recalculate, or retain an already declared compatible source.
