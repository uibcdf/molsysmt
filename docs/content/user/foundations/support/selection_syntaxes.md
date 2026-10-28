(user-foundations-support-selection-syntaxes)=
# Selection Syntaxes

MolSysMT provides a native declarative selection engine and selected interoperability with third-party selection syntaxes. Support is directional: parsing a query string for atom selection and translating atom indices into external selection strings are separate capabilities.

---

## Supported Syntaxes and Shortcuts

| Syntax | Selection Input | Translation Output | Scope |
| :--- | :---: | :---: | :--- |
| **`MolSysMT`** (native) | Yes | No | Any supported molecular-system form |
| **`MDTraj`** | Yes | Yes | Inputs convertible to `mdtraj.Topology` |
| **`MDAnalysis`** | Yes | No | Inputs convertible to `MDAnalysis.Universe` |
| **`NGLView`** | No | Yes | Atom, group, and chain translations |

Input query interpretation is selected via `syntax=...`; output translation is requested via `to_syntax=...`. A syntax supported in one direction is not implicitly supported in the other. Users can inspect the active runtime matrix via `msm.supported.syntaxes()`.

The native **`MolSysMT`** syntax supports topological attributes (including `atom_name`, `atom_type`, `group_name`, `group_id`, `chain_id`, `molecule_type`, `entity_type`), logical operators (`and`, `or`, `not`), and grouping parenthetical expressions.

Built-in selection shortcuts (such as `"backbone"`, `"heavy atoms"`, `"solvent"`, `"hydrogens"`) are configured dynamically through `msm.configure.selection_shortcuts`.

## Empty connectivity selections

In MolSysMT syntax, a valid `bonded to` operand with no matching atoms returns
an empty selection; `not bonded to` that operand retains the left selection.
An empty match is valid even inside a larger logical expression. Missing or
ambiguous chemistry continues to raise its documented diagnostic. See
{ref}`Tutorial_Select` for connectivity selection examples.

## MDTraj parser compatibility

MDTraj input selection uses its installed PyParsing provider. PyParsing 3.3.3
regresses symbolic `<=` and `>=` comparisons; MolSysMT's optional `soft` extra
and maintained development/test environments exclude that exact version.
MDTraj 1.11.2 also excludes it in its public dependency metadata, but requires
Python 3.12 or later. MolSysMT therefore keeps older MDTraj available on Python
3.11 and constrains the transitive parser rather than raising MDTraj's floor.

For an existing Conda environment containing the incompatible parser, resolve
the dependency explicitly:

```bash
mamba install -c conda-forge 'pyparsing!=3.3.3'
```

With MDTraj 1.11.1, twelve symbolic/alias comparisons were verified using
PyParsing 3.2.5, 3.3.0, 3.3.1 and 3.3.2 on Linux/Python 3.14.7. Future parser
releases still require normal compatibility checks. The explicit `le` and `ge`
aliases work in the observed 3.3.3 pair, but MolSysMT does not rewrite queries,
patch the provider or silently change syntax. Provider parsing failures retain
their cause in the public `ArgumentError`.

See [MDTraj #2190](https://github.com/mdtraj/mdtraj/issues/2190),
[PyParsing #672](https://github.com/pyparsing/pyparsing/issues/672) and
[MolSysMT #484](https://github.com/uibcdf/molsysmt/issues/484).

## Missing hierarchy

MDTraj requires a target residue and chain for each atom. When native groups or
chains are absent, conversion supplies external-only UNL groups and a fallback
chain, preserving source atom correspondence and available charges/bonds. Known
molecules share a placeholder within each chain; atoms with no known molecule
get separate placeholders. Existing group rows retain their target order. A
partially assigned group uses its one known chain; multiple known chains in one
group fail explicitly. No groups, chains or chemical assignments are added to
the native source.

MDTraj `resid`, `chainid`, `protein` and related predicates use the external
target metadata, including placeholders. Missing biological identity is not
inferred; UNL placeholders do not count as proteins or water. Returned atom
indices remain aligned with the source used for selection. See
{ref}`Cookbook_Group_Free_Hierarchy` for executable source-preservation examples.


## Rule Languages

A function's built-in chemical rules and the user's query language are separate
contracts. The classic hydrogen-bond donor/acceptor readers evaluate their
built-in rules in MolSysMT syntax. Their `syntax` argument governs your selection
and custom inclusion/exclusion expressions, including supported MDTraj inputs.
An unsupported or malformed query raises rather than being silently translated
or retried in another language. Input rule lists remain unchanged. See
{ref}`Tutorial_Get_donor_atoms` and {ref}`Tutorial_Get_acceptor_atoms`.
