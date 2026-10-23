(Tutorial_Merge_Nonpolar_Hydrogens)=
# Merging nonpolar hydrogens

*Projecting an explicitly typed molecular representation with conserved charge.*

{func}`molsysmt.build.merge_nonpolar_hydrogens` creates a detached native system.
It merges AutoDock4 `H` atoms into their bonded parents and retains `HD` atoms.
The labels supply this policy; atom names do not. This is an experimental
representation transform, not a protonation, charge-calculation or force-field
parameterization method.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.build.merge_nonpolar_hydrogens`
:::

## Preparing explicit inputs

The transform needs complete single-state connectivity, elements, explicit
AutoDock4 labels and finite per-atom charges. Merged H must be neutral,
nonradical, nonisotopic and single-bonded to a retained heavy atom. Their parents
need known virtual explicit-H counts and zero implicit-H counts. Unknown counts
are not assumed to be zero.

This example explicitly uses optional RDKit to prepare the stored H inventory
and named typing/charge models. The merge itself needs no RDKit or Meeko:

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'], to_form='rdkit.Mol')
molsys = msm.build.assign_autodock_atom_types(molsys, typing_scheme='autodock4')
molsys = msm.build.assign_partial_charges(molsys, method='gasteiger_marsili')
projection = msm.build.merge_nonpolar_hydrogens(
    molsys, typing_scheme='autodock4', return_report=True)
assert molsys.get_n_atoms() == 24
assert projection['molecular_system'].get_n_atoms() == 14
```

All source coordinates, labels, charges and analyses remain unchanged. The
output retains selected structures and the surviving atom IDs. Parent virtual
explicit-H counts increase by the merged H count, and further implicit-H
inference is disabled for those parents. No H coordinate is generated.
Output analyses are cleared after a merge: changing atom representation and
charges requires recalculating analyses on the derived system.

## Reading the maps

The report has schema `molsysmt.atom_projection@1` and compact NumPy arrays:

| Field | Meaning |
| --- | --- |
| `output_to_source_atom_indices` | Source index of each retained output atom. |
| `source_to_output_atom_indices` | Direct output index, or -1 for an absent source atom. |
| `source_atom_status` | `retained`, `merged` or `omitted`. |
| `merged_source_atom_pairs` | Merged H source index and receiving parent source index. |
| `charge_transfers` | Full-precision charge transferred for each pair. |
| `omitted_source_atom_indices` | Atoms outside the requested selection. |
| `source_structure_indices` | Original structure indices in output order. |

Indices are positions; IDs are labels. Both source/output IDs and names are
retained as provenance. A merged H has **no direct output coordinate index**;
the parent relation does not turn the parent's position into an H position.
Charges and conservation tolerances use the report's explicit
`charge_unit='elementary_charge'`, independent of the active unit policy.

Selections are sorted and deduplicated. If a selected H's parent is excluded,
the operation fails. It does not transfer charge across the selection boundary.
Selected and full-source charge totals are separate fields; charge is conserved
over the selected scope before any file rounding, without renormalization.

## Retaining calculation provenance

`molecular_mechanics.partial_charge_assignment` identifies the result as
`nonpolar_hydrogen_charge_aggregation`, with status `derived`. Its nested
`source_assignment` preserves the original calculation, software versions,
parameters and attribution. A merged value is not relabelled as a fresh
Gasteiger or force-field calculation. Existing named typing is inherited and
rebound as a derived assignment, without reclassifying isolated fragments.
Copying and pickle preserve these reports. Writers detect stale chemistry,
labels or numeric charge changes through their existing binding checks.

The terminal charge-transfer contract was inspected in
[Meeko 0.8.0](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/molsetup.py).
MolSysMT implements this bounded transform independently; no Meeko code is
copied or executed. Reports retain this reference and optional Ackredit records
it as a reference implementation. Original charge calculations are retained as
provenance, without claiming that they executed again during merging.

## Recording the written order

The ordinary PDBQT writer retains every atom of its input. Export the derived
system explicitly and opt into a **completed** export map:

```python
text, exported = msm.convert(
    projection['molecular_system'], to_form='string:pdbqt_text',
    structure_indices=[0], typing_scheme='autodock4', return_atom_map=True)
original_indices_in_written_order = projection['report'][
    'output_to_source_atom_indices'][exported['output_to_source_atom_indices']]
assert len(original_indices_in_written_order) == 14
```

File output also returns `(destination, map)` with `return_atom_map=True`.
The default return is unchanged. With the separate `return_report=True` option,
the public converter returns `((destination, map), conversion_report)`.
The latter remains a preflight fidelity report; it is not the completed map.

The export map has schema `molsysmt.atom_export@1`. Its source indices refer to
the complete system passed to the writer, including when selecting a subset.
It records actual written atom order/serials/names, ordered ROOT membership,
first ROOT atom, oriented branch pairs and the parsed torsion tree. These are
representation facts, not a choice of a scientifically optimal ROOT protocol.
It also records full-precision and rounded charges in written order, three-digit
charge precision, the total rounding bound and a SHA-256 of the actual payload
(excluding the `pdbqt_text:` prefix). Rounding is reported, never corrected by
renormalizing charge.

For a selected atom export, mapping composition is ordinary array indexing as
above. A caller may explicitly rename atoms before export; the projection's
original names and the export's written names remain linked by source indices.
The writer never truncates names. Names may repeat; identity is carried by
unique serial IDs. Width violations and invalid serial IDs fail before opening
the output. This operation does not discover a match to an unrelated molecule.

## Saving the report

The versioned dict contains arrays and primitive metadata, without a dictionary
per atom. Convert its arrays explicitly when saving JSON:

```python
import json

encoded = json.dumps(projection['report'], default=lambda value: value.tolist())
restored_report = json.loads(encoded)
assert restored_report['schema'] == 'molsysmt.atom_projection@1'
```

The schema identifies axes, units and meaning; JSON arrays must be restored to
the documented integer/float/string types by a receiving application. Loading a
report does not authenticate correspondence or rerun its calculation.

:::{warning}
This bounded transform rejects multiple chemical states, unknown parent H
inventories, isotope-labelled/charged/radical merged H and force-field settings
beyond per-atom charges and types. It does not derive bonded parameters for a
united-atom force field. It copies selected structures into resident memory.
H5MSM 0.5 does not persist MolecularMechanics or these mechanical assignments;
use a separate report until that domain has a supported persistence contract.
Maps refer to the prepared input supplied here. Atoms generated in an earlier
preparation step need that step's own provenance/map when tracing further back;
this transform does not invent pre-preparation source IDs. Multi-MODEL PDBQT
pose reconstruction remains separate work.
:::

:::{seealso}
:class: dropdown

- {func}`molsysmt.build.assign_autodock_atom_types`
- {func}`molsysmt.build.assign_partial_charges`
- {func}`molsysmt.physchem.get_hydrogen_inventory`
- {ref}`cookbook-native-pdbqt`
:::
