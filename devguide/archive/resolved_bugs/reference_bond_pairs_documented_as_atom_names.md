---
summary: Reference bond-pair help describes names instead of integer indices.
issue: uibcdf/molsysmt#548
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: low
verification: reproduced
area: [docs, api, tests]
guard: tests/element/group/test_reference_bond_index_contracts.py
normative:
blocked_by: []
supersedes: []
---

# Reference bond-pair return contracts

## What and how

The seven public group reference helpers return mapped integer index pairs for
valid input maps, not the atom-name pairs advertised by their older docstrings.
#550 already corrects the saccharide, small-molecule and cap helper help. The
general dispatcher, amino-acid, ion and water docstrings still describe string
pairs on source 93d29bf23. The original seven-node return-contract guard fails
on those four helpers and passes on the three received helpers.

## Why

A caller must distinguish local positions, explicit atom-index correspondence
and atom IDs. Row sorting is separate from endpoint orientation: water keeps
oxygen first; the other five reference families place the smaller index first.
Amino-acid repeated names can expand edges over all occurrences; ions and the
three #550 families retain first occurrences. Missing-reference None, empty
lists and family errors must not be silently normalized in an addon.

## Correction and scope

Update the four remaining docstrings and preserve all executable bodies,
signatures, existing ArgDigest entry points, SMonitor diagnostics and reference
data. Explain all seven successful contracts, empty/unknown/layout distinctions,
scalar compatibility in the two existing digested families, order, input
ownership and the distinction from graph inference or chemical-state assignment.

The direct numerical guards use literal selected reference edges, reversed names,
default/nonconsecutive integer maps, list/tuple/NumPy containers, sorted/unsorted
rows and readonly/strided input preservation. They also protect declared
None/empty/error outcomes. The return-help guard checks the declared integer
pair type against an actual numerical reference result; it is not a substitute
for the value assertions.

Document the same behavior in the existing general/amino-acid tutorials,
Foundations, recipe and Module 03. Existing notebook code, outputs, cell IDs,
cell metadata and notebook metadata stay unchanged. The paired tutorial
contracts and manifest are updated.

## Refuted interpretations and boundaries

This does not show that the sampled template bonds are chemically incorrect.
The expected API remains integer index pairs; changing outputs to names to match
old prose would introduce the wrong contract. No new scientific validation or
performance claim follows from a reference-output contract test.

Malformed explicit maps are a distinct reproduced defect, owned by #554. Some
plain helpers accept noninteger maps or ignore extras. The input precondition
is now explicit, but this documentation change does not claim uniform
ArgDigest enforcement. #549's naming/protonation dialect decision also remains
separate. DepDigest needs no new guard for a bundled reference lookup with no
optional scientific engine; existing lazy-dependency policy is unchanged.

## Receiving

The baseline docstring guard reports four failures and three passes, with 188
other cases deselected and one pytest import-rewrite warning. The corrected
195-case seven-entry-point matrix plus #550's 147-case regression pass all 342
cases without omissions or warnings (6.00 seconds). The subsequent final checks are recorded below; this paragraph preserves the
initial baseline and contract-receiving results.

## Provenance

2026-11-04, Linux x86_64, shared Python 3.14.7 / NumPy 2.4.6, published Pytest
Receptor 1.2.1. No environments or packages are installed. The compiled backend
is copied unchanged into the isolated worktree. Raw evidence remains under
`.pytest_cache/template-bond-contracts-548-550/`.


## Resolution — 2026-11-04

The four remaining docstrings now describe integer list pairs, explicit/local
mapping and real family-specific outcomes. Existing general/amino-acid tutorials,
Foundations, the recipe and Module 03 explain the same conventions. The seven-
entry-point test guards literal endpoint values, mapping, ordering, ownership and
return prose; the documentation-type assertion is paired with actual values.
#554 retains malformed-map enforcement as a separate open runtime defect.

Final local receiving on the isolated branch, advanced over the documentation-only
audit commit e62557952, establishes:

- all 342 contract/container cases pass without omissions or warnings;
- all 572 documentation/doctest cases pass, zero failures/errors/omissions;
  their 529 warnings comprise 514 Sphinx/MyST deprecations, eight legacy H5MSM
  notices, six headless plotting notices and one deliberate attribute-drop notice;
- the remaining 99 existing group cases pass with two legacy H5MSM notices;
  the two previously completed 342-case modules were deliberately excluded
  rather than rerun and double-counted;
- all 246 public docstrings pass the separate default/content validator;
- the executable ASTs of all four changed package files are unchanged after
  removing docstrings, compared with main 93d29bf23; no signature, decorator,
  import, reference table or executable body is changed;
- all three changed notebooks preserve code cells, outputs, IDs, metadata,
  cell counts and non-source markdown fields; only markdown source differs;
- all fourteen fast release gates pass, and whole-tree Ruff lint/format pass
  for 4,328 files. These checks are not a full platform or installed-pair gate.

The original JUnit files and the final preservation proof remain in the named
ignored evidence directory. This resolution introduces no new scientific
criterion, optional dependency, unit convention or runtime validation bypass.
The existing returned values and legacy unknown/empty/error distinctions remain
intact. Hosted routine CI on the integrated source is a subsequent checkpoint,
not retroactively claimed for this local receiving.

Commands from the isolated worktree used the existing published Pytest Receptor
payload and controlled Viewer runtime on PYTHONPATH:

```bash
python -m pytest --receptor=llm -n 2 \
  tests/element/group/test_reference_bond_index_contracts.py \
  tests/element/group/test_template_atom_name_containers.py
python -m pytest --receptor=llm -n 2 tests/documentation --doctest-modules \
  molsysmt/element/group/get_bonded_atom_pairs.py \
  molsysmt/element/group/amino_acid/get_bonded_atom_pairs.py \
  molsysmt/element/group/ion/get_bonded_atom_pairs.py \
  molsysmt/element/group/saccharide/get_bonded_atom_pairs.py \
  molsysmt/element/group/small_molecule/get_bonded_atom_pairs.py \
  molsysmt/element/group/terminal_capping/get_bonded_atom_pairs.py \
  molsysmt/element/group/water/get_bonded_atom_pairs.py
python -m pytest --receptor=llm -n 2 tests/element/group \
  --ignore=tests/element/group/test_reference_bond_index_contracts.py \
  --ignore=tests/element/group/test_template_atom_name_containers.py
python devtools/scripts/validate_docstrings.py
python devtools/scripts/release_gate.py
ruff check .
ruff format --check .
```
