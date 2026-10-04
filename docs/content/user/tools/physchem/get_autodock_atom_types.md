(Tutorial_AutoDock_Typing)=
# Getting AutoDock types

*Classifying an explicit chemical graph under a named parameter profile.*

{func}`molsysmt.physchem.get_autodock_atom_types` calculates labels without
changing your molecular system. `atom_type` remains the chemical element symbol;
`atom_ff_type` denotes a parameter label. Explicitly choose
`typing_scheme='autodock4'`. The experimental method is `chemical_environment`,
with inspectable rule version `chemical_environment@1`.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.physchem.get_autodock_atom_types`
:::

## Supplying complete chemistry

Your selected chemical state must have complete covalent connectivity, elements,
formal charges, closed-shell radical counts and supported bond orders. Every H
must be an indexed atom. Missing aromatic flags can be perceived through
{func}`molsysmt.physchem.get_aromaticity`; known contradictory flags fail.
The function does not infer missing bonds, repair protonation, add H, calculate
partial charges or merge nonpolar H. Numeric H5MSM inputs can read chemistry
without structural arrays; spatial selections can require coordinates.

The bounded profile supports H/C/N/O/F/P/S/Cl/Br/I. Allowed formal charges are
zero for every element, additionally +1 for N/P and -1 for O/S. Unsupported
charges, metals, pseudoatoms, radicals, queries and virtual H raise clearly.
A readable PDB or PDBQT with coordinates alone does not establish this chemistry.
Apply separately justified chemical assignments before requesting typing.

## Following the rules

Rules run in the following order; a later matching rule overrides an earlier
label. All atoms first receive the element default: N becomes NA, O becomes OA,
and other supported elements retain their symbol.

| Code | Chemical environment | Label |
| --- | --- | --- |
| 0 | Element default | N: NA; O: OA; other: element |
| 1 | Aromatic C | A |
| 2 | Trivalent N adjacent to an aromatic atom | N |
| 3 | Trivalent N adjacent to sp2 C or the specified triazene environment | N |
| 4 | N with formal charge +1 | N |
| 5 | Nonaromatic S with total degree two | SA |
| 6 | H bonded to N/O/F/P/S | HD |

Trivalent means total degree three and total valence three, counting indexed H.
The sp2 C neighbor has total degree three and total valence four. The triazene
neighbor is N with total degree two and a double bond. H bonded to C stays H;
each H must have exactly one supported covalent parent. Sulfone, sulfoxide and
aromatic S stay S. A one-connected thiolate also stays S in this bounded profile.
These are AutoDock parameter rules, not universal donor/acceptor definitions.

The profile uses the [AutoDock4 vocabulary](https://autodock.scripps.edu/wp-content/uploads/sites/56/2021/10/AutoDock4.2.6_UserGuide.pdf).
[Meeko's ordered chemical-context typing](https://github.com/forlilab/Meeko/blob/1eac18bd6d1111f35f9f1abaa8af502c2668d054/meeko/atomtyper.py)
was inspected as a reference at the recorded commit. Meeko is neither a runtime
dependency nor a vendored rule table. This bounded local profile does not claim
identical coverage or docking outcomes. RDKit supplies explicit aromaticity and
valence interpretation; its original version is recorded separately from the
reference implementation. Optional Ackredit failures preserve the result.

## Inspecting coverage

```python
import molsysmt as msm

molsys = msm.systems['caffeine']['caffeine.sdf']
result = msm.physchem.get_autodock_atom_types(
    molsys, typing_scheme='autodock4', selection=[5, 0, 5], return_report=True)
assert result['report']['atom_indices'].tolist() == [0, 5]
assert result['report']['n_atoms'] == 24
assert result['atom_ff_type'].shape == (2,)
```

The full source graph is evaluated before selection. Output indices are sorted
and unique. Labels are U2 arrays; an empty selection gives shape `(0,)` without
hiding incomplete chemistry elsewhere. No numerical units apply to labels or
indices. The report includes full evaluated scope, selected source indices,
state, rule precedence, per-atom winning rule codes, overlap counts, polar and
nonpolar H indices, evidence, references and original producer versions.
`chemical_state='structure'` must resolve one state across the requested frames.
The calculation copies chemical tables/provider graphs; it does not offer
streaming or a bounded-memory guarantee for arbitrary graphs.

:::{seealso}
:class: dropdown

- {ref}`Tutorial_Assign_AutoDock_Types`
- {ref}`Tutorial_Get_Aromaticity`
- {ref}`cookbook-native-pdbqt`
:::
