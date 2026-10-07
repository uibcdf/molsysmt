(Tutorial_Atom_Types)=
# Checking and normalizing atom types

*Validating chemical elements and preserving explicit isotope assignments.*

In MolSysMT, `atom_type` is a chemical element symbol. It is independent of
`atom_name` (an atom's name in a molecule) and `atom_ff_type` (a force-field
assignment). A PDB atom named `CA` may be an alpha carbon; calcium has the
chemical atom type `Ca`. An AutoDock label such as `OA` needs its own format
interpretation before it becomes the chemical atom type `O`.

:::{versionadded} 1.0.0
:::

:::{admonition} API documentation
:class: dropdown

- {func}`molsysmt.element.atom.is_atom_type`
- {func}`molsysmt.element.atom.normalize_atom_types`
:::

## Checking symbols

`is_atom_type` accepts a string or a one-dimensional collection of strings.
It recognizes the 118 chemical element symbols with canonical capitalization.
It returns one boolean for a string, or a NumPy boolean array for a collection.
Invalid symbols return `False`; invalid input shapes or non-string entries
raise an argument error. Empty collections return a boolean array of shape `(0,)`.

Dummy particles (`Du`, `X`), unknown markers (`UNK`), and isotope aliases
(`D`, `T`) are not canonical element symbols. This check deliberately distinguishes
real elements from the wider labels that a molecular model may store.

## Normalizing isotopes

`normalize_atom_types` returns a pair: canonical atom types and isotope mass
numbers. `D` becomes `('H', 2)` and `T` becomes `('H', 3)`. A scalar input gives
a scalar pair; collection input gives two new lists in the same order. `None`
and `pandas.NA` denote an unspecified isotope and become `None` in the output.
An empty input gives `([], [])`.

Supply either no isotope argument or isotope entries aligned with the atom
types. A scalar isotope is not broadcast across a collection. Conflicts such
as `D` with isotope 3 raise an error. Mass numbers must be integers between 1
and 65535, matching the native nullable isotope storage. They are dimensionless
mass numbers, not atomic masses or charges. The tool does not check isotope
stability, infer a default isotope or alter capitalization.

Neither tool changes its input or assigns chemistry to a system. To validate
values from any supported molecular-system form, first obtain `atom_type`
through {func}`molsysmt.basic.get`. Inferring elements from standard atom names
is a separate operation: {func}`molsysmt.element.atom.get_atom_type_from_atom_name`.

## Decoding named model labels

Use {func}`molsysmt.element.atom.get_atom_type_from_atom_ff_type` to decode
labels already assigned under the explicit `autodock4` dictionary:

```python
msm.element.atom.get_atom_type_from_atom_ff_type(
    ['A', 'NA', 'OA', 'HD', 'Cl'], typing_scheme='autodock4')
# ['C', 'N', 'O', 'H', 'Cl']
```

A string yields a string; a one-dimensional collection yields a new list.
Names are case sensitive. Unknown schemes, custom labels, macrocycle glue
labels (`G0`, `CG0`, etc.) and the hydrated-ligand pseudoatom `W` raise an
argument error. This operation does not assign labels to atoms or infer
aromaticity, hydrogen polarity or charges. An empty collection still requires
a supported named scheme.
