# Conversion execution coverage

This operational guide accompanies uibcdf/molsysmt#181. Reachability evidence,
conversion fidelity and scientific accuracy are distinct claims.

## Inventory and execution

The declared graph comes from each form adapter's `_convert_to` mapping.
Discovery temporarily enables all capabilities and restores the caller's policy;
installed optional providers must not silently change the declared inventory.

```bash
# Check the plan against the graph; does not execute converters
python devtools/scripts/audit_conversion_execution.py --json

# Execute all profiled edges, including direct and public routes
python -m pytest tests/conversion_truth/test_declared_native_edges.py tests/conversion_truth/test_declared_h5msm_edges.py tests/conversion_truth/test_declared_pdb_edges.py tests/conversion_truth/test_declared_docking_edges.py --receptor=llm -n 12

# Exercise the inventory's adversarial controls
python -m pytest devtools/tests/test_audit_conversion_execution.py --receptor=llm
```

`devtools/data/conversion_execution_baseline.json` defines the
`resident-files-v5` profile: thirteen native containers/dictionary forms, four
resident MDTraj/OpenMM forms, H5MSM disk/handler forms, PDB file/text/handler
forms, and SDF/PDBQT file/text forms. Earlier native, engine, H5MSM and PDB
subsets remain covered.
Every currently declared direct edge between its source/target forms becomes a
parametrized case. A small fresh four-atom, two-structure system supplies each
input; domain fixtures include mechanics parameters and a nonempty interaction
analysis. External water fixtures are built with their providers' own topology
APIs and literal coordinates. Dictionary fixture preparation is not an independent
fidelity oracle. Topology-only sources receive explicit coordinate quantities for
coordinate-bearing targets; a topology alone is not treated as a trajectory.

Each case calls the declared converter with normal argument digestion, then
calls public `convert` with a separately prepared source. Both must return the
declared target form. No runtime exceptions are converted into skips or accepted
failures. Two adversarial controls prove that a broken callable or wrong output
form fails this check. Existing fidelity suites add their separate assertions.

## H5MSM schema and resource boundaries

`test_declared_native_edges.py` executes the resident subset;
`test_declared_h5msm_edges.py` executes every selected edge involving a disk
path or `H5MSMFileHandler`, with fresh temporary sources and destinations. Both
modules derive their cases from the same declared graph and profile. The graph
remains version-agnostic; the fixtures and assertions state their version scope.

The existing low-level legacy adapters read/write 0.4, while public `convert`
writes 0.5 and materializes modular input through the versioned reader before
resident dispatch. File output tests assert 0.4 for raw legacy adapter calls and
0.5 for the public route. This is execution evidence for different supported
paths, not codec parity. No assertion certifies that every registered low-level
adapter directly reads 0.5. The handler supports only 0.3/0.4 and rejects 0.5;
changing that capability is outside this profile.

Handler sources use context managers. New handler results are closed separately;
alias results are closed once by their source owner. Cases assert closed HDF5
identifiers. Setup writes a small 0.4 fixture with the existing legacy adapter;
it is not an independent expected-data oracle.

Additional public 0.5 controls cover a complete system and topology-only,
structures-only, chemical-states-only and interactions-only files. They check
stored domain presence, explicit nm coordinate/box values, named analyses,
parallel occurrence indices, source-axis maps and empty/unevaluated coverage.
A nonconsecutive/repeated structure selection plus atom selection checks geometry
and analysis remapping together. These bounded value assertions supplement the
weaker per-edge smoke promise; they do not certify every format field. A negative
control proves that rejecting 0.5 as a legacy handler does not first materialize
the resident domains.

## PDB execution and serialization

`test_declared_pdb_edges.py` owns every profiled edge involving `file:pdb`,
`string:pdb_text` or `molsysmt.PDBFileHandler`; the resident module excludes them.
The literal PDB witness contains two distinguishable water structures, explicit
CONECT records and angstrom positions, without a network lookup or generated
expected data. Native output fixtures carry topology and coordinates; topology-only
sources receive full-source coordinate quantities and optional cells. Files go to
fresh pytest directories. New handler results are closed separately, while aliased
results remain owned by the input context; source and result buffers are checked.

The per-edge promise remains completion and output form. Mirrored regressions add
byte-preserving copies, matched names/positions after nonconsecutive atom selection,
source owner retention, equivalent nm/angstrom inputs and native multi-structure PDB
output. Text-to-MDTraj scratch paths must disappear after success, reader exceptions
and interruptions, without mutating the input text. These controls do not certify all
PDB fields or make optional OpenMM inference independent of that provider.

## SDF and PDBQT witnesses

`test_declared_docking_edges.py` owns every selected edge involving `file:sdf`,
`file:pdbqt` or `string:pdbqt_text`. Its 19 edges each run with two input variants:
V2000/V3000 or rigid/ligand PDBQT. Each of the 38 cases exercises both direct
and public conversion with fresh local inputs and destinations. The four test
modules form a disjoint partition of the selected graph; a guard checks that
nothing selected is omitted or counted twice.

The literal source records are shared with the existing format-contract suites.
Native SDF sources are loaded from the labelled-formate witness, which provides
a complete graph and explicit formal charges, isotopes and radicals. PDBQT native
sources are loaded from explicit AutoDock4 records with nonconsecutive serial IDs,
partial charges and types. A ligand's tree is retrieved separately and supplied
to the native writer; `discard_torsion_tree=True` is explicit when projecting the
complete ligand into MolSys. No typing, preparation or graph completion is inferred.
Native source preparation is not an independent writer oracle.

Value checks compare literal atom types, SDF isotope/charge/bond assignments,
PDBQT serial strings, partial charges and types, explicit nm positions and exact
identity-file bytes. Wholly unknown PDBQT formal charges remain absent (`get`
returns `None`), not zero or a populated chemical assignment. Rereading generated
files is a bounded round-trip control; existing RDKit/MDAnalysis comparisons and
real-file suites supply their separate reference evidence.

A separate fresh-interpreter guard executes every witness while rejecting actual
module creation for RDKit, MDAnalysis, MDTraj, OpenMM and Vina. Availability-only
queries remain allowed, and both recorded attempts and loaded modules are checked.
It exposed uibcdf/molsysmt#426: declared text used to reach unrelated SMILES
heuristics. Generic registry-confirmed prefix dispatch repairs that path; no native
parser support or format/serialization scope is expanded.

## Coverage debt

Edges outside the profile are explicitly listed by source and target, with a
reason, in `accepted_unexecuted_edges`. They are coverage debt, not demonstrated
impossible routes, and existing adapter tests may exercise some of them.
The audit rejects an unaccounted edge and stale debt. New edges within the
profile become cases automatically. Extending a profile requires a real source
fixture and removal of the corresponding debt; do not regenerate the baseline
to absorb a failure. The audit reports planned cases, never successful execution.

Further profiles need file/string fixtures, other external objects and
separately marked network cases. Optional dependencies should produce clear
skips only when genuinely unavailable; a provider-complete qualification must
report those skips explicitly. The thirteen-form native subset needs no external provider; the expanded cases
skip only when MDTraj/OpenMM is genuinely unavailable during setup. Conversion
exceptions are never interpreted as optional-provider skips.
Neither a green inventory nor this bounded profile establishes that every
conversion in MolSysMT executes. See [form adapter testing](testing_form_adapters.md)
for value, unit, hierarchy and loss checks.
