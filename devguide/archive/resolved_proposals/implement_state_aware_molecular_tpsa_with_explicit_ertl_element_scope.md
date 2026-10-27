---
summary: Implement state-aware molecular TPSA with explicit Ertl element scope
issue: uibcdf/molsysmt#492
status: resolved
opened: 2026-10-26
closed: 2026-10-26
verification: measured
area: [physchem, api, units, docs]
guard: tests/physchem/test_get_tpsa.py::test_tpsa_primary_fragment_sums_across_forms
normative:
blocked_by: []
supersedes: []
---

# Implementing molecular TPSA with explicit scientific scope

**Requested:** 2026-10-26, maintainer acceptance of the TPSA boundary studied
under uibcdf/molsysmt#485, after addressing molecule-axis prerequisite #491.
**Status:** implemented and locally qualified; experimental scientific scope retained.

## What

Provide experimental `physchem.get_tpsa`, calculating one Ertl topological polar
surface area per selected complete molecule through optional RDKit. Return a
PyUnitWizard area quantity and optionally a detached provenance report. Keep the
N/O versus N/O/S/P choice explicit. No logP implementation is included.

## How

The public ArgDigest boundary accepts molecule-level selections, a chemical
state and structure indices used only for state/spatial-selection context.
Native molecule membership is reused rather than redefined. Read the full
state's covalent graph to reject bonds crossing selected molecular boundaries,
then calculate only intact selected molecules. Reject disconnected molecule
labels and unsupported chemistry. Repeated molecular indices repeat values
and source maps, while each distinct selected molecule is calculated once.

Reuse the existing chemical-graph context, detached chemistry view, conversion
and public aromaticity tool. No coordinate series is copied into that view.
The initial route supports concrete closed-shell organic chemistry with declared
formal charges, radical counts and hydrogen inventory. Known aromaticity or
hydrogen contradictions fail. No selected fragment is capped and no protonation,
neutralization, tautomer or missing-H preparation runs. Charged supported graphs
are valid TPSA inputs; they do not acquire partition or permeability meaning.

Execute RDKit CalcTPSA with force=True and explicit includeSandP on detached
working molecules; input caches and scientific assignments are unchanged.
The default N/O-only subset follows the reference-program/RDKit convention.
The original fragment table additionally supports polar S/P contributions,
enabled with include_sulfur_phosphorus=True. Neither subset is universally better.
Original coefficients are area values in angstrom squared, standardized to the
active PyUnitWizard policy. Empty selected axes remain float shape (0,).

The optional report stores source molecule indices, flattened atom membership
with offsets, net formal charges, selected state/digest, method/options,
hydrogen policy, actual software versions and detached attribution. The area
quantity stays alongside the report; metadata alone contains no area values.
No automatic native/H5MSM attachment or standalone JSON codec is promised.
Optional Ackredit contributes to the application's session, records the actual
aromaticity child operation and credits the Ertl model. Empty lookups retain the
chosen model reference without claiming to have run aromaticity on a molecule.

## Why

This is a molecular graph descriptor, unlike amino-acid reference lookup or
coordinate-dependent SASA. It provides reusable characterization for small
molecules and other supported chemical graphs without hiding new algorithms
inside downstream DockingMT/PharmacophoreMT pipelines. Client adoption and model
usefulness for a particular prediction remain separate from API implementation.

## Evidence and scope

The original reference is Ertl, Rohde and Selzer (2000),
doi:10.1021/jm000942e, Table 1. The
[study receipt](../../../devtools/data/tpsa_logp_contract_review_20261026.json)
records primary fragment sums and the RDKit documented variant comparison.
Independent scientific evidence remains bounded to simple N/O cases. Broader
provider parity is not validation of transport prediction, actual solvent
exposure or every supported fragment environment. The scientific registry stays
partial and the public API experimental.

Native SDF files may omit explicit valence/H evidence. Those inputs fail with a
missing-inventory diagnostic rather than guessing. Tests cover native SDF with
explicit CTAB valences, which do supply the required fixed-state inventory.
This is an input-information boundary, not a hidden change of parser or provider.
MolSysDict 0.1's inventory transport does not establish preservation of all
chemical assignments; a form must actually supply the required evidence.

## Alternatives and reusable boundaries

- Reusing get_surface_area would conflate historical descriptors and TPSA;
  the new name is intentionally distinct.
- A selected induced subgraph is insufficient evidence of molecule completeness;
  crossing bonds are tested before extraction.
- Reimplementing provider fragment coefficients or adding Rust is unnecessary:
  the executed descriptor kernel is already compiled. No benchmark advantage
  is asserted for the Python orchestration.
- The general group-free molecule defect is fixed under #491, without invented
  groups or a competing physchem molecule partition.
- Atom-contribution output, learned descriptors, pKa, logP/logD and new persistence
  formats are outside this bounded implementation.

## Acceptance criteria

Protect primary fragment sums separately from parity. Test molecule order and
repetitions, source membership, empty dtype/shape, pm/angstrom/nm policies,
explicit states and ambiguous structure-state requests, indexed/nonindexed H,
stale caches, missing/unsupported chemistry, independent report ownership,
provider absence/failure and enclosing attribution sessions. Exercise supported
native/RDKit/H5MSM/explicit-valence-SDF routes. Preserve source objects and keep
unselected unsupported molecules out of the calculation. Complete docstring,
User Guide, Cookbook, course and stability/evidence registry lifecycle.

## Local qualification

The [implementation receipt](../../../devtools/data/molecular_tpsa_implementation_20261026.json)
records source hashes, environment and commands. The expanded scope passes
5,129 tests; its one sandbox DNS/download failure passes unchanged when retried
with network access (14.77 seconds). The 121 final focused native/builder/TPSA controls pass in
17.33 seconds. Another 502 doctest/schema controls pass in 14.40 seconds.
The tutorial executes in 8.3 seconds, the cookbook executes with checked source
order and values, and all five course notebooks preserve code/outputs. HTML
compiles without errors or a TPSA diagnostic; 25 existing warning-debt entries
remain under #144. Ruff, dependency/docstring/signature/stability/evidence and
developer-guide checks pass, along with all fourteen fast gates.

## Resolution

The public experimental boundary is implemented with explicit model/subset,
whole-molecule selection, unit-aware outputs and optional detached provenance.
Its guard compares independently derived primary fragment sums across five
routes. Separate tests protect units, state choice, covariance of source maps,
empty/repeated selections, missing/unsupported chemistry, declared molecular
boundaries, optional attribution, caches, unchanged file bytes and no source
structure-series copy. Scientific evidence remains partial; no permeability,
all-fragment or environmental-solvent validation is claimed. LogP remains a
proposal. No installed-package, cross-platform, benchmark or release claim is made.
