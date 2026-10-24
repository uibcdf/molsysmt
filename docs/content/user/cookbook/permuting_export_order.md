(Cookbook_Permuting_Export_Order)=
# Restoring atom order

*Reordering a known export axis while retaining molecular correspondence.*

A producer may deliberately traverse atoms in a different order. When its exact
bijection is known, apply it to all supported molecular domains with
{func}`molsysmt.basic.permute_atoms`. Do not infer correspondence from matching
counts, coordinates or atom names. This recipe uses a reverse traversal so the
expected mapping is independent of any writer's implementation.

:::{versionadded} 1.0.0
:::

## Recording the traversal

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'])
order = list(range(molsys.get_n_atoms() - 1, -1, -1))
transformed = msm.permute_atoms(molsys, order, return_report=True)
molsys_reordered = transformed['molecular_system']
assert transformed['report']['output_to_source_atom_indices'].tolist() == order
```

This changes the whole molecular atom axis, including stored bond references.
It does not add coordinates, establish chemical equivalence or recalculate a
scientific assignment. Keep the original preparation/export reports; their axes
remain historical. Use {func}`molsysmt.basic.compose_atom_maps` to compose the
new transform at its actual position in a workflow.

## Restoring and saving

```python
from tempfile import TemporaryDirectory
from pathlib import Path
molsys_restored = msm.permute_atoms(molsys_reordered,
    transformed['report']['source_to_output_atom_indices'])
assert molsys_restored.topology.atoms.atom_name.tolist() == molsys.topology.atoms.atom_name.tolist()
with TemporaryDirectory() as directory:
    path = Path(directory) / 'restored.h5msm'
    msm.convert(molsys_restored, to_form=path)
    loaded = msm.convert(path, to_form='molsysmt.MolSys')
    assert loaded.topology.atoms.atom_id.tolist() == molsys.topology.atoms.atom_id.tolist()
```

H5MSM 0.5 retains supported structural, topological, chemical and named interaction
domains. It does not persist experimental MolecularMechanics. The returned map
is a sidecar, not a new molecular-file domain. Reordering a complete result
requires resident output memory even though coordinates are read in blocks.
Unsupported native extensions fail before publication of an output.

:::{admonition} Related Tools & References
:class: dropdown seealso

- {ref}`Tutorial_Permute_Atoms`: full permutation contract and limits.
- {ref}`Tutorial_Compose_Atom_Maps`: composition of declared preparation/export maps.
- {ref}`user-foundations-native-world-classes-molsysmt-molsys`: native domain ownership.
:::
