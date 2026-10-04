(Tutorial_Get_Aromaticity)=
# Getting aromaticity

*Perceiving atom and bond flags from a complete chemical graph.*

The experimental {func}`molsysmt.physchem.get_aromaticity` interprets a selected
chemical state through RDKit's aromaticity model. It returns detached source-indexed
flags; it changes neither `ChemicalStates` nor coordinates or hydrogen inventory.
Use {func}`molsysmt.physchem.get_aromatic_rings` when you instead want rings from
flags already stored in a chemical state.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.physchem.get_aromaticity`
:::

## Choosing the interpretation

`method='fused_ring_electron_count'` names the implemented criterion. Its explicit
provider implementation is `rdkit.AROMATICITY_RDKIT`: environment-dependent
contributions and a 4N+2 criterion on rings and fused systems, as defined in the
[RDKit Book](https://www.rdkit.org/docs/RDKit_Book.html#aromaticity).
RDKit is optional; an unavailable provider raises instead of selecting another model.
The report identifies its original version. The criterion is model-dependent,
not a universal aromaticity definition or a geometric plane test.

A bond between two aromatic atoms need not be aromatic. Fused-ring controls
check that distinction explicitly. Do not infer bond flags by combining only
endpoint flags. A flat ring alone, atom names and residue names are insufficient.

## Inspecting a native source

```python
import molsysmt as msm

source = msm.systems['caffeine']['caffeine.sdf']
molsys = msm.convert(source, to_form='molsysmt.MolSys')
result = msm.physchem.get_aromaticity(molsys)
assert int(result['atom_is_aromatic'].sum()) == 9
```

:::{admonition} Demo Systems Catalog
:class: dropdown

See {ref}`user-foundations-entrance-demo-systems` for the bundled caffeine source.
:::

Complete Kekule bond orders can supply evidence when stored aromatic flags are
unknown. Known atom or bond flags must agree with perception. Source formal charges,
closed-shell assignments and the atom/bond inventory must remain consistent.
No inferred flags are written back to the source. Attaching chemical assignments
is a separate operation and may invalidate analyses depending on that state.

The bounded route requires explicit elements, formal charges, closed-shell radical
counts, complete connectivity and supported covalent orders. It supports
H/B/C/N/O/F/Si/P/S/Cl/Se/Br/Te/I; query/dummy atoms, metals, dative relationships,
radicals, incomplete graphs and unsupported orders fail clearly. Provider valence
interpretation may use virtual H but does not create indexed H. This aromaticity
calculation does not prepare a fixed-state ligand or establish a charge model.

## Following the source axes

```python
subset = msm.physchem.get_aromaticity(molsys, selection=[5, 0, 5])
assert subset['atom_indices'].tolist() == [0, 5]
empty = msm.physchem.get_aromaticity(molsys, selection=[])
assert empty['atom_is_aromatic'].shape == (0,)
assert empty['bonded_atom_pairs'].shape == (0, 2)
```

Perception uses the full graph before selection. Atom indices are sorted and
unique; only bonds whose endpoints are both selected are returned. Bond indices
refer to the selected state's source table, independently of bond IDs.
`chemical_state='structure'` must resolve one state for the selected structures.
Explicit frame requests are range checked against an actual source frame axis.

`atom_is_aromatic` and `bond_is_aromatic` are bool arrays aligned with
`atom_indices` and `bond_indices`. `bonded_atom_pairs` has shape `(n_bonds, 2)`.
Indices and flags carry no physical units. Empty arrays retain their shape and
dtype; evaluated scope, state, method, evidence, references and original producer
versions remain present even when the selected output is empty.

Numeric H5MSM queries read chemical domains without loading structural arrays.
Rich spatial string selections can require the original coordinates and full
loading. The calculation may copy chemical tables/provider graphs; it is not a
bounded-memory proof for every graph or a streaming trajectory API. Optional
Ackredit failures do not discard the detached result or its references.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Get_aromatic_rings`
- {ref}`Tutorial_Chemical_Readiness`
- {ref}`cookbook-native-sdf`
:::
