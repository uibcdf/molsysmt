---
summary: OpenMM solvate rejects nonnumeric or missing atom IDs.
issue: uibcdf/molsysmt#574
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: reproduced
area: [build, tests]
guard: tests/build/solvate/test_source_identifiers.py::test_source_atom_and_group_ids_are_preserved
normative:
blocked_by: []
supersedes: []
---

# OpenMM solvate rejects nonnumeric or missing atom IDs

## What

On main `b8cdbd101841f957cb6eb5ac46629bb19ab07ec9`, the issue's native
AlaValPro reproduction fails after solvent construction with
`ValueError: invalid literal for int() with base 10: 'alpha'`.
The input retains its original label. Python 3.14.7 and OpenMM 8.6.1.

## How

`build.solvate` converts the first atom and external residue IDs to integers and
renumbers every site. OpenMM's public Modeller.addSolvent instead copies source
labels verbatim before appending solvent. The failure is in MolSysMT's extra
postprocessing, not a scientific charge calculation.

## Why

IDs are nullable string labels, not positional indices. Nonnumeric labels,
nonconsecutive numbers and missing metadata must not prevent valid solvation.
Both atom and group labels need a defined output policy and source ownership.

## Bounded correction

Preserve original atom/group labels, including missing values and duplicates,
on retained source sites in native output. Assign only newly created sites the
lowest unused positive decimal string, reserving known retained source labels.
Keep atom and group label namespaces separate. No source labels are parsed as
integers or used to match molecular sites.

Use the original positional prefix in OpenMM's water-construction result. Reject
noncanonical provider traversal before construction rather than silently
misassigning source metadata; the current conversion route assumes traversal
agrees with positional atom/group indices. For explicit native ion placement,
reuse its source-to-output atom map when original waters are replaced, and derive
the retained group map from atom membership. Native finalization precedes the
requested output conversion, whose own representation constraints still apply.

No public argument, backend force-field criterion or solvation geometry changes.
Public validation, dependency guards, diagnostics and unit management remain in
their existing owners. This is metadata transport, not a new third-party
scientific method; it requires no new scientific attribution.

## Acceptance criteria

- Actual solvation succeeds for consecutive/nonconsecutive numeric, arbitrary
  string, missing and duplicate atom/group labels.
- The source and its coordinates/labels remain independent; retained output
  labels, atom names, bonds and rigid relative geometry correspond by index.
- Generated labels are deterministic and do not collide with retained source
  labels; original duplicates/missing values are not repaired implicitly.
- Exercise ordinary OpenMM defaults, explicit ion placement and equivalent
  units/box shapes, including replacement of original waters and foreign forms.
- Keep #575's composition checks passing and update the solvation tutorial,
  Foundations, Cookbook and course without rewriting their existing outputs.

## Evidence status

**Contract-tested** and **Parity-tested** within the declared metadata profile;
this changes no scientific placement criterion. The independent source failure
is retained above. No new benchmark or equilibration claim is made.

## Resolution and receiving — 2026-11-05

Removed both integer-based renumbering loops. OpenMM output is finalized in
native MolSys before the requested conversion. A private label adapter captures
source labels through public get(), then restores retained source sites and
allocates only generated labels through public set(). It reuses the shared
nullable-ID correction in #579 and native ion-replacement maps from #575; no
label-matching algorithm or competing identity store is introduced.

For an ordinary provider result, the original input is the leading positional
prefix. For native ion replacement, the solvation context records the original
atom/group counts; the first original-atom-count entries of the existing forward
map identify retained or removed source sites. Derived group correspondence uses
membership of those retained atoms. A real water-only-source fixture deliberately
selects and replaces the original source water, proving that labels are not
blindly restored onto a different prefix after deletion.

Receiving passes **3,273 tests** across basic queries, all native tests, solvation,
ion addition, atom-map composition and OpenMM Modeller/Topology adapters. **167
tests** pass with published ArgDigest 0.14.0, DepDigest 0.15.1, SMonitor 0.16.0 and
Ackredit 0.9.0 payloads. **585 documentation/governance/doctest controls** pass.
These suites overlap; they are not an aggregate unique-case count. Four workers
are used for the broad run and two for floor/docs runs, with Pytest Receptor
1.2.1. The floor route disables only the known editable pytest entry point
under #524, not runtime diagnostics.

Guards check actual successful solvent construction, source tables/coordinates,
retained bonds and relative geometry, arbitrary/missing/duplicate labels,
collision-free generated labels, H5MSM 0.5 missing-versus-literal round trips,
foreign Modeller input/output, actual source-water removal and early rejection
of malformed provider traversal. The bundled legacy pentalanine reader already
returns literal 'None' labels: the fixture preserves those labels rather than
pretending their missingness can be recovered. Genuine native missing values
have separate parameterized coverage.

Ruff, dependency scanning, public signature/docstring, course and developer-guide
checks pass. All code cells, stored outputs and notebook metadata remain unchanged
in the five edited lessons. No dependency floor, public signature, compiled
kernel, H5MSM schema or citation record changes. Existing ArgDigest/DepDigest,
SMonitor and PyUnitWizard boundaries remain active. Pure label transport defines
no new scientific method and adds no Ackredit credit; existing solvation credits
remain unchanged.

The receiving receipt is
[source_identifier_receiving_574_579_20261105.json](../../../devtools/data/source_identifier_receiving_574_579_20261105.json).
Exact-candidate installed/platform/release qualification remains separate.

## Failed draft corrected

The first bundle assertion expected actual missing values, but inspection showed
literal 'None' labels supplied by the legacy converter. The corrected guard
preserves the actual delivered input contract and tests true missing values
independently. Another initial missing-value normalization draft let NumPy coerce
a mixed list containing numeric NaN into strings; #579 records its correction.
