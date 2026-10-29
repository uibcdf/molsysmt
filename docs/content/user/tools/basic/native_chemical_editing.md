(Tutorial_Native_Chemical_Editing)=
# Native chemical editing

*Editing one resident chemical state with validated publication.*

Use these native methods when you already hold a `molsysmt.ChemicalStates`,
including `molsys.chemical_states`. See the
{ref}`ChemicalStates foundation <user-foundations-native-world-classes-molsysmt-chemicalstates>`
for availability and ownership, and {ref}`Cookbook_Group_Free_Hierarchy` for
executed standalone and selected-state examples.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{ref}`API Native Chemical Editing` provides the argument, return and exception
contracts for these methods and the live `get_bonds` interchange view.
:::

## Inspecting stored chemistry

Use `chemical_states.get(n_bonds=True, n_components=True, chemical_state=...)`
to inspect one state's stored graph inventory. The same attributes are available
through `msm.get(chemical_states, ...)`. Atom and component queries can also read
declared membership and incident counts; see the
{ref}`ChemicalStates foundation <user-foundations-native-world-classes-molsysmt-chemicalstates>`
for the supported element/attribute table and the executed Cookbook example.
Completeness/evidence describe the selected state; state indices/IDs describe
the entire collection. These reads never rebuild or prepare chemistry.

The same queries can read stored atom charges/aromaticity/hydrogen assignments,
bond metadata and state-local component labels. For example,
`chemical_states.get(element='bond', chemical_state=1, bond_order=True)` reads
the selected edge rows without assigning an unknown order. Atom properties with
no stored column return `None`; existing columns retain one nullable value per
selected atom. Missing bond fields retain one nullable entry per edge (two atom
references for bond stereochemistry). Formal charges are integer multiples of
the elementary charge, following the existing schema. See the foundation for
the complete supported field list and the Cookbook for executed examples.

## Choosing an operation

| Method | Use |
| :--- | :--- |
| `add_bonds(pairs, chemical_state=...)` | Add unique unordered atom pairs and rebuild that state's observed component graph. Edge order/type remain unknown until explicitly assigned. |
| `remove_bonds(indices, chemical_state=...)` | Remove positional rows from the selected state's bond table and compact the result. `'all'` removes every stored edge; repeated indices remove a row once. |
| `rebuild_components(..., chemical_state=..., topology=...)` | Reconstruct graph membership or update component labels from available stable context. |

`chemical_state` is a nonnegative index or `'reference'`. A missing or ambiguous
state rejects the operation, even for empty inputs. No state is created or
selected as a new reference. Atom and bond indices are positions; bond selectors
belong to the selected state's local table. Boolean, fractional and unitful
indices reject before editing. These operations use no coordinate input.

## Reconstructing component labels

`redefine_indices=True` reconstructs the stored graph; `force=True` also does so
when `redefine_indices=False`. These are logical flags. Missing membership is
reconstructed when type/name inference needs it. `redefine_ids=True` generates
local string IDs. Set individual label flags to False to preserve those columns
only for unchanged full source atom sets during reconstruction.

An attached collection uses its owner's Topology for stable group context. You
may supply a matching native `topology` explicitly. No copy or chemical recovery
through Topology is needed, and missing group typing is inferred without changing
that context. Missing evidence remains missing rather than a generated chemical
name/type. Neither `force` nor complete component membership establishes that a
fragment is chemically prepared.

## Handling edits and failures

Validation and all component reconstruction/invalidation allocation precede
publication. A failed operation preserves bonds, components and named analyses.
Successful graph/completeness changes invalidate the owner's evaluated scope,
including evaluated-empty structures; existing analysis snapshots stay intact.
Coordinates, other chemical states, producer histories and structure-to-state
associations are retained. Empty edits preserve table and analysis identity.
Label-only reconstruction preserves observations.

`get_bonds()` exposes a live table for reading and interchange. Direct table
writes bypass this contract. Existing atom/bond assignment routes on MolSys
remain available through supported `msm.set` attributes; general standalone
assignment and dictionary query dispatch are still being migrated. Use these native methods
for graph editing. No detector,
chemical perception, cap placement or hydrogen addition runs automatically.

Supported atom/bond metadata assignments also validate the selected state's typed
values before publishing and invalidate observations for scientific changes.
Changing only `bond_id` preserves observations, stored bond positions and nullable
columns. It does not infer new chemical participation flags. IDs are string labels;
they do not select bond rows.
