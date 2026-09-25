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
