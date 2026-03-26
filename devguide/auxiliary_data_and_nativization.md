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

data/water/             # pre-equilibrated water box PDB files (see below)
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

### `data/water/` — pre-equilibrated water boxes

Introduced in March 2026 to support `solvate(engine='MolSysMT')`.
Contains four pre-equilibrated water box PDB files:

| File | Water model | N waters | Box size (nm) | Source |
|------|------------|----------|---------------|--------|
| `tip3p.pdb` | TIP3P | 895 | 3.0 × 3.0 × 3.0 | OpenMM template |
| `spce.pdb` | SPC/E | 895 | 3.0 × 3.0 × 3.0 | OpenMM template |
| `tip4pew.pdb` | TIP4P-EW | 895 | 3.0 × 3.0 × 3.0 | OpenMM template |
| `spc216.gro` | SPC | 216 | 1.86206 × 1.86206 × 1.86206 | Berendsen 1984 (GROMACS) |

The directory is a Python package (`__init__.py`) so that
`importlib.resources` can locate the files at runtime without hardcoding
file-system paths.

**Canonical water model names** (as accepted by `solvate` and defined in
`molsysmt/molecular_mechanics/forcefields.py`): `'SPC'`, `'SPC/E'`,
`'TIP3P'`, `'TIP4P-EW'`. Internal normalisation (stripping `/` and `-`)
maps these to `spce.pdb`, `tip3p.pdb`, `tip4pew.pdb`, and `spc216.gro`.

---

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

### `build.add_missing_heavy_atoms`

**Native engine** (`engine='MolSysMT'`): for each amino-acid residue with
missing heavy atoms, calls `load_residue_template` to load the JSON
coordinate template, then `place_missing_in_group` which uses
`get_least_rmsd_rotation_and_translation_single_structure` (Kabsch alignment)
to overlay the template onto the residue's present backbone atoms. Missing
atoms are appended to the MolSys topology and coordinates, and bonds are
resolved from the template. Logic lives in
`molsysmt/build/_native_placers.py`.

**PDBFixer engine**: delegates to `pdbfixer.findMissingAtoms` +
`pdbfixer.addMissingAtoms`.

Key helpers in `build/_native_placers.py`:
- `load_residue_template(name)` — load JSON template from `residue_templates/`
- `place_missing_in_group(tmp, group_index, template)` — Kabsch-align + append
- `append_atoms_to_molsys(tmp, new_atoms_df, new_coords)` — low-level append
- `place_oxt_atom(C_pos, CA_pos, O_pos, n_structures)` — mirror O through C→CA axis
- `place_ace_group / place_nme_group` — geometry-based capping placement
- `rebuild_molsys_with_new_groups` — full topology rebuild when inserting new groups

### `build.add_missing_terminal_cappings`

**Native engine** (`engine='MolSysMT'`): two cases:

- **Case A** (missing `OXT` on C-terminal residue): OXT is not in the standard
  residue template (templates contain the non-terminal form). It is placed
  geometrically using `place_oxt_atom`: OXT is the mirror image of O reflected
  through the C→CA axis (symmetric carboxylate geometry, C-OXT ≈ 1.23 Å).
  This is called after `add_missing_heavy_atoms` (which handles all other
  missing atoms) using `get_missing_terminal_cappings` to identify the affected
  groups.
- **Case B** (missing ACE or NME capping group): builds a new capping group
  from scratch using trans peptide-bond geometry, then calls
  `rebuild_molsys_with_new_groups` to insert it into the topology.

Before querying `component_type`, always calls
`topology.rebuild_components(redefine_indices=True)` to ensure connectivity is
up to date — do not rely on metadata alone.

**PDBFixer engine**: delegates to `pdbfixer.missingTerminals` from
`findMissingAtoms`.

### `build.add_missing_hydrogens`

**Native engine** (`engine='MolSysMT'`): uses the amino-acid topology database
(`data/databases/amino_acids/`) to enumerate expected hydrogen names per
residue, identifies missing ones by set difference, and places them using
geometric rules (bond lengths and angles from CHARMM/AMBER conventions). No
protonation-state prediction.

**PDBFixer engine**: delegates to `pdbfixer.addMissingHydrogens(pH)` which
uses OpenMM force-field templates and protonation-state libraries.

### `build.solvate`

**Native engine** (`engine='MolSysMT'`):

1. Loads a pre-equilibrated water box from `data/water/` (see above).
2. Computes the number of tile copies needed in each dimension to cover the
   target box size.
3. Tiles the water box using numpy broadcasting:
   ```python
   tiled_xyz = template_xyz[np.newaxis] + offsets[:, np.newaxis]
   # shape: (n_tiles, n_atoms_per_tile, 3)
   ```
   All tile coordinates are generated in a single vectorised operation —
   no Python loop over individual tiles.
4. Topology arrays (atoms, groups, bonds) are replicated with `np.tile` plus
   index offset arithmetic.
5. Clips the combined water box to the target box dimensions.
6. Removes water molecules within `clearance_nm` of any solute atom (KD-tree
   distance query).
7. Merges solute + remaining waters using `molsysmt.basic.merge`.

**Constraints of the MolSysMT engine:**
- Orthogonal boxes only (no triclinic support).
- Cannot add ions. For salt concentration or charge neutralisation, use
  `engine='OpenMM'` after solvation.
- No energy minimisation. It is strongly recommended to minimise with OpenMM
  after solvation to resolve any steric clashes at the solute–water interface.

**PDBFixer engine**: delegates to OpenMM/PDBFixer modeller for solvation and
(optionally) ion placement.

### `build.mutate`

**Native engine** (`engine='MolSysMT'`):

1. Parses the `mutations` argument (list of strings, dict by group index,
   dict by group id, or dict by group name) — same logic as the PDBFixer branch.
2. Renames the target groups directly in the topology DataFrame.
3. Strips all non-backbone atoms from each mutated group.
   Kept atoms: `{'N', 'CA', 'C', 'O', 'OXT'}`.
4. Calls `add_missing_heavy_atoms(engine='MolSysMT')` to rebuild the sidechain
   via Kabsch alignment against the residue template.
5. If the original system had hydrogen atoms, calls
   `add_missing_hydrogens(engine='MolSysMT')`.

**No energy minimisation is performed.** It is strongly recommended to
minimise the structure afterwards to resolve any steric clashes introduced
by the new sidechain. A future `engine='PyRosetta'` option is planned for
rotamer-library-based placement with full energy minimisation.

**PDBFixer engine**: uses `pdbfixer.applyMutations` (removes old sidechain,
Kabsch alignment on backbone, adds missing atoms via Langevin +
LocalEnergyMinimizer). Requires OpenMM and PDBFixer.

---

## Remaining PDBFixer-only Functions (as of March 2026)

Only one `build/` function still lacks a native engine:

| Function | Why PDBFixer is still needed |
|----------|------------------------------|
| `get_missing_residues` | Requires SEQRES records or external sequence databases not currently in MolSysMT's data layer |

All other `build/` functions (`add_missing_heavy_atoms`,
`add_missing_terminal_cappings`, `add_missing_hydrogens`, `solvate`, `mutate`)
now have `engine='MolSysMT'` as the default.

---

## PDBFixer Engine: the `set()` Guard Pattern

After PDBFixer modifies a structure (adding atoms, terminal groups, or
hydrogens), it converts the result back to the original form and then restores
metadata (component names, molecule names, chain IDs, entity names) that
PDBFixer would otherwise reset to generic values.

**Problem:** structural modifications can change the number of components or
molecules (e.g. adding sidechain atoms that bridge two previously disconnected
fragments reduces `n_components`; PDBFixer's entity grouping after
`addMissingAtoms` may differ from MolSysMT's). Calling `set(element='component', ...)`
with the old count onto a system with a new count raises `ValueError`.

**Pattern:** always check that the count matches before calling `set()`:

```python
_n_comp = get(output_ms, element='component', n_components=True, skip_digestion=True)
if _n_comp == len(next(iter(atts_from_components.values()))):
    set(output_ms, element='component', **atts_from_components, skip_digestion=True)
```

Apply this guard to component, molecule, chain, and entity `set()` calls in
every PDBFixer engine branch of `build/` functions. It is already implemented
in `add_missing_heavy_atoms`, `add_missing_terminal_cappings`, and
`add_missing_hydrogens`.

---

## Parity Tests: Engine Agreement

Every nativized `build/` function has a dedicated parity test file that runs
both engines on the same structure and checks they agree:

| Function | Parity test file |
|----------|-----------------|
| `get_missing_heavy_atoms` | `test_get_missing_heavy_atoms.py` (inline) |
| `get_missing_terminal_cappings` | `test_get_missing_terminal_cappings.py` (inline) |
| `get_non_standard_residues` | `test_get_non_standard_residues_parity.py` |
| `add_missing_heavy_atoms` | `test_add_missing_heavy_atoms_parity.py` |
| `add_missing_terminal_cappings` | `test_add_missing_terminal_cappings_parity.py` |
| `add_missing_hydrogens` | `test_add_missing_hydrogens_parity.py` |
| `mutate` | `test_mutate_parity.py` |

**Known expected difference** in `add_missing_hydrogens`: PDBFixer calls
`addMissingHydrogens(pH=7.4)` which uses OpenMM's protonation-state library
(ASP/GLU deprotonated at physiological pH, HIS tautomers assigned). The
MolSysMT engine adds all hydrogens from the topology database without
protonation-state prediction. For neutral peptides with no ionisable residues
the counts are identical; for real proteins the counts diverge by up to ~15 %,
which the parity test allows explicitly. Improving MolSysMT's protonation
prediction is a pending future task (see pending tasks).

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
