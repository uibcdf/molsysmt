---
name: Public API candidates from _native_placers
description: Suggestion to promote load_residue_template (and possibly a generic place_template_atoms) from build/_native_placers.py to the public API
type: project
---

`molsysmt/build/_native_placers.py` contains `load_residue_template()` and the Kabsch-based `place_missing_in_group()` helper. During the implementation of `add_missing_heavy_atoms(engine='MolSysMT')` and `add_missing_terminal_cappings(engine='MolSysMT')`, the user noted these could have legitimate independent public value.

**Why:** Advanced users building custom residues, placing ligand atoms, or inspecting/extending the residue template database would benefit from direct access. Currently the templates are only accessible implicitly through `get_expected_heavy_atoms` and the peptide builder.

**How to apply:** After dogfooding/beta, consider promoting `load_residue_template` to `molsysmt.element.group` or `molsysmt.build`, and a generic `place_template_atoms(molsys, group_idx, template)` to `molsysmt.build`. Keep the current private versions in place until the public API is stable.
