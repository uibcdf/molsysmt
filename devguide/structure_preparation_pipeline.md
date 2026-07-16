# Structure Preparation Pipeline

## Overview

Before a protein structure can be used for molecular dynamics simulation it
typically needs to be "prepared": missing atoms must be added, termini must be
completed, hydrogens placed, and the system solvated. MolSysMT provides native
implementations for the preparation steps shown below, so an explicitly
selected native pipeline can run without an optional reconstruction dependency.
Energy minimization still requires an MD engine.

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
msm.build.solve_atoms_with_alternate_location(mol, location_id='occupancy')
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

**MolSysMT limitations:** the current missing-heavy-atom implementation targets
amino-acid groups using the standard residue templates. The presence of ACE,
NME, and nucleotide template files supports other build paths but does not by
itself make nucleotide heavy-atom reconstruction part of this function's
contract. Non-standard residues without a supported canonical template are not
completed.

---

### 2. Add missing terminal cappings

Completes free termini.  Two cases are handled by the native engine:

* **Case A** (`N_terminal=None, C_terminal=None`): completes the existing
  terminal residues by adding atoms that are absent.  Two sub-steps:
  - Adds OXT at the C-terminal carboxylate if absent.
  - Adds H2/H3 at the free N-terminal amine if absent (skipped when the first
    group in the chain is a non-amino-acid capping group such as ACE).
  This is the default when no capping groups are requested.
* **Case B**: inserts ACE (N-terminal) or NME (C-terminal) as new groups, using
  trans peptide-bond geometry.  Both groups are inserted **with all H atoms**
  (HH31/HH32/HH33 for ACE; H, H1/H2/H3 for NME), so no additional H placement
  is needed for the capping groups.

```python
# Case A — complete free termini only
mol = msm.build.add_missing_terminal_cappings(mol, engine='MolSysMT')

# Case B — neutralise termini with ACE/NME caps
mol = msm.build.add_missing_terminal_cappings(
    mol, N_terminal='ACE', C_terminal='NME', engine='MolSysMT'
)
```

**Key rule:** `topology.rebuild_components()` is called internally before
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

The native engine uses documented fixed pKa and tautomer rules. OpenMM and
PDBFixer apply their own template-based hydrogen-placement behavior for the
requested pH. None of these choices should be presented as an
environment-dependent pKa calculation comparable to PROPKA. Cross-engine
agreement must be demonstrated for each tested residue state rather than
assumed globally.

**Note on capping groups:** ACE/NME are fully supported by `engine='MolSysMT'`:
- Groups inserted by `add_missing_terminal_cappings(engine='MolSysMT')` (Case B)
  already carry all H atoms from the capping step.
- Pre-existing ACE/NME groups imported from a PDB file are handled by
  `add_missing_hydrogens(engine='MolSysMT')` using their residue templates.

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
# msm.build.solve_atoms_with_alternate_location(mol, location_id='occupancy')

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
| Minimization | — | Use a suitable external MD engine; the example uses OpenMM |

---

## See Also

- `devguide/BUILD_ECOSYSTEM.md` — how native chemical knowledge and build data
  are organized and maintained
- `devguide/CORE_SPECIFICATION.md` — component vs molecule concepts and native
  molecular-system invariants
- `tests/build/test_structure_preparation_pipeline.py` — end-to-end integration
  test covering this pipeline on a real PDB structure
