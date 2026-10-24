(Tutorial_Permute_Atoms)=
# Permuting atoms

*Applying a declared atom order to a complete molecular system.*

{func}`molsysmt.basic.permute_atoms` returns an independent native MolSys with
all atoms in the supplied order. The experimental contract requires a complete
bijection: `atom_indices[new_index] = old_index`. Atom IDs remain string labels.
The operation accepts supported molecular forms through their conversion to
MolSys. Native MolSys inputs use their stored domains directly.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.basic.permute_atoms`
:::

## Applying a known order

A reverse order makes the convention easy to inspect:

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['caffeine']['caffeine.sdf'])
order = list(range(molsys.get_n_atoms() - 1, -1, -1))
permuted = msm.basic.permute_atoms(molsys, atom_indices=order, return_report=True)
molsys_reordered = permuted['molecular_system']
assert permuted['report']['output_to_source_atom_indices'][:3].tolist() == [23, 22, 21]
```

:::{admonition} Demo Systems Catalog
:class: dropdown note

This example uses the bundled {ref}`Demo Systems <user-foundations-entrance-demo-systems>`.
:::

The returned `molsysmt.atom_map@1` report includes inverse
`source_to_output_atom_indices` and forward `output_to_source_atom_indices`
(the names describe the source and output axes explicitly). Both are positional
integer arrays. Restore the original order with the inverse map:

```python
molsys_restored = msm.permute_atoms(molsys_reordered,
    permuted['report']['source_to_output_atom_indices'])
assert molsys_restored.topology.atoms.atom_id.tolist() == molsys.topology.atoms.atom_id.tolist()
```

## Preserving domains

Only the atom axis changes. Group, chain, molecule, entity, component, bond,
chemical-state and structure indices retain their original order. All chemical
states' atom assignments, component membership, bond endpoints, directed bond
roles and stereo references follow their atoms. Absolute stereo assignments and
physical values are transported, without chemical inference.

Coordinates, velocities, occupancies, B factors and sparse alternate locations
follow the new atom order. Boxes, times, observables, chain-based bioassemblies
and structure/state associations stay on their existing axes. Named interaction
analyses retain roles, compound participants, coverage, images, source maps and
occurrence indices. References to the source analyses continue to describe the
source; use the analyses attached to the returned MolSys for its new atom axis.

Per-atom mechanics follows the permutation. Named charge/type assignments keep
their original method and producing software and receive a derived
`atom_order_transform`; already stale assignments remain stale. Preparation
history keeps its historical operation axes. The optional atom map describes
this new transform and can be joined to earlier reports with
{func}`molsysmt.basic.compose_atom_maps`.

## Supported limits

This first version supports the built-in native domains, canonical tables and
full named interaction results. Missing domains remain absent. Unknown subclasses,
extension fields, untyped table metadata, malformed references or incompatible
atom axes reject explicitly. An undeclared atom axis cannot be permuted.
Duplicates, omissions, booleans, quantities and non-flat orders are invalid.

The source remains unchanged, including on failure. Protected coordinate blocks
are processed through bounded delivery; the full result remains resident.
An identity permutation shares immutable geometry bytes through independent
handles. The numeric-output budget is an allocation estimate, not a process-RSS
limit; Python/pandas object overhead, temporary remapping work, conversion costs
and the already resident source require additional memory. There is no out-of-core
molecular-file transform in this API.

To persist the supported domains, use the ordinary conversion to H5MSM 0.5.
That format excludes experimental MolecularMechanics persistence. The optional
atom-map report remains a separate sidecar; permutation adds no H5MSM domain.
See {doc}`../../cookbook/permuting_export_order` for a complete workflow.

:::{admonition} Related Tools & References
:class: dropdown seealso

- {ref}`Tutorial_Compose_Atom_Maps`: composing declared transformation stages with {func}`molsysmt.basic.compose_atom_maps`.
- {func}`molsysmt.basic.extract`: selecting subsets; a full selection does not declare a permutation.
:::
