(Cookbook_Aligning_Components_By_Sequence)=
# Aligning components by sequence

*Mapping atomic anchors through sequence groups and checking a rigid fit.*

Use sequence-guided alignment when corresponding amino-acid groups must be
identified before fitting. Selections address atoms; group indices are used
only inside the sequence projection. This example checks a known rigid pose
on the bundled capped pentalanine system.

:::{versionadded} 1.0.0
:::

The query must retain its `ChemicalStates` domain with component membership:
those components determine which atoms move together. Pure `Topology` contains
no covalent graph. When combining inventory with a separate trajectory, supply
`[topology, chemical_states, coordinate_file]` to `msm.convert`, or keep the
complete molecular system. The coordinate-only route reads the requested
structures and retains explicit chemistry instead of reconstructing it.

## Preparing independent atomic anchors

Move a copy by 1 nm. Resolve query and reference anchors on their own atom axes.
The input order does not define correspondence: identical aligned groups and
unique selected atom names within each pair do. Caps supply no sequence letters.

```python
import numpy as np
import molsysmt as msm
puw = msm.pyunitwizard
molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     structure_indices=[0])
query = msm.structure.translate(molsys, translation='[1, 0, 0] nm')
query_atoms = msm.select(query, selection='atom_name=="CA"')
reference_atoms = msm.select(molsys, selection='atom_name=="CA"')
query_before = puw.get_value(msm.get(query, element='atom', coordinates=True),
                             to_unit='nm').copy()
```

## Keeping the fitted system and measuring RMSD

The function returns a molecular system, not its RMSD. Complete query components
containing selected atoms move, including atoms outside the anchors. The default
returns an independent object and preserves both inputs.

```python
aligned = msm.structure.least_rmsd_align(
    query, selection=query_atoms[::-1], reference_molecular_system=molsys,
    reference_selection=reference_atoms, use_gpu=False)
rmsd = msm.structure.get_rmsd(
    aligned, selection=query_atoms, reference_molecular_system=molsys,
    reference_selection=reference_atoms)
assert np.allclose(puw.get_value(rmsd, to_unit='nm'), 0., atol=1e-11)
np.testing.assert_allclose(
    puw.get_value(msm.get(aligned, element='atom', coordinates=True), to_unit='nm'),
    puw.get_value(msm.get(molsys, element='atom', coordinates=True), to_unit='nm'),
    atol=1e-11)
np.testing.assert_array_equal(
    puw.get_value(msm.get(query, element='atom', coordinates=True), to_unit='nm'),
    query_before)
```

Omitting the reference, or supplying None, uses the query's original
`reference_structure_index`. `structure_indices` can be nonconsecutive or
repeated. Boolean masks span the full atom axis of their corresponding system.
In-place edits return None and invalidate interaction coverage on edited
structures. Invalid scopes, insufficient or collinear anchors and ambiguous
atom-name pairs reject before publication. No chain assignment or periodic
reconstruction is performed. Use `least_rmsd_fit` for arbitrary ordered atom
pairs rather than sequence-derived atom-name correspondences.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Least_rmsd_align`
- {ref}`Tutorial_Least_rmsd_fit`
- {ref}`user-foundations-molecular-system-definition`
- {func}`molsysmt.topology.get_sequence_identity`
:::
