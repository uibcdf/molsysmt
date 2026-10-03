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
forms directly. Group, atom and frame indices refer to the system being queried.

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
