# Structure Preparation Pipeline

## Overview

Before a protein structure can be used for molecular dynamics simulation it
typically needs to be "prepared": missing atoms must be added, termini must be
completed, hydrogens placed, and the system solvated.  MolSysMT provides native
implementations of each step so the full pipeline can be run without any
external dependency.

This document describes:

1. The canonical step order and the reason for it.
2. The available engines at each step and their trade-offs.
3. A complete end-to-end example.
4. Limitations that still require an external engine (OpenMM).

---

## Canonical Step Order

```
(optional) solve_atoms_with_alternate_location
                    ↓
         add_missing_heavy_atoms
                    ↓
       add_missing_terminal_cappings
                    ↓
          add_missing_hydrogens
                    ↓
               solvate
                    ↓
         minimize  (OpenMM — outside MolSysMT scope)
```

The order is not arbitrary:

| Why this order | Consequence of reversing |
|----------------|--------------------------|
| Heavy atoms before terminal cappings | `add_missing_terminal_cappings` calls `add_missing_heavy_atoms` internally for Case A (native engine). Running heavy atoms first avoids double work and ensures the topology is complete before deciding capping geometry. |
| Heavy atoms and cappings before hydrogens | `add_missing_hydrogens` places H relative to heavy-atom neighbors. If heavy atoms are missing, H positions will be wrong or the function will skip the residue entirely. |
| Hydrogens before solvation | The overlap-removal step in `solvate` needs all solute atoms present so the exclusion volume is correct. Solvating a heavy-only structure leaves too little clearance around H positions that will be added later. |
| Solvation before minimization | The initial water/ion positions from tiling are not equilibrated. A short energy minimization (steepest descent or L-BFGS in OpenMM) relaxes clashes and bad contacts. |

---

## Step Details

### 0. Solve alternate locations (optional)

If the PDB file contains atoms with alternate location indicators (column 17),
only one conformer should be kept before proceeding.

```python
mol = msm.build.solve_atoms_with_alternate_location(mol, criterion='occupancy')
```

**Engine:** `engine='MolSysMT'` (only option). Selects the conformer with the
highest occupancy for each atom that has multiple alternate locations.

---

### 1. Add missing heavy atoms

Adds sidechain and backbone heavy atoms that are absent from the input
structure.  Does **not** add OXT (handled in the next step) or any H atom.

```python
mol = msm.build.add_missing_heavy_atoms(mol, engine='MolSysMT')
```

| Engine | Approach | Dependency |
|--------|----------|------------|
| `'MolSysMT'` | Kabsch alignment against 3D residue templates in `data/databases/residue_templates/` | none |
| `'PDBFixer'` | PDBFixer `findMissingAtoms` + `addMissingAtoms` | pdbfixer, openmm |

**MolSysMT limitations:** residue templates exist for the 20 standard amino
acids, ACE, NME, and the 8 standard DNA/RNA nucleotides.  Non-standard residues
fall back to no-op (atoms not added).

---

### 2. Add missing terminal cappings

Completes free termini.  Two cases are handled by the native engine:

* **Case A** (`N_terminal=None, C_terminal=None`): completes the existing
  terminal residues by adding atoms that are absent, most importantly OXT at
  the C-terminal carboxylate.  This is the default when no capping groups are
  requested.
* **Case B**: inserts ACE (N-terminal) or NME (C-terminal) as new groups, using
  trans peptide-bond geometry.

```python
# Case A — complete free termini only
mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')

# Case B — neutralise termini with ACE/NME caps
mol = msm.build.add_missing_terminal_cappings(
    mol, N_terminal='ACE', C_terminal='NME', engine='MolSysMT'
)
```

**Key rule:** call `topology.rebuild_components()` is handled internally before
querying `component_type`, so the function is robust to any input origin.

**MolSysMT limitations:** only ACE and NME are supported as capping groups.
PDBFixer supports a wider range of terminal variants via its residue template
library.

---

### 3. Add missing hydrogens

Places all hydrogen atoms that are absent from the structure.

```python
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')
```

| Engine | pH model | Dependency |
|--------|----------|------------|
| `'MolSysMT'` | Fixed pKa thresholds from `get_expected_hydrogens` | none |
| `'PDBFixer'` | Same fixed pKa thresholds via OpenMM `addMissingHydrogens` | pdbfixer, openmm |
| `'OpenMM'` | Same fixed pKa thresholds via `Modeller.addHydrogens` | openmm |

All three engines use **the same pH model** (fixed thresholds): ASP and GLU
deprotonated at pH ≥ 4.4, HIS in HIE tautomer at pH ≥ 6.5, LYS protonated
below pH 10.5, CYS HG removed when in a disulfide bond.  There is no
environment-dependent pKa prediction (PROPKA-style) in any engine; that is a
post-1.0 item.

**MolSysMT limitation:** non-standard groups (ACE, NME) are silently skipped;
their H atoms are not placed.  Use `engine='OpenMM'` or `engine='PDBFixer'`
if H on capping groups is required.

---

### 4. Solvate

Surrounds the prepared solute with an explicit water box and optionally adds
counter-ions.

```python
mol = msm.build.solvate(
    mol,
    box_shape='cubic',
    clearance='14 angstroms',
    water_model='TIP3P',
    n_cations='neutralize',
    n_anions='neutralize',
    ionic_strength='0.15 molar',
    engine='MolSysMT',
)
```

| Engine | Box shapes | Water models | Ions | Dependency |
|--------|------------|-------------|------|------------|
| `'MolSysMT'` | cubic, rectangular, truncated octahedral, rhombic dodecahedral | SPC, SPC/E, TIP3P, TIP4P-EW | Na+, K+, Li+, Rb+, Cs+, Cl-, Br-, F-, I- | none |
| `'OpenMM'` | same as above + more | all above + TIP3P-FB, TIP4P-2005, TIP5P, … | same | openmm |
| `'PDBFixer'` | same as OpenMM | same as OpenMM | same | pdbfixer, openmm |

**Ion placement (MolSysMT):** random rejection sampling from water oxygens,
accepting only candidates that are ≥ 5 Å from any solute atom and ≥ 0.5 Å from
previously placed ions.  This avoids placing ions in pockets or channels.

**Non-orthogonal boxes (MolSysMT):** truncated octahedral and rhombic
dodecahedral boxes are built from the conventional box vectors, water tiling
uses the Cartesian bounding box of the unit cell, and molecules outside the
unit cell are removed via fractional coordinate filtering (`s = xyz @ M⁻¹`).

---

### 5. Energy minimization (outside MolSysMT scope)

After solvation the initial atomic positions are not equilibrated.  A short
energy minimization removes clashes introduced by tiling and ion placement.
This step requires OpenMM (or another MD engine) and is intentionally outside
MolSysMT's scope:

```python
import openmm as mm
import openmm.app as app

# Convert to OpenMM simulation
simulation = msm.convert(mol, to_form='openmm.Simulation',
                          forcefield='AMBER14', water_model='TIP3P')
simulation.minimizeEnergy(maxIterations=1000)

# Convert back to MolSysMT if needed
mol_min = msm.convert(simulation, to_form='molsysmt.MolSys')
```

---

## Complete Example

```python
import molsysmt as msm

# --- Load a raw PDB structure ---
mol = msm.convert('181L', to_form='molsysmt.MolSys',
                  selection='molecule_type=="protein"')

# --- Optional: resolve alternate locations ---
# mol = msm.build.solve_atoms_with_alternate_location(mol, criterion='occupancy')

# --- Step 1: complete heavy atoms ---
mol = msm.build.add_missing_heavy_atoms(mol, engine='MolSysMT')

# --- Step 2: complete terminal residues ---
mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')

# --- Step 3: add hydrogens at pH 7.4 ---
mol = msm.build.add_missing_hydrogens(mol, pH=7.4, engine='MolSysMT')

# --- Step 4: solvate ---
mol = msm.build.solvate(
    mol,
    box_shape='cubic',
    clearance='14 angstroms',
    water_model='TIP3P',
    n_cations='neutralize',
    n_anions='neutralize',
    ionic_strength='0.15 molar',
    engine='MolSysMT',
)

# --- Step 5: minimize (requires OpenMM) ---
# simulation = msm.convert(mol, to_form='openmm.Simulation', ...)
# simulation.minimizeEnergy(maxIterations=1000)
```

---

## Engine Choice Summary

| Step | Recommended engine | When to use PDBFixer/OpenMM instead |
|------|--------------------|--------------------------------------|
| `solve_atoms_with_alternate_location` | `MolSysMT` | (only option) |
| `add_missing_heavy_atoms` | `MolSysMT` | Non-standard residues with templates only in PDBFixer |
| `add_missing_terminal_cappings` | `MolSysMT` | Capping groups other than ACE/NME |
| `add_missing_hydrogens` | `MolSysMT` | H on capping groups (ACE/NME) required |
| `solvate` | `MolSysMT` | TIP5P or other unsupported water models; box shapes beyond cubic/rectangular/truncated octahedral/rhombic dodecahedral |
| Minimization | — | Always OpenMM (outside MolSysMT scope) |

---

## See Also

- `devguide/auxiliary_data_and_nativization.md` — how native engine data is
  organized, the `set()` guard pattern for PDBFixer branches, parity tests
- `devguide/element_and_native_rebuild.md` — component vs molecule concepts,
  when to call `rebuild_components()`
- `tests/build/test_structure_preparation_pipeline.py` — end-to-end integration
  test covering this pipeline on a real PDB structure
