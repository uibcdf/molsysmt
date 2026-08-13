(user-foundations-support-selection-syntaxes)=
# Selection Syntaxes

MolSysMT provides a native declarative selection engine and selected interoperability
with third-party syntaxes. Support is directional: parsing a query and translating a set
of indices are separate capabilities.

---

## Supported syntaxes and shortcuts

| Syntax | Selection input | Translation output | Scope |
| :--- | :---: | :---: | :--- |
| **`MolSysMT`** (native) | Yes | No | Any supported molecular-system form |
| **`MDTraj`** | Yes | Yes | Inputs convertible to `mdtraj.Topology` |
| **`MDAnalysis`** | Yes | No | Inputs convertible to `MDAnalysis.Universe` |
| **`NGLView`** | No | Yes | Atom, group, and chain translations |

The input direction is selected with `syntax=...`; the output direction is requested
with `to_syntax=...`. A syntax listed in one direction is not implicitly supported in the
other. Use `msm.supported.syntaxes()` to inspect this matrix in the running version.

The native syntax includes attributes such as `atom_name`, `atom_type`, `group_name`,
`group_id`, `chain_id`, and `molecule_type`, together with `and`, `or`, and `not`.
Shortcuts such as `"protein"`, `"water"`, `"ions"`, and `"backbone"` are configured
through `msm.configure.selection_shortcuts`.
