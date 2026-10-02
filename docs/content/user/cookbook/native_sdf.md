(cookbook-native-sdf)=
# Reading and writing native SDF

*Exchanging explicit small-molecule chemistry without installing RDKit.*

You can read a single V2000 or V3000 SDF record into native domains and write
one selected structure back to SDF. This experimental adapter retains source
hydrogens and explicit chemistry. It does not prepare a ligand for docking.

## Reading a molecule

```python
import molsysmt as msm

source = msm.systems['caffeine']['caffeine.sdf']
molsys = msm.convert(source, to_form='molsysmt.MolSys')
assert molsys.topology.n_atoms == 24
assert molsys.topology.n_bonds == 25
```

The ten source hydrogens remain atoms. Formal charges and bond orders belong
to `chemical_states`; coordinates belong to `structures`. SDF declares
coordinates in angstroms. Native structures store nanometers, and writing
converts explicitly back to angstroms regardless of your unit policy.

## Writing and selecting

```python
msm.convert(molsys, to_form='caffeine.sdf', ctfile_version='V3000')
msm.convert(molsys, selection=[0, 2, 4], to_form='selected.sdf')
```

With multiple structures, select exactly one using `structure_indices=[index]`.
Without that selection, output fails. MolSys extraction with topology orders
selected atoms by ascending source index; connectivity and coordinates use the
same map. Output atom/bond serials are newly assigned sequential integers;
they are read back as string IDs. V2000 writes four decimal places in coordinate
fields and supports at most 999 atoms or bonds. Use V3000 for larger tables.

## Inspecting information loss

```python
output, report = msm.convert(molsys, to_form='caffeine_report.sdf',
                             return_report=True)
print(report.outcome, report.is_exhaustive)
```

SDF cannot retain arbitrary native IDs/names, residue/chain hierarchy, partial
charges, force-field parameters, interaction analyses or extra structural
fields. Reports check chemical capabilities and selected native losses, but
cross-form audits are not exhaustive. `strict=True` rejects detected losses
before writing.

If your source has SD property blocks, ordinary native conversion raises an
error because MolSys has no general storage for them yet. You can explicitly
authorize their loss with `discard_properties=True`; `return_report=True`
lists that loss, and strict mode still rejects it. To preserve source bytes and
properties, use `msm.copy(source, output_filename='source_copy.sdf')`.

:::{warning}
The native subset rejects stereochemical flags/labels, query atoms/bonds,
valence overrides, reaction maps, Sgroups and unsupported radical/bond types.
Writing rejects atom aromaticity that the supplied bond types cannot retain.
It does not sanitize valence, infer hydrogen counts, perceive aromaticity from
Kekule bonds or derive CIP labels from 3D coordinates. Multiple SDF records
are rejected. Keep the original file when it carries unsupported information.
:::

:::{seealso}
:class: dropdown

- {func}`molsysmt.basic.convert` for form conversion and reports.
- {func}`molsysmt.basic.get` for form-independent attribute queries.
- {ref}`user-foundations-support-forms-files` for supported file forms.
:::
