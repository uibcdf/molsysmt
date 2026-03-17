# Testing Form Adapters

This guide covers the practical patterns for writing tests for MolSysMT form adapters. It
complements `testing_strategy.md` (which governs what to test and why) with concrete
implementation guidance for how to test each form's `get_topological_attributes`,
`get_structural_attributes`, and related functions.

---

## Two test files per form

Each supported form in `tests/form/<form_name>/` should have at least two test files:

| File | Purpose |
|------|---------|
| `test_get_topological_attributes_from_builder.py` | Ground-truth fixture built with `MolSysBuilder`; tests the adapter's attribute extraction functions with known-exact values |
| `test_get_topological_attributes_from_<ext>.py` | Parser test using a real external file (PDB, XTC, etc.); confirms the adapter correctly parses actual format output |

The builder-based file is the primary correctness test. The parser-based file guards against
regressions in format-specific parsing logic.

Completed form adapters with both test files (as of March 2026):

| Form | Builder tests | Parser/oracle tests | Notes |
|------|:---:|:---:|-------|
| `mdtraj_Topology` | 384 | 15 (PDB oracle) | |
| `openmm_Topology` | 393 | 15 (PDB oracle) | |
| `openmm_Modeller` | ~393 | 15 (PDB oracle) | delegates to `openmm_Topology` |
| `openmm_Simulation` | ~393 | 13 (real AMBER14+CPU fixture) | delegates to `openmm_Topology` |
| `string_pdb_id` | — | 13 (local + 1 network smoke) | see "Network-dependent forms" below |
| `string_alphafold_id` | — | 13 (local + 1 network smoke) | see "Network-dependent forms" below |

---

## Network-dependent forms (`string:pdb_id`, `string:alphafold_id`)

Forms whose adapter internally downloads data from a remote service (PDB, AlphaFold)
cannot use a builder fixture or a local file fixture in the conventional sense. Their
tests use a two-tier strategy:

### Tier 1 — Local delegation tests (no network required)

The adapter delegates all getter calls to `molsysmt_Topology` through
`to_molsysmt_Topology(item, ...)`. We can exercise this delegation chain
without any network download by passing a locally-built `molsysmt.Topology`
(from the bundled `1l2y.pdb`) with `skip_digestion=True`:

```python
from molsysmt.form.string_pdb_id import get_topological_attributes as aux

@pytest.fixture(scope='module')
def topo():
    return msm.convert(PDB_PATH, to_form='molsysmt.Topology')

def test_n_atoms(topo):
    # skip_digestion=True bypasses the form check so a molsysmt.Topology
    # can be passed directly — the body still calls to_molsysmt_Topology()
    # internally, exercising the full delegation chain.
    assert aux.get_n_atoms_from_system(topo, skip_digestion=True) == 304
```

This approach:
- Tests the actual code path of the adapter's getter functions
- Exercises the `molsysmt_Topology` delegation correctly
- Runs entirely offline
- Shares the 1l2y PDB oracle values (304 atoms, 20 groups, 1 chain, etc.)

### Tier 2 — Network smoke test (requires live network)

A single test per form verifies that the download pipeline is alive end-to-end.
It is tagged with `@pytest.mark.network`:

```python
@pytest.mark.network
def test_download_and_basic_count():
    n = aux.get_n_atoms_from_system('pdb_id:1l2y')
    assert n == 304
```

### Running and skipping network tests

```bash
# Run only network tests
pytest -m network tests/form/string_pdb_id/

# Skip network tests (default for offline / CI)
pytest -m "not network" tests/form/string_pdb_id/
```

The `network` mark is registered in `pytest.ini`. Any test that requires a live
internet connection **must** carry this mark so offline runs remain fully green.

---

## The builder fixture pattern

Use `MolSysBuilder` to construct a small, fully-controlled molecular system, then convert it
to the target form. The builder is the ground truth — every value is known by construction.

```python
@pytest.fixture(scope="module")
def topo():
    b = msm.MolSysBuilder()
    # ... add atoms, groups, bonds, chains, molecules, entities ...
    molsys = b.build()
    return msm.convert(molsys, to_form='mdtraj.Topology')
```

**Standard reference system** (used across all topology-focused form tests):

```
Atoms   : 13 (ALA×5, GLY×5, HOH×1, HOH×1, NA×1)
Groups  : 5  (ALA, GLY, HOH, HOH, NA)
Chains  : 2  (A=peptide, B=solvent)
Molecules: 4 (peptide, water 0, water 1, ion 0)
Entities : 3 (peptide, water, NA)
Components: 4 (each disconnected fragment)
Bonds   : 9  (ALA backbone + sidechain + peptide bond to GLY + GLY backbone)
Bonded atoms: 10 (atoms 0–9; waters/ion have no bonds)
```

Using the same reference system across all form adapters makes it straightforward to
compare results and diagnose discrepancies.

The standard reference system builder code is in
`tests/form/mdtraj_Topology/test_get_topological_attributes_from_builder.py`
and should be copied verbatim to each new form's builder test (changing only the
`to_form=` argument in the fixture). This exact system was carefully chosen because:
- it has two chains (A=peptide, B=solvent) to test chain-level queries
- it has four distinct components (one peptide + two waters + one ion) to test component/bond
  disconnection logic
- it has three entity types (peptide, water, ion) to test entity-level type counts
- the bond graph is non-trivial (branched: CA connects to N, C, and CB)

---

## Form capability boundaries

Not all forms expose the same attributes. Tests must respect these boundaries explicitly.

### Attributes that may return `None`

Some forms genuinely do not store certain attributes. When a form's adapter returns `None`
for an attribute by design, write a dedicated test instead of including the function in
a length-checking parametrize block:

```python
# Wrong: will fail with TypeError when trying len(None)
@pytest.mark.parametrize("func_name", [
    "get_chain_name_from_chain",  # mdtraj has no chain names
])
def test_chain_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert len(result) == N_CHAINS  # crashes if result is None

# Correct: dedicated None test
def test_chain_name_is_none(topo):
    assert aux.get_chain_name_from_chain(topo) is None
```

**Known `None`-returning attributes by form:**

| Attribute family | mdtraj.Topology | openmm.Topology |
|---|---|---|
| `get_chain_name_from_*` | None (all variants) | None (all variants) |

Neither `mdtraj.Topology` nor `openmm.Topology` store chain names — only chain IDs. This
means all six variants (`_from_atom`, `_from_group`, `_from_component`, `_from_molecule`,
`_from_entity`, `_from_chain`) must return `None`. Each adapter must implement them as
`return None` directly; delegating through `np.array(None)[indices]` will crash with an
`IndexError` on 0-dimensional arrays.

The `attributes.py` file for each form is the authoritative source of which attributes are
available (`True`) or absent (`False`). If a function returns `None` for a given form, the
corresponding `attributes.py` entry should be `False`.

### Functions that raise `NotImplementedMethodError`

Some forms implement certain queries but not others. For example, `mdtraj.Topology` and
`openmm.Topology` do not store per-residue or per-chain bond bookkeeping, so functions
like `get_bond_index_from_group` or `get_bonded_atoms_from_molecule` raise
`NotImplementedMethodError`. Exclude these from the parametrized tests and document the
exclusion explicitly in the test file's module docstring:

```python
"""
Bond-related queries *from group/component/molecule/entity/chain* raise
NotImplementedMethodError in this adapter because the format does not store
per-residue or per-chain bond bookkeeping. These functions are intentionally
excluded from the parametrized tests below.
"""
```

Do not add `pytest.raises(NotImplementedMethodError)` tests for these unless there is a
specific regression risk. Documenting the boundary is enough.

---

## Behavioral differences between form adapters

This section documents confirmed behavioral differences between adapter implementations
that new developers must know to avoid writing wrong tests or implementations.

### Return-type differences: per-element list vs. scalar

The same conceptual question "how many X are in Y?" can be answered differently depending
on the form adapter's design:

- **Per-element list**: returns one value per queried Y element (length = N_Y)
- **Scalar**: returns a single aggregate value across all queried Y elements

The correct return type for each function in each form must be established empirically
(by running the function) before writing tests, not assumed.

**Confirmed per-element vs. scalar differences between mdtraj.Topology and openmm.Topology:**

| Function | mdtraj.Topology | openmm.Topology |
|---|---|---|
| `get_n_bonds_from_atom` | list of len N_ATOMS | scalar (total unique bonds) |
| `get_n_inner_bonds_from_atom` | list of len N_ATOMS | scalar (total unique bonds) |
| `get_n_components_from_group` | list `[1, 1, 1, ...]` (one per group) | scalar (unique component count) |
| `get_n_chains_from_group` | list `[1, 1, 1, ...]` (one per group) | scalar (unique chain count) |
| `get_n_chains_from_component` | list `[1, 1, 1, 1]` (one per component) | scalar (unique chain count) |
| `get_n_amino_acids_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_nucleotides_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_ions_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_waters_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_lipids_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_saccharides_from_molecule` | list (per molecule) | scalar (system total) |
| `get_n_chains_from_molecule` | list (per molecule) | scalar (unique chain count) |
| `get_n_amino_acids_from_entity` | list (per entity) | scalar (system total) |
| `get_n_ions_from_entity` | list (per entity) | scalar (system total) |
| `get_n_waters_from_entity` | list (per entity) | scalar (system total) |
| `get_n_chains_from_entity` | list `[1, 1, 1]` (per entity) | scalar (unique chain count) |
| `get_n_amino_acids_from_component` | list (per component) | scalar (system total) |
| `get_n_ions_from_component` | list (per component) | scalar (system total) |
| `get_n_waters_from_component` | list (per component) | scalar (system total) |
| `get_n_chains_from_component` | list (per component) | scalar (unique chain count) |
| `get_n_amino_acids_from_chain` | list (per chain) | scalar (system total) |
| `get_n_ions_from_chain` | list (per chain) | scalar (system total) |
| `get_n_waters_from_chain` | list (per chain) | scalar (system total) |
| `get_n_peptides_from_chain` | list (per chain) | scalar |
| `get_n_proteins_from_chain` | list (per chain) | scalar |
| `get_n_dnas_from_chain` | list (per chain) | scalar |
| `get_n_rnas_from_chain` | list (per chain) | scalar |
| `get_n_peptides_from_entity` | list (per entity) | scalar |
| `get_n_proteins_from_entity` | list (per entity) | scalar |
| `get_n_dnas_from_entity` | list (per entity) | scalar |
| `get_n_rnas_from_entity` | list (per entity) | scalar |

**Rule**: before writing any `test_X_array_length` test, verify empirically which functions
return per-element lists vs. scalars for the specific form under test. A function in the
scalar-returning category should be moved to the total-count parametrize block.

### Bond semantic functions — important naming distinction

Two families of bond-related functions have confusingly similar names but different semantics:

| Function | Returns |
|---|---|
| `get_bonded_atoms_from_bond(indices=bonds)` | Flat **sorted unique** atom index list of all atoms touching the queried bonds |
| `get_bonded_atom_pairs_from_bond(indices=bonds)` | List of `[atom1, atom2]` pairs for each queried bond |
| `get_bonded_atoms_from_system()` | Same as `get_bonded_atoms_from_bond` with all bonds (flat unique atoms) |
| `get_bonded_atom_pairs_from_system()` | Same as `get_bonded_atom_pairs_from_bond` with all bonds |

`get_bonded_atoms_from_bond` does NOT return a list of pairs. It returns a flat list of
unique atom indices (N_BONDED_ATOMS long, not N_BONDS long). In the standard reference
system: 9 bonds → 10 unique bonded atoms (atoms 0–9), so `len(get_bonded_atoms_from_bond(topo))
== 10`.

---

## `get_total_n_*` functions

### What they are

`get_total_n_*` functions (e.g., `get_total_n_atoms_from_group`) return the total count of
element X across all queried Y elements, as a **scalar**. They exist in all Tier 1 form
adapters. They are distinct from `get_n_*` functions, which may return per-element lists
in some adapters.

The semantic contract: `get_total_n_atoms_from_group(item)` == `N_ATOMS`, always.
`get_total_n_atoms_from_group(item, indices=[0,1])` == total atoms in groups 0 and 1.

### Implementation rules

The correct implementation depends on what `get_n_*_from_Y` returns for the form:

**Case 1: `get_n_X_from_Y` returns a per-element list** → sum:
```python
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):
    return int(sum(get_n_atoms_from_group(item, indices=indices, skip_digestion=True)))
```

**Case 2: `get_n_X_from_Y` returns a scalar** → delegate directly (do NOT `int(sum(scalar))`):
```python
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):
    return get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)
```

**Case 3: Unique-count relationships** (where sum would give the wrong answer):
If multiple groups can share a chain, summing `[1, 1, 1, ...]` would give N_GROUPS, not
N_CHAINS. Use a unique-index set instead:
```python
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):
    # mdtraj version — get_n_chains_from_group returns [1,1,1,...] per group
    return len(set(get_chain_index_from_group(item, indices=indices, skip_digestion=True)))
```
In openmm, `get_n_chains_from_group` already returns the unique count, so `get_total_n_chains_from_group` just delegates.

**Critical**: always check whether the underlying `get_n_*` function returns a list or a
scalar before deciding which case applies. This varies by form. A common bug is applying
`int(sum(...))` to a scalar return value, which raises `TypeError: 'int' object is not
iterable`.

### Bond total from atom

Bond totals from atom require special treatment because iterating over per-atom bond lists
would double-count each bond (both atoms of a bond are present). Use unique bond indices:

```python
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):
    per_atom = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    unique_bonds = set()
    for bond_list in per_atom:
        unique_bonds.update(bond_list)
    return len(unique_bonds)
```

Using `int(sum(get_n_bonds_from_atom(...)))` is **wrong** because it double-counts.

---

## Structuring parametrize blocks

Group tests by query element (atom, group, molecule, entity, component, chain, bond,
system) and by test type (array length, total count, spot values):

```python
# 1. Array-length tests: each function returns a list of length N_<ELEMENT>
@pytest.mark.parametrize("func_name", [
    "get_atom_index_from_group",
    "get_group_name_from_group",
    # DO NOT include functions that return scalars in this adapter
    ...
])
def test_group_array_length(topo, func_name):
    result = getattr(aux, func_name)(topo)
    assert isinstance(result, list)
    assert len(result) == N_GROUPS

# 2. Total-count tests: each function returns a scalar equal to the system total
@pytest.mark.parametrize("func_name, expected", [
    ("get_total_n_atoms_from_group", N_ATOMS),
    ("get_total_n_bonds_from_group", N_BONDS),
    # Also include n_* functions that are scalar in this adapter:
    ("get_n_chains_from_group", N_CHAINS),  # openmm only
    ...
])
def test_group_total_count(topo, func_name, expected):
    result = getattr(aux, func_name)(topo)
    assert result == expected

# 3. Spot-value tests: exact values known by construction
def test_group_names(topo):
    assert aux.get_group_name_from_group(topo) == ['ALA', 'GLY', 'HOH', 'HOH', 'NA']
```

Spot-value tests are the most valuable: they confirm not just shape but correctness.
Add at least one spot-value test for each element level.

---

## Return type convention

All `get_*_from_*` functions that return per-element data must return Python `list` (not
`numpy.ndarray`). Parametrized tests should assert `isinstance(result, list)` before
checking length.

Bond pair functions return a list of pairs; bonded-atom functions return a flat list of
unique atom indices.

---

## The convert-then-delegate pattern for derived attributes

Some attributes are not natively stored by a form but can be derived by converting to
`molsysmt.Topology` first. This is the preferred pattern for attributes that require
component/molecule/entity hierarchy, which most third-party forms do not store:

```python
def get_component_index_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.element.component import get_component_index as _get
    return _get(item, element='atom', selection=indices,
                redefine_indices=True, skip_digestion=True)
```

Or, for bulk attribute functions that need the full topology:

```python
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):
    import molsysmt as msm
    tmp = msm.convert(item, to_form='molsysmt.Topology')
    from molsysmt.form.molsysmt_Topology import get_topological_attributes as _ref
    return _ref.get_total_n_atoms_from_group(tmp, indices=indices, skip_digestion=True)
```

The overhead of the conversion is acceptable for individual derived-attribute queries.
For bulk multi-attribute operations (e.g., `msm.info`, `msm.compare`), set
`piped_topological_attribute` in the form's `__init__.py` so a single conversion is done
once and all attributes are extracted from the target form:

```python
# in molsysmt/form/mdtraj_Topology/__init__.py
piped_topological_attribute = 'molsysmt.Topology'
```

---

## Importing the module under test

Import the adapter module directly to test functions in isolation, bypassing the public API
dispatch layer:

```python
from molsysmt.form.mdtraj_Topology import get_topological_attributes as aux
```

This makes it clear that you are testing the adapter, not the public `msm.get()` dispatch.
The public API dispatch is tested separately via `msm.get(topo, atom_name=True)` style tests.

---

## Checking `attributes.py` consistency

The `attributes.py` file for each form declares which attributes are available. If a test
reveals that a function silently returns `None` or raises an unexpected error, check whether
`attributes.py` correctly marks that attribute as `False`. The public API uses `attributes.py`
to gate dispatch: if an attribute is `True` but the implementation is broken, the public API
will try to call a broken function; if it is `False` but the implementation works, the public
API will silently return `None` instead of calling the function.

---

## Parser-based test file

The second test file uses a real external file to guard against parser-specific regressions.
Prefer bundled files from `molsysmt.data` over downloads:

```python
from pathlib import Path
import molsysmt as msm

PDB_PATH = str(Path(msm.__file__).parent / 'data' / 'pdb' / '1l2y.pdb')

@pytest.fixture(scope='module')
def topo():
    t = msm.convert(PDB_PATH, to_form='mdtraj.Topology')
    assert t is not None
    return t
```

**Standard PDB oracle** (used across all topology-focused form parser tests):
`molsysmt/data/pdb/1l2y.pdb` — Trp-cage miniprotein (1L2Y):
- 304 atoms, 20 groups, 1 chain (id='A'), 310 bonds
- 1 molecule, 1 entity, 1 component, 20 amino acids
- Sequence starts: ASN-LEU-TYR-ILE-GLN-..., ends: SER

Parser tests do not need to cover every attribute — focus on the attributes most likely to
be wrong if the parser has a bug: group names, chain IDs, atom counts, bond counts.

---

## Bugs discovered during form adapter testing

The following bugs were found and fixed while writing the builder-based tests. They are
documented here as a learning record for future adapter authors.

### mdtraj.Topology adapter

| Bug | Symptom | Fix |
|---|---|---|
| `get_n_polysaccharides/peptides/proteins/dnas/rnas_from_molecule` returned lists | Expected scalar (count of molecule types in system), got list | Changed to `int(sum(1 for t in mol_types if t == '...'))` |
| `get_n_chains_from_entity` returned scalar | Expected per-entity list (each entity → 1 chain by construction), got scalar | Changed to `return [1] * n` |
| `get_total_n_bonds_from_atom` double-counted | `sum(get_n_bonds_from_atom(...))` double-counts each bond (it appears in both endpoint atoms) | Changed to collect unique bond indices via set, then `len(set)` |
| All `get_total_n_*` ignored `indices` parameter | Always returned system-wide total, even with `indices=[0]` | Rewrote all ~99 functions to pass `indices` through to the delegate and apply correct sum/unique pattern |

### openmm.Topology adapter

| Bug | Symptom | Fix |
|---|---|---|
| `@arg_digest(form=type)` typo | Used Python builtin `type` as keyword arg; argdigest raised a confusing error | Changed to `@arg_digest(form=form)` where `form` is the module-level string constant |
| `get_bonded_atoms_from_bond` returned pairs | Returned `[[a1,a2], [a1,a2], ...]` instead of flat unique atom list | Rewrote to collect unique atom indices via set |
| `get_bonded_atom_pairs_from_bond` delegated to `get_bonded_atoms_from_bond` | After the above fix, `get_bonded_atom_pairs_from_bond` now received a flat atom list, not pairs | Gave `get_bonded_atom_pairs_from_bond` its own implementation |
| `get_bonded_atoms_from_system` built a graph and returned per-atom neighbor lists | Returned a list of length N_ATOMS (neighbor lists), not the flat bonded-atom list | Replaced with `return get_bonded_atoms_from_bond(item, skip_digestion=True)` |
| `get_chain_name_from_{atom,group,component,molecule,entity}` crashed | `np.array(None)[indices]` raises `IndexError: too many indices for array: array is 0-dimensional` | Changed all five variants to `return None` directly |
| `get_n_peptides/proteins/dnas/rnas_from_{chain,entity}` crashed | `get_molecule_index_from_chain/entity` returns a list of lists with variable-length sublists; `np.unique(list_of_lists)` raises `ValueError: inhomogeneous shape` | Added `np.concatenate([np.array(ii) for ii in molecule_indices])` before `np.unique` |
| `get_total_n_*` functions entirely absent | ~97 functions missing | Added full set, adapting sum vs. delegate vs. unique-set logic to match openmm's scalar-returning conventions |
| `get_total_n_*` used `int(sum(...))` on scalar-returning functions | `get_n_amino_acids_from_molecule` returns a scalar in openmm; `int(sum(scalar))` raises `TypeError: 'int' object is not iterable` | Changed these to delegate directly: `return get_n_amino_acids_from_molecule(...)` |

---

## Checklist for a new form adapter test

When writing tests for a new form for the first time:

- [ ] Create `tests/form/<form_name>/__init__.py` (empty)
- [ ] **Run each function with the standard reference system and record empirically whether it returns a list or a scalar** — do not assume based on function name
- [ ] Identify which attributes the form natively stores vs. which require conversion
- [ ] Verify that `get_chain_name_from_*` variants return `None` if the format has no chain names; fix any that try to index `np.array(None)[...]`
- [ ] Verify `get_bonded_atoms_from_bond` returns a flat unique atom list (not pairs); verify `get_bonded_atom_pairs_from_bond` returns pairs — these must be separate implementations
- [ ] Check `@arg_digest` decorators for the correct `form=form` argument (not `form=type` or any other accidental Python expression)
- [ ] Build the standard reference system with `MolSysBuilder` and convert to the form
- [ ] Write array-length tests for each element level — **only for functions confirmed to return lists**
- [ ] Write total-count scalar tests — **including `get_n_*` functions that return scalars in this form**
- [ ] Write at least one spot-value test per element level
- [ ] Separate `None`-returning functions into dedicated tests
- [ ] Exclude `NotImplementedMethodError`-raising functions and document why
- [ ] Implement `get_total_n_*` functions if absent — use the correct sum/delegate/unique-set pattern
- [ ] Verify `attributes.py` is consistent with what the tests reveal
- [ ] Write the second test file using the standard bundled PDB file (`1l2y.pdb`)
