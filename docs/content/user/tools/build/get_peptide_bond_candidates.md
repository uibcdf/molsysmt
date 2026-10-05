(Tutorial_Peptide_Bond_Candidates)=
# Get peptide bond candidates

*Inspecting adjacent backbone C–N evidence without changing the system.*

Use {func}`molsysmt.build.get_peptide_bond_candidates` to review an experimental,
bounded peptide-link report before choosing a reconstruction policy.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

See {func}`molsysmt.build.get_peptide_bond_candidates` for arguments and errors.
:::

## Choosing a scope

Integer selections are **source atom indices**. Both candidate endpoints must be
selected. Choose one structure with `structure_indices` when the system contains
several; structure IDs remain separate labels. The stored chemical state can be
chosen explicitly, or associated with the selected structure using
`chemical_state='structure'`. Unresolved chemistry remains unassessed.

The method `adjacent_backbone_distance` reuses the
{ref}`heavy-template report <Tutorial_Covalent_Bond_Candidates>` and
{func}`molsysmt.structure.get_distances` with explicit pairs. It examines only
consecutive source group indices in one defined chain. A selection cannot make
groups consecutive, and equal or nonconsecutive group IDs do not establish a link.

Native PDB conversion creates different chain indices across `TER`, even if the
chain labels repeat. Insertion-code groups remain distinct even when their group
IDs are equal. The report respects those axes. An adapter that discarded a file
boundary cannot supply it later merely through a group or chain label.

## Reviewing the result

The detached dictionary uses schema `molsysmt.peptide_bond_candidates@1`.

| Field | Meaning |
| :--- | :--- |
| `bonded_atom_pairs` | Sorted source atom pairs, shape `(n_candidates, 2)`, dtype `int64`. |
| `group_pairs` | Aligned, directional source group pairs: outgoing C group, incoming N group. |
| `carbon_atom_indices`, `nitrogen_atom_indices` | Roles remain explicit even when source atom order differs. |
| `distances` | Aligned length quantities honoring the active output-unit policy. |
| `missing_mask` | True if no stored edge has these endpoints. Existing edges are preserved. |
| `links` | Examined selected group boundaries, status, reasons and measured distance when evaluated. |
| `group_coverage` | Exact heavy-template report, including template hashes and unassessed groups. |
| `parameters` | Requested and effective length ceilings, with units, and the PBC flag. |
| `pbc_applied` | Whether a periodic box was used to evaluate the eligible pairs. |
| `software`, `method`, `rule_version` | Original producer version and executed descriptive rule. |

All candidates have `inferred_candidate` evidence. `candidate` means the bounded
criteria passed; `rejected` means an evaluated distance exceeded the ceiling;
`unassessed` means required evidence is missing, ambiguous or conflicting.
Empty arrays retain their types and shapes.

## Respecting geometric and chemical limits

Groups need compatible exact heavy-template mappings and unique C/N endpoints.
Missing other heavy atoms may leave a partial group without blocking a known
endpoint. Contradictory stored peptide edges or an already linked external
backbone endpoint block the affected proposal. Unknown bond orders remain
unknown. An outgoing group with OXT is excluded by this first terminal policy.

The positive finite C–N distance must not exceed either `max_bond_length` or
the existing protein C–N reference plus its tolerance: **0.153 nm**. The default
requested ceiling is `2 angstroms`. This is a heuristic candidate criterion,
not a validated bond-energy or valence calculation. Coordinates and ceilings
can use other length units; numerical delegation names nm explicitly.

PBC is disabled by default. With `pbc=True`, a valid available box enables
minimum-image distances; a missing box leaves Cartesian geometry. A present
invalid box leaves eligible links unassessed. Crystallographic periodicity alone
does not declare a polymer bond. Alternate-site evidence at either backbone
endpoint also leaves that link unassessed: this first policy does not select or
combine alternate conformers. Alternate side-chain atoms do not block a unique
backbone pair.

Without coordinates, eligible links remain unassessed. Terminal caps, other
polymers, sequence completion, hydrogen edges, bond-order assignments, valence
and protonation are outside this method. The source, declared file edges and
named interaction analyses are unchanged; this does not change the PDB reader.

## Reading from disk

Native H5MSM 0.5 numeric/all queries read chemical/topological layers and one
coordinate structure, its box and sparse alternate-site evidence through the
existing adapter iterator. They do not load all coordinate structures. Rich
selections retain their source behavior and may need broader access. Legacy
H5MSM files retain their adapter route and deprecation warning.
Legacy alternate-location label arrays without the native sparse-site contract
leave affected calculations unassessed; they are not treated as absent evidence.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Covalent_Bond_Candidates`
- {ref}`Tutorial_Get_missing_bonds`
- {ref}`cookbook-pdb-connectivity-policy`
:::
