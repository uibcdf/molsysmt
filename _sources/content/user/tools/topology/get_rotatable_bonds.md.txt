(Tutorial_Rotatable_Bonds)=
# Classifying rotatable bonds

*Getting torsion candidates with source correspondence and exclusion evidence.*

Use {func}`molsysmt.topology.get_rotatable_bonds` on a complete declared chemical
graph. Choose a named criterion, inspect its exclusions, then pass the source
bond indices you want to cut to {func}`molsysmt.topology.get_rigid_fragments`.
The result describes graph eligibility; it does not predict rotational barriers.

:::{versionadded} 1.0.0
:::

## Choosing criteria

Both experimental methods require a single, nonaromatic bond that is a bridge
in the original covalent graph. Both endpoints must be heavy atoms with at least
two heavy neighbors, and neither endpoint may participate in a triple bond.
Counting heavy neighbors makes eligibility independent of whether the same H
inventory is implicit or represented by indexed atoms.

| Method | Additional restriction |
| :--- | :--- |
| `acyclic_single` | None; amide and ester links may be candidates. |
| `conjugation_restricted` (default) | Exclude a single C–N/O/S link when that C also has a nonaromatic double bond to N/O/S. |

The second criterion excludes amide, thioamide, amidine, ester and thioester
links. It includes formamides and does not release tertiary amides based on
substituent symmetry. These descriptive policies draw on inspected
[RDKit definitions](https://github.com/rdkit/rdkit/blob/cbfb37abddcd5b5feeac97d53530ae6be83cac0d/Code/GraphMol/Descriptors/Lipinski.cpp)
and [Meeko bond typing](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/bondtyper.py),
but do not reproduce either complete implementation. RDKit Strict also excludes
some symmetry-equivalent terminal groups that these policies retain. Meeko's
tertiary-amide exceptions and internal-alkyne replacement torsions are absent.

## Inspecting results

```python
import molsysmt as msm
from rdkit import Chem

molsys = Chem.MolFromSmiles('CC(=O)OCC')  # explicit optional RDKit input
result = msm.topology.get_rotatable_bonds(molsys)
assert result['rotatable_bonded_atom_pairs'].tolist() == [[3, 4]]
broader = msm.topology.get_rotatable_bonds(molsys, method='acyclic_single')
assert broader['rotatable_bonded_atom_pairs'].tolist() == [[1, 3], [3, 4]]
bits = result['exclusion_bits']
restricted = (result['exclusion_mask'] & bits['restricted_conjugation']) != 0
assert result['bonded_atom_pairs'][restricted].tolist() == [[1, 3]]
fragments = msm.topology.get_rigid_fragments(
    molsys, bond_indices=result['rotatable_bond_indices'])
assert fragments['fragment_offsets'].tolist() == [0, 4, 6]
```

`bond_indices` and `bonded_atom_pairs` describe **all returned source bonds**,
including rejected ones. The aligned `is_rotatable` is boolean;
`exclusion_mask` is uint8. Decode each bit with `exclusion_bits`. Several reasons
may apply to the same bond. `rotatable_bond_indices` and
`rotatable_bonded_atom_pairs` contain only eligible candidates. Atom and bond
indices are 0-based positions, distinct from string IDs. No physical units apply.

## Selecting scope

Classification always precedes selection. Only bonds with both endpoints in
the selected atom set are returned. Selecting two atoms in an amide does not
remove the carbonyl environment, and selecting the middle pair in butane does
not make those atoms terminal. Requested atom indices are sorted and deduplicated.
The full `evaluated_atom_indices` and `evaluated_bond_indices` remain in the
report, including when the returned selection is empty.

`chemical_state` chooses one state. With `'structure'`, the explicitly requested
structures must resolve to that same state. Structure indices are validated;
coordinate values are unused except when a spatial selection needs them.
Native MolSys/Topology, supported chemical file forms and H5MSM may be passed
directly. A chemistry-only object without element inventory is insufficient.
Numeric H5MSM queries read chemical domains; rich selections may load coordinates.

The report retains `schema`, `method`, `rule_version`, parameters, state,
chemical evidence, bibliography and original producer versions. Reference
implementations are distinguished from executed software. Optional Ackredit
tracking does not determine the scientific result. No assignment is attached.

## Limits and failures

Connectivity must be declared complete. Each bond needs order 1, 2 or 3, or an
explicit aromatic declaration. Missing aromatic flags do not trigger perception:
a ring edge is already excluded by connectivity. An aromatic bridge contradicts
that complete graph and raises. Missing elements/orders, unsupported elements,
dative relationships and query inputs also fail before selection. Supported
element symbols are H/B/C/N/O/F/Si/P/S/Cl/Br/I. The graph classifier does not
certify valence, infer formal charges, select protonation, canonicalize resonance
or tautomer forms, or assign aromaticity. It does not generate macrocycle cuts
or pseudoatoms. Empty arrays have defined shapes `(0,)` and `(0, 2)`.

RDKit is unnecessary for classification of native graphs. An input form may
require its own optional conversion provider. Graph storage and bridge detection
scale with atoms and listed bonds; no atom-pair matrix or cycle enumeration is
used. No large-system timing, RSS or Rust speedup is claimed.

The original Vina ligands give restricted candidate counts 7, 5, 2 and 2 for
1IEP, 1S63, 5X72 P59 and P69. Exact branch pairs and heavy-fragment memberships
agree with the prepared references except the 1S63 aryl–nitrile branch, which
these criteria exclude. Those published preparations are comparison inputs,
not universal chemical truth. DockingMT owns the final active-torsion policy.

:::{seealso}
:class: dropdown

{ref}`Tutorial_Rigid_Fragments` and {ref}`cookbook-native-pdbqt` explain the
separate fragment and rooted-export operations.
:::
