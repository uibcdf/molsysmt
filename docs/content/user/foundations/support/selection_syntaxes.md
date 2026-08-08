(user-foundations-support-selection-syntaxes)=
# Selection Syntaxes

MolSysMT provides a powerful selection engine supporting native declarative expressions and cross-compatibility shortcuts with major third-party selection syntaxes.

---

## Supported Syntaxes & Shortcuts

| Syntax Name | Key Operators & Keywords | Example Expression |
| :--- | :--- | :--- |
| **`MolSysMT`** (Native) | `atom_name`, `atom_type`, `group_name`, `group_id`, `chain_id`, `molecule_type`, `and`, `or`, `not` | `"atom_name == 'CA' and group_name in ['ALA', 'GLY']"` |
| **`AMBER`** | `:res_name`, `@atom_name`, `*`, `:` | `":1-100@CA"` |
| **`MDAnalysis`** | `resname`, `name`, `resid`, `protein`, `backbone` | `"resname ALA and name CA"` |
| **`PyTraj`** | `:res_range@atom_name` | `":1-50@C,CA,N"` |
| **Shortcuts** | Shortcuts configured via `msm.configure.selection_shortcuts` | `"protein"`, `"water"`, `"ions"`, `"backbone"` |
