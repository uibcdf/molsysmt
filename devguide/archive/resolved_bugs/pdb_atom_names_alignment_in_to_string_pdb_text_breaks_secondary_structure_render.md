---
summary: PDB atom names alignment in to_string_pdb_text breaks secondary structure rendering in NGLView
issue: uibcdf/molsysmt#174
status: resolved
opened: 2026-08-19
closed: 2026-08-19
severity: high
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_MolSys/test_pdb_text_atom_name_alignment.py
normative:
blocked_by: []
supersedes: []
---

# PDB atom names alignment in to_string_pdb_text breaks secondary structure rendering in NGLView

**Reported:** 2026-08-19 during NGLView visual inspection and tutorial unit compilation in `docs/content/user/tools/third_party/nglview/`.
**Status:** Open defect report awaiting code fix.

## What

When converting molecular systems to `string:pdb_text` via `msm.form.molsysmt_MolSys.to_string_pdb_text`, atom names in columns 13–16 are formatted using left alignment `{str(atom.atom_name)[:4]:<4}`. This outputs 1- and 2-character atom names starting at column 13 (e.g. `'N   '`, `'CA  '`, `'C   '`, `'O   '`) rather than the standard PDB format which indents 1- and 2-character chemical elements to start at column 14 (e.g. `' N  '`, `' CA '`, `' C  '`, `' O  '`).

When NGLView loads this PDB structure via its WebGL engine (NGL.js), the NGL.js PDB parser fails to recognize the amino acid backbone atoms because it looks for standard 4-character column alignment (`' CA '`, `' N  '`). Consequently, NGL.js fails to build secondary structure spline ribbons, rendering an empty/blank canvas when representations like `cartoon` or `ribbon` are applied.

```python
import molsysmt as msm
molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'], to_form='molsysmt.MolSys')
pdb_text = msm.convert(molsys, to_form='string:pdb_text', structure_indices=[0])
# ATOM      1 N    MET A   1      43.982  -3.258   9.163  0.00 28.71           N  
# ATOM      2 CA   MET A   1      43.434  -1.917   9.134  0.00 24.31           C  
```

## How

In `molsysmt/form/molsysmt_MolSys/to_string_pdb_text.py` at lines 290–292:

```python
lines.append(
    f"{'ATOM':<6}{serial:>5} "
    f"{str(atom.atom_name)[:4]:<4}{location:1}"
    f"{str(group['group_name'])[:3]:>3} "
    f"{chain_id[:1]:1}{str(group['group_id'])[:4]:>4}    "
    f"{x:>8.3f}{y:>8.3f}{z:>8.3f}"
    f"{float(occupancies[variant_index]):>6.2f}"
    f"{float(b_factors[variant_index]):>6.2f}"
    f"{'':10}{element_symbol[:2]:>2}"
    f"{_charge_field(charge):>2}\n"
)
```

According to the WWPDB PDB Format 3.3 specifications (ATOM / HETATM record format, columns 13–16):
- Atom names start in column 13 if the chemical symbol has two letters (e.g., `FE`, `MG`, `CL`, `NA`), or if it is a 4-character name (e.g., `1HG1`).
- Atom names start in column 14 (preceded by a space in column 13) if the chemical symbol has one letter (e.g., `C`, `N`, `O`, `S`, `H`, `P`).

## Why

This affects every downstream tool or converter relying on `string:pdb_text`, including `molsysmt.third_party.nglview.molsysmt_trajectory.MolSysMTTrajectory`, which converts snapshots to `string:pdb_text` for NGLView visualization. All cartoon representations in NGLView rendered from `molsysmt.MolSys` display an invisible structure.

## What is measured and what is assumed

- **Measured:** Tested PDB text with `f" {name:<3}"` vs `f"{name:<4}"` with `nglview.show_text()`. The standard-aligned PDB immediately renders the 3D protein cartoon in NGL.js WebGL canvas, whereas the left-aligned PDB renders 0 spline segments (blank canvas).
- **Measured:** `view_181.html` in `docs/_static/nglview/` contains `"  N   "` and `"  CA  "` generated historically by OpenMM 8.0, and renders correctly.

## What was refuted

- **Refuted:** The blank canvas was initially suspected to be only caused by widget module version mismatch (`model_module_version: "4.0"` vs `"3.0.1"`). Resolving the widget version allows the canvas to initialize, but secondary structure remains completely blank due to the PDB atom name column misalignment.

## Scope and exclusions

- **Scope:** `molsysmt/form/molsysmt_MolSys/to_string_pdb_text.py` and any other native PDB writers in MolSysMT.
- **Exclusions:** Does not affect readers or non-PDB formats (`mmcif`, `h5msm`).

## Acceptance criteria

- `to_string_pdb_text` formats atom names adhering to the standard PDB 3.3 specification (columns 13–16).
- A unit test verifies standard column alignment for 1-letter, 2-letter, and 4-letter atom names in generated PDB text.
- `msm.view(molsys, viewer='NGLView')` displays the 3D cartoon structure in NGLView.

## Provenance

- Linux 6.6, Python 3.13.2, NGLView 4.0.1, MolSysMT 0.20.0 (2026-08-19).

## Resolution — 2026-08-19

The report is correct, and was validated against the specification rather than
accepted. wwPDB v3.3, ATOM record: "Alignment of one-letter atom name such as C
starts at column 14, while two-letter atom name such as FE starts at column 13."

The rule keys on the element symbol, not on the length of the name. The alpha carbon
`CA` is element `C` and starts at column 14; the calcium ion `CA` is element `CA` and
starts at column 13.

Measured against the RCSB file MolSysMT ships for the same system, **1439 of 1441
atoms** were misaligned. The two that matched were chlorides, where a two-letter
element makes left-justification correct by accident — which is itself the clearest
demonstration that the rule is about the element.

After the fix, 9 312 atoms across `181l`, `1tcd`, `1atp` and `1ycr` round-trip with
zero differences in columns 13-16.

### This is the cause of uibcdf/molsysmt#163

That report was closed on 2026-08-18 as a MolSysViewer defect and filed as
[`uibcdf/molsysviewer#64`](https://github.com/uibcdf/molsysviewer/issues/64). The
diagnosis was wrong.

`third_party/nglview/molsysmt_trajectory.py` converts the system to
`string:pdb_text` and returns it from `get_structure_string()`, which is what NGL
parses. A backbone NGL.js cannot recognise explains precisely what was observed: the
waters of every symmetry copy rendered as points, and the proteins — which need a
recognised backbone for cartoon — rendered as nothing.

Everything measured for #163 remains true: `make_bioassembly` does generate all 60
copies, transformed and with secondary structure assigned, and the viewer does
receive all 95 280 atoms. What was wrong was the conclusion drawn from it. The data
reached the viewer; the *format* did not let it be read.

### What was refuted

*The problem is only that MolSysViewer does not render large assemblies.* It is not
about size. The same misalignment affects every system converted to `string:pdb_text`,
including a single-chain protein.

### Scope

`to_string_pdb_text` in `molsysmt_MolSys` is the only writer of ATOM records.
`native/_pdb_file_handler_content.py` matches the same names but parses them.
