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

**ACE/NME templates include H-atom bonds** (updated March 2026):
- `ACE.json` bonds include `["CH3","HH31"]`, `["CH3","HH32"]`, `["CH3","HH33"]`.
- `NME.json` bonds include `["N","H"]`, `["C","H1"]`, `["C","H2"]`, `["C","H3"]`.

These bonds are resolved by `append_atoms_to_molsys` when inserting capping
groups so that downstream OpenMM conversion sees correct connectivity.

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

- **Case A** (completing existing free termini): two sub-steps:
  1. **C-terminus**: adds OXT if absent, placed geometrically using
     `place_oxt_atom` (mirror image of O reflected through the C→CA axis,
     symmetric carboxylate geometry, C-OXT ≈ 1.23 Å).
  2. **N-terminus**: adds H2/H3 if the N-terminal residue has a free amine
     (i.e. is not preceded by a non-amino-acid group such as ACE). H2/H3 are
     placed via `place_hydrogens_on_parent` using sp3 geometry on the nitrogen.
     If the first group in the chain is not an amino acid, the N-terminus is
     assumed to be already capped and this step is skipped.
- **Case B** (missing ACE or NME capping group): builds a new capping group
  from scratch using trans peptide-bond geometry, then calls
  `rebuild_molsys_with_new_groups` to insert it into the topology.
  Both ACE and NME are placed **with all H atoms** (HH31/HH32/HH33 for ACE;
  H, H1/H2/H3 for NME), so a separate `add_missing_hydrogens` call is not
  needed for the capping groups themselves.

Before querying `component_type`, always calls
`topology.rebuild_components(redefine_indices=True)` to ensure connectivity is
up to date — do not rely on metadata alone.

**PDBFixer engine**: delegates to `pdbfixer.missingTerminals` from
`findMissingAtoms`.

### `build.add_missing_hydrogens`

**Native engine** (`engine='MolSysMT'`): uses the amino-acid topology database
(`data/databases/amino_acids/`) to enumerate expected hydrogen names per
residue via `get_expected_hydrogens(pH=pH, ...)`, identifies missing ones by
set difference, and places them using geometric rules (bond lengths and angles
from CHARMM/AMBER conventions).

pH model applied by `get_expected_hydrogens`:
- **ASP**: deprotonated (no HD2) at pH ≥ 4.4
- **GLU**: deprotonated (no HE2) at pH ≥ 4.4
- **HIS**: HIE tautomer (HE2 only, no HD1) at pH ≥ 6.5
- **LYS**: deprotonated NZ (no HZ3) at pH ≥ 10.5
- **CYS**: no HG when in a disulfide bond (detected from SG–SG bonds)

**Capping groups:** ACE and NME are handled via their residue templates
(`residue_templates/ACE.json`, `residue_templates/NME.json`).  H atoms placed:
HH31/HH32/HH33 on ACE CH3; H on NME N; H1/H2/H3 on NME C.

**PDBFixer engine**: delegates to `pdbfixer.addMissingHydrogens(pH)` which
uses the same fixed-threshold pH model via OpenMM force-field templates.

**Both engines use the same pH model** (fixed pKa thresholds). Neither
implements environment-dependent pKa prediction (PROPKA-style), which is a
post-1.0 item.

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

**Ion placement (MolSysMT engine):** after water tiling and overlap removal,
ions are placed by a rejection-sampling loop over shuffled water oxygens:
a candidate is accepted only if its distance to every solute atom is ≥ 5 Å
(avoids pockets and channels) and its distance to every previously placed ion
is ≥ 0.5 Å. Accepted water molecules are removed and replaced by single-atom
ion groups. The number of ions is determined by:
- `n_cations/n_anions='neutralize'` — reads solute charge via
  `get_charge(definition='physical_pH7')` and adds enough counter-ions.
- `ionic_strength` — adds extra Na⁺/Cl⁻ pairs using OpenMM's formula:
  `n_pairs ≈ n_waters × C_M / 55.4`.

**Box shapes (MolSysMT engine):** cubic, rectangular, truncated octahedral,
and rhombic dodecahedral.  For non-orthogonal shapes the box is described by a
full 3×3 matrix; water tiling uses the Cartesian bounding box of the 8
unit-cell corners, and molecules outside the unit cell are removed via
fractional-coordinate filtering (`s = xyz @ M⁻¹`, keep if all sᵢ ∈ [0, 1)).

**Constraints of the MolSysMT engine:**
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

## `build.get_missing_residues`

**Native engine** (`engine='MolSysMT'`, default):

Compares the *structural* sequence (groups actually present in the system)
against a *reference* sequence using `difflib.SequenceMatcher`.  Each
`'delete'` opcode (residues in the reference but absent from the structure)
produces one entry in the output dict.

**Reference sequence resolution** (in order of priority):

1. `sequence` argument — explicit `{chain_id: [res_name, ...]}` dict.
2. Auto-detected from the input form:
   - `file:pdb` → SEQRES records parsed by `PDBFileHandler`
     (`entry.primary_structure.seqres`).
   - `file:bcif`, `file:bcif_gz` → `_entity_poly_seq` table from the mmCIF
     binary container, with chain mapping via `_entity_poly.pdbx_strand_id`.
   - `string:pdb_id` → downloads the bcif and uses the same path.
3. If no sequence is available → emits a `UserWarning` and returns `{}`.

The function converts the molecular system to `molsysmt.MolSys` internally
before querying structural sequences, so all forms that support conversion
to MolSys are supported.

**PDBFixer engine**: delegates to `pdbfixer.findMissingResidues`.  Requires
PDBFixer and OpenMM.  Ignores the `sequence` argument.

---

## Native Coverage of `build/` (as of March 2026)

All public `build/` functions now have `engine='MolSysMT'` as the default:

| Function | Notes |
|----------|-------|
| `add_missing_heavy_atoms` | Kabsch alignment against JSON residue templates |
| `add_missing_terminal_cappings` | Case A (free termini) + Case B (ACE/NME) |
| `add_missing_hydrogens` | Fixed pKa thresholds; ACE/NME fully supported via templates |
| `solvate` | All four orthogonal/non-orthogonal box shapes; ions via rejection sampling |
| `mutate` | Kabsch sidechain placement; PyRosetta engine is post-1.0 |
| `get_missing_residues` | SequenceMatcher + SEQRES/bcif auto-detection |
| `get_missing_heavy_atoms` | Template lookup |
| `get_missing_terminal_cappings` | Template lookup |
| `get_non_standard_residues` | Residue name lookup |

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

**Note on `add_missing_hydrogens` parity:** both engines (MolSysMT and
PDBFixer) use the same fixed-threshold pH model and are at parity for standard
residues. For neutral internal residues the H counts are identical. Small
differences (< 15 %) can arise from terminal handling (OXT, HXT, N-terminal
protonation variants) and are expected — the parity test allows a ±15 %
tolerance for real proteins. Environment-dependent pKa prediction (PROPKA-
style) is a post-1.0 item.

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

## `amino_acids/` database: AMBER force-field variants (added March 2026)

The per-residue topology databases (`A.pkl.gz` … `Y.pkl.gz`) store a list of
topology *variants* for each amino acid (e.g. mid-chain, N-terminal, C-terminal,
protonation states). Two AMBER-specific mid-chain variants were missing and
caused `add_missing_heavy_atoms` to generate wrong atom names after `mutate`:

| Residue | AMBER mid-chain naming | Was missing |
|---------|----------------------|-------------|
| GLY | `HA2`, `HA3` | yes — database only had `HA1/HA2` variant |
| LEU | `HB2`, `HB3` | yes — database only had `HB1/HB2` variant |

Both variants were added programmatically (via the `make_*_db` script) at
index 2 in the variant list, before the existing HA1/HA2 and HB1/HB2 entries.
`get_expected_heavy_atoms` selects the tightest-fit variant, so the AMBER
naming is now chosen when the present atoms already use HA2/HA3 or HB2/HB3.

**Rule**: whenever a post-`mutate` structure shows wrong heavy atom names
(e.g. `HA1` instead of `HA3`), check whether the AMBER variant for that
residue is present in the database.

---

## `append_atoms_to_molsys`: atom ordering invariant (March 2026)

OpenMM requires all atoms within a residue to be contiguous in the topology.
`append_atoms_to_molsys` (in `build/_native_placers.py`) used to append new
atoms at the end of the atom list regardless of their group membership, which
broke OpenMM conversion for any system where the new atoms belonged to a group
in the middle of the chain.

**Fix**: after collecting all new atoms, `append_atoms_to_molsys` now sorts
the new-atom list by `group_index` (stable sort) and remaps all bond indices
accordingly before inserting them into the topology.

**Rule**: every code path that calls `append_atoms_to_molsys` must set the
correct `group_index` on new atoms before the call. The sort is a safety net
but not a substitute for correct group assignment.

---

## `rebuild_molecules` ordering invariant (March 2026)

`infer_molecule_names_from_topology` reads `molecule_type` from the molecules
DataFrame to decide which naming scheme to apply (e.g. `'peptide 0'`, `'water'`,
ion name). In `topology.rebuild_molecules`, the previous code computed names
*before* types, so `molecule_type` was always NaN at the time names were
generated, causing all molecules to fall through to the `'unknown N'` branch.

**Fix**: in `rebuild_molecules`, `redefine_types` now runs before
`redefine_names`. The rule generalises: any inference function that reads a
derived attribute must be called after the function that writes that attribute.

---

## `get_missing_residues` (PDBFixer and native, March 2026)

The native engine (`engine='MolSysMT'`, default) compares the structural
sequence against a reference sequence using `difflib.SequenceMatcher`.
The reference is resolved from SEQRES records (PDB), `_entity_poly_seq`
(mmCIF/bcif), or an explicit `sequence` argument.

The PDBFixer engine (`engine='PDBFixer'`) delegates to
`pdbfixer.findMissingResidues`. It requires OpenMM and PDBFixer and ignores
the `sequence` argument.
