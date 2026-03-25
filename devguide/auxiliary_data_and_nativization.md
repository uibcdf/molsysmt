# Auxiliary Data Repositories and Build Nativization

## Overview

MolSysMT has two canonical locations for auxiliary chemical and structural
information that supports the implementation of public functions:

| Directory | Role |
|-----------|------|
| `molsysmt/element/` | Classification helpers, look-up functions, and compact in-memory tables for atoms, groups, components, and molecules |
| `molsysmt/data/databases/` | Serialized databases (pickle + gzip, JSON) for topology templates, residue names, coordinate templates, and connectivity |

Any function that needs static chemical knowledge — residue names, expected
atoms, bond connectivity, 3D coordinate templates, classification rules —
should source it from these two locations, **not** from `build/_private/` or
other ad-hoc local stores.

---

## `molsysmt/element/`

Mirrors the hierarchy of MolSysMT's element model (atom → group → component →
molecule → entity → chain → system):

```
element/
  atom/        # atom name lists, element types, mass tables
  group/
    amino_acid/      # canonical amino acid functions
    nucleotide/      # nucleotide name lookups
    saccharide/      # saccharide names
    lipid/           # lipid names
    small_molecule/  # small-molecule classification
    water/           # water residue names
    ion/             # ion names
  component/
  molecule/
  entity/
```

### Atom name → element type mapping

**File:** `molsysmt/element/atom/names.py`

Contains a plain Python dict `atom` mapping ~250 standard atom names to element
symbols (e.g. `'CA' → 'C'`, `'OW' → 'O'`, `'HB2' → 'H'`).  Covers the most
common names from AMBER, CHARMM, OPLS, and GROMOS force fields.

Used by `get_atom_type_from_atom_name(atom_name)` (same package), which returns
`'UNK'` and prints a warning for any name not in the dict.

**When to extend it:**  whenever a file is loaded and `atom_type` is inferred as
`'UNK'` for atoms whose element is unambiguous (e.g. AMBER heme hydrogen names
`1HAA`, `2HAA`, CHARMM lipid names, custom residue names, etc.), add the missing
entries to `names.py`.  The dict is the canonical, single place to maintain this
mapping — do not add local fallback logic in parsers or converters.

```python
# Example: AMBER heme hydrogens (meso and beta positions)
'1HAA': 'H',  '2HAA': 'H',
'1HBA': 'H',  '2HBA': 'H',
'HHA':  'H',  'HHB':  'H',  'HHC': 'H',  'HHD': 'H',
'1HMA': 'H',  '2HMA': 'H',  '3HMA': 'H',
# ... add the full set when the source force field is known
```

The inference is used as a fallback whenever `atom_type` cannot be read directly
from the source file (e.g. PDB files that omit element columns 76-78).

---

### Key amino-acid helpers

All live in `molsysmt/element/group/amino_acid/`:

| Function / Object | What it provides |
|-------------------|-----------------|
| `group_names` | `list` of 134 recognized 3-letter names (`ALA`, `ARG`, …) |
| `group_types` / `name_to_type` | `dict` mapping ~817 names (standard + non-standard, D-forms, PTMs, protonation variants) to canonical 3-letter codes — derived from MDTraj |
| `get_standard_name(name)` | Returns the canonical standard 3-letter code for a non-standard amino acid, or `None` if the name is already standard, unknown, or not an amino acid |
| `get_expected_heavy_atoms(name, present_atom_names)` | Returns the set of expected heavy atoms for a residue using the topology database; selects the *tightest-fit* variant (fewest extra atoms among variants that are a superset of the present heavy atoms) |
| `get_group_db(name)` | Returns the full topology database entry (atoms + bonds per variant) for a residue name |

`get_standard_name` and `get_expected_heavy_atoms` are public API additions
introduced for the nativization of `build/` functions (see below).

---

## `molsysmt/data/databases/`

```
data/databases/
  amino_acids/          # per-residue topology: atoms + bonds, all variants
                        # keyed by first letter (A.pkl.gz, C.pkl.gz, …)
                        # 134 amino acid names, ~817 name aliases covered
  terminal_cappings/    # N- and C-terminal capping topology
                        # n_terminal.json  (NME, NHE, NH2)
                        # c_terminal.json  (ACE)
  residue_templates/    # 3D coordinate templates for structure placement
                        # one JSON file per residue (see below)
  nucleotides/          # nucleotide topology
  saccharides/          # saccharide topology
  ions/                 # ion data
  waters/               # water residue data
  small_molecules/      # small-molecule data
  peptide_builder/      # auxiliary data for build_peptide
```

### `residue_templates/`

Introduced in March 2026 to support future `add_missing_heavy_atoms(engine='MolSysMT')`.
Contains one JSON file per residue:

```json
{
  "name": "ALA",
  "atoms": ["N", "CA", "C", "O", "CB"],
  "coords_nm": [[-0.1444, -0.0596, 0.0968], ...],
  "bonds": [["N", "CA"], ["CA", "C"], ...]
}
```

- **atoms**: heavy atoms only (no hydrogens).
- **coords_nm**: ideal coordinates in **nanometres** (Angstrom source / 10).
- **bonds**: bonds between heavy atoms.

Covered residues (30 total): 20 standard amino acids, ACE, NME, 4 RNA
nucleotides (A, C, G, U), 4 DNA nucleotides (DA, DC, DG, DT).

Source: PDBFixer templates at `pdbfixer/pdbfixer/templates/*.pdb`.
Bond connectivity: MolSysMT amino-acid database (`amino_acids/`) and
terminal-capping database (`terminal_cappings/`). RNA/DNA nucleotides have
empty bond lists (no MolSysMT database yet).

**To regenerate:**
```bash
python molsysmt/data/databases/residue_templates/make_residue_templates_db.py
```
Requires PDBFixer source available at `~/repos@others/pdbfixer`.

### When to add data here

Add new data to `data/databases/` when:
- The data is larger than a few hundred bytes and benefits from serialization.
- The data is domain knowledge (topology, connectivity, masses, charges) rather
  than implementation logic.
- The data needs to be loaded lazily (only when the relevant function is called).

Add small classification tables or name lists directly in `element/` (as Python
dicts or lists in `.py` files).

---

## Build Nativization: Design Principles

Several functions in `molsysmt/build/` originally depended on PDBFixer as their
only backend. The nativization effort (March 2026) follows these principles:

1. **Native as default** — `engine='MolSysMT'` is the default. It works with
   any supported form and requires no external dependency.

2. **PDBFixer as fallback** — `engine='PDBFixer'` is preserved for parity and
   for cases where PDBFixer's richer template library gives better results.

3. **Auxiliary data in canonical locations** — Supporting data lives in
   `element/group/amino_acid/` (classification) and `data/databases/amino_acids/`
   or `data/databases/residue_templates/` (serialized topology). Never in
   `build/_private/`.

4. **PDBFixer remains a soft dependency** — declared in
   `[project.optional-dependencies] soft` in `pyproject.toml`. It is lazily
   imported only inside `if engine == 'PDBFixer':` branches.

---

## Nativized Functions (March 2026)

### `build.get_non_standard_residues`

**Native engine**: uses `name_to_type` from
`element/group/amino_acid/group_types.py` (~817-entry MDTraj-derived table) to
identify residues whose name maps to a *different* canonical 3-letter code.
Residues mapping to `XAA` (completely unknown) are not reported.

**PDBFixer engine**: uses `pdbfixer.findNonstandardResidues` (~150-entry table).
Also reads MODRES records when the source is a PDB/mmCIF file.

The native engine covers a much larger synonym space than PDBFixer.

### `build.get_missing_heavy_atoms`

**Native engine**: for each amino-acid residue in the selection, calls
`get_expected_heavy_atoms` with the present atom names to select the
tightest-fit topology variant, computes the set difference, and excludes
`OXT` (which is the responsibility of `get_missing_terminal_cappings`).

**PDBFixer engine**: delegates to `pdbfixer.findMissingAtoms`.

Both engines return identical results on Barnase-Barstar (1brs, 25 residues
with missing sidechain/backbone atoms).

Key detail: `get_expected_heavy_atoms` selects among all topology variants the
one whose heavy atoms are a superset of the present heavy atoms AND that has
the fewest extra atoms — the *tightest fit*. This avoids false-positive reports
of `OXT` as missing for internal residues (whose topology database entry has an
OXT-containing variant as canonical).

### `build.get_missing_terminal_cappings`

**Native engine**: for each chain, finds the C-terminal amino-acid residue by
sorting groups within the chain by their `group_id` (sequence number cast to
`int`) and taking the last one. If the very last group in the chain (by
`group_id`) is *not* an amino acid (e.g. NME or ACE capping group), the chain
is skipped. Otherwise, checks for `OXT`; if absent, reports it as missing.

**PDBFixer engine**: uses `pdbfixer.missingTerminals` from `findMissingAtoms`.

This sorting-by-group-id approach correctly handles multi-model structures
(e.g. 1brs) where MolSysMT stores group indices within a chain in group-index
order rather than sequence order.

---

## Remaining PDBFixer-only Functions (as of March 2026)

The following `build/` functions still require `engine='PDBFixer'` because they
need PDBFixer's 3D placement or force-field knowledge:

| Function | Why PDBFixer is still needed |
|----------|------------------------------|
| `add_missing_heavy_atoms` | Needs 3D coordinate templates for atom placement (residue_templates/ populated but placement code not yet written) |
| `add_missing_terminal_cappings` | Same — 3D placement |
| `add_missing_hydrogens` | Needs OpenMM/PDBFixer for H-bond geometry and protonation states |
| `solvate` | Needs OpenMM for water box placement |
| `mutate` | Needs PDBFixer template-substitution logic |

The `residue_templates/` database provides all 3D coordinate data needed for a
future native implementation of `add_missing_heavy_atoms`.

---

## How to Add a New Native Build Function

1. **Identify the auxiliary data needed** (topology, atom names, coordinates).
2. **Check `element/` first** — is there already a look-up function for the
   residue type?
3. **Check `data/databases/`** — is the topology or coordinate data already
   serialized?
4. If not, add the data to the appropriate location:
   - Small tables: add as Python dicts/lists in `element/group/<type>/`.
   - Larger serialized data: add to `data/databases/<type>/` as pickle or JSON,
     with a `make_<name>_db.py` generation script.
5. Implement the native engine in the `if engine == 'MolSysMT':` branch.
6. Keep `engine='PDBFixer'` as a fallback if PDBFixer covers the same use case.
7. Set `engine='MolSysMT'` as the default once the native engine is verified.
8. Write tests that verify both engines agree on at least one real structure.

---

## `get_missing_residues` (PDBFixer-only, bug fixed March 2026)

`build.get_missing_residues` uses `pdbfixer.missingResidues`, which is a dict
`{(chain_index, insertion_position): [residue_names]}`. The function now
correctly iterates with `.items()` and returns this dict directly.

This function has no native implementation planned for 1.0.0 (detecting
missing residues requires SEQRES records or sequence databases not currently
in MolSysMT's data layer).
