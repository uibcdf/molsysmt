(Tutorial_Normalize_Indexed_Hydrogen_Policy)=
# Normalizing indexed hydrogen policy

*Closing implicit-H permission without changing an indexed H inventory.*

Two producers can describe the same indexed H atoms with different
`allows_implicit_hydrogens` flags. Strict chemical correspondence compares that
stored policy along with charge, isotope, H counts and stereochemistry. Apply
an explicit common policy before comparing when that is the intended operation.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

{func}`molsysmt.chemical_states.normalize_indexed_hydrogen_policy`
:::

## Applying the policy

This small example uses the optional RDKit SMILES converter to prepare its input.
The normalization itself uses native stored fields and needs no RDKit.
Deuterium remains an atom with element `H` and isotope label 2.

```python
import molsysmt as msm

molsys = msm.convert('smiles:[2H]O')
msm.set(molsys, selection="atom_type=='H'", allows_implicit_hydrogens=True)
result = msm.chemical_states.normalize_indexed_hydrogen_policy(molsys)
normalized = result['molecular_system']
report = result['report']
assert report['status'] == 'normalized'
assert report['changed_atom_indices'].tolist() == [0]
assert report['atom_correspondence'] == {'indices': 'identity', 'n_atoms': 2}
assert msm.get(molsys, element='atom', selection=[0], allows_implicit_hydrogens=True) == [True]
assert msm.get(normalized, element='atom', selection=[0], allows_implicit_hydrogens=True) == [False]
```

The method `closed_neutral_terminal_hydrogens` is an experimental MolSysMT
representation policy. It sets only the permission flag to False on all already
indexed H atoms. It retains heavy-atom permissions, virtual counts, bonds, charge,
isotopes, radicals, stereo, names, IDs and positional axes. It neither adds H nor
chooses protonation, and it does not certify molecular equivalence or geometry.

## Checking admission

The existing {ref}`inventory audit <Tutorial_Hydrogen_Inventory>` must be available:
complete declared ordinary covalent connectivity, known stored virtual counts,
and exactly one non-H parent for each indexed H. Each indexed H must also have:

- zero implicit and annotated explicit virtual H counts;
- known zero formal charge and unpaired-electron count;
- known nonaromaticity, unspecified atom stereo and a Boolean permission flag;
- a declared single, nonaromatic bond without bond stereo.

A single bond can use integer order 1, fractional order 1.0, or compatible both.
The original encoding is preserved; the operation does not fill a missing order.

Unknown fields, charged or radical H, H–H relationships, nonterminal H, dative
chemistry, incompatible orders and unsupported stereo reject before preparing
the result. The tool never fills unknown counts with zero. It preserves isotope
labels, including deuterium and tritium. An H atom's name alone does not establish
its element or isotope.

The complete stored inventory is audited. This conservative profile can reject
a system whose heavy-atom virtual counts are unknown even when its indexed H
look ordinary. Complete inventory is a representation precondition, not an
independent validation of valence, protonation or coordinate quality.

## Choosing a state

`chemical_state='reference'` resolves the reference; an integer selects a state
without changing that reference or any structure association. Other states are
retained. Missing chemistry, zero states and an ambiguous reference are explicit
errors. This operation does not use structures, so `chemical_state='structure'`
is unavailable. Normalize each intended state explicitly.

Any supported form can supply the required elements and chemistry through its
existing conversion. Standalone ChemicalStates cannot identify H without stable
element context. An explicit `[topology, chemical_states]` input declares shared
atom indices and needs no coordinates. A compatible native Structures domain
can accompany that pair; it is not inspected for admission.

## Keeping evidence

The detached `molsysmt.indexed_hydrogen_policy@1` report retains sorted int64
H/changed indices, parent-first H pairs, the original Boolean flags, state index,
method/rule version and the software version that performed the operation.
Its compact identity map declares unchanged atom indices without allocating a
pair for every atom. All counts, indices and flags are dimensionless; the report
contains no coordinate snapshot.

`status` is `normalized` when flags change, `unchanged` when all indexed H already
have closed permission, and `empty` when none are indexed. Empty arrays retain
their types; pairs have shape `(0, 2)`. Every success, including no-op calls,
appends an independent operation record to the selected state's preparation
history. Previous records remain intact. H5MSM and ChemicalStatesDict preserve
the typed report and original producer version.

Historical indices and identity maps belong to the recorded operation domain.
After extraction or reordering, they do not address the current atom axis and
do not certify its current chemical state.

## Preserving memory and analyses

The native result has independent chemical tables, metadata and analysis handles.
It uses {ref}`deferred native geometry copying <user-foundations-molsys-copying>`:
coordinate and box blocks remain protected and shared until a controlled edit
replaces affected blocks. The policy does not examine or duplicate coordinate
structures. A foreign converter or a complete H5MSM load can still materialize
coordinates; provide already loaded native domains for repeated operations.

Native quantities retain their exact values and units. Foreign reading follows
the existing reader/unit contract, and the operation preserves the caller's
PyUnitWizard policy. Changed chemical assignments invalidate named analyses on
the returned system through the existing chemical owner. The names remain with
unevaluated coverage. Unchanged/empty results retain coverage. Source analyses
and assignments are preserved; this operation does not recalculate interactions.

:::{seealso}
:class: dropdown

- {ref}`cookbook-aligning-hydrogen-policies` — composing an explicit policy with
  strict correspondence and persistence.
- {ref}`Tutorial_Get_atom_correspondences` — comparing complete declared context.
- {ref}`Tutorial_Fixed_State_Hydrogens` — materializing a fixed declared inventory.
:::
